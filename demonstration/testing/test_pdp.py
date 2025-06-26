import requests
import demonstration.pdp_organisation_specific as pdp_os

from demonstration.classes.action import Action
from demonstration.classes.context import Context
from demonstration.classes.resource import Resource
from demonstration.classes.user import User
from demonstration.classes.machine import Machine
# todo: repair this -> I want to use all tests :)

import unittest

# setup
URL = 'http://127.0.0.1:2111/'

def create_dummy_access_request_no_context(subject_dict: dict) -> dict:
    target_resource = Resource('pdf_file', '2025')
    target_action = Action()
    return {
        "subject": subject_dict,
        "resource": target_resource.__make_dict__(),
        "action": target_action.__make_dict__()
    }


class TestPDP(unittest.TestCase):
    # SUBJECT id type
    def test_valid_check_stype_sid_1(self):
        access_request_valid = create_dummy_access_request_no_context(User('ethan@mission−thesis.org').__make_dict__())
        response = requests.get(URL + 'check_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request_valid)
        print(response.json()['demo'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('valid', response.json()['message']['subject']['type'])
        self.assertEqual('valid', response.json()['message']['subject']['id'])

    def test_valid_check_stype_sid_2(self):
        access_request_valid = create_dummy_access_request_no_context(Machine('c-3po@mission−thesis.org').__make_dict__())
        response = requests.get(URL + 'check_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request_valid)
        print(response.json()['demo'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('valid', response.json()['message']['subject']['type'])
        self.assertEqual('valid', response.json()['message']['subject']['id'])

    def test_invalid_check_stype_sid_1(self):
        access_request_invalid = create_dummy_access_request_no_context(User('ethanol@mission−thesis.org').__make_dict__())
        response = requests.get(URL + 'check_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request_invalid)
        print(response.json()['demo'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('valid', response.json()['message']['subject']['type'])
        self.assertEqual('invalid', response.json()['message']['subject']['id'])

    def test_invalid_check_stype_sid_2(self):
        response = requests.get(URL + 'check_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json={'subject': {'type': 'admin', 'id': ''}})
        print(response.json()['demo'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('invalid', response.json()['message']['subject']['type'], )
        self.assertEqual('invalid', response.json()['message']['subject']['id'])

    def test_invalid_check_stype_sid_3(self):
        response = requests.get(URL + 'check_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json={'subject': {'type': 'admin'}})
        print(response.json()['demo'])
        self.assertEqual(400, response.status_code)
        self.assertEqual('error', response.json()['message']['subject']['type'], )
        self.assertEqual('error', response.json()['message']['subject']['id'])

    # SUBJECT properties
    def test_valid_properties_missing_1(self):
        access_request_valid = create_dummy_access_request_no_context(User('ethan@mission−thesis.org').__make_dict__())
        response = requests.get(URL + 'check_params',
                                params={'parametrised': True, 'drop_ok': False},
                                json=access_request_valid)
        print(response.json()['demo'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('valid', response.json()['message']['subject']['type'])
        self.assertEqual('valid', response.json()['message']['subject']['id'])



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
