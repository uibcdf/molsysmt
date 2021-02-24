class BadCallError(ValueError):
    def __init__(self):
        message = 'Wrong way of invoking this method. Check the online documentation for more information: http://www.uibcdf.org/MolSysMT'
        super().__init__(message)

class NotWithThisFormError(ValueError):
    def __init__(self):
        message = 'This method can not be applied over this molecular system form.'
        super().__init__(message)

class NeedsMultipleMolecularSystemsError(ValueError):
    def __init__(self):
        message = 'This method works only over a single molecular system. But multiple molecular systems are provided.'
        super().__init__(message)

class NeedsSingleMolecularSystemError(ValueError):
    def __init__(self):
        message = 'This method works only over a single molecular system. But multiple molecular systems are provided.'
        super().__init__(message)

class NotImplementedError(NotImplementedError):
    def __init__(self):
        message = 'It has not been implemeted yet.\n Write a new issue in https://github.com/uibcdf/MolSysMT/issues asking for it.'
        super().__init__(message)

class LibraryNotFound(NotImplementedError):
    def __init__(self, library):
        message = 'The python library {} was not found.'.format(library)
        super().__init__(message)

