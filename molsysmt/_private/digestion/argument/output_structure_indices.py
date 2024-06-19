from ...exceptions import ArgumentError
from ...variables import is_all

def digest_output_structure_indices(output_structure_indices, caller=None):

    if caller=='molsysmt.structure.get_distances.get_distances':

        if output_structure_indices is None:
            return None
        elif isinstance(output_structure_indices, str):
            if output_structure_indices.lower() in ['selection', 'structure']:
                return output_structure_indices.lower()

    raise ArgumentError('output_structure_indices', value=output_structure_indices, caller=caller, message=None)

