import requests
from demonstration.classes.user import User

URL = 'http://127.0.0.1:2110/'

arg_parametrised: bool = True
arg_drop_ok: bool = True

gabriel = User('gabriel@mission-thesis.org')

# PEP infers parameters
gabriel.fingerprint = 'fef2e6094100944eb27f5aa88f3fe110ce2a7066d0d68256c1ec621776339349'
gabriel.ip_address = '210.30.1.241'
gabriel.device_id = '8:65:cc:18:8c:0c'
gabriel.user_session = 'hHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'

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

subject: dict = {
        "type": gabriel.type,
        "id": gabriel.id,
        "properties": {
            "ip_address": gabriel.ip_address,
            "fingerprint": gabriel.fingerprint,
            "device_id": gabriel.device_id,
            "user_session": gabriel.user_session,
        }
}

payload: dict = {
    "subject": subject,
    "resource": resource,
    "action": action,
    "context": context
}

print('Hello')
print(payload)

try:
    response = requests.get(URL + 'check_required_params',
                            params={'parametrised': arg_parametrised, 'drop_ok': arg_drop_ok},
                            json=payload)
except requests.exceptions.JSONDecodeError:
    print('Connection Error')
print(response.status_code, response.json())

subject['properties']['user_session'] = 'hHQWx3VGAttackDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f'

try:
    response = requests.get(URL + 'check_update', json=payload)
except requests.exceptions.JSONDecodeError:
    print('Connection Error')
print(response.status_code, response.json())
