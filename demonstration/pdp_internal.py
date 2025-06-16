from dotenv import load_dotenv

import sqlite3
import os
import ipinfo

# Note: The internal functionality of the helper functions is non-normative functionality and a more sophisticated
#       implementation is to be expected in a real implementation.
#       Many checks are kept simple for illustrative purposes.

# load API keys as environment variables
load_dotenv()
IPINFO_KEY = os.getenv('IPINFO_API')

BLOCK_LIST_COUNTIES: set[str] = {
    'China'
}

ALLOWED_TYPES: set[str] = {
    'user',
    'machine'
}


CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURR_DIR, 'data_sources', 'pdp_source_1.db')

# Note: In a real implementation, this function would be more sophisticated since it would allow to add an 'id' to the
# database. The attack scenarios do not contain a scenario where the 'id' needs to be added. Hence, the functionality
# is not implemented in this non-normative function.
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
    result: bool = stype in ALLOWED_TYPES
    if log:
        print(f'\tis_valid_stype: \'{stype}\' is valid? \'{result}\'')
    return result

def _is_mandatory_param_valid(param: any, data: dict, log=False) -> bool:
    """
    Check the validity of a single mandatory parameter by referring to the corresponding policy of the organisation.
    :param param: Parameter to check
    :param data: Dict of access request
    :return: Value determined by check of policy of parameter. If check fails, return False by default..
    """
    user_id = data['subject']['id']
    param_to_check = data['subject']['properties'][param]

    # check parameter validity
    if param == 'ip_address':
        if log:
            print(f'_is_mandatory_param_valid: {param_to_check} for user {user_id}')
        return _is_valid_ip(user_id, param_to_check, True)
    elif param == 'geolocation':
        if log:
            print(f'Checking geolocation: {param_to_check}')
        return _is_valid_geolocation(param_to_check, data['subject']['properties']['ip_address'])
    elif param == 'fingerprint':
        if log:
            print(f'Checking fingerprint: {param_to_check} for user {user_id}')
        return _is_valid_fingerprint(user_id, param_to_check)
    elif param == 'user_session':
        if log:
            print(f'Checking user_session: {param_to_check} for user {user_id}')
        return _is_valid_session_id(user_id, param_to_check)

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
                print(f'_is_valid_geolocation: {geolocation} != {details.country_name}')
            return False

    if log:
        print(f'_is_valid_geolocation: country found in blocklist? {details.country_name not in BLOCK_LIST_COUNTIES}')
    return details.country_name not in BLOCK_LIST_COUNTIES


def _is_valid_ip(id: str, ip: str, log=False) -> bool:
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
    conn = sqlite3.connect('data_sources/pdp_source_1.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    res = c.fetchall()
    print(res)

    c.execute("SELECT ip_v4 FROM users WHERE id=? AND ip_v4=?", (id, ip))
    res = c.fetchall()

    for r in res:
        if ip in r:
            if log:
                print(f'_is_valid_ip: known IP {ip} found in database\n')
            conn.close()
            return True

    # add IP address after validity check according to policy of organisation
    return False


def _is_valid_fingerprint(id: str, fingerprint: str) -> bool:
    """
    Check whether fingerprint of subject (i.e. fingerprint of system beingn used) is known in database. If not,
    additional authentication or enrollment of device are possible options (up to implementation details).
    :param id: ID of subject
    :param fingerprint: Fingerprint (SHA256) of system being used (calculation up to implementation details)
    :return: True if fingerprint is known, False if unknown.
    """
    conn = sqlite3.connect('data_sources/pdp_source_1.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=? AND fingerprint=?", (id, fingerprint))
    if c.fetchall():
        conn.close()
        return True
    return False

def _is_valid_session_id(user_id: str, user_session: str) -> bool:
    conn = sqlite3.connect('data_sources/pdp_source_1.db')
    c = conn.cursor()
    c.execute("SELECT user_sessions FROM users WHERE id=? AND user_session=?", (user_id, user_session))
    print(c.fetchall())
    if c.fetchall():
        conn.close()
        return True
    return False