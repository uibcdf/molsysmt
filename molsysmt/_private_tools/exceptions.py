class BadCallError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'Wrong way of invoking this method. Check the online documentation for more information: http://www.uibcdf.org/MolSysMT'
        super().__init__(message)

class NotWithThisFormError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'This method can not be applied over this molecular system form.'
        super().__init__(message)

class NotWithThisMolecularSystemError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'This method can not be applied over this molecular system.'
        super().__init__(message)

class NeedsMultipleMolecularSystemsError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'This method works only over a single molecular system. But multiple molecular systems are provided.'
        super().__init__(message)

class NeedsSingleMolecularSystemError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'This method works only over a single molecular system. But multiple molecular systems are provided.'
        super().__init__(message)

class NoMolecularSystemError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'A molecular system is needed.'
        super().__init__(message)

class NotImplementedError(NotImplementedError):
    def __init__(self, message=None):
        if message is None:
            message = 'It has not been implemeted yet. Write a new issue in https://github.com/uibcdf/MolSysMT/issues asking for it.'
        super().__init__(message)

class NotImplementedConversionError(NotImplementedError):
    def __init__(self, from_form, to_form, message=None):
        if message is None:
            message = 'The conversion from {} to {} has not been implemeted yet. Write a new issue in https://github.com/uibcdf/MolSysMT/issues \
asking for it.'.format(from_form, to_form)
        super().__init__(message)

class NotImplementedFormError(NotImplementedError):
    def __init__(self, message=None):
        if message is None:
            message = 'Either the python library this form belongs to was not found, either this form has not been implemeted yet. \
In this last case, Write a new issue in https://github.com/uibcdf/MolSysMT/issues asking for it.'
        super().__init__(message)

class NotImplementedSyntaxisError(NotImplementedError):
    def __init__(self, message=None):
        if message is None:
            message = 'Either this selection syntaxis is misspelled or it has not been implemented yet. \
In this last case, Write a new issue in https://github.com/uibcdf/MolSysMT/issues asking for it.'
        super().__init__(message)

class NotImplementedEngineError(NotImplementedError):
    def __init__(self, message=None):
        if message is None:
            message = 'This engine has not been implemented yet in this method. \
Write a new issue in https://github.com/uibcdf/MolSysMT/issues asking for it.'
        super().__init__(message)

class LibraryNotFound(NotImplementedError):
    def __init__(self, library):
        message = 'The python library {} was not found.'.format(library)
        super().__init__(message)

