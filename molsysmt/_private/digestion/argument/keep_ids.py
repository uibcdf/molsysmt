from ...exceptions import ArgumentError

def digest_keep_ids(keep_ids, caller=None):

    if caller.endswith('.merge.merge'):
        if isinstance(keep_ids, bool):
            return keep_ids

    if caller.endswith('.add.add'):
        if isinstance(keep_ids, bool):
            return keep_ids

    raise ArgumentError('keep_ids', value=keep_ids, caller=caller, message=None)
