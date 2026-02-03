from ...exceptions import ArgumentError

def digest_center_at_origin(center_at_origin, caller=None):

    if isinstance(center_at_origin, bool):
        return center_at_origin

    raise ArgumentError('center_at_origin', value=center_at_origin, caller=caller, message=None)

