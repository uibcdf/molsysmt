class WrongFormError(ValueError):
    """Exception raised when the item has not the correct form expected by a method or a class.

    This exception is raised when an item has not the correct form for the method to work or the
    class to be instantiated.

    Parameters
    ----------
    form : str
        The form accepted by the method or the class.

    Raises
    ------
    WrongFormError
        A message is printed out with the name of the right form, the name of the class or
        the method raising the exception, the link to the API documentation, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import WrongFormError
    >>> from molsysmt import get_form
    >>> input_form = get_form('1VII.pdb')
    ... if input_form != 'file:top':
    ...    raise WrongFormError('file:top')

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> WrongFormError <developer:exceptions:WrongFormError>`

    """

    def __init__(self, form):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = (
                f"The input item's form of \"{caller_name}\" should be {form} and is not. "
                f"Check {api_doc} for more information. "
                f"If you still need help, open a new issue in {__github_issues_web__}."
                )

        super().__init__(message)



