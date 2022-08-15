from ...exceptions import ArgumentError

def digest_reference_coordinates(reference_coordinates, caller=None):

    if reference_coordinates is None:
        return None

    from .coordinates import digest_coordinates

    try:
        return digest_coordinates(reference_coordinates, caller=caller)
    except:
        raise ArgumentError('reference_coordinates', value=reference_coordinates, caller=caller, message=None)

