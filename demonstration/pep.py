from datetime import datetime, timezone

import requests
import pep_internal as pepi

URL = 'http://127.0.0.1:2109/'
path = 'handle_request'

# todo: check out requests library about JSON
#       difference to Flask?

# todo: default False param or so ...

DEFAULT_PARAMS: dict = {
    'subject': {
        'type': 'False',
        'id': 'False',
        'properties': {
            'ip_v4': 'False',
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

response = requests.get(URL + 'check_mandatory_params', json=payload)
if response.status_code != 200:
    print(f'Server: {response.json()}')
else:
    print(f'Server: {response.json()}')


### handle basic request
# response = requests.post(URL + path, json=payload)
# if response.status_code != 200:
#     print(f'Server Error: {response.status_code}')
# else:
#     print(f'Server: {response.json()}')
