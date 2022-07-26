from molsysmt._private.exceptions import ArgumentError

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

    from molsysmt.syntax.syntaxes import lowercase_syntaxes

    if isinstance(syntax, str):
        try:
            return lowercase_syntaxes[syntax.lower()]
        except:
            pass

    raise ArgumentError('syntax', caller=caller, message=None)

