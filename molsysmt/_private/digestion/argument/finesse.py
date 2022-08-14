from ...exceptions import ArgumentError

def digest_finesse(finesse, caller=None):

    if isinstance(finesse, int):
        return finesse

    raise ArgumentError('finesse', value=finesse, caller=caller, message=None)

