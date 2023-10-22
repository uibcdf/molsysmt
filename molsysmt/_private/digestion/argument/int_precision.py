from molsysmt._private.exceptions import ArgumentError

def digest_int_precision(int_precision, caller=None):

    if isinstance(int_precision, str):

        if caller.endswith('to_file_msmh5'):
            if int_precision in ['single', 'double']:
                return int_precision

    raise ArgumentError('int_precision', value=int_precision, caller=caller, message=None)

