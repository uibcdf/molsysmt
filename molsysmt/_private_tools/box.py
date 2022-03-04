import numpy as np
from molsysmt import puw

def digest_box(box):

    raise NotImplementedError

def digest_box_lengths_value(box_lengths):

    output = None

    if type(box_lengths) is not np.ndarray:
        box_lengths = np.array(box_lengths)

    shape = box_lengths.shape

    if len(shape)==1:
        if shape[0]==3:
            output = np.expand_dims(box_lengths, axis=0)
        else:
            raise ValueError('box_lengths array with has not the correct shape.')
    elif len(shape)==2:
        if shape[1]==3:
            output = box_lengths
        else:
            raise ValueError('box_lengths array with has not the correct shape.')
    else:
        raise ValueError('box_lengths array with has not the correct shape.')

    return output

def digest_box_lengths(box_lengths):

    output = None
    unit = puw.get_unit(box_lengths)
    box_lengths_value = puw.get_value(box_lengths)
    box_lengths_value = digest_box_lengths_value(box_lengths_value)
    output = box_lengths_value*unit

    return output

def digest_box_angles_value(box_angles):

    output = None

    if type(box_angles) is not np.ndarray:
        box_angles = np.array(box_angles)

    shape = box_angles.shape

    if len(shape)==1:
        if shape[0]==3:
            output = np.expand_dims(box_angles, axis=0)
        else:
            raise ValueError('box_angles array with has not the correct shape.')
    elif len(shape)==2:
        if shape[1]==3:
            output = box_angles
        else:
            raise ValueError('box_angles array with has not the correct shape.')
    else:
        raise ValueError('box_angles array with has not the correct shape.')

    return output

def digest_box_angles(box_angles):

    output = None
    unit = puw.get_unit(box_angles)
    box_angles_value = puw.get_value(box_angles)
    box_angles_value = digest_box_angles_value(box_angles_value)
    output = box_angles_value*unit

    return output

