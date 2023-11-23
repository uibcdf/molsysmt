from ...exceptions import ArgumentError

def digest_redefine_types(redefine_types, caller=None):

    if isinstance(redefine_types, bool):
        return redefine_types

    raise ArgumentError('redefine_types', value=redefine_types, caller=caller, message=None)

