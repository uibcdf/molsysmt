from ...exceptions import ArgumentError

def digest_keep_covalent_bonds(keep_covalent_bonds, caller=None):

    if isinstance(keep_covalent_bonds, bool):
        return keep_covalent_bonds

    raise ArgumentError('keep_covalent_bonds', value=keep_covalent_bonds, caller=caller, message=None)

