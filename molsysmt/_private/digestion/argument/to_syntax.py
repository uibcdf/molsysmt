from molsysmt._private.exceptions import ArgumentError

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

    from molsysmt.syntax.syntaxes import lowercase_syntaxes

    if caller=='molsysmt.basic.select.select':

        if to_syntax is None:
            return to_syntax
        elif isinstance(to_syntax, str):
            try:
                return lowercase_syntaxes[to_syntax.lower()]
            except:
                raise ArgumentError('to_syntax', value=to_syntax, caller=caller, message=None)

    else:

        try:
            return lowercase_syntaxes[to_syntax.lower()]
        except:
            raise ArgumentError('to_syntax', value=to_syntax, caller=caller, message=None)


