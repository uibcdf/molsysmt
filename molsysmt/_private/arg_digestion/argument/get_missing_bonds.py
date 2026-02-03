from ...exceptions import ArgumentError

def digest_get_missing_bonds(get_missing_bonds, caller=None):

    if isinstance(get_missing_bonds, bool):
        return get_missing_bonds

    raise ArgumentError('get_missing_bonds', value=get_missing_bonds, caller=caller, message=None)

