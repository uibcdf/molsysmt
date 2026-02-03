from molsysmt._private.exceptions import ArgumentError

def digest_C_terminal(C_terminal, caller=None):

    if C_terminal is None:
        return None

    if isinstance(C_terminal, str):
        return C_terminal

    raise ArgumentError('C_terminal', value=C_terminal, caller=caller, message=None)

