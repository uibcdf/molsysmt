from ...exceptions import ArgumentError

def digest_redefine_molecules(redefine_molecules, caller=None):

    if isinstance(redefine_molecules, bool):
        return redefine_molecules

    raise ArgumentError('redefine_molecules', value=redefine_molecules, caller=caller, message=None)

