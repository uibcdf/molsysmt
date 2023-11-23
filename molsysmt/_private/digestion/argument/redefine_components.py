from ...exceptions import ArgumentError

def digest_redefine_components(redefine_components, caller=None):

    if isinstance(redefine_components, bool):
        return redefine_components

    raise ArgumentError('redefine_components', value=redefine_components, caller=caller, message=None)

