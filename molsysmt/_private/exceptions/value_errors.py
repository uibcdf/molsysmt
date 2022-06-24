
__github_web__ = 'https://github.com/uibcdf/MolSysMT'
__github_issues_web__ = __github_web__ + '/issues'
api_doc = ''


class MolSysValueError(ValueError):
    """ Base class for value errors. """

    def __init__(self, message=None):
        if message is None:
            message = ""

        message += (
            f" Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {__github_issues_web__}."
        )
        super().__init__(message)


class NotWithThisMolecularSystemError(MolSysValueError):
    """ Error raised when trying to call a function that does not accept
        the given type of molecular system.
    """

    def __init__(self, message=None):
        if message is None:
            message = 'This method can not be applied over this molecular system. '
        super().__init__(message)


class MolecularSystemNeededError(MolSysValueError):
    def __init__(self, message=None):
        if message is None:
            message = ( f"The method works over a molecular system. "
                        f"Either no molecular system or multiple systems were provided.")
        super().__init__(message)


class MultipleMolecularSystemsNeededError(MolSysValueError):
    def __init__(self, message=None):
        if message is None:
            message = ('This method works only over a single molecular system. '
                       'But multiple molecular systems are provided. ')
        super().__init__(message)


class NotSupportedFormError(MolSysValueError):
    """ Exception raised when the item's form is unknown and thereby not supported.

        This exception is raised when Sabueso does not recognize the item as a supported form.
    """
    def __init__(self, form_type):
        message = f"The input molecular system or item has a not supported form: {form_type} "
        super().__init__(message)


class NotWithThisFormError(MolSysValueError):
    """ Exception raised when a method or a class can not accept a specific item's form -by no means-.

        This exception is raised when a method or a class should be able to work with an item's form,
        but it has not been implemented yet. For instance, the method used to get the value of the
        dihedral angle defined by four atoms can not work over a GROMACS topology file (.top). In this
        case the method will raise a 'NotWithTisFormError' exception.
    """
    def __init__(self, form):
        message = f"Invalid form: {form} "
        super().__init__(message)


class WrongGetArgumentError(MolSysValueError):
    """ Exception raised when the get method is called with a not valid input argument.
    """
    def __init__(self, argument=None):
        message = f"The get method was invoked with not valid input argument: \"{argument}\""
        super().__init__(message)

# TODO: WrongFormError and NotWithThisFormError are redundant.


class WrongFormError(MolSysValueError):
    """Exception raised when the item has not the correct form expected by a method or a class.
    """
    def __init__(self, form):
        message = f"The input item's should be {form} and is not. "
        super().__init__(message)


class WrongAtomIndicesError(MolSysValueError):
    pass


class WrongSelectionError(MolSysValueError):
    pass


class WrongIndicesError(MolSysValueError):
    pass


class WrongOutputFilenameError(MolSysValueError):
    pass


class WrongComparisonError(MolSysValueError):
    pass


class WrongStepError(MolSysValueError):
    pass


class WrongStructureIndicesError(MolSysValueError):
    pass


class WrongSyntaxisError(MolSysValueError):
    pass


class WrongTimeError(MolSysValueError):
    pass


class WrongToFormError(MolSysValueError):
    pass
