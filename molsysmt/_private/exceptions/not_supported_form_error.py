class NotSupportedFormError(ValueError):
    """Exception raised when the item's form is unknown and thereby not supported.

    This exception is raised when Sabueso does not recognize the item as a supported form.

    Note
    ----
    This exception does not require input arguments.

    Raises
    ------
    NotSupportedFormError
        A message is printed out with the name of the class or the method raising the exception,
        the link to the API documentation with the list of supported forms, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import NotSupportedFormError
    >>> from molsysmt import get_form
    >>> try:
    ...    _ = get_form(item)
    ... except:
    ...    raise NotSupportedFormError

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> NotSupportedFormError <developer:exceptions:NotSupportedFormError>`

    """

    def __init__(self, form_type):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = (
            f"The input molecular system or item in \"{caller_name}\" has a not supported form: {form_type} "
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {__github_issues_web__}."
            )

        super().__init__(message)

