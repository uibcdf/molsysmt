from ...exceptions import ArgumentError

def digest_output(output, caller=None):

    if caller=='molsysmt.basic.info.info':

        if isinstance(output, str):
            if output.lower() in ['dataframe', 'short_string', 'long_string']:
                return output.lower()

    elif caller=='molsysmt.structure.get_distances.get_distances':

        if isinstance(output, str):
            if output.lower() in ['numpy.ndarray', 'dict']:
                return output.lower()

    elif caller=='molsysmt.structure.get_neighbors.get_neighbors':

        if isinstance(output, str):
            if output.lower() in ['numpy.ndarray', 'dict']:
                return output.lower()

    elif caller=='molsysmt.structure.get_contacts.get_contacts':

        if isinstance(output, str):
            if output.lower() in ['numpy.ndarray', 'dict']:
                return output.lower()

    elif caller=='molsysmt.topology.get_covalent_blocks.get_covalent_blocks':

        if isinstance(output, str):
            if output.lower() in ['numpy.ndarray', 'sets']:
                return output.lower()


    raise ArgumentError('output', value=output, caller=caller, message=None)

