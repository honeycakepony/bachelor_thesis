from flask import Flask, abort, request, jsonify
from deepdiff import DeepDiff
from requests import Response
from http_status_code_exception.client_error import BadRequest
from pdp_wrapper_functions import _check_params_subject

import pdp_organisation_specific as pdp_os
import re

app = Flask(__name__)

# defining 'required' parameters for this PDP
DEFAULT_PARAM: str = 'False'
REQUIRED_PARAMS_SUBJECT: dict[str, str] = {
    'fingerprint': DEFAULT_PARAM,
    'ip_address': DEFAULT_PARAM,
    'device_id': DEFAULT_PARAM,
    'user_session': DEFAULT_PARAM,
    'requested_ports': DEFAULT_PARAM
}

# global variables required for PDP's functionality
MAX_LENGTH_LOG_LIST: int = 10  # organisation-specific
required_params_subject: dict[str, str] = dict()
optional_params_subject: dict[str, str] = list()
required_params_subject_log: list[dict[str, str]] = list()
optional_params_subject_log: list[dict[str, str]] = list()

# to make use of logging functionality -> print statements in this file
LOG: bool = True


@app.route('/check_params', methods=['GET', 'POST'])
def check_params():
    """
    Check whether all required params are present. This check is used for the first encounter between PEP and PDP.
    Dependent on the arguments in the request, this function models the different versions of the API.
    If so, allow connection between PEP and PDP. If not, abort connection.
    Note: It is possible that PEP provides more parameters than PDP requires. This is okay.
    :return: JSON response
    """
    # load all variables with global scope and complete setup for function
    global required_params_subject
    global optional_params_subject
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

    # flag for control flow of function
    if flag_error:
        return jsonify({'status': 'Bad Request', 'decision': False, 'demo': 'check_params -> _check_params_subject',
                        'message': response_pep}), 400
    if flag_invalid:
        return jsonify({'status': 'OK', 'decision': False, 'demo': 'check_params -> _check_params_subject',
                        'message': response_pep}), 200

    required_params_subject_log.append(required_params_subject)
    optional_params_subject_log.append(optional_params_subject)

    # Note: As mentioned in Section 5.1 Assumptions, the required JSON objects 'action' and 'resource'
    #       and the optional one 'context' are left out to allow for a better focus on the handling of 'subject',
    #       i.e. there is no check_params_action, check_params_resource, or check_params_context function implemented.

    return jsonify({'status': 'OK', 'decision': True, 'demo': 'check_params -> _check_params_subject',
                    'message': response_pep}), 200


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

    # basic setup
    response_pep: dict = {'subject': dict(), 'action': dict(), 'resource': dict(), 'context': dict()}
    updated_data: dict = request.get_json(silent=True)  # sets 'data = None' if payload cannot be parsed
    if updated_data is None:
        return jsonify(
            {'status': 'Bad Request', 'decision': False, 'demo': 'check_update -> request.get_json',
             'message': response_pep}), 400
    if len(required_params_subject_log) > MAX_LENGTH_LOG_LIST:
        return jsonify(
            {'status': 'OK', 'decision': False, 'demo': 'check_update -> log length valid?',
             'message': response_pep}), 200

    is_valid: bool = True
    if arg_parametrised:  # checking value changes
        diff: dict = DeepDiff(updated_data['subject']['properties'], required_params_subject_log[-1])
        for path in diff.affected_paths:
            if not is_valid:
                break
            matches: list[str] = re.findall("'([^']+)'", path)
            param_to_check: str = matches[-1]
            if param_to_check in set(required_params_subject.keys()):
                is_valid = pdp_os.is_required_param_valid(
                    updated_data['subject']['properties'][param_to_check], param_to_check,
                    updated_data['subject']['id'],
                    updated_data, log=True)
                response_pep['subject'][param_to_check] = 'valid' if is_valid else 'invalid'
        required_params_subject_log.append(updated_data['subject']['properties'])
        optional_params_subject_log.append(dict())

    if is_valid:
        return jsonify({'status': 'OK', 'decision': True, 'demo': 'check_update',
                        'message': response_pep}), 200

    return jsonify({'status': 'Forbidden', 'decision': False, 'demo': 'check_update',
                    'message': response_pep}), 403


if __name__ == '__main__':
    app.run(debug=True, port=2111)
