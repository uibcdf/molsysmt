from molsysmt._private.exceptions import ArgumentError

def digest_n_molecules(n_molecules, caller=None):

    if caller=='get':
        if isinstance(n_molecules, bool):
            return n_molecules
        else:
            raise ArgumentError('n_molecules', caller=caller, message=None)
    else:
        raise ArgumentError('n_molecules', caller=caller, message=None)

