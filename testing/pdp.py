from flask import Flask, abort, request, jsonify
from deepdiff import DeepDiff
from dotenv import load_dotenv

import ipinfo
import os

# todo: count how many different JSON modules I'm using
#       flask.jsonify, requests.post(..., json=)

# todo: check this: https://stackoverflow.com/questions/12806386/is-there-any-standard-for-json-api-response-format
# -> format for error handling
# -> e.g. 1. Consistent JSON response structure with 'status' and 'message' fields.

app = Flask(__name__)

# define mandatory params for all access requests
MANDATORY_PARAMS: set[str] = {
    # Attack Scenario: Change of IP Address and Geolocation
    'ip_v4',
    'geolocation',

    # Attack Scenario: Compromised User Credentials
    'fingerprint'
}

# load API keys as environment variables
load_dotenv()
IPINFO_KEY = os.getenv('IPINFO_API')

BLOCK_LIST_COUNTIES: set[str] = {
    'China'
}

json_reqeust: dict = dict()

# todo: check error codes -> stick to conventions
@app.route('/check_mandatory_params', methods=['GET', 'POST'])
def check_mandatory_params():
    """
    Check whether all mandatory params are present. This check is used for the first encounter between PEP and PDP.
    If so, allow connection between PEP and PDP.
    If not, abort connection.
    Note: It is possible that PEP provides more keys than PDP requires. This is okay.
    :return: JSON response
    """
    data = request.get_json()
    json_reqeust = data
    if not data:
        return jsonify({'Error': 'No data provided to process'}), 400

    candidate_keys = data['subject']['properties'].keys()
    if MANDATORY_PARAMS.issubset(candidate_keys):
        return jsonify('Successful connection attempt. All mandatory parameters are present.'), 200

    return jsonify('Error! Not all mandatory parameters are present.'), 400


# 1 June
def _check_differences(old_data: dict, new_data: dict) -> dict:
    """
    Check for differences of values, i.e. detect changes in security posture.
    :param old_data:
    :param new_data:
    :return:
    """
    diff: dict = DeepDiff(old_data, new_data)
    print(diff)


@app.route('/handle_access_request', methods=['GET', 'POST'])
def handle_access_request():
    data = request.get_json()
    check_valid = True
    for k in MANDATORY_PARAMS:
        print(f'in handle_access_request: {k}')
        if not check_valid:
            return jsonify('Invalid! '), 400
        match k:
            case 'ip_v4':
                # the checks consume some of my rate limiting
                pass
                #print('checking IP v4', data['subject']['properties'][k])
                #check_valid = _is_valid_geolocation(data['subject']['properties'][k])
            case _:
                pass

    return jsonify('Done.'), 200


# todo: check IP and geolocation

# def _check_ip() # todo
# known vs. unknown location -> e.g. unknown location may require additional authentication


# https://ipinfo.io/dashboard
# 1.0.42.211 -> https://lite.ip2location.com/china-ip-address-ranges
# {'ip': '1.0.42.211', 'city': 'Shenzhen', 'region': 'Guangdong', 'country': 'CN', 'loc': '22.5455,114.0683', 'postal': '518000', 'timezone': 'Asia/Shanghai', 'country_name': 'China', 'isEU': False, 'country_flag_url': 'https://cdn.ipinfo.io/static/images/countries-flags/CN.svg', 'country_flag': {'emoji': '🇨🇳', 'unicode': 'U+1F1E8 U+1F1F3'}, 'country_currency': {'code': 'CNY', 'symbol': '¥'}, 'continent': {'code': 'AS', 'name': 'Asia'}, 'latitude': '22.5455', 'longitude': '114.0683'}
def _is_valid_geolocation(ip: str) -> bool:
    """
    Checks whether an IP address is contained in blocklist, i.e. whether the geolocation via lookup is considered valid.
    :param ip: IPv4 address
    :return: True if IP is allowed access, False if IP is on blocklist.
    """
    handler = ipinfo.getHandler(IPINFO_KEY)
    details = handler.getDetails(ip)
    #print(details.country)
    #print(details.country_name)
    # print(details.loc)
    # print(details.timezone)
    return details.country_name not in BLOCK_LIST_COUNTIES


# 1 June
@app.route('/check_update', methods=['GET', 'POST'])
def check_update():
    new_data = request.get_json()
    old_data = json_reqeust
    # todo: check differences -> only values which changed


"""
    diff.affected_paths)
    for k in diff.affected_paths:
        start = k[:-2].rfind("'")
        relevant_param: str = k[start+1:-2]
        print(k, relevant_param, 'bla')
        print(diff.get_stats())
    for e in diff['values_changed']:
        print(e)
        print(diff['values_changed'][e])
        print()
"""

if __name__ == '__main__':
    app.run(debug=True, port=2110)
