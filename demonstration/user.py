class User:
    def __init__(self, subject_id: str):
        self.type: str = 'user'
        self.id: str = subject_id
        self.ip_address: str = 'False'
        self.device_id: str = 'False'
        # todo: continue from here