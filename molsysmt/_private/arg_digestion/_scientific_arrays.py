import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError


def normalize_lengths_to_nm_array(value, argname, caller=None):
    if isinstance(value, np.ndarray):
        array = np.asarray(value, dtype=np.float64)
    else:
        if not puw.check(value, dimensionality={"[L]": 1}):
            raise ArgumentError(argname, value=value, caller=caller, message=None)
        array = np.asarray(puw.get_value(puw.to_nanometers(value)), dtype=np.float64)

    if array.ndim == 1:
        if array.shape[0] != 3:
            raise ArgumentError(argname, value=value, caller=caller, message=None)
        return np.expand_dims(array, axis=0)

    if array.ndim == 2 and array.shape[1] == 3:
        return array

    raise ArgumentError(argname, value=value, caller=caller, message=None)


def normalize_box_to_nm_array(value, argname, caller=None):
    if value is None:
        return None

    if isinstance(value, np.ndarray):
        array = np.asarray(value, dtype=np.float64)
    else:
        if not puw.check(value, dimensionality={"[L]": 1}):
            raise ArgumentError(argname, value=value, caller=caller, message=None)
        array = np.asarray(puw.get_value(puw.to_nanometers(value)), dtype=np.float64)

    if array.ndim == 2:
        if array.shape != (3, 3):
            raise ArgumentError(argname, value=value, caller=caller, message=None)
        return np.expand_dims(array, axis=0)

    if array.ndim == 3 and array.shape[1:] == (3, 3):
        return array

    raise ArgumentError(argname, value=value, caller=caller, message=None)
