class NotImplementedEngineError(NotImplementedError):

    """Exception raised when executing a method with a specific engine is not supported yet.

    This exception is raised when a method can not be executed with the selected engine by the user.

    Parameters
    ----------
    engine : str
        The engine not supported yet.

    Raises
    ------
    NotImplementedFormError
        A message is printed out with the name of the engine not supported, the name of the class or
        the method raising the exception, the link to the API documentation, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import NotImplementedEngineError
    >>> def method_name(engine):
    ...    if engine not in ['MolSysMT', 'MDTraj']:
    ...       raise NotImplementedEngineError(engine)
    ...    pass

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> NotImplementedEngineError <developer:exceptions:NotImplementedEngineError>`

    """

    def __init__(self, syntaxis):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = (
                f"The \"{engine}\" engine in \"{caller_name}\" has not been implemented yet. "
                f"Check {api_doc} for more information. "
                f"Write a new issue in {__github_issues_web__} asking for its implementation."
                )

        super().__init__(message)


