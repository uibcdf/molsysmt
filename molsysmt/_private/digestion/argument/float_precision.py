from molsysmt._private.exceptions import ArgumentError

def digest_float_precision(float_precision, caller=None):

    if isinstance(float_precision, str):

        if caller.endswith('to_file_msmh5'):
            if float_precision in ['single', 'double']:
                return float_precision

    raise ArgumentError('float_precision', value=float_precision, caller=caller, message=None)

