from molsysmt._private.exceptions import ArgumentError

def digest_n_lipids(n_lipids, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_lipids, bool):
            return n_lipids
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_lipids, (bool, int)):
            return n_lipids
    elif caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(n_lipids, (bool, int)):
            return n_lipids

    raise ArgumentError('n_lipids', value=n_lipids, caller=caller, message=None)

