def _is_valid_geolocation(ip: str) -> bool:
    """
    Checks whether an IP address is contained in blocklist, i.e. whether the geolocation via lookup is considered valid.
    :param ip: IPv4 address
    :return: True if IP is allowed access, False if IP is on blocklist.
    """
    handler = ipinfo.getHandler(IPINFO_KEY)
    details = handler.getDetails(ip)
    return details.country_name not in BLOCK_LIST_COUNTIES

def _is_valid_ip(): # todo
    # known vs. unknown location -> e.g. unknown location may require additional authentication
    pass

def _is_valid_fingerprint(): # todo
    pass
