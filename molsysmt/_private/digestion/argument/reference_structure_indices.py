from ...exceptions import ArgumentError


def digest_reference_structure_indices(reference_structure_indices, caller=None):

    from .indices import digest_indices

    try:
        return digest_indices(reference_structure_indices, caller=caller)
    except:
        raise ArgumentError('reference_structure_indices', value=reference_structure_indices, caller=caller, message=None)

