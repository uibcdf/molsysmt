class WrongSyntaxisError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)

class WrongSelectionError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)

class WrongTargetError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)

class WrongComparisonError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)

class WrongOutputFilenameError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)

class WrongStepError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)

class WrongTimeError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)

class WrongCoordinatesError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)

class WrongBoxError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = ''
        super().__init__(message)

