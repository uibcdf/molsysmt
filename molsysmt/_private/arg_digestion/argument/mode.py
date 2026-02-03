from molsysmt._private.exceptions import ArgumentError

def digest_mode(mode, caller=None):

    if isinstance(mode, str):

        if caller.startswith('molsysmt.file'):
            if mode in ['auto', 'read', 'write']:
                return mode

    raise ArgumentError('mode', value=mode, caller=caller, message=None)

