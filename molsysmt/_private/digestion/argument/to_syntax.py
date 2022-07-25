from molsysmt._private.exceptions import ArgumentError
from molsysmt.syntax.syntaxes import syntaxes

syntax_from_lower = {ii.lower(): ii for ii in syntaxes}

def digest_to_syntax(to_syntax, caller=None):
    """ Checks if a to_syntax argument has the correct type and value

        Parameters
        ----------
        to_syntax : str
            The name of the syntax.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        WrongSyntaxError
            A WrongSyntaxError is raised if the to_syntax argument is not in deed a supported syntax.

    """

    if isinstance(to_syntax, str):
        try:
            return syntax_from_lower[to_syntax.lower()]
        except:
            pass

    raise ArgumentError('to_syntax', caller=caller, message=None)


