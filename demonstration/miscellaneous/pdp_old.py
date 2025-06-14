# @app.route('/check_mandatory_params_1', methods=['GET', 'POST'])
# def check_mandatory_params_1():
#     """
#     Check whether all mandatory params are present. This check is used for the first encounter between PEP and PDP.
#     This function models version 1 as specified in the section on 'Mandatory Parameters'.
#     If so, allow connection between PEP and PDP.
#     If not, abort connection.
#     Note: It is possible that PEP provides more keys than PDP requires. This is okay.
#     :return: JSON response
#     """
#     data = request.get_json()
#     if not data:
#         return jsonify({
#             'status': 'Bad Request',
#             'message': 'No data provided to process.'
#         }), 400
#
#     # guard clause for check of 'id' and 'type'
#     # Note:
#     # "type: REQUIRED. A string value that specifies the type of the Subject."
#     # "id: REQUIRED. A string value containing the unique identifier of the Subject, scoped to the type."
#     # Source: OpenID AuthZEN, 2025, section 5.1 -> see Bibliography of thesis
#     type_check: bool = data['subject']['type'] in ALLOWED_TYPES
#     id_check: bool = _is_id_valid(data['subject']['id'], data['subject']['type'], LOG)
#     if not type_check or not id_check:
#         return jsonify({
#             'status': 'Forbidden',
#             'message': 'Mandatory parameter(s) for \'id\' or \'type\' invalid.'
#         }), 403
#
#     candidate_keys = data['subject']['properties'].keys()
#     if MANDATORY_PARAMS.issubset(candidate_keys):
#         global mandatory_params
#         global copy_request
#         mandatory_params = MANDATORY_PARAMS
#         copy_request = deepcopy(data)
#         return jsonify({
#             'status': 'OK',
#             'message': 'All mandatory parameters are present.'
#         }), 200
#
#     return jsonify({
#         'status': 'Forbidden',
#         'message': 'Mandatory parameter(s) for \'properties\' invalid.'
#     }), 403
#
#
# @app.route('/check_mandatory_params_2', methods=['GET', 'POST'])
# def check_mandatory_params_2():
#     """
#     Check whether all mandatory params are present. This check is used for the first encounter between PEP and PDP.
#     This function models version 2 as specified in the section on 'Mandatory Parameters'.
#     If so, allow connection between PEP and PDP.
#     If not, abort connection.
#     Note: It is possible that PEP provides more keys than PDP requires. This is okay.
#     :return: JSON response
#     """
#     data = request.get_json()
#     if not data:
#         return jsonify({
#             'status': 'Bad Request',
#             'message': 'No data provided to process.'
#         }), 400
#
#     # guard clause for check of 'id' and 'type' -> check explanation in check_mandatory_params_1
#     type_check: bool = data['subject']['type'] in ALLOWED_TYPES
#     id_check: bool = _is_id_valid(data['subject']['id'], data['subject']['type'], LOG)
#     if not type_check or not id_check:
#         return jsonify({
#             'status': 'Forbidden',
#             'message': 'Mandatory parameter(s) for \'id\' or \'type\' invalid.'
#         }), 403
#
#     # Check for relative size of intersection. If size suffices for pre-determined threshold (THRESHOLD_PARAMS),
#     # create reduced set of mandatory params.
#     candidate_keys = data['subject']['properties'].keys()
#     if len(MANDATORY_PARAMS & candidate_keys) >= THRESHOLD_PARAMS * len(MANDATORY_PARAMS):
#         global mandatory_params
#         global copy_request
#         copy_request = deepcopy(data)
#         mandatory_params = MANDATORY_PARAMS.intersection(candidate_keys)
#         return jsonify({
#             'status': 'OK',
#             'message': 'All mandatory parameters are present.'
#         }), 200
#
#     return jsonify({
#         'status': 'Forbidden',
#         'message': 'Mandatory parameter(s) for \'properties\' invalid.'
#     }), 403