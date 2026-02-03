from ...exceptions import ArgumentError

def digest_filename(filename, caller=None):

    if isinstance(filename, str):
        return filename

    raise ArgumentError('filename', value=filename, caller=caller, message=None)

