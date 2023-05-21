class NotConfigured(Exception):
    "Exception raised when non existing key in settings module is raised"
    pass


class NotImplementedInterface(TypeError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        