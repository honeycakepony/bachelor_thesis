from flask import Flask, abort, request, jsonify
from deepdiff import DeepDiff
from pdp_internal import _is_mandatory_param_valid, _is_id_valid

from copy import deepcopy

app = Flask(__name__)

# define mandatory params for all access requests
MANDATORY_PARAMS: set[str] = {
    # Attack Scenario: Change of IP Address and Geolocation
    'ip_address',
    'geolocation',

    # Attack Scenario: Compromised User Credentials
    'fingerprint'
}

ALLOWED_TYPES: set[str] = {
    'user',
    'machine'
}

LOG: bool = True
THRESHOLD_PARAMS: float = 0.50 # dummy value
mandatory_params: set[str] = set()
copy_request: dict = dict()  # used to check for changes of security posture

# NOTE: The http status code 401 is never used in this implementation since the means of authorisation of the API is
# assumed and an implementation of such does not alter the findings of the juxtaposition of the parametrised and
# non-parametrised version of the API. Therefore, this functionality is not implemented in this version.
# Reason for status code 401:
# "[A] 401 HTTPS status code indicates that the caller (policy enforcement point) did not properly authenticate to the
#  PDP - for example, by omitting a required Authorization header, or using an invalid access token."
# Source: OpenID AuthZEN, 2025, section 12.1.11. -> see Bibliography of thesis


# todo: refactor fuction check_required_params

# page 49-64, HTTP Status Codes https://datatracker.ietf.org/doc/html/rfc7231#section-6.2
# https://datatracker.ietf.org/doc/html/rfc9110#name-status-codes
@app.route('/check_required_params', methods=['GET', 'POST'])
def check_required_params():
    """
    Check whether all required params are present. This check is used for the first encounter between PEP and PDP.
    Dependent on the arguments in the request, this function models the different versions of the API.
    If so, allow connection between PEP and PDP. If not, abort connection.
    Note: It is possible that PEP provides more keys than PDP requires. This is okay.
    :return: JSON response
    """
    # retrieve data containing parameters and arguments
    data = request.get_json()
    arg_parametrised: str = request.args.get('parametrised')
    arg_drop_ok: str = request.args.get('drop_ok')
    args_present: bool = arg_parametrised in {'True', 'False'} and arg_drop_ok in {'True', 'False'}
    try:
        candidate_keys = data['subject']['properties'].keys()
    except KeyError:
        if arg_parametrised == 'True':
            return jsonify({
                'status': 'Forbidden',
                'message': 'Mandatory parameter(s) required for \'properties\' missing.'
            }), 403
    # check for a valid http request format
    if not data or not args_present:
        return jsonify({
            'status': 'Bad Request',
            'message': 'No data provided to process or invalid arguments.'
        }), 400


    # guard clause for check of 'id' and 'type'
    # Note:
    # "type: REQUIRED. A string value that specifies the type of the Subject."
    # "id: REQUIRED. A string value containing the unique identifier of the Subject, scoped to the type."
    # Source: OpenID AuthZEN, 2025, section 5.1 -> see Bibliography of thesis
    type_check: bool = data['subject']['type'] in ALLOWED_TYPES
    id_check: bool = _is_id_valid(data['subject']['id'], data['subject']['type'], LOG)
    if not type_check or not id_check:
        return jsonify({
            'status': 'Forbidden',
            'message': 'Mandatory parameter(s) for \'id\' or \'type\' invalid.'
        }), 403


    if arg_parametrised == 'False':
        return jsonify({
            'status': 'OK',
            'message': 'All mandatory parameters are present.'
        }), 200

    global mandatory_params
    global copy_request
    if arg_drop_ok == 'False':
        if MANDATORY_PARAMS.issubset(candidate_keys):
            mandatory_params = MANDATORY_PARAMS
            copy_request = deepcopy(data)
            return jsonify({
                'status': 'OK',
                'message': 'All mandatory parameters are present.'
            }), 200
    if arg_drop_ok == 'True':
        if len(MANDATORY_PARAMS & candidate_keys) >= THRESHOLD_PARAMS * len(MANDATORY_PARAMS):
            mandatory_params = MANDATORY_PARAMS.intersection(candidate_keys)
            copy_request = deepcopy(data)
            return jsonify({
                'status': 'OK',
                'message': 'All mandatory parameters are present.'
            }), 200

    return jsonify({
        'status': 'Forbidden',
        'message': 'Mandatory parameter(s) for \'properties\' invalid.'
    }), 403

@app.route('/handle_access_request', methods=['GET', 'POST'])
def handle_access_request():
    """
    Check whether all mandatory params are present and valid. This is a wrapper function that calls all check functions.
    Note: In a real implementation, the logic for the Trust Algortihm (TA) could be implemented here in a more
        advanced version. This is just a placeholder.
    :return: JSON response
    """
    data = request.get_json()
    is_valid = True
    for k in mandatory_params:
        if not is_valid:
            break
        if LOG:
            print(f'Handling access request for mandatory parameter: {k} for {data['subject']['id']}')
        is_valid = _is_mandatory_param_valid(k, data, log=True)

    if is_valid:
        return jsonify({
            'status': 'OK',
            'message': 'All mandatory parameters are present and valid.'
        }), 200

    return jsonify({
        'status': 'OK',
        'message': 'Mandatory parameter(s) are either not present or invalid.'
    }), 200


@app.route('/check_update', methods=['GET', 'POST'])
def check_update():
    new_data = request.get_json()
    diff: dict = DeepDiff(new_data, copy_request)
    is_valid: bool = True
    for k in diff.affected_paths:
        if not is_valid:
            break
        indices: list[int] = [i for i, c in enumerate(k) if c == "'"]
        param_to_check: str = k[indices[-2] + 1:indices[-1]]
        if param_to_check in mandatory_params:
            is_valid = _is_mandatory_param_valid(param_to_check, new_data, log=True)

    if is_valid:
        return jsonify({
            'status': 'OK',
            'message': 'All mandatory parameters are present and valid.'
        }), 200

    return jsonify({
        'status': 'OK',
        'message': 'Mandatory parameter(s) are either not present or invalid.'
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=2110)
