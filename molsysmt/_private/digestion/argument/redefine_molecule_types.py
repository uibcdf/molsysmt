from ...exceptions import ArgumentError

def digest_redefine_molecule_types(redefine_molecule_types, caller=None):

    if isinstance(redefine_molecule_types, bool):
        return redefine_molecule_types

    raise ArgumentError('redefine_molecule_types', value=redefine_molecule_types, caller=caller, message=None)

