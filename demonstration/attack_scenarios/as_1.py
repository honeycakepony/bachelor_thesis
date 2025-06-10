import requests

URL = 'http://127.0.0.1:2110/'

subject: dict = {
        "type": "user",
        "id": "ethan@mission−thesis.org",
        "properties": {
            "ip_v4": "217.233.97.120",
            "geolocation": "Germany",
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

response = requests.get(URL + 'check_mandatory_params_1', json=payload)
print(response.status_code, response.json())

response = requests.get(URL + 'check_mandatory_params_2', json=payload)
print(response.status_code, response.json())
#
# response = requests.get(URL + 'handle_access_request', json=payload)
# print(response.status_code, response.json())

subject: dict = {
        "type": "user",
        "id": "ethan@mission−thesis.org",
        "properties": {
            "ip_v4": "110.40.0.211", # changed IP
            "geolocation": "Germany",
        }
}

payload: dict = {
    "subject": subject,
    "resource": resource,
    "action": action,
    "context": context
}

response = requests.get(URL + 'check_update', json=payload)
print(response.status_code, response.json())
