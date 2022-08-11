from ...exceptions import ArgumentError

def digest_output_with_structure_indices(output_with_structure_indices, caller=None):

    if isinstance(output_with_structure_indices, bool):
        return output_with_structure_indices

    raise ArgumentError('output_with_structure_indices', value=output_with_structure_indices, caller=caller, message=None)

