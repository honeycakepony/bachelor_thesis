from flask import Flask, abort, request, jsonify
from deepdiff import DeepDiff
from requests import Response

# https://pypi.org/project/http-status-code-exception/
from http_status_code_exception.client_error import BadRequest
from pdp_wrapper_functions import _check_params_subject
import pdp_organisation_specific as pdp_os

import re

# todo: simply add optional_params_subject and required_params_subject to a list
#       (allows to compare values against former values), e.g. 10 values

app = Flask(__name__)

DEFAULT_PARAM: str = 'False'

REQUIRED_PARAMS_SUBJECT: dict[str, str] = {
    'fingerprint': DEFAULT_PARAM,
    'ip_address': DEFAULT_PARAM,
    'device_id': DEFAULT_PARAM,
    'user_session': DEFAULT_PARAM,
    'requested_ports': DEFAULT_PARAM
}

required_params_subject: dict[str, str] = dict()
optional_params_subject: dict[str, str] = list()
# used to check for changes of security posture
required_params_subject_log: list[dict[str, str]] = list()
optional_params_subject_log: list[dict[str, str]] = list()

LOG: bool = True
MAX_LENGTH_LOG_LIST: int = 10


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
    global required_params_subject
    global optional_params_subject
    flag_error: bool = False  # flag for control flow of function
    flag_invalid: bool = False
    response_pep: dict = {'subject': dict(), 'action': dict(), 'resource': dict(), 'context': dict()}

    # retrieve data of access request (sent as JSON) and parameters (called 'args')
    data: dict = request.get_json(silent=True)  # sets 'data = None' if payload cannot be parsed
    if data is None:
        return jsonify({'status': 'Bad Request', 'decision': False, 'demo': 'check_params -> request.get_json',
                        'message': response_pep}), 400
    arg_parametrised: str = True if request.args.get('parametrised') != 'False' else False
    arg_drop_ok: str = True if request.args.get('drop_ok') != 'False' else False

    # handle SUBJECT
    if LOG:
        print('check_params -> _check_params_subject: ', arg_parametrised)
    response_pep, required_params_subject, optional_params_subject, flag_error, flag_invalid = _check_params_subject(
        data['subject'], REQUIRED_PARAMS_SUBJECT, response_pep, arg_parametrised, arg_drop_ok, LOG)

    if flag_error:
        return jsonify({'status': 'Bad Request', 'decision': False, 'demo': 'check_params -> _check_params_subject',
                        'message': response_pep}), 400

    if flag_invalid:
        return jsonify({'status': 'OK', 'decision': False, 'demo': 'check_params -> _check_params_subject',
                        'message': response_pep}), 200

    print(f'{required_params_subject=}, {optional_params_subject=}')
    required_params_subject_log.append(required_params_subject)
    optional_params_subject_log.append(optional_params_subject)
    if True:
        return jsonify({'status': 'OK', 'decision': True, 'demo': 'check_params -> _check_params_subject',
                        'message': response_pep}), 200

    # todo: check_params_action
    # todo: check_params_resource
    # todo: check_params_context [Optional]

@app.route('/check_update', methods=['GET', 'POST'])
def check_update():
    """
    Check which parameters have been updated and re-evaluate required parameters which have been altered since
    the last check.
    :return: JSON response
    """
    # loading global variables, especially for keeping track of changes
    global required_params_subject, required_params_subject_log
    global optional_params_subject, optional_params_subject_log
    global LOG, MAX_LENGTH_LOG_LIST
    arg_parametrised: str = True if request.args.get('parametrised') != 'False' else False
    arg_drop_ok: str = True if request.args.get('drop_ok') != 'False' else False

    # basic setup
    response_pep: dict = {'subject': dict(), 'action': dict(), 'resource': dict(), 'context': dict()}
    updated_data: dict = request.get_json(silent=True)  # sets 'data = None' if payload cannot be parsed
    # todo: does 'response_pep' make sense here?
    if updated_data is None:
        return jsonify(
            {'status': 'Bad Request', 'decision': False, 'demo': 'check_update -> request.get_json',
             'message': response_pep}), 400
    if len(required_params_subject_log) > MAX_LENGTH_LOG_LIST:
        return jsonify(
            {'status': 'OK', 'decision': False, 'demo': 'check_update -> log length valid?',
             'message': response_pep}), 200

    is_valid: bool = True
    if arg_parametrised: # checking value changes
        diff: dict = DeepDiff(updated_data['subject']['properties'], required_params_subject_log[-1])
        for path in diff.affected_paths:
            if not is_valid:
                break
            matches: list[str] = re.findall("'([^']+)'", path)
            param_to_check: str = matches[-1]
            if param_to_check in set(required_params_subject.keys()):
                is_valid = pdp_os.is_required_param_valid(
                    updated_data['subject']['properties'][param_to_check], param_to_check, updated_data['subject']['id'],
                    updated_data, log=True)
                response_pep['subject'][param_to_check] = 'valid' if is_valid else 'invalid'
        required_params_subject_log.append(updated_data['subject']['properties'])
        optional_params_subject_log.append(dict())

    # note that 'check_update' is not used for the non-parametrised API version
    # this function invocation is for illustrative purposes only
    if not arg_parametrised:
        required_params_subject_log.append(dict())
        optional_params_subject_log.append(updated_data['subject']['properties'])


    print('ARRIVED: check_update - 3')
    if is_valid:
        return jsonify({'status': 'OK', 'decision': True, 'demo': 'check_update',
                        'message': response_pep}), 200

    return jsonify({'status': 'Forbidden', 'decision': False, 'demo': 'check_update',
                    'message': response_pep}), 403


if __name__ == '__main__':
    app.run(debug=True, port=2111)
