from molsysmt._private.exceptions import ArgumentError

def digest_copy_if_None(copy_if_None, caller=None):

    if isinstance(copy_if_None, bool):
        return copy_if_None

    raise ArgumentError('copy_if_None', value=copy_if_None, caller=caller, message=None)

