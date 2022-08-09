from molsysmt._private.exceptions import ArgumentError

def digest_rnas(rnas, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(rnas, (bool, int)):
            return rnas
    if caller=='molsysmt.basic.contains.contains':
        if isinstance(rnas, (bool, int)):
            return rnas
        elif rnas is None:
            return None

    raise ArgumentError('rnas', value=rnas, caller=caller, message=None)

