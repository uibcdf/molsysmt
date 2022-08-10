from ...exceptions import ArgumentError

def digest_structure_indices_2(structure_indices_2, caller=None):

    if structure_indices_2 is None:
        return None

    from .structure_indices import digest_structure_indices

    try:
        return digest_structure_indices(structure_indices_2, caller=caller)
    except:
        raise ArgumentError('structure_indices_2', value=structure_indices_2, caller=caller, message=None)

