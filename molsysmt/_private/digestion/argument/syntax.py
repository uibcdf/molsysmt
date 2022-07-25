from molsysmt._private.exceptions import ArgumentError
from molsysmt.syntax.syntaxes import syntaxes

syntax_from_lower = {ii.lower(): ii for ii in syntaxes}

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

    if isinstance(syntax, str):
        try:
            return syntax_from_lower[syntax.lower()]
        except:
            pass

    raise ArgumentError('syntax', caller=caller, message=None)

