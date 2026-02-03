from ...exceptions import ArgumentError

def digest_skip_digestion(skip_digestion, caller=None):

    if isinstance(skip_digestion, bool):
        return skip_digestion

    raise ArgumentError('skip_digestion', value=skip_digestion, caller=caller, message=None)

