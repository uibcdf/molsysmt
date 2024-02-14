from ...exceptions import ArgumentError

def digest_check_if_None(check_if_None, caller=None):

    if isinstance(check_if_None, bool):
        return check_if_None

    raise ArgumentError('check_if_None', value=check_if_None, caller=caller, message=None)

