from dotenv import load_dotenv

import sqlite3
import os
import ipinfo

# Note: The internal functionality of the helper functions is placeholder functionality and a more sophisticated
#       implementation is to be expected in a real implementation.
#       Many checks are kept simple for illustrative purposes.

# load API keys as environment variables
load_dotenv()
IPINFO_KEY = os.getenv('IPINFO_API')

BLOCK_LIST_COUNTIES: set[str] = {
    'China'
}

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
    if param == 'ip_v4':
        if log:
            print(f'_is_mandatory_param_valid: {param_to_check} for user {user_id}')
        return _is_valid_ip(user_id, param_to_check, True)
    elif param == 'geolocation':
        if log:
            print(f'Checking geolocation: {param_to_check}')
        return _is_valid_geolocation(param_to_check, data['subject']['properties']['ip_v4'])
    elif param == 'fingerprint':
        if log:
            print(f'Checking fingerprint: {param_to_check} for user {user_id}')
        return _is_valid_fingerprint(user_id, param_to_check)

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
    with open('ipv4_placeholder_blocklist.txt') as f:
        # this logic is very roughy and is only used for its simplicity for illustrative purposes
        for line in f:
            ip_temp = '.'.join(ip.split('.')[0:3])
            line = '.'.join(line.split('.')[0:3])
            if ip_temp == line:
                if log:
                    print(f'_is_valid_ip: IP {ip_temp} found on blocklist.\n')
                return False

    # 2) lookup in database
    conn = sqlite3.connect('pdp_source_1.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    res = c.fetchall()
    print(res)

    c.execute("SELECT ip_v4 FROM users WHERE id=? AND ip_v4=?", (id, ip))
    res = c.fetchall()

    for r in res:
        if ip in r:
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
    conn = sqlite3.connect('pdp_source_1.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=? AND fingerprint=?", (id, fingerprint))
    if c.fetchall():
        conn.close()
        return True
    return False
