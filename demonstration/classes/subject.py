class Subject:
    fingerprint: str
    ip_address: str
    device_id: str
    user_session: str

    def __init__(self, sid: str):
        self.type: str = 'None'
        self.id: str = sid

    # todo: define dummy values
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