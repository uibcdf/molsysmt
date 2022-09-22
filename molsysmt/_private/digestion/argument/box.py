import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

methods_where_bool = [
    'molsysmt.basic.get.get',
    'molsysmt.basic.compare.compare'
]

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

    if caller in methods_where_bool:

        if isinstance(box, bool):
            return box
        else:
            raise ArgumentError('box', value=box, caller=caller, message=None)

    else:

        if box is None:
            return box

        if not puw.check(box, dimensionality={'[L]':1}):
            raise ArgumentError('box', caller=caller, message=None)

        box_value = puw.get_value(box)
        box_unit = puw.get_unit(box)

        if not isinstance(box_value, np.ndarray):
            box_value = np.array(box_value)

        shape = box_value.shape

        if len(shape) == 2:
            if shape[0] != 3 or shape[1] != 3:
                raise ArgumentError('box', caller=caller, message=None)
            box_value = np.expand_dims(box_value, axis=0)
        elif len(shape) == 3:
            if shape[1] != 3 or shape[2] != 3:
                raise ArgumentError('box', value=box, caller=caller, message=None)
        else:
            raise ArgumentError('box', value=box, caller=caller, message=None)

        box = puw.quantity(box_value, box_unit)
        box = puw.standardize(box)

        return box

