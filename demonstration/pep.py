from datetime import datetime, timezone

import requests
import pep_internal as pepi

URL = 'http://127.0.0.1:2110/'
path = 'handle_request'

# todo: check out requests library about JSON
#       difference to Flask?

# todo: default False param or so ...

DEFAULT_PARAMS: dict = {
    'subject': {
        'type': 'False',
        'id': 'False',
        'properties': {
            'ip_address': 'False',
            'geolocation': 'False',

            'fingerprint': 'False',

            "name": "False",
            "os": "False",
            "os_version": "False",
            "integrity_check": "False",
            "device_check": "False",
            "time_system": "False",
            "authentication": "False",
            "privileges": "False"
        }
    },

    "resource": {
        "type": "False",
        "id": "False"
    },

    "action": {
        "name": "False",
        "properties": {
            "method": "False"
         }
    },

    "context": {
        "time": f"{datetime.now(timezone.utc).isoformat()}"
    }
}

subject_valid: dict = {
        "type": "user",
        "id": "ethan@mission−thesis.org",
        "properties": {
            "ip_address": "217.233.97.120",
            "geolocation": "Germany",
        }
}

subject_valid_no_properties: dict = {
        "type": "user",
        "id": "ethan@mission−thesis.org",
}

subject_invalid: dict = {
        "type": "user",
        "id": "ethan@mission−thesis.org",
        "properties": {
            "ip_address": "217.233.97.120",
            "geolocation": "Germany",
        }
}

subject_invalid_ip: dict = {
        "type": "user",
        "id": "ethan@mission−thesis.org",
        "properties": {
            "ip_address": "110.40.0.211", # changed IP
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

payload_valid_user: dict = {
    "subject": subject_valid_no_properties,
    "resource": resource,
    "action": action,
    "context": context
}



response = requests.get(
    URL + 'check_required_params', params={'parametrised': True, 'drop_ok': False}, json=payload_valid_user)
print(response.status_code, response.json())


### handle basic request
# response = requests.post(URL + path, json=payload)
# if response.status_code != 200:
#     print(f'Server Error: {response.status_code}')
# else:
#     print(f'Server: {response.json()}')
