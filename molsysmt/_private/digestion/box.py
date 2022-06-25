import numpy as np
from molsysmt import puw
from ..exceptions import IncorrectShapeError


def digest_box(box):
    # TODO: Function doesn't do anything.
    return box


def digest_box_vectors_value(box_vectors):
    """ Checks if box_vectors has the correct shape.

        The array should have shape (n, 3) where n is any integer.
        However, if a list, tuple is passed it will be converted
        to an array with the desired shape. Also, if an array of
        shape (3, ) is passed its dimensions will be expanded to
        (1, 3). If an array with rank > 2 is passed and exception
        is raised.

        Parameters
        ----------
        box_vectors : np.ndarray, list or tuple
            A quantity with the box lengths.

        Raises
        ------
        IncorrectShapeError
            If box_vectors doesn't have the correct shape.
    """
    if not(isinstance(box_vectors, np.ndarray)):
        box_vectors = np.array(box_vectors)

    shape = box_vectors.shape

    if len(shape) == 1:
        if shape[0] == 3:
            box_vectors = np.expand_dims(box_vectors, axis=0)
        else:
            raise IncorrectShapeError(expected_shape="(1, 3)", actual_shape=str(shape))
    elif len(shape) == 2:
        if shape[1] != 3:
            raise IncorrectShapeError(expected_shape="(n, 3)", actual_shape=str(shape))
    else:
        raise IncorrectShapeError(expected_shape="(n, 3)", actual_shape=str(shape))

    return box_vectors


def digest_box_vectors(box_vectors):
    """ Checks if box vectors have the correct shape. Can be used
        to check box_lengths and box_angles.

        Parameters
        ----------
        box_vectors : puw.Quantity
            A quantity with the box vectors.

        Returns
        -------
        puw.Quantity
            The box vectors with the shape corrected.

        Raises
        ------
        IncorrectShapeError
            If box_vectors doesn't have the correct shape.
    """
    unit = puw.get_unit(box_vectors)
    box_vectors = puw.get_value(box_vectors)
    box_vectors = digest_box_vectors_value(box_vectors)
    return box_vectors * unit
