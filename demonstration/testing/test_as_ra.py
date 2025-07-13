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
    # todo: adjust to times mentioned in BHT_Akira
    'time': 'Wed Feb 25 14:57:55 CEST 2024'
}

access_request: dict = {
    'subject': subject,
    'action': action,
    'resource': resource,
    'context': context
}

# usage could be run against 'normal' user behaviour,
# how often are requests typcially made from outside

# perhaps fingerprint oder device_id match

# 2024-02-14 13:15:48 - lab1_pc1_acc1 using RDP
# 2024-02-14 13:22:44 - lab1-pc1_acc2 using RDP
# 2024-02-14 13:57:56 - lab2-pc1 using RDP
# 2024-02-16 11:38:42 - hrz-computer2 using RDP
# 2024-02-16 11:54:49 - hrz-computer3 using RDP
# 2024-02-16 11:54:49 - hrz-computer4 using RDP
# 2024-02-19 08:28:30 - lab_acc using RDP
# 2024-02-19 09:11:38 - lab2-pc1 using RDP
# 2024-02-20 06:54:24 - lab1-pc2 using RDP
# 2024-02-20 07:20:56 - hrz-computer1 using RDP


class TestAttackScenarioRA(unittest.TestCase):
    # ------------------
    # Parametrised
    # ------------------
    def test_param_ra_attacker(self):
        # changed subject user_session mid-session detected -> possibly re-authentication and re-authorisation necessary
        response = requests.get(URL + 'check_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json()['decision'])


    # ------------------
    # Non-parametrised
    # ------------------
    def test_nonparam_ra_attacker(self):
        response = requests.get(URL + 'check_params',
                                params={'parametrised': False, 'drop_ok': False},
                                json=access_request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json()['decision'])

if __name__ == '__main__':
    unittest.main()
