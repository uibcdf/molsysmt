from molsysmt._private.exceptions import ArgumentError

def digest_n_molecules(n_molecules, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_molecules, bool):
            return n_molecules

    raise ArgumentError('n_molecules', value=n_molecules, caller=caller, message=None)

