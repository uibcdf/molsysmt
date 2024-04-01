from ...exceptions import ArgumentError

def digest_redefine_molecule_indices(redefine_molecule_indices, caller=None):

    if isinstance(redefine_molecule_indices, bool):
        return redefine_molecule_indices

    raise ArgumentError('redefine_molecule_indices', value=redefine_molecule_indices, caller=caller, message=None)

