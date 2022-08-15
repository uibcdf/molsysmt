from ...exceptions import ArgumentError
from molsysmt import puw

def digest_center_coordinates(center_coordinates, caller=None):

    from .coordinates import digest_coordinates

    if center_coordinates is None:
        return None

    try:
        return digest_coordinates(center_coordinates, caller=caller)
    except:
        raise ArgumentError('center_coordinates', value=center_coordinates, caller=caller,
                message=None)

