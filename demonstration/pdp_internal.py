import sqlite3

# Note: The internal functionality of the helper functions is placeholder functionality and a more sophisticated
#       implementation is to be expected in a real implementation.
#       Many checks are kept simple for illustrative purposes.

def _is_valid_geolocation(ip: str) -> bool:
    """
    Checks whether an IP address is contained in blocklist, i.e. whether the geolocation via lookup is considered valid.
    :param ip: IPv4 address
    :return: True if IP is allowed access, False if IP is on blocklist.
    """
    handler = ipinfo.getHandler(IPINFO_KEY)
    details = handler.getDetails(ip)
    return details.country_name not in BLOCK_LIST_COUNTIES

def _is_valid_ip(id: str, ip: str) -> bool:
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
            ip = '.'.join(ip.split('.')[0:3])
            line = '.'.join(line.split('.')[0:3])
            if ip == line:
                return False

    # 2) lookup in database
    conn = sqlite3.connect('pdp_source_1.db')
    c = conn.cursor()
    c.execute("SELECT ip_v4 FROM users WHERE id=? AND ip_v4=?", (id, ip))
    res = c.fetchall()
    for r in res:
        if ip in r:
            conn.close()
            return True

    # add IP address after validity check according to policy of organisation
    return False

def _is_valid_fingerprint(id: str, fingerprint:str) -> bool:
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

if __name__ == '__main__':
    #_is_valid_ip('ethan@mission−thesis.org', '1.0.1.0')
    #_is_valid_ip('ethan@mission−thesis.org', '1.2.64.0')
    _is_valid_fingerprint('ethan@mission−thesis.org', '7514118a4a9aa4a0998d4e14efbfd73550bfcb08e313bb87e7f4bdd8b22a2ef4')
    _is_valid_fingerprint('ethan@mission−thesis.org', '30cd5227e750fe8848fc32fd4683b8d66e654567c708445be76bc8fe34f2dc74')
