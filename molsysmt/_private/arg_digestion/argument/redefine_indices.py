from ...exceptions import ArgumentError

def digest_redefine_indices(redefine_indices, caller=None):

    if isinstance(redefine_indices, bool):
        return redefine_indices

    raise ArgumentError('redefine_indices', value=redefine_indices, caller=caller, message=None)

