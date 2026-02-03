from ...exceptions import ArgumentError

def digest_sorted(sorted, caller=None):

    if isinstance(sorted, bool):
        return sorted

    raise ArgumentError('sorted', value=sorted, caller=caller, message=None)

