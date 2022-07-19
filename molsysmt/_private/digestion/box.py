import numpy as np
from molsysmt import puw
from ..exceptions import WrongBoxError


def digest_box(box, caller=None):
    """ Checks if box has the correct shape.

    The array should have shape (n_structures, 3, 3) where n is any integer.
    However, if a list, tuple is passed it will be converted
    to an array with the desired shape. Also, if an array of
    shape (3, 3) is passed its dimensions will be expanded to
    (1, 3, 3). If an array with rank different from 2 or 3 is passed and exception
    is raised.

    Parameters
    ----------
    box : np.ndarray, list or tuple
        A quantity with the box coordinates.

    caller: str, optional
        Name of the function or method that is being digested.

    Raises
    ------
    WrongBoxError
        If box doesn't have the correct shape.
    """
    if not(isinstance(box, np.ndarray)):
        box = np.array(box)

    shape = box.shape

    if len(shape) == 2:
        if shape[0] != 3 or shape[1] != 3:
            raise WrongBoxError(box, caller=caller)
        box = np.expand_dims(box, axis=0)
    elif len(shape) == 3:
        if shape[1] != 3 or shape[2] != 3:
            raise WrongBoxError(box, caller=caller)
    else:
        raise WrongBoxError(box, caller=caller)

    return box


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


def digest_box_angles(box_angles, caller=None):
    """ Checks if box_angles has the correct type, shape and units.

    Parameters
    ----------
    box_angles : Quantity(value: ndarray or list or tuple, unit: any with dimensionality [])
        The box angles.

    caller: str, optional
        Name of the function or method that is being digested.

    Returns
    -------
    Quantity(value: ndarray with shape [n_structures, 3], unit: default units with dimensionality [])
        The box angles with the shape corrected if necessary.

    Raises
    ------
    IncorrectShapeError
        If box_vectors doesn't have the correct shape.
    """
    unit = puw.get_unit(box_angles)
    box_angles = puw.get_value(box_angles)
    box_angles = digest_box_values(box_angles, caller)

    return box_angles * unit

