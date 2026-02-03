import numpy as np
from molsysmt import pyunitwizard as puw
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

        value, unit = puw.get_value_and_unit(box_lengths)
        
        if not isinstance(value, np.ndarray):
            value = np.array(value)
        
        shape = value.shape

        if len(shape) == 1:
            if shape[0] != 3:
                raise ArgumentError('box_lengths', caller=caller, message=None)
            value = np.expand_dims(value, axis=0)
        elif len(shape) == 2:
            if shape[1] != 3:
                raise ArgumentError('box_lengths', value=box_lengths, caller=caller, message=None)
        else:
            raise ArgumentError('box_lengths', value=box_lengths, caller=caller, message=None)

        box_lengths = puw.quantity(value, unit, standardized=True)

        return box_lengths

