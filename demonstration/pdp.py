from flask import Flask, abort, request, jsonify
from deepdiff import DeepDiff
from requests import Response

# https://pypi.org/project/http-status-code-exception/
from http_status_code_exception.client_error import BadRequest

from pdp_internal import _check_params_subject

from copy import deepcopy

app = Flask(__name__)

DEFAULT_PARAM: str = 'False'

REQUIRED_PARAMS_SUBJECT: dict[str, str] = {
    'fingerprint': DEFAULT_PARAM,
    'ip_address': DEFAULT_PARAM,
    'device_id': DEFAULT_PARAM,
    'user_session': DEFAULT_PARAM
}

required_params_subject: dict[str, str] = dict()
optional_params_subject: dict[str, str] = dict()

LOG: bool = True
THRESHOLD_PARAMS: float = 0.50  # dummy value
mandatory_params: set[str] = set()
copy_request: dict = dict()  # used to check for changes of security posture


# NOTE: The http status code 401 is never used in this implementation since the means of authorisation of the API is
# assumed and an implementation of such does not alter the findings of the juxtaposition of the parametrised and
# non-parametrised version of the API. Therefore, this functionality is not implemented in this version.
# Reason for status code 401:
# "[A] 401 HTTPS status code indicates that the caller (policy enforcement point) did not properly authenticate to the
#  PDP - for example, by omitting a required Authorization header, or using an invalid access token."
# Source: OpenID AuthZEN, 2025, section 12.1.11. -> see Bibliography of thesis


# todo: refactor function check_required_params
# check_required_params()
#   subject:
#       parametrised == False
#       drop_args    == False
#       drop_args    == True
#   action:
#       pass
#   resource:
#       pass
#   context:
#       pass
#   grant or deny access
#       add to dict: status_subject, status_action, status_resource, status_context ... -> elegant way for this

# page 49-64, HTTP Status Codes https://datatracker.ietf.org/doc/html/rfc7231#section-6.2
# https://datatracker.ietf.org/doc/html/rfc9110#name-status-codes
@app.route('/check_params', methods=['GET', 'POST'])
def check_params():
    """
    Check whether all required params are present. This check is used for the first encounter between PEP and PDP.
    Dependent on the arguments in the request, this function models the different versions of the API.
    If so, allow connection between PEP and PDP. If not, abort connection.
    Note: It is possible that PEP provides more keys than PDP requires. This is okay.
    :return: JSON response
    """
    # load all variables with global scope and complete setup for function
    global copy_request
    global mandatory_params
    flag_error: bool = False  # flag for control flow of function
    flag_invalid: bool = False
    response_pep: dict = {'subject': dict(), 'action': dict(), 'resource': dict(), 'context': dict()}

    # retrieve data of access request (sent as JSON) and parameters (called 'args')
    data: dict = request.get_json(silent=True)  # sets 'data = None' if payload cannot be parsed
    if data is None:
        pass
    arg_parametrised: str = True if request.args.get('parametrised') != 'False' else False
    arg_drop_ok: str = True if request.args.get('drop_ok') != 'False' else False

    # handle SUBJECT
    # todo: check_params_subject
    #       parametrised == False
    #       drop_args    == False
    #       drop_args    == True

    response_pep, required_params_subject, optional_params_subject, flag_error, flag_invalid = (_check_params_subject(data['subject'], REQUIRED_PARAMS_SUBJECT, response_pep, arg_parametrised, arg_drop_ok, LOG))
    if flag_error:
        return jsonify({'status': 'Bad Request', 'demo': 'check_params -> _check_params_subject', 'message': response_pep}), 400

    if flag_invalid:
        return jsonify({'status': 'OK', 'demo': 'check_params -> _check_params_subject', 'message': response_pep}), 200

    if True:
        return jsonify({'status': 'OK', 'demo': 'check_params -> _check_params_subject', 'message': response_pep}), 200

    # todo: check_params_action
    # todo: check_params_resource
    # todo: check_params_context [Optional]

    # check REQUIRED subject type and subject id
    stype, sid = _retrieve_stype_sid(data)
    if arg_parametrised == 'False':
        if None in (stype, sid):
            return jsonify(JSON_INVALID_ID_TYPE), 403
        if all((stype, sid)):
            return jsonify(JSON_VALID_ID_TYPE), 200

    try:
        candidate_keys = data['subject']['properties'].keys()
    except KeyError:
        if arg_parametrised == 'True':
            return jsonify({
                'status': 'Forbidden',
                'message': 'Mandatory parameter(s) required for \'properties\' missing.'
            }), 403
        else:
            pass

    # guard clause for check of 'id' and 'type'
    # Note:
    # "type: REQUIRED. A string value that specifies the type of the Subject."
    # "id: REQUIRED. A string value containing the unique identifier of the Subject, scoped to the type."
    # Source: OpenID AuthZEN, 2025, section 5.1 -> see Bibliography of thesis
    type_check: bool = data['subject']['type'] in ALLOWED_TYPES
    print(f'{type_check=}')
    id_check: bool = _is_valid_sid(data['subject']['id'], data['subject']['type'], LOG)
    print(f'{id_check=}')
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
    """
    Check which parameters have been updated and re-evaluate required parameters which have been altered since
    the last check.
    :return: JSON response
    """
    print(f'{copy_request=}')
    new_data = request.get_json()
    diff: dict = DeepDiff(new_data, copy_request)
    print(f'{diff=}')
    is_valid: bool = True
    for k in diff.affected_paths:
        if not is_valid:
            break
        indices: list[int] = [i for i, c in enumerate(k) if c == "'"]
        print(f'{indices=}')
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
    app.run(debug=True, port=2111)
