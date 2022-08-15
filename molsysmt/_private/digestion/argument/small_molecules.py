from molsysmt._private.exceptions import ArgumentError

def digest_small_molecules(small_molecules, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(small_molecules, (bool, int)):
            return small_molecules
    if caller=='molsysmt.basic.contains.contains':
        if isinstance(small_molecules, (bool, int)):
            return small_molecules
        elif small_molecules is None:
            return None

    raise ArgumentError('small_molecules', value=small_molecules, caller=caller, message=None)

