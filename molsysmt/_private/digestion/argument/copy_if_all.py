from molsysmt._private.exceptions import ArgumentError

def digest_copy_if_all(copy_if_all, caller=None):

    if isinstance(copy_if_all, bool):
        return copy_if_all

    raise ArgumentError('copy_if_all', value=copy_if_all, caller=caller, message=None)

