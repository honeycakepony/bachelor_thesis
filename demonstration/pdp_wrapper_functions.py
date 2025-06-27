import pdp_organisation_specific as pdp_os
from copy import deepcopy


# Note: The internal functionality of the helper functions is non-normative functionality and a more sophisticated
#       implementation is to be expected in a real implementation.
#       Many checks are kept simple for illustrative purposes.

def _check_params_subject(
        data_subject: dict, required_params_subject: dict, response_pep: dict, parametrised: bool, drop_ok: bool,
        log=False) \
        -> tuple[dict, dict, bool, bool]:
    # SUBJECT properties -> needs to be extracted first
    try:
        candidate_params: dict = data_subject['properties']
    except KeyError:
        candidate_params: dict = {}

    # SUBJECT id and type
    # Note:
    # "type: REQUIRED. A string value that specifies the type of the Subject."
    # "id: REQUIRED. A string value containing the unique identifier of the Subject, scoped to the type."
    # Source: OpenID AuthZEN, 2025, section 5.1 -> see Bibliography of thesis
    try:
        stype, sid = data_subject['type'], data_subject['id']
        stype_valid: bool = pdp_os._is_valid_stype(stype, log)
        sid_valid: bool = pdp_os._is_valid_sid(sid, stype, log)
        response_pep['subject']['type'] = 'valid' if stype_valid else 'invalid'
        response_pep['subject']['id'] = 'valid' if sid_valid else 'invalid'
        if not parametrised:
            required_params_subject: dict = {}
            optional_params_subject: dict = deepcopy(candidate_params)
            if stype_valid and sid_valid:
                return response_pep, required_params_subject, optional_params_subject, False, False
            if not stype_valid or not sid_valid:
                return response_pep, required_params_subject, optional_params_subject, False, True
    except KeyError:
        response_pep['subject']['type'] = 'error'
        response_pep['subject']['id'] = 'error'
        return response_pep, None, None, True, True

    # todo: check_params_subject
    #       parametrised == False
    #       drop_args    == False
    #       drop_args    == True

    set_required_params_subject: set[str] = set(required_params_subject.keys())
    set_candidate_params: set[str] = set(candidate_params.keys())
    print('check subject', drop_ok)
    if drop_ok:
        if log:
            print('\t_check_params_subject -> checking for possible subset match')
        if set_required_params_subject.issubset(set_candidate_params):
            required_params_subject: dict = deepcopy(candidate_params)
            optional_params_subject: dict = {}
        else:
            return response_pep, None, None, False, True

    if drop_ok:
        threshold_params_subject: float = 0.50  # dummy value # todo: add to pdp_os
        if (len(set_required_params_subject & set_candidate_params)
                > threshold_params_subject * len(set_required_params_subject)):
            # todo: add function which determines required_params_subject and optional_params_subject
            required_params_subject: dict = deepcopy(candidate_params)
            optional_params_subject: dict = {}
        else:
            return response_pep, None, None, False, True

    is_valid: bool = True
    required_params_subject: dict = deepcopy(candidate_params)
    optional_params_subject: dict = {}
    for k in required_params_subject.keys():
        if not is_valid:
            break
        try:
            if log:
                print(f'\tcheck_params_subject -> pdp_os.is_required_param_valid: {k} for {sid}')
            param_to_check: str = data_subject['properties'][k]
            is_valid = pdp_os.is_required_param_valid(k, param_to_check, sid, data_subject, log)
            response_pep['subject'][k] = 'valid' if is_valid else 'invalid'
        except KeyError:
            response_pep['subject'][k] = 'error'
            return response_pep, None, None, True, True
    else:
        return response_pep, required_params_subject, optional_params_subject, False, False

    return response_pep, None, None, False, True

    # SUBJECT all other properties
    # todo: check_params_subject
    #       parametrised == False
    #       drop_args    == False
    #       drop_args    == True
    #       if flag_error_or_invalid:
    #           return 'Error' or 'Access denied'