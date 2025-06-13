import requests

URL = 'http://127.0.0.1:2110/'

subject: dict = {
        "type": "user",
        "id": "user@mail.com",
        "properties": {
            # author's fingerprint using https://amiunique.org/fingerprint (sligthly adjusted), last access 3 June 2025
            "fingerprint": "dfd1fd7cf55ab8de9cc656c3716dbc1d85713480"
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

response = requests.get(URL + 'check_mandatory_params', json=payload)
if response.status_code != 200:
    print(f'Server: {response.json()}')
else:
    print(f'Server: {response.json()}')

response = requests.get(URL + 'handle_access_request', json=payload)
if response.status_code != 200:
    print(f'Server: {response.json()}')
else:
    print(f'Server: {response.json()}')