from ...exceptions import ArgumentError

def digest_pairs(pairs, caller=None):

    if isinstance(pairs, bool):
        return pairs

    raise ArgumentError('pairs', value=pairs, caller=caller, message=None)

