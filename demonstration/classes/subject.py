class Subject:
    DEFAULT_PARAM: str = 'False'
    type: str
    fingerprint: str = DEFAULT_PARAM
    ip_address: str = DEFAULT_PARAM
    device_id: str = DEFAULT_PARAM
    user_session: str = DEFAULT_PARAM

    def __init__(self, sid: str):
        self.id: str = sid

    def __make_dict__(self):
        return {
            'id': self.id,
            'type': self.type,
            'properties': {
                'fingerprint': self.fingerprint,
                'ip_address': self.ip_address,
                'device_id': self.device_id,
                'user_session': self.user_session
            }
        }
