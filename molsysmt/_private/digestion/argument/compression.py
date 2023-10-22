from molsysmt._private.exceptions import ArgumentError

def digest_compression(compression, caller=None):

    if isinstance(compression, str):

        if caller.endswith('to_file_msmh5'):
            if compression in ['gzip', 'lzf', 'szip']:
                return compression

    raise ArgumentError('compression', value=compression, caller=caller, message=None)

