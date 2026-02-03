from molsysmt._private.exceptions import ArgumentError

def digest_N_terminal(N_terminal, caller=None):

    if N_terminal is None:
        return None

    if isinstance(N_terminal, str):
        return N_terminal

    raise ArgumentError('N_terminal', value=N_terminal, caller=caller, message=None)

