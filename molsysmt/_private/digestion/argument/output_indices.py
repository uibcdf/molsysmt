from ...exceptions import ArgumentError
from ...variables import is_all

def digest_output_indices(output_indices, caller=None):

    if caller=='molsysmt.structure.get_contacts.get_contacts':

        if output_indices is None:
            return None
        elif isinstance(output_indices, str):
            if output_indices.lower() in ['selection', 'atom', 'group']:
                return output_indices.lower()

    if caller=='molsysmt.structure.get_distances.get_distances':

        if output_indices is None:
            return None
        elif isinstance(output_indices, str):
            if output_indices.lower() in ['selection', 'atom', 'group']:
                return output_indices.lower()


    raise ArgumentError('output_indices', value=output_indices, caller=caller, message=None)

