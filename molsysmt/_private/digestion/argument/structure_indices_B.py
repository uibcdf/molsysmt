from ...exceptions import ArgumentError

def digest_structure_indices_B(structure_indices_B, caller=None):

    from .structure_indices import digest_structure_indices

    try:
        return digest_structure_indices(structure_indices_B, caller=caller)
    except:
        raise ArgumentError('structure_indices_B', value=structure_indices_B, caller=caller, message=None)

