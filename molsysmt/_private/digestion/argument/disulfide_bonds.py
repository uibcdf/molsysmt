from ...exceptions import ArgumentError

functions_with_boolean = (
        'get_missing_bonds',
        )

def digest_disulfide_bonds(disulfide_bonds, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(disulfide_bonds, bool):
                return disulfide_bonds

    raise ArgumentError('disulfide_bonds', value=disulfide_bonds, caller=caller, message=None)


