import requests

from demonstration.classes.action import Action
from demonstration.classes.context import Context
from demonstration.classes.resource import Resource
from demonstration.classes.user import User
from demonstration.classes.machine import Machine
from demonstration.pdp_internal import _is_valid_sid, _is_valid_stype, _is_valid_session_id

import unittest

# setup
URL = 'http://127.0.0.1:2110/'

def create_dummy_access_request_no_context(subject_dict: dict) -> dict:
    target_resource = Resource('pdf_file', '2025')
    target_action = Action()
    return {
        "subject": subject_dict,
        "resource": target_resource.__make_dict__(),
        "action": target_action.__make_dict__()
    }

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
        self.assertFalse(response) # 'gabrielll@mission−thesis.org' invalid

    def test_sid_invalid_2(self):
        user_invalid = User('gabriel@mission−thesis.org')
        user_invalid.type = 'superuser'
        response: bool = _is_valid_sid(user_invalid.id, user_invalid.type, log=True)
        self.assertFalse(response)  # 'user_invalid.type' invalid

    def test_sid_invalid_3(self):
        machine_invalid = Machine('gabriel@mission−thesis.org')
        machine_invalid.type = 'auditor'
        response: bool = _is_valid_sid(machine_invalid.id, machine_invalid.type, log=True)
        self.assertFalse(response) # 'machine_invalid.type' invalid

    # testing subject type (stype)
    def test_stype_valid_1(self):
        user_valid = User('type@mission−thesis.org')
        response: bool = _is_valid_stype(user_valid.type, log=True)
        self.assertTrue(response)

    def test_stype_valid_2(self):
        machine_valid = Machine('test@mission−thesis.org')
        response: bool = _is_valid_stype(machine_valid.type, log=True)
        self.assertTrue(response)

    def test_stype_invalid_1(self):
        machine_invalid = Machine('test@mission−thesis.org')
        machine_invalid.type = 'auditor'
        response: bool = _is_valid_stype(machine_invalid.type, log=True)
        self.assertFalse(response)  # 'machine_invalid.type' invalid

    def test_stype_invalid_2(self):
        machine_invalid = Machine('test@mission−thesis.org')
        machine_invalid.type = 'supermachine'
        response: bool = _is_valid_stype(machine_invalid.type, log=True)
        self.assertFalse(response) # 'machine_invalid.type' invalid

    def test_stype_invalid_3(self):
        user_invalid = User('test@mission−thesis.org')
        user_invalid.type = 'superuser'
        response: bool = _is_valid_stype(user_invalid.type, log=True)
        self.assertFalse(response) # 'user_invalid.type' invalid

    def test_check_required_params_valid_1(self):
        user_valid = User('gabriel@mission−thesis.org')
        access_request_valid: dict = create_dummy_access_request_no_context(user_valid.__make_dict__())
        response = requests.get(URL + 'check_required_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request_valid)
        self.assertEqual(response.status_code, 200)

    def test_check_required_params_valid_2(self):
        machine_valid = Machine('r2-d2@mission−thesis.org')
        access_request_valid: dict = create_dummy_access_request_no_context(machine_valid.__make_dict__())
        response = requests.get(URL + 'check_required_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request_valid)
        self.assertEqual(response.status_code, 200)

    def test_check_required_params_invalid_1(self):
        user_invalid = User('gabriel@mission_thesis.org')
        access_request_invalid: dict = create_dummy_access_request_no_context(user_invalid.__make_dict__())
        response = requests.get(URL + 'check_required_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request_invalid)
        # 'ethan@mission_thesis.org' invalid
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['testing'], 'Invalid \'stype\' or \'sid\'')

    def test_session_valid(self):
        user_valid = User('ethan@mission−thesis.org')
        user_valid.user_session = 'aHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'
        response: bool = _is_valid_session_id(user_valid.id, user_valid.user_session, log=True)
        self.assertTrue(response)

    def test_session_invalid_1(self):
        user_invalid = User('ethan@mission_thesis.org')
        user_invalid.user_session = 'aHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'
        response: bool = _is_valid_session_id(user_invalid.id, user_invalid.user_session, log=True)
        self.assertFalse(response) # 'ethan@mission_thesis.org' invalid

    def test_session_invalid_2(self):
        user_invalid = User('ethan@mission-thesis.org')
        user_invalid.user_session = 'aHQWx3VGAmhlsATTxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'
        response: bool = _is_valid_session_id(user_invalid.id, user_invalid.user_session, log=True)
        self.assertFalse(response) # 'user_invalid.user_session' invalid


if __name__ == '__main__':
    unittest.main()
