from ...exceptions import ArgumentError

def digest_output(output, caller=None):

    if caller=='molsysmt.basic.info.info':

        if isinstance(output, str):
            if output.lower() in ['dataframe', 'short_string', 'long_string']:
                return output.lower()

    raise ArgumentError('output', value=output, caller=caller, message=None)

