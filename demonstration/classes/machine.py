from demonstration.classes.subject import Subject


class Machine(Subject):
    fingerprint: str
    ip_address: str
    device_id: str
    user_session: str

    def __init__(self, sid: str):
        self.type: str = 'machine'
        super().__init__(sid)


