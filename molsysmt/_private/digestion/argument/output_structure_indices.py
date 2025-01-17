from ...exceptions import ArgumentError
from ...variables import is_all


def digest_output_structure_indices(output_structure_indices, caller=None):

    if caller is not None:

        if caller.endswith(('molsysmt.structure.get_contacts.get_contacts',
                            'molsysmt.structure.get_distances.get_distances',
                            'molsysmt.structure.get_neighbors.get_neighbors',)):

            if output_structure_indices is None:
                return None
            elif isinstance(output_structure_indices, str):
                if output_structure_indices.lower() in ['selection', 'structure']:
                    return output_structure_indices.lower()

    raise ArgumentError('output_structure_indices', value=output_structure_indices, caller=caller, message=None)

