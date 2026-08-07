"""Shared validation for public nullable chemical-state bond attributes."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import ArgumentError


def _values(value):
    if value is None or value is pd.NA or np.isscalar(value):
        return [value], True
    array = np.asarray(value, dtype=object)
    if array.ndim != 1:
        return None, False
    return array.tolist(), False


def digest_bond_state_attribute(name, value, caller, kind, choices=None):
    """Validate a get flag or a scalar/vector assignment by semantic kind."""

    if caller in {'molsysmt.basic.get.get', 'molsysmt.basic.compare.compare'}:
        if isinstance(value, (bool, np.bool_)):
            return bool(value)
        raise ArgumentError(name, value=value, caller=caller, message=None)

    if caller != 'molsysmt.basic.set.set':
        raise ArgumentError(name, value=value, caller=caller, message=None)

    values, scalar = _values(value)
    if values is None:
        raise ArgumentError(name, value=value, caller=caller, message=None)

    normalized = []
    for item in values:
        if item is None or item is pd.NA:
            normalized.append(item)
        elif kind == 'string' and not isinstance(item, (list, tuple, dict, set)):
            normalized.append(str(item))
        elif kind == 'choice' and isinstance(item, str) and item in choices:
            normalized.append(item)
        elif kind == 'integer' and isinstance(item, (int, np.integer)) and not isinstance(
            item, (bool, np.bool_)
        ) and int(item) >= 0:
            normalized.append(int(item))
        elif kind == 'float' and isinstance(item, (int, float, np.integer, np.floating)) and not isinstance(
            item, (bool, np.bool_)
        ) and np.isfinite(item) and float(item) >= 0:
            normalized.append(float(item))
        elif kind == 'boolean' and isinstance(item, (bool, np.bool_)):
            normalized.append(bool(item))
        else:
            raise ArgumentError(name, value=value, caller=caller, message=None)
    return normalized[0] if scalar else normalized


def digest_stereo_atom_indices(name, value, caller):
    """Validate the nullable two-column stereo-reference public shape."""

    if caller in {'molsysmt.basic.get.get', 'molsysmt.basic.compare.compare'}:
        if isinstance(value, (bool, np.bool_)):
            return bool(value)
        raise ArgumentError(name, value=value, caller=caller, message=None)
    if caller != 'molsysmt.basic.set.set':
        raise ArgumentError(name, value=value, caller=caller, message=None)
    if value is None or value is pd.NA:
        return value
    array = np.asarray(value, dtype=object)
    if array.shape == (2,):
        array = array.reshape(1, 2)
    if array.ndim != 2 or array.shape[1] != 2:
        raise ArgumentError(name, value=value, caller=caller, message=None)
    for item in array.ravel():
        if item is None or item is pd.NA:
            continue
        if isinstance(item, (bool, np.bool_)) or not isinstance(item, (int, np.integer)) or item < 0:
            raise ArgumentError(name, value=value, caller=caller, message=None)
    return array.tolist()
