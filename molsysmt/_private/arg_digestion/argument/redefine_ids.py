from ...exceptions import ArgumentError

def digest_redefine_ids(redefine_ids, caller=None):

    if isinstance(redefine_ids, bool):
        return redefine_ids

    raise ArgumentError('redefine_ids', value=redefine_ids, caller=caller, message=None)

