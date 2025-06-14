class User:
    def __init__(self, subject_id: str):
        self.type: str = 'user'
        self.id: str = subject_id
        self.ip_address: str = ''
        self.device_id: str = ''
        # todo: continue from here