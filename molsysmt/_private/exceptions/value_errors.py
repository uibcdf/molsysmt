from molsysmt._private.exceptions.caller_name import caller_name

__github_web__ = 'https://github.com/uibcdf/MolSysMT'
__github_issues_web__ = __github_web__ + '/issues'
api_doc = ''


class MolSysValueError(ValueError):
    """ Base class for value errors. It prints a message
        containing info such as the function that raised
        the error, and a link to GitHub repository.

        Parameters
        ----------
        message : str, optional
            An informative message of the exception.

        caller : str, optional
            Name of the function or method that raised the error.

    """

    def __init__(self, message="", caller=""):

        if not caller:
            caller = caller_name(skip=3)

        if not message:
            full_message = f"Error in {caller}. "
        else:
            full_message = f"Error in {caller}. " + message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {__github_issues_web__}."
        )
        super().__init__(full_message)


class NotWithThisMolecularSystemError(MolSysValueError):
    """ Error raised when trying to call a function that does not accept
        the given type of molecular system.
    """

    def __init__(self, message="", caller=""):
        if not message:
            message = 'This method can not be applied over this molecular system. '
        super().__init__(message, caller)


class MolecularSystemNeededError(MolSysValueError):
    def __init__(self, message="", caller=""):
        if not message:
            message = (f"The method works over a molecular system. "
                       f"Either no molecular system or multiple systems were provided.")
        super().__init__(message, caller)


class MultipleMolecularSystemsNeededError(MolSysValueError):
    def __init__(self, message="", caller=""):
        if not message:
            message = ('This method works only over a single molecular system. '
                       'But multiple molecular systems are provided. ')
        super().__init__(message, caller)


class NotSupportedFormError(MolSysValueError):
    """ Exception raised when the item's form is unknown and thereby not supported.

        This exception is raised when Sabueso does not recognize the item as a supported form.
    """

    def __init__(self, form_type, caller=""):
        message = f"The input molecular system or item has a not supported form: {form_type} "
        super().__init__(message, caller)


class NotWithThisFormError(MolSysValueError):
    """ Exception raised when a method or a class can not accept a specific item's form -by no means-.

        This exception is raised when a method or a class should be able to work with an item's form,
        but it has not been implemented yet. For instance, the method used to get the value of the
        dihedral angle defined by four atoms can not work over a GROMACS topology file (.top). In this
        case the method will raise a 'NotWithTisFormError' exception.
    """

    def __init__(self, form, caller=""):
        message = f"Invalid form: {form} "
        super().__init__(message, caller)


class WrongGetArgumentError(MolSysValueError):
    """ Exception raised when the get method is called with a not valid input argument.
    """

    def __init__(self, argument=None, caller=""):
        message = f"The get method was invoked with not valid input argument: \"{argument}\""
        super().__init__(message, caller)


# TODO: WrongFormError and NotWithThisFormError are redundant.


class WrongFormError(MolSysValueError):
    """Exception raised when the item has not the correct form expected by a method or a class.
    """

    def __init__(self, form, caller=""):
        message = f"The input item's should be {form} and is not. "
        super().__init__(message, caller)


class WrongAtomIndicesError(MolSysValueError):
    pass


class WrongSelectionError(MolSysValueError):
    pass


class WrongIndicesError(MolSysValueError):
    """ Exception raised when atom, group, or structure indices are not of the
        expected type.
    """
    def __init__(self, indices_type, caller=""):
        message = f"Wrong indices type: {indices_type}"
        super().__init__(message, caller)


class WrongOutputFilenameError(MolSysValueError):
    pass


class WrongComparisonError(MolSysValueError):
    pass


class WrongStepError(MolSysValueError):
    """ Exception raised when a step is of an incorrect type."""
    def __init__(self, step_type, caller=""):
        message = f"Wrong step type: {step_type}"
        super().__init__(message, caller)


class WrongStructureIndicesError(MolSysValueError):
    pass


class WrongSyntaxisError(MolSysValueError):
    pass


class WrongTimeError(MolSysValueError):
    """ Exception raised when time is of an incorrect type."""
    def __init__(self, step_type, caller=""):
        message = f"Wrong time type: {step_type}"
        super().__init__(message, caller)


class WrongToFormError(MolSysValueError):
    pass


class WrongElementError(MolSysValueError):
    """ Exception raised when an element is not supported by MolSysMT. """
    def __init__(self, element, caller=""):
        if isinstance(element, str):
            message = f"Wrong element name: {element}. "
        else:
            message = ""
        super().__init__(message, caller)


class WrongEngineError(MolSysValueError):
    """ Exception raised when an engine is not supported by MolSysMT. """
    def __init__(self, engine, caller=""):
        if isinstance(engine, str):
            message = f"Unsupported engine {engine}. "
        else:
            message = ""
        super().__init__(message, caller)


class IncorrectShapeError(MolSysValueError):
    """Exception raised when a quantity or array doesn't have the correct shape.
    """

    def __init__(self, expected_shape=None, actual_shape=None, caller=""):
        message = ""
        if expected_shape:
            message = f"Expected shape {expected_shape}. "
        if actual_shape:
            message += f"Actual shape {actual_shape}. "
        super().__init__(message, caller)


class IteratorStartError(MolSysValueError):
    """ Exception raised when an incorrect start value is passed to an iterator.
    """
    pass


class IteratorIntervalError(MolSysValueError):
    """ Exception raised when an incorrect interval value is passed to an iterator.
    """
    pass


class IteratorChunkSizeError(MolSysValueError):
    """ Exception raised when an incorrect chunk size value is passed to an iterator.
    """
    pass


class ConcatenationError(MolSysValueError):
    """ Exception raised when two arrays cannot be concatenated because one if them is null.
    """
    pass
