class NotImplementedSyntaxisError(NotImplementedError):

    """Exception raised when a syntaxis is not supported yet.

    This exception is raised when a syntaxis not supported yet has been selected by the user.

    Parameters
    ----------
    syntaxis : str
        The syntaxis not supported yet.

    Raises
    ------
    NotImplementedFormError
        A message is printed out with the name of the syntaxis not supported, the name of the class or
        the method raising the exception, the link to the API documentation, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import NotImplementedSyntaxisError
    >>> def method_name(syntaxis):
    ...    if syntaxis not in ['MolSysMT', 'MDTraj']:
    ...       raise NotImplementedSyntaxisError(syntaxis)
    ...    pass

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> NotImplementedSyntaxisError <developer:exceptions:NotImplementedSyntaxisError>`

    """

    def __init__(self, syntaxis):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = (
                f"The \"{syntaxis}\" syntaxis in \"{caller_name}\" has not been implemented yet. "
                f"Check {api_doc} for more information. "
                f"Write a new issue in {__github_issues_web__} asking for its implementation."
                )

        super().__init__(message)


