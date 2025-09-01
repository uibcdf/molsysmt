from ...exceptions import ArgumentError

def digest_include_none(include_none, caller=None):

    if isinstance(include_none, bool):
        return include_none

    raise ArgumentError('include_none', value=include_none, caller=caller, message=None)

