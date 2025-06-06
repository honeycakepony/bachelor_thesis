from flask import Flask, abort, request, jsonify
from deepdiff import DeepDiff
from dotenv import load_dotenv

import ipinfo
import os
import pdp_internal as pdpi

log: bool = True

app = Flask(__name__)

# define mandatory params for all access requests
MANDATORY_PARAMS: set[str] = {
    # Attack Scenario: Change of IP Address and Geolocation
    'ip_v4',
    'geolocation',

    # Attack Scenario: Compromised User Credentials
    'fingerprint'
}

THRESHOLD_PARAMS: float = 0.70

mandatory_params: set[str] = set()

# load API keys as environment variables
load_dotenv()
IPINFO_KEY = os.getenv('IPINFO_API')

BLOCK_LIST_COUNTIES: set[str] = {
    'China'
}

json_reqeust: dict = dict()  # used for copy of last json


# page 49-64, HTTP Status Codes https://datatracker.ietf.org/doc/html/rfc7231#section-6.2
# https://datatracker.ietf.org/doc/html/rfc9110#name-status-codes
@app.route('/check_mandatory_params_1', methods=['GET', 'POST'])
def check_mandatory_params_1():
    """
    Check whether all mandatory params are present. This check is used for the first encounter between PEP and PDP.
    This function models version 1 as specified in the section on 'Mandatory Parameters'.
    If so, allow connection between PEP and PDP.
    If not, abort connection.
    Note: It is possible that PEP provides more keys than PDP requires. This is okay.
    :return: JSON response
    """
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'Bad Request',
            'message': 'No data provided to process.'
        }), 400

    candidate_keys = data['subject']['properties'].keys()
    if MANDATORY_PARAMS.issubset(candidate_keys):
        mandatory_params = MANDATORY_PARAMS
        return jsonify({
            'status': 'OK',
            'message': 'All mandatory parameters are present.'
        }), 200

    return jsonify({
        'status': 'Forbidden',
        'message': 'Server refuses to process request.'
    }), 403

@app.route('/check_mandatory_params_2', methods=['GET', 'POST'])
def check_mandatory_params_2():
    """
    Check whether all mandatory params are present. This check is used for the first encounter between PEP and PDP.
    This function models version 2 as specified in the section on 'Mandatory Parameters'.
    If so, allow connection between PEP and PDP.
    If not, abort connection.
    Note: It is possible that PEP provides more keys than PDP requires. This is okay.
    :return: JSON response
    """
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'Bad Request',
            'message': 'No data provided to process.'
        }), 400

    # Check for relative size of intersection. If size suffices for pre-determined threshold (THRESHOLD_PARAMS),
    # create reduced set of mandatory params.
    candidate_keys = data['subject']['properties'].keys()
    if len(MANDATORY_PARAMS & candidate_keys) >= THRESHOLD_PARAMS * len(MANDATORY_PARAMS):
        mandatory_params = MANDATORY_PARAMS.intersection(candidate_keys)
        return jsonify({
            'status': 'OK',
            'message': 'All mandatory parameters are present.'
        }), 200

    return jsonify({
        'status': 'Forbidden',
        'message': 'Insufficiently many mandatory parameters are present.'
    }), 403

@app.route('/handle_access_request', methods=['GET', 'POST'])
def handle_access_request():
    data = request.get_json()
    is_valid = True
    for k in mandatory_params:
        if not check_valid:
            return jsonify({
                'status': 'OK',
                'message': 'Mandatory parameter(s) are either not present or invalid.'
            }), 200

        if log:
            print(f'Handling access request -> checking parameter {k}')

        # check parameter validity
        if k == 'ip_v4':
            # the checks consume some of my rate limiting
            # print('checking IP v4', data['subject']['properties'][k])
            # is_valid = pdpi._is_valid_geolocation(data['subject']['properties'][k])
            pass
        elif k == 'geolocation':
            # the checks consume some of my rate limiting
            pass
        elif k == 'fingerprint':
            pass

    return jsonify({
            'status': 'OK',
            'message': 'All mandatory parameters are present and valid.'
        }), 200


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
