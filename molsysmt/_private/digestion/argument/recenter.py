from ...exceptions import ArgumentError

def digest_recenter(recenter, caller=None):

    if isinstance(recenter, bool):
        return recenter

    raise ArgumentError('recenter', value=recenter, caller=caller, message=None)

