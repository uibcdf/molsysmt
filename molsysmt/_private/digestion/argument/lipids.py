from molsysmt._private.exceptions import ArgumentError

def digest_lipids(lipids, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(lipids, (bool, int)):
            return lipids

    raise ArgumentError('lipids', value=lipids, caller=caller, message=None)

