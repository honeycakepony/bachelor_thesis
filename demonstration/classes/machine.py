from demonstration.classes.subject import Subject


class Machine(Subject):
    def __init__(self, sid: str):
        self.type: str = 'machine'
        super().__init__(sid)
