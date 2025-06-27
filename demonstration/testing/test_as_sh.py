import unittest
from copy import deepcopy

import requests

URL = 'http://127.0.0.1:2111/'

# setup
subject: dict = {
    'type': 'user',
    'id': 'gabriel@mission−thesis.org',
    'properties': {
        'fingerprint': 'fef2e6094100944eb27f5aa88f3fe110ce2a7066d0d68256c1ec621776339349',
        'ip_address': '210.30.1.241',
        'device_id': '2:42:aa:e8:8d:0c',
        'user_session': 'hHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f',
        'requested_ports': '443'
    }
}

action: dict = {
    'name': 'can_read'
}

resource: dict = {
    'type': 'file',
    'id': '2025'
}

context: dict = {
    'time': 'Wed Jun 25 14:57:55 CEST 2025'
}

access_request: dict = {
    'subject': subject,
    'action': action,
    'resource': resource,
    'context': context
}

class TestAttackScenarioSH(unittest.TestCase):
    # Parametrised
    def test_param_sh_attacker(self):
        response = requests.get(URL + 'check_params',
                                params={'parametrised': True, 'drop_ok': False},
                                json=access_request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json()['decision'])
        # hijack session -> user_session of hijacked session
        access_request_change = deepcopy(access_request)
        access_request_change['subject']['properties']['user_session'] = 'gHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'
        response = requests.get(URL + 'check_update',
                                params={'parametrised': True, 'drop_ok': False},
                                json=access_request_change)
        print(f'The following change was detected: {response.json()['message']['subject']}')
        self.assertEqual(403, response.status_code)
        self.assertEqual(False, response.json()['decision'])


    # Non-parametrised
    def test_nonparam_sh_attacker(self):
        response = requests.get(URL + 'check_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json()['decision'])
        # hijack session -> user_session of hijacked session
        access_request_change = deepcopy(access_request)
        access_request_change['subject']['properties'][
            'user_session'] = 'gHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'
        # note that 'check_update' is not used for the non-parametrised API version
        # this function invocation is for illustrative purposes only
        response = requests.get(URL + 'check_update',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request_change)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json()['decision'])

if __name__ == '__main__':
    unittest.main()
