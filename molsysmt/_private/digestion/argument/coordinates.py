from ...exceptions import ArgumentError
from molsysmt import puw

def digest_coordinates(coordinates, caller=None):
    """Checks if `coordinates` has the expected type and value.

    Parameters
    ----------
    coordinates : Any
        The coordinates for digestion.
    caller: str, optional
        Name of the function or method that is being digested.

    Returns
    -------
    Quantity (value : ndarray)
        The coordinates with proper type and value.

    Raises
    -------
    WrongCoordinatesError
        If the given coordinates argument has not of the correct type or value.
    """

    if caller == 'molsysmt.basic.get.get':
        if isinstance(coordinates, bool):
            return coordinates

    if not puw.check(coordinates, dimensionality={'[L]':1}):
        raise ArgumentError('coordinates', value=coordinates, caller=caller, message=None)

    return puw.standardize(coordinates)

