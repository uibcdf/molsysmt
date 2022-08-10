from ...exceptions import ArgumentError
from molsysmt import puw

def digest_new_coordinates_center(new_coordinates_center, caller=None):

    from .coordinates import digest_coordinates

    if new_coordinates_center is None:
        return None

    try:
        return digest_coordinates(new_coordinates_center, caller=caller)
    except:
        raise ArgumentError('new_coordinates_center', value=new_coordinates_center, caller=caller,
                message=None)

