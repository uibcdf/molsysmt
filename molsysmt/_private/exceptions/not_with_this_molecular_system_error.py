class NotWithThisMolecularSystemError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'This method can not be applied over this molecular system.'
        super().__init__(message)


