from molsysmt._private.exceptions import ArgumentError

def digest_compression_opts(compression_opts, caller=None):

    if isinstance(compression_opts, int):

        if caller.endswith('to_file_msmh5'):
            if 0<=compression_opts<=9:
                return compression_opts

    raise ArgumentError('compression_opts', value=compression_opts, caller=caller, message=None)

