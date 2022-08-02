import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

def digest_translation(translation, caller=None):

    if not puw.is_quantity(translation):
        raise ArgumentError('translation', caller=caller, message=None)

    value = puw.get_value(translation)
    unit = puw.get_unit(translation)

    if not isinstance(value, np.ndarray):
        value = np.array(value)

    shape = value.shape

    if len(shape) == 1:
        if shape[0] != 3:
            raise ArgumentError('translation', caller=caller, message=None)
    elif len(shape) == 2:
        if shape[1] != 3:
            raise ArgumentError('translation', caller=caller, message=None)
    else:
        raise ArgumentError('translation', caller=caller, message=None)

    

    if caller=='translate':

        if isinstance(box, bool):
            return box
        else:
            raise ArgumentError('box', caller=caller, message=None)

    else:

        if not(isinstance(box, np.ndarray)):
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

