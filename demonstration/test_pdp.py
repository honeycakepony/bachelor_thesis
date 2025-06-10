import unittest

import requests

# setup
URL = 'http://127.0.0.1:2110/'

subject: dict = {
        "type": "user",
        "id": "ethan@mission−thesis.org",
        "properties": {
            "ip_v4": "217.233.97.120",
            "geolocation": "Germany",
        }
}

subject_invalid_ip: dict = {
        "type": "user",
        "id": "ethan@mission−thesis.org",
        "properties": {
            "ip_v4": "110.40.0.211", # changed IP
            "geolocation": "Germany", # does it detect the wrong country
        }
}

resource: dict = {
        "type": "account",
        "id": "42"
}

action: dict = {
        "name": "can_read",
        "properties": {
            "method": "GET"
         }
    }

context: dict = {
        "time": "Sun May 18 12:02:55 CEST 2025"
}

payload: dict = {
    "subject": subject,
    "resource": resource,
    "action": action,
    "context": context
}


class TestPDP(unittest.TestCase):
    def test_missing_mandatory_params(self):
        response = requests.get(URL + 'check_mandatory_params_1', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Mandatory parameter(s) are either not present or invalid.')

    def test_mandatory_params_reduction(self):
        response = requests.get(URL + 'check_mandatory_params_2', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'All mandatory parameters are present.')

if __name__ == '__main__':
    unittest.main()
