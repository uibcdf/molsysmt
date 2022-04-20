from molsysmt import puw
import numpy as np

def get_rank_3_XYZ(item):

    unit = puw.get_unit(item)
    value = puw.get_value(item)

    if type(value)==list:
        value = np.array(value)

    if len(value.shape)==2:
        value = np.expand_dims(value, axis=0)
    elif len(value.shape)==1:
        value = np.expand_dims(value, axis=0)
        value = np.expand_dims(value, axis=0)

    return value*unit


