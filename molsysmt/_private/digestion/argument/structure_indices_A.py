from ...exceptions import ArgumentError

def digest_structure_indices_A(structure_indices_A, caller=None):

    from .structure_indices import digest_structure_indices

    try:
        return digest_structure_indices(structure_indices_A, caller=caller)
    except:
        raise ArgumentError('structure_indices_A', value=structure_indices_A, caller=caller, message=None)

