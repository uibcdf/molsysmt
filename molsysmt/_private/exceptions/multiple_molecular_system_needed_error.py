class MultipleMolecularSystemsNeededError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'This method works only over a single molecular system. But multiple molecular systems are provided.'
        super().__init__(message)


