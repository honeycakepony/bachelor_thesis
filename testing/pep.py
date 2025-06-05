import requests

URL = 'http://127.0.0.1:2109/'
path = 'handle_request'

# todo: check out requests library about JSON
#       difference to Flask?

# todo: default False param or so ...

### Mandatory Params
payload = {
    "subject": {
        "type": "user",
        "id": "user@mail.com",
        "properties": {
            "name": "Duffy",
            "os": "iOS",
            "os_version": "16.1",
            "integrity_check": "True",
            "fingerprint": "1234567890",
            "device_check": "True",
            "ip_v4": "122.158.6.12",
            "geolocation": "Germany",
            "time_system": "Sun May 18 12:02:53 CEST 2025",
            "authentication": "True",
            "privileges": "privileged"
        }
    },

    "resource": {
        "type": "account",
        "id": "42"
    },

    "action": {
        "name": "can_read",
        "properties": {
            "method": "GET"
         }
    },

    "context": {
        "time": "Sun May 18 12:02:55 CEST 2025"
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
