class NotImplementedMethodError(NotImplementedError):
    """Exception raised when a method has not been fully implemented yet.

    This exception is raised when a method has been already defined but its code was not fully
    implemented yet. Maybe the method was just included in a developing version to be coded in the
    future. Or maybe the method works already for certain values of the input arguments, but not
    for others yet.

    Note
    ----
    This exception does not require input arguments.

    Raises
    ------
    NotImplementedMethodError
        A message is printed out with the name of the method raising the exception, the link to
        the API documentation, and the link to the issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import NotImplementedMethodError
    >>> def method_name(a, b=True):
    ...    raise NotImplementedMethodError
    ...    pass

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> NotImplementedMethodError <developer:exceptions:NotImplementedMethodError>`

    """

    def __init__(self):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = (
                f"The \"{caller_name}\" method has not been implemented yet in the way you are using it. "
                f"Check {api_doc} for more information. "
                f"If you still want to suggest its implementation, open a new issue in {__github_issues_web__}"
                )

        super().__init__(message)

