from ...exceptions import ArgumentError

def digest_digest(digest, caller=None):

    if isinstance(digest, bool):
        return digest

    raise ArgumentError('digest', value=digest, caller=caller, message=None)

