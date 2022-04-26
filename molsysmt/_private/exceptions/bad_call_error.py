class BadCallError(ValueError):
    """Exception raised when a method, or a class, was not properly called or instantiated.

    This exception is raised when a method or a class was not properly called or instantiated.

    Parameters
    ----------
    argument : str, optional
        The name of the possible wrong input argument.

    Raises
    ------
    BadCallError
        A message is printed out with the name of the class or the method raising the exception,
        the possible wrong argument, the link to the API documentation, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import BadCallError
    >>> def method_name(item, a=True):
    ...    if type(a) not in [int, float]:
    ...       raise BadCallError('a')
    ...    pass

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> BadCallError <developer:exceptions:BadCallError>`

    """

    def __init__(self, argument=None):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = f"The \"{caller_name}\" method or class was not properly invoked"
        if argument is not None:
            message += f", probably due to the \"{argument}\" input argument"
        message += (
                f". Check {api_doc} for more information. "
                f"If you still need help, open a new issue in {__github_issues_web__}."
                )

        super().__init__(message)


