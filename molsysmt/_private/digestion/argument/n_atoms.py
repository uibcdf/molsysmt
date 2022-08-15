from molsysmt._private.exceptions import ArgumentError

def digest_n_atoms(n_atoms, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_atoms, bool):
            return n_atoms

    raise ArgumentError('n_atoms', value=n_atoms, caller=caller, message=None)

