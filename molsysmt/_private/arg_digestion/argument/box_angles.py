import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

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

    if caller=='molsysmt.basic.get.get':

        if isinstance(box_angles, bool):
            return box_angles
        else:
            raise ArgumentError('box_angles', value=box_angles, caller=caller, message=None)

    else:

        if not puw.check(box_angles, dimensionality={}):
            raise ArgumentError('box_angles', value=box_angles, caller=caller, message=None)

        value, unit = puw.get_value_and_unit(box_angles)
        
        if not isinstance(value, np.ndarray):
            value = np.array(value)
        
        shape = value.shape

        if len(shape) == 1:
            if shape[0] != 3:
                raise ArgumentError('box_angles', caller=caller, message=None)
            value = np.expand_dims(value, axis=0)
        elif len(shape) == 2:
            if shape[1] != 3:
                raise ArgumentError('box_angles', value=box_angles, caller=caller, message=None)
        else:
            raise ArgumentError('box_angles', value=box_angles, caller=caller, message=None)

        box_angles = puw.quantity(value, unit, standardized=True)

        return box_angles

