from ...exceptions import ArgumentError
from ...variables import is_all


def digest_output_indices(output_indices, caller=None):

    if caller is not None:

        if caller.endswith(('molsysmt.structure.get_contacts.get_contacts',
                            'molsysmt.structure.get_distances.get_distances',
                            'molsysmt.structure.get_neighbors.get_neighbors',)):

            if output_indices is None:
                return None
            elif isinstance(output_indices, str):
                if output_indices.lower() in ['selection', 'atom', 'group']:
                    return output_indices.lower()

    raise ArgumentError('output_indices', value=output_indices, caller=caller, message=None)

