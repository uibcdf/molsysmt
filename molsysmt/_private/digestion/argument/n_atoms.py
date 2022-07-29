from molsysmt._private.exceptions import ArgumentError

def digest_n_atoms(n_atoms, caller=None):

    if caller=='get':
        if isinstance(n_atoms, bool):
            return n_atoms
        else:
            raise ArgumentError('n_atoms', caller=caller, message=None)
    else:
        raise ArgumentError('n_atoms', caller=caller, message=None)

