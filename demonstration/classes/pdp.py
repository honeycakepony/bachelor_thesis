class PDP:


    OPTIONAL_PARAMS_SUBJECT: dict[str, str] = dict()

    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value