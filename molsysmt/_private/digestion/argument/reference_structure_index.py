from ...exceptions import ArgumentError


def digest_reference_structure_index(reference_structure_index, caller=None):

    from .index import digest_index

    try:
        return digest_index(reference_structure_index, caller=caller)
    except:
        raise ArgumentError('reference_structure_index', value=reference_structure_index, caller=caller, message=None)

