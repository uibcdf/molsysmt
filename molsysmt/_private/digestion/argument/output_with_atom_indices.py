from ...exceptions import ArgumentError

def digest_output_with_atom_indices(output_with_atom_indices, caller=None):

    if isinstance(output_with_atom_indices, bool):
        return output_with_atom_indices

    raise ArgumentError('output_with_atom_indices', value=output_with_atom_indices, caller=caller, message=None)

