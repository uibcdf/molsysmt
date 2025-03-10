from ...exceptions import ArgumentError

def digest_magnitude(magnitude, caller=None):

    if isinstance(magnitude, bool):
        return magnitude

    raise ArgumentError('magnitude', value=magnitude, caller=caller, message=None)

