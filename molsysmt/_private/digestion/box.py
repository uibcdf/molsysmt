import numpy as np
from molsysmt import puw
from ..exceptions import IncorrectShapeError


def digest_box(box):
    # TODO: Function doesn't do anything.
    return box


def digest_box_values(box_values, caller=""):
    """ Checks if box_values has the correct shape.

        The array should have shape (n, 3) where n is any integer.
        However, if a list, tuple is passed it will be converted
        to an array with the desired shape. Also, if an array of
        shape (3, ) is passed its dimensions will be expanded to
        (1, 3). If an array with rank > 2 is passed and exception
        is raised.

        Parameters
        ----------
        box_values : np.ndarray, list or tuple
            A quantity with the box lengths.

        caller: str, optional
            Name of the function or method that is being digested.
            For debugging purposes.

        Raises
        ------
        IncorrectShapeError
            If box_vectors doesn't have the correct shape.
    """
    if not(isinstance(box_values, np.ndarray)):
        box_values = np.array(box_values)

    shape = box_values.shape

    if len(shape) == 1:
        if shape[0] == 3:
            box_values = np.expand_dims(box_values, axis=0)
        else:
            raise IncorrectShapeError(expected_shape="(1, 3)",
                                      actual_shape=str(shape),
                                      caller=caller)
    elif len(shape) == 2:
        if shape[1] != 3:
            raise IncorrectShapeError(expected_shape="(n, 3)",
                                      actual_shape=str(shape),
                                      caller=caller
                                      )
    else:
        raise IncorrectShapeError(expected_shape="(n, 3)",
                                  actual_shape=str(shape),
                                  caller=caller)

    return box_values


def digest_box_lengths_or_angles(box_parameters, caller=""):
    """ Checks if box_parameters have the correct shape. Can be used
        to check box_lengths and box_angles.

        Parameters
        ----------
        box_parameters : puw.Quantity
            A quantity with the box lengths or box values.

        caller: str, optional
            Name of the function or method that is being digested.
            For debugging purposes.

        Returns
        -------
        puw.Quantity
            The box vectors with the shape corrected.

        Raises
        ------
        IncorrectShapeError
            If box_vectors doesn't have the correct shape.
    """
    unit = puw.get_unit(box_parameters)
    box_parameters = puw.get_value(box_parameters)
    box_parameters = digest_box_values(box_parameters, caller)
    return box_parameters * unit


def digest_box_lengths(box_lengths, caller=""):
    """ Checks if box_lengths have the correct shape. """
    return digest_box_lengths_or_angles(box_lengths, caller)


def digest_box_angles(box_angles, caller=""):
    """ Checks if box_angles have the correct shape. """
    return digest_box_lengths_or_angles(box_angles, caller)
