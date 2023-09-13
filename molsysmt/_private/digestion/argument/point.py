import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError


def digest_point(point, caller=None):

    if caller=='molsysmt.structure.flip.flip':

        if puw.is_quantity(point):
            if puw.check(point, dimensionality={'[L]':1}):

                value, unit = puw.get_value_and_unit(point)
                value = value.astype(np.float64)
                if (len(value.shape)==1) and (value.shape[0]==3):
                    return puw.quantity(value, unit)

    raise ArgumentError('point', value=point, caller=caller, message=None)

