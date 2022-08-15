import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

def digest_box_lengths(box_lengths, caller=None):
    """ Checks if box_lengths has the correct type, shape and units.

    Parameters
    ----------
    box_lengths : Quantity(value: ndarray or list or tuple, unit: any with dimensionality [L])
        The box lengths.

    caller: str, optional
        Name of the function or method that is being digested.

    Returns
    -------
    Quantity(value: ndarray with shape [n_structures, 3], unit: default units with dimensionality [L])
        The box vectors with the shape corrected if necessary.

    Raises
    ------
    IncorrectShapeError
        If box_vectors doesn't have the correct shape.
    """

    if caller=='molsysmt.basic.get.get':

        if isinstance(box_lengths, bool):
            return box_lengths
        else:
            raise ArgumentError('box_lengths', value=box_lengths, caller=caller, message=None)

    else:

        if not puw.check(box_lengths, dimensionality={'[L]':1}):
            raise ArgumentError('box_lengths', value=box_lengths, caller=caller, message=None)

        return puw.standardize(box_lengths)

