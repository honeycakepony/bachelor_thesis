# for my convenience, this is written in Python format
# gematik2023feinkonzept, pp. 111-123

# todo:
#   a. Hintergrundcheck: Entspricht Duffys iPhone den vorgegebenen Bedingungen zum lesenden Zugriff auf die ePA

sample_json_file = {
    # openid2025authorization
    'type': 'user',
    'id': 'user@mail.com',
    'properties': {

        # gematik2023feinkonzept, pp. 111-123
        # 2a
        'name': 'Duffy',
        # 2b
        'os': 'iOS', 'version': '16.1',
        # 2c
        'integrity_check': True,
        'fingerprint': '1234567890',
        # 2d
        'device_check': True,
        # 2e
        'ipv4': '122.158.6.12',
        # 3:
        'geolocation': 'Germany',
        # 4:
        'time_system': 'Sun May 18 12:02:53 CEST 2025',
        # 5:
        'authentication': True,
        # 6:
        'privileges': 'privileged'
    },
    'resource': {
        'type': 'account',
        'id': '42'
    },
    'action': {
        'name': 'can_read'
        'properties': {
            'method': 'GET'
         }
    },
    'context': {
        'time': 'Sun May 18 12:02:55 CEST 2025' # request sent,
    }
}