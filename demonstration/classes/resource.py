class Resource:
    def __init__(self, r_type: str, r_id: str):
        self.type: str = r_type
        self.id: str = r_id

    def __make_dict__(self):
        return {
            'type': self.type,
            'id': self.id
        }
