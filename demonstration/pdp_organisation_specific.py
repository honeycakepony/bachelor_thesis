from dotenv import load_dotenv

import sqlite3
import os
import ipinfo

# load API keys as environment variables
load_dotenv()
IPINFO_KEY = os.getenv('IPINFO_API')

BLOCK_LIST_COUNTIES: set[str] = {
    'China'
}

ALLOW_LIST_PORTS: set[int] = {
    443, # HTTPS
    3389, # RDP
}

ALLOW_LIST_STYPES: set[str] = {
    'user',
    'machine'
}

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURR_DIR, 'data_sources', 'pdp_source_1.db')

def is_required_param_valid(param: any, param_to_check: str, sid: str, data_subject: dict, log=False) -> bool:
    """
    Check the validity of a single mandatory parameter by referring to the corresponding policy of the organisation.
    :param log:
    :param sid:
    :param param_to_check:
    :param param: Parameter to check
    :param data_subject: Dict of access request
    :return: Value determined by check of policy of parameter. If check fails, return False by default.
    """
    if param == 'ip_address':
        if log:
            print(f'\t\tis_mandatory_param_valid -> _is_valid_ip\n'
                  f'\t\t\tChecking ip_address: {param_to_check} for user {sid}')
        return _is_valid_ip(sid, param_to_check, log)
    elif param == 'geolocation':
        if log:
            print(f'\t\tis_mandatory_param_valid -> _is_valid_geolocation\n'
                  f'\t\t\tChecking geolocation: {param_to_check}')
        return _is_valid_geolocation(param_to_check, data_subject['properties']['ip_address'])
    elif param == 'fingerprint':
        if log:
            print(f'\t\tis_mandatory_param_valid -> _is_valid_fingerprint\n'
                  f'\t\t\tChecking fingerprint: {param_to_check} for user {sid}')
        return _is_valid_fingerprint(sid, param_to_check, log)
    elif param == 'user_session':
        if log:
            print(f'\t\tis_mandatory_param_valid -> _is_valid_session_id\n'
                  f'\t\t\tChecking user_session: {param_to_check} for user {sid}')
        return _is_valid_session_id(sid, param_to_check, log)
    elif param == 'requested_ports':
        if log:
            print(f'\t\tis_mandatory_param_valid -> _is_valid_requested_ports\n'
                  f'\t\t\tChecking requested_ports: {param_to_check} for user {sid}')
        return _is_valid_requested_ports(param_to_check, log)
    elif param == 'device_id':
        if log:
            print(f'\t\tis_mandatory_param_valid -> _is_valid_device_id\n'
                  f'\t\t\tChecking device_id: {param_to_check} for user {sid}')
        return _is_valid_device_id(sid, param_to_check, log)

    return False

def _is_valid_sid(sid: str, stype: str, log=False) -> bool:
    """
    Check whether 'id' is known in database.
    :param sid: 'id' provided by access request
    :param stype: 'type' provided by access request
    :return: True if 'id' can be found in database, False if not.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM subjects WHERE id=? AND type=?", (sid, stype))
    if c.fetchone() is not None:
        conn.close()
        if log:
            print(f'\t_is_valid_sid: \'{sid}\' is valid? \'True\'')
        return True

    conn.close()
    if log:
        print(f'\t_is_valid_sid: \'{sid}\' is valid? \'False\'')
    return False


def _is_valid_stype(stype: str, log=False) -> bool:
    result: bool = stype in ALLOW_LIST_STYPES
    if log:
        print(f'\t_is_valid_stype: \'{stype}\' is valid? \'{result}\'')
    return result

def _is_valid_requested_ports(param_to_check: str, log=False) -> bool:
    if param_to_check in ALLOW_LIST_PORTS:
        if log:
            print(f'\t\t\t\t_is_valid_requested_ports: \'{param_to_check}\' is valid? \'True\'')
        return True

    if log:
        print(f'\t\t\t\t_is_valid_requested_ports: \'{param_to_check}\' is valid? \'False\'')
    return False

def _is_valid_device_id(sid: str, device_id: str, log=False) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM subjects WHERE id=? AND device_id=?", (sid, device_id))
    if c.fetchone() is not None:
        conn.close()
        if log:
            print(f'\t\t\t\t_is_valid_device_id: \'{device_id}\' is valid? \'True\'')
        return True

    if log:
        print(f'\t\t\t\t_is_valid_device_id: \'{device_id}\' is valid? \'False\'')
    return False


def _is_valid_geolocation(geolocation: str, ip: str, log=False) -> bool:
    """
    Checks whether an IP address is contained in blocklist, i.e. whether the geolocation via lookup is considered valid.
    :param geolocation: Geolocation, i.e. country, provided by subject (can be 'None')
    :param ip: IPv4 address
    :return: True if IP is allowed access, False if IP is on blocklist.
    """
    handler = ipinfo.getHandler(IPINFO_KEY)
    details = handler.getDetails(ip)
    if geolocation:
        if geolocation != details.country_name:
            if log:
                print(f'\t\t\t\t_is_valid_geolocation: {geolocation} != {details.country_name}')
            return False

    if log:
        print(f'\t\t\t\t_is_valid_geolocation: country found in blocklist? {details.country_name not in BLOCK_LIST_COUNTIES}')
    return details.country_name not in BLOCK_LIST_COUNTIES


def _is_valid_ip(sid: str, ip: str, log=False) -> bool:
    """
    Checks 1) whether an IP address is contained in blocklist, 2) whether IP address is known for subject.
    :param ip: ID of subject
    :param ip: IPv4 address
    :return: True if IP is allowed access (known in database in this case), False if IP is on blocklist or unknown.
    """
    # 1) check against blocklist
    with open('data_sources/ipv4_placeholder_blocklist.txt') as f:
        # this logic is very roughy and is only used for its simplicity for illustrative purposes
        for line in f:
            ip_temp = '.'.join(ip.split('.')[0:3])
            line = '.'.join(line.split('.')[0:3])
            if ip_temp == line:
                if log:
                    print(f'_is_valid_ip: IP {ip_temp} found on blocklist.\n')
                return False

    # 2) lookup in database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM subjects WHERE id=? AND ip_address=?", (sid, ip))
    if c.fetchone() is not None:
        conn.close()
        if log:
            print(f'\t\t\t\t_is_valid_ip: \'{ip}\' is valid? \'True\'')
        return True

    # add IP address after validity check according to policy of organisation
    if log:
        print(f'\t\t\t\t_is_valid_ip: \'{ip}\' is valid? \'False\'')
    return False


def _is_valid_fingerprint(sid: str, fingerprint: str, log=False) -> bool:
    """
    Check whether fingerprint of subject (i.e. fingerprint of system benign used) is known in database. If not,
    additional authentication or enrollment of device are possible options (up to implementation details).
    :param id: ID of subject
    :param fingerprint: Fingerprint (SHA256) of system being used (calculation up to implementation details)
    :return: True if fingerprint is known, False if unknown.
    """
    conn = sqlite3.connect('data_sources/pdp_source_1.db')
    c = conn.cursor()
    c.execute("SELECT * FROM subjects WHERE id=? AND fingerprint=?", (sid, fingerprint))
    if c.fetchone() is not None:
        conn.close()
        if log:
            print(f'\t\t\t\t_is_valid_fingerprint: \'{fingerprint}\' is valid? \'True\'')
        return True

    if log:
        print(f'\t\t\t\t_is_valid_fingerprint: \'{fingerprint}\' is valid? \'False\'')
    return False


def _is_valid_session_id(sid: str, user_session: str, log=False) -> bool:
    """
    Check whether session_id of subject is the same as for the start -> stored in database.
    If change mid-session to unknow session_id is detected, require re-authentication and re-authorisation.
    :param sid: ID of subject
    :param user_session: Session ID of current session (in cookie)
    :return: True if fingerprint is known, False if unknown.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM subjects WHERE id=? AND user_session=?", (sid, user_session))
    if c.fetchone() is not None:
        conn.close()
        if log:
            print(f'\t\t\t\t_is_valid_session_id: \'{user_session}\' for \'{sid}\' is valid? \'True\'')
        return True
    if log:
        print(f'\t\t\t\t_is_valid_session_id: \'{user_session}\' for \'{sid}\' is valid? \'False\'')
    return False