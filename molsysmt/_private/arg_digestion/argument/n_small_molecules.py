from molsysmt._private.exceptions import ArgumentError

def digest_n_small_molecules(n_small_molecules, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_small_molecules, bool):
            return n_small_molecules
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_small_molecules, (bool, int)):
            return n_small_molecules
    elif caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(n_small_molecules, (bool, int)):
            return n_small_molecules


    raise ArgumentError('n_small_molecules', value=n_small_molecules, caller=caller, message=None)

