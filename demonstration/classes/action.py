class Action:
    def __init__(self):
        self.name: str = 'can_read' # in line with PoLP

    def __make_dict__(self):
        return {
            'name': self.name
        }

# more complex example in gematik2023feinkonzept, p. 12