from ...exceptions import ArgumentError

def digest_keep_ids(keep_ids, caller=None):

    if isinstance(keep_ids, bool):
        return keep_ids

    raise ArgumentError('keep_ids', value=keep_ids, caller=caller, message=None)

