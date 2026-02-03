from ...exceptions import ArgumentError

def digest_unique_pairs(unique_pairs, caller=None):

    if isinstance(unique_pairs, bool):
        return unique_pairs

    raise ArgumentError('unique_pairs', value=unique_pairs, caller=caller, message=None)

