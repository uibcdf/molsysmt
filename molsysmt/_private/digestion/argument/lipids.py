from molsysmt._private.exceptions import ArgumentError

def digest_lipids(lipids, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(lipids, (bool, int)):
            return lipids
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(lipids, (bool, int)):
            return lipids
        elif lipids is None:
            return None


    raise ArgumentError('lipids', value=lipids, caller=caller, message=None)

