import requests
from demonstration.user import User

URL = 'http://127.0.0.1:2110/'

gabriel = User('gabriel@mission-thesis.com')
print(gabriel.type, gabriel.id, gabriel.device_id, gabriel.ip_address)
gabriel.device_id = '123456789'
print(gabriel.type, gabriel.id, gabriel.device_id, gabriel.ip_address)


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