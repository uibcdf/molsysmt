class WrongCoordinatesError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)


