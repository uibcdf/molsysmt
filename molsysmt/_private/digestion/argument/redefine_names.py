from ...exceptions import ArgumentError

def digest_redefine_names(redefine_names, caller=None):

    if isinstance(redefine_names, bool):
        return redefine_names

    raise ArgumentError('redefine_names', value=redefine_names, caller=caller, message=None)

