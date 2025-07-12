from demonstration.classes.subject import Subject


class User(Subject):
    def __init__(self, sid: str):
        self.type: str = 'user'
        super().__init__(sid)


