from molsysmt._private.exceptions import ArgumentError

def digest_dnas(dnas, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(dnas, (bool, int)):
            return dnas
    if caller=='molsysmt.basic.contains.contains':
        if isinstance(dnas, (bool, int)):
            return dnas
        elif dnas is None:
            return None

    raise ArgumentError('dnas', value=dnas, caller=caller, message=None)

