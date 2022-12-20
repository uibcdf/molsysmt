from ...exceptions import ArgumentError

def digest_output_type(output_type, caller=None):

    if caller=='molsysmt.basic.info.info':

        if isinstance(output_type, str):
            if output_type.lower() in ['dataframe', 'short_string', 'long_string']:
                return output_type.lower()

    elif caller=='molsysmt.structure.get_distances.get_distances':

        if isinstance(output_type, str):
            if output_type.lower() in ['numpy.ndarray', 'dictionary']:
                return output_type.lower()

    elif caller=='molsysmt.structure.get_neighbors.get_neighbors':

        if isinstance(output_type, str):
            if output_type.lower() in ['numpy.ndarray', 'dictionary']:
                return output_type.lower()

    elif caller=='molsysmt.structure.get_contacts.get_contacts':

        if isinstance(output_type, str):
            if output_type.lower() in ['numpy.ndarray', 'dictionary']:
                return output_type.lower()

    elif caller=='molsysmt.topology.get_covalent_blocks.get_covalent_blocks':

        if isinstance(output_type, str):
            if output_type.lower() in ['numpy.ndarray', 'sets']:
                return output_type.lower()

    elif caller.endswith(('.iterator.__init__', '.iterators.__init__')):

        if isinstance(output_type, str):
            if output_type.lower() in ['values', 'dictionary']:
                return output_type.lower()

    raise ArgumentError('output_type', value=output_type, caller=caller, message=None)

