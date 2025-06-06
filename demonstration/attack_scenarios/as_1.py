import requests

URL = 'http://127.0.0.1:2110/'

subject: dict = {
        "type": "user",
        "id": "user@mail.com",
        "properties": {
            "ip_v4": "1.0.42.211", # 217.233.97.120 my IP on 2 June
            "geolocation": "China",
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