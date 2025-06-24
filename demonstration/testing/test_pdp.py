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


class TestPDP(unittest.TestCase):
    # LOGGING
    def test_logging_True(self):
        user_valid = User('ethan@mission−thesis.org')
        access_request_invalid = create_dummy_access_request_no_context(user_valid.__make_dict__())
        response = requests.get(URL + 'check_params',
                                params={'parametrised': False, 'drop_ok': False}, json=access_request_invalid)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(response.json()['message']['subject']['type'], 'valid')
        self.assertEqual(response.json()['message']['subject']['id'], 'valid')

    # SUBJECT PROPERTIES



    #   testing subject id (sid)
    # def test_sid_valid_1(self):
    #     user_valid = User('gabriel@mission−thesis.org')
    #     response: bool = _is_valid_sid(user_valid.id, user_valid.type, log=True)
    #     self.assertTrue(response)
    #
    # def test_sid_valid_2(self):
    #     machine_valid = Machine('r2-d2@mission−thesis.org')
    #     response: bool = _is_valid_sid(machine_valid.id, machine_valid.type, log=True)
    #     self.assertTrue(response)
    #
    # def test_sid_invalid_1(self):
    #     user_invalid = User('gabrielll@mission−thesis.org')
    #     response: bool = _is_valid_sid(user_invalid.id, user_invalid.type, log=True)
    #     self.assertFalse(response) # 'gabrielll@mission−thesis.org' invalid
    #
    # def test_sid_invalid_2(self):
    #     user_invalid = User('gabriel@mission−thesis.org')
    #     user_invalid.type = 'superuser'
    #     response: bool = _is_valid_sid(user_invalid.id, user_invalid.type, log=True)
    #     self.assertFalse(response)  # 'user_invalid.type' invalid
    #
    # def test_sid_invalid_3(self):
    #     machine_invalid = Machine('gabriel@mission−thesis.org')
    #     machine_invalid.type = 'auditor'
    #     response: bool = _is_valid_sid(machine_invalid.id, machine_invalid.type, log=True)
    #     self.assertFalse(response) # 'machine_invalid.type' invalid
    #
    # # testing subject type (stype)
    # def test_stype_valid_1(self):
    #     user_valid = User('type@mission−thesis.org')
    #     response: bool = _is_valid_stype(user_valid.type, log=True)
    #     self.assertTrue(response)
    #
    # def test_stype_valid_2(self):
    #     machine_valid = Machine('test@mission−thesis.org')
    #     response: bool = _is_valid_stype(machine_valid.type, log=True)
    #     self.assertTrue(response)
    #
    # def test_stype_invalid_1(self):
    #     machine_invalid = Machine('test@mission−thesis.org')
    #     machine_invalid.type = 'auditor'
    #     response: bool = _is_valid_stype(machine_invalid.type, log=True)
    #     self.assertFalse(response)  # 'machine_invalid.type' invalid
    #
    # def test_stype_invalid_2(self):
    #     machine_invalid = Machine('test@mission−thesis.org')
    #     machine_invalid.type = 'supermachine'
    #     response: bool = _is_valid_stype(machine_invalid.type, log=True)
    #     self.assertFalse(response) # 'machine_invalid.type' invalid
    #
    # def test_stype_invalid_3(self):
    #     user_invalid = User('test@mission−thesis.org')
    #     user_invalid.type = 'superuser'
    #     response: bool = _is_valid_stype(user_invalid.type, log=True)
    #     self.assertFalse(response) # 'user_invalid.type' invalid
    #
    # def test_check_required_params_valid_1(self):
    #     user_valid = User('gabriel@mission−thesis.org')
    #     access_request_valid: dict = create_dummy_access_request_no_context(user_valid.__make_dict__())
    #     response = requests.get(URL + 'check_required_params',
    #                             params={'parametrised': False, 'drop_ok': False},
    #                             json=access_request_valid)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_check_required_params_valid_2(self):
    #     machine_valid = Machine('r2-d2@mission−thesis.org')
    #     access_request_valid: dict = create_dummy_access_request_no_context(machine_valid.__make_dict__())
    #     response = requests.get(URL + 'check_required_params',
    #                             params={'parametrised': False, 'drop_ok': False},
    #                             json=access_request_valid)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_check_required_params_invalid_1(self):
    #     user_invalid = User('gabriel@mission_thesis.org')
    #     access_request_invalid: dict = create_dummy_access_request_no_context(user_invalid.__make_dict__())
    #     response = requests.get(URL + 'check_required_params',
    #                             params={'parametrised': False, 'drop_ok': False},
    #                             json=access_request_invalid)
    #     # 'ethan@mission_thesis.org' invalid
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json()['testing'], 'Invalid \'stype\' or \'sid\'')
    #
    # def test_session_valid(self):
    #     user_valid = User('ethan@mission−thesis.org')
    #     user_valid.user_session = 'aHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'
    #     response: bool = _is_valid_session_id(user_valid.id, user_valid.user_session, log=True)
    #     self.assertTrue(response)
    #
    # def test_session_invalid_1(self):
    #     user_invalid = User('ethan@mission_thesis.org')
    #     user_invalid.user_session = 'aHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'
    #     response: bool = _is_valid_session_id(user_invalid.id, user_invalid.user_session, log=True)
    #     self.assertFalse(response) # 'ethan@mission_thesis.org' invalid
    #
    # def test_session_invalid_2(self):
    #     user_invalid = User('ethan@mission-thesis.org')
    #     user_invalid.user_session = 'aHQWx3VGAmhlsATTxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'
    #     response: bool = _is_valid_session_id(user_invalid.id, user_invalid.user_session, log=True)
    #     self.assertFalse(response) # 'user_invalid.user_session' invalid

    # todo:
    #   - check_required_params
    #   - handle_access_request
    #   - check_update

if __name__ == '__main__':
    unittest.main()
