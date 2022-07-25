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
    unit = puw.get_unit(box_lengths)
    box_lengths = puw.get_value(box_lengths)
    box_lengths = digest_box_values(box_lengths, caller)

    return box_lengths * unit

