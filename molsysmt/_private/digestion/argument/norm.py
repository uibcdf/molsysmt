from ...exceptions import ArgumentError

def digest_norm(norm, caller=None):

    if isinstance(norm, bool):
        return norm

    raise ArgumentError('norm', value=norm, caller=caller, message=None)

