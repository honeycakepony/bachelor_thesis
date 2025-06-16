import requests

from demonstration.classes.action import Action
from demonstration.classes.context import Context
from demonstration.classes.resource import Resource
from demonstration.classes.user import User
from demonstration.classes.machine import Machine
from demonstration.pdp_internal import _is_valid_sid, is_valid_stype

import unittest

# setup
URL = 'http://127.0.0.1:2110/'

# subject_valid: dict = {
#     "type": "user",
#     "id": "ethan@mission−thesis.org",
#     "properties": {
#         "ip_address": "217.233.97.120",
#         "geolocation": "Germany",
#     }
# }
#
# subject_invalid: dict = {
#     "type": "user",
#     "id": "ethan@mission−thesis.org",
#     "properties": {
#         "ip_address": "217.233.97.120",
#         "geolocation": "Germany",
#     }
# }
#
# subject_invalid_ip: dict = {
#     "type": "user",
#     "id": "ethan@mission−thesis.org",
#     "properties": {
#         "ip_address": "110.40.0.211",  # changed IP
#         "geolocation": "Germany",  # does it detect the wrong country
#     }
# }
#
# resource: dict = {
#     "type": "account",
#     "id": "42"
# }
#
# action: dict = {
#     "name": "can_read",
#     "properties": {
#         "method": "GET"
#     }
# }
#
# context: dict = {
#     "time": "Sun May 18 12:02:55 CEST 2025"
# }
#
# payload_valid_user: dict = {
#     "subject": subject_valid,
#     "resource": resource,
#     "action": action,
#     "context": context
# }
#
# payload_invalid_user: dict = {
#     "subject": subject_invalid,
#     "resource": resource,
#     "action": action,
#     "context": context
# }

target_resource = Resource('pdf_file', '2025')
target_action = Action()


# payload: dict = {"subject": subject, "resource": resource, "action": action, "context": context}
# access_request: dict = {"subject": user_valid, "resource": target_resource, "action": target_action}

class TestPDP(unittest.TestCase):
    #
    # testing subject properties
    #

    #   testing subject id (sid)
    def test_sid_valid_1(self):
        user_valid = User('gabriel@mission−thesis.org')
        response: bool = _is_valid_sid(user_valid.id, user_valid.type, log=True)
        self.assertTrue(response)

    def test_sid_valid_2(self):
        machine_valid = Machine('r2-d2@mission−thesis.org')
        response: bool = _is_valid_sid(machine_valid.id, machine_valid.type, log=True)
        self.assertTrue(response)

    def test_sid_invalid_1(self):
        user_invalid = User('gabrielll@mission−thesis.org')
        response: bool = _is_valid_sid(user_invalid.id, user_invalid.type, log=True)
        self.assertFalse(response)

    def test_sid_invalid_2(self):
        user_invalid = User('gabriel@mission−thesis.org')
        user_invalid.type = 'superuser'
        response: bool = _is_valid_sid(user_invalid.id, user_invalid.type, log=True)
        self.assertFalse(response)

    def test_sid_invalid_3(self):
        machine_invalid = Machine('gabriel@mission−thesis.org')
        machine_invalid.type = 'auditor'
        response: bool = _is_valid_sid(machine_invalid.id, machine_invalid.type, log=True)
        self.assertFalse(response)

    # testing subject type (stype)
    def test_stype_valid_1(self):
        user_valid = User('type@mission−thesis.org')
        response: bool = is_valid_stype(user_valid.type, log=True)
        self.assertTrue(response)

    def test_stype_valid_2(self):
        machine_valid = Machine('test@mission−thesis.org')
        response: bool = is_valid_stype(machine_valid.type, log=True)
        self.assertTrue(response)

    def test_stype_invalid_1(self):
        machine_invalid = Machine('test@mission−thesis.org')
        machine_invalid.type = 'auditor'
        response: bool = is_valid_stype(machine_invalid.type, log=True)
        self.assertFalse(response)

    def test_stype_invalid_2(self):
        machine_invalid = Machine('test@mission−thesis.org')
        machine_invalid.type = 'supermachine'
        response: bool = is_valid_stype(machine_invalid.type, log=True)
        self.assertFalse(response)

    def test_stype_invalid_3(self):
        user_invalid = User('test@mission−thesis.org')
        user_invalid.type = 'superuser'
        response: bool = is_valid_stype(user_invalid.type, log=True)
        self.assertFalse(response)

    def test_check_required_params_valid_1(self):
        user_valid = User('gabriel@mission−thesis.org')
        access_request_valid = {"subject": user_valid.__make_dict__(), "resource": target_resource, "action": target_action}
        print(access_request_valid)
        response = requests.get(URL + 'check_required_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request_valid)
        self.assertEqual(response.status_code, 200)

    def test_check_required_params_valid_2(self):
        machine_valid = Machine('r2-d2@mission−thesis.org')
        access_request_valid = {"subject": machine_valid.__make_dict__(), "resource": target_resource, "action": target_action}
        print(access_request_valid)
        response = requests.get(URL + 'check_required_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request_valid)
        self.assertEqual(response.status_code, 200)

    # def test_missing_mandatory_params(self):
    #     response = requests.get(URL + 'check_mandatory_params_1', json=payload_valid_user)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['message'], 'Mandatory parameter(s) are either not present or invalid.')
    #
    # def test_mandatory_params_reduction(self):
    #     response = requests.get(URL + 'check_mandatory_params_2', json=payload_valid_user)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['message'], 'All mandatory parameters are present.')
    #
    # # doesn't matter which check_mandatory_params_X is used
    # def test_invalid_id(self):
    #     payload_invalid_user['subject']['id'] = 'gabriel@mission−thesis.org'
    #     response = requests.get(URL + 'check_mandatory_params_1', json=payload_invalid_user)
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json()['status'], 'Forbidden')
    #
    # # doesn't matter which check_mandatory_params_X is used
    # def test_invalid_type(self):
    #     payload_invalid_user['subject']['type'] = 'superuser'
    #     response = requests.get(URL + 'check_mandatory_params_2', json=payload_invalid_user)
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json()['status'], 'Forbidden')


if __name__ == '__main__':
    unittest.main()
