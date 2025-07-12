from datetime import datetime, timezone

import requests
import pep_internal as pepi

URL = 'http://127.0.0.1:2110/'
path = 'handle_request'

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
        "time": f"{datetime.now(timezone.utc).isoformat()}"
}

payload_valid_user: dict = {
    "subject": subject_valid_no_properties,
    "resource": resource,
    "action": action,
    "context": context
}

response = requests.get(URL + 'say_hello', json=payload_valid_user)
print(response.status_code, respone.json())

response = requests.get(
    URL + 'check_required_params', params={'parametrised': True, 'drop_ok': False}, json=payload_valid_user)
print(response.status_code, response.json())
