import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

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

    if caller=='get':

        if isinstance(box, bool):
            return box
        else:
            raise ArgumentError('box', caller=caller, message=None)

    else:

        if not isinstance(box, np.ndarray):
            box = np.array(box)

        shape = box.shape

        if len(shape) == 2:
            if shape[0] != 3 or shape[1] != 3:
                raise ArgumentError('box', caller=caller, message=None)
            box = np.expand_dims(box, axis=0)
        elif len(shape) == 3:
            if shape[1] != 3 or shape[2] != 3:
                raise ArgumentError('box', caller=caller, message=None)
        else:
            raise ArgumentError('box', caller=caller, message=None)

        return box

