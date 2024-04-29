class UserAlreadyExists(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message) 


class WrongPassword(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)        