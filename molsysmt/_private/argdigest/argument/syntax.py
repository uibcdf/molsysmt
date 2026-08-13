from molsysmt._private.smonitor import ArgumentError

def digest_syntax(syntax, caller=None):
    """ Checks if a syntax has the correct type and value

        Parameters
        ----------
        syntax : str
            The name of the syntax.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        WrongSyntaxError
            A WrongSyntaxError is raised if the syntax argument is not in deed a supported syntax.

    """

    from molsysmt.supported._syntaxes import lowercase_selection_syntaxes

    if isinstance(syntax, str):
        if syntax.lower() in lowercase_selection_syntaxes:
            return lowercase_selection_syntaxes[syntax.lower()]

    raise ArgumentError('syntax', value=syntax, caller=caller, message=None)
