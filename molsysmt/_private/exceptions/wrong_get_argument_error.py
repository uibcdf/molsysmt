class WrongGetArgumentError(ValueError):
    """Exception raised when the get method is called with a not valid input argument.

    This exception is raise when the get method is called with an input argument not recognized by
    MolSySMT

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
    >>> from molsysmt._private.exceptions import WrongGetArgumentError
    >>> from molsysmt.basic.get.arguments import arguments
    >>> argument = 'atom_color'
    >>> if atom_color not in arguments:
    ...    raise WrongGetArgumentError(argument)

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> WrongGetArgumentError <developer:exceptions:WrongGetArgumentError>`

    """

    def __init__(self, argument=None):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = f"The get method was invoked with not valid input argument:\"{argument}\""
        message += (
                f". Check {api_doc} for more information. "
                f"If you still need help, open a new issue in {__github_issues_web__}."
                )

        super().__init__(message)


