import unittest
from copy import deepcopy

import requests

URL = 'http://127.0.0.1:2111/'

# setup
# data partly based on~\cite[p. 7]{BHT_Akira}
subject: dict = {
    'type': 'user',
    'id': 'account3@mission−thesis.org',
    'properties': {
        'fingerprint': '38eda86f21d3c8c316d08b376ec437051cf3d7146d79c7301bd6d63b4fc8b0af',
        'device_id': '4:41:bb:ee:8f:0c',
        'user_session': '66d8c683f483cc9c0e7335b25ec25cd490da5111123a87b4',
        'requested_ports': '3389'
    }
}

action: dict = {
    'name': 'can_read'
}

resource: dict = {
    'type': 'files',
    'id': '2024'
}

context: dict = {
    'time': 'Tue Feb 20 06:54:24 CEST 2024'
}

access_request: dict = {
    'subject': subject,
    'action': action,
    'resource': resource,
    'context': context
}


class TestAttackScenarioRA(unittest.TestCase):
    # ------------------
    # Parametrised
    # ------------------
    # note: this implementation issues the following message if an RDP request is detected:
    #       'CAUTION: remote access via RDP' -> could be used for further checks or close monitoring of connection
    def test_param_ra_attacker(self):
        response = requests.get(URL + 'check_params',
                                params={'parametrised': True, 'drop_ok': False},
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
