from ...exceptions import ArgumentError

def digest_mutual_only(mutual_only, caller=None):

    if isinstance(mutual_only, bool):
        return mutual_only

    raise ArgumentError('mutual_only', value=mutual_only, caller=caller, message=None)

