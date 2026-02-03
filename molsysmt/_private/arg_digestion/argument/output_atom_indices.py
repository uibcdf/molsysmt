from ...exceptions import ArgumentError
from ...variables import is_all

def digest_output_atom_indices(output_indices, caller=None):

    if caller=='molsysmt.structure.get_distances.get_distances':

        if output_atom_indices is None:
            return None
        elif isinstance(output_atom_indices, str):
            if output_atom_indices.lower() in ['selection', 'atom', 'group']:
                return output_atom_indices.lower()

    raise ArgumentError('output_atom_indices', value=output_atom_indices, caller=caller, message=None)

