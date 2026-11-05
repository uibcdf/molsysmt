"""Validate the explicit native group-name declaration boundary."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError, ArgumentLengthError
from molsysmt._private.variables import is_all

from .argument._correspondence_axes import _has_units, flat_axis
from .argument.skip_digestion import digest_skip_digestion


def _self(self, caller=None):
    from molsysmt.native.topology import Topology

    if not isinstance(self, Topology):
        raise ArgumentError("self", value=self, caller=caller)
    return self


def _indices(group_indices, self, caller=None):
    if np.ma.isMaskedArray(group_indices):
        raise ArgumentError("group_indices", value=group_indices, caller=caller)
    result = flat_axis(group_indices, "group_indices", caller)
    if is_all(result):
        return "all"
    if (
        result is None
        or isinstance(result, str)
        or np.any(result >= self.n_groups)
        or len(np.unique(result)) != len(result)
    ):
        raise ArgumentError("group_indices", value=group_indices, caller=caller)
    return result


def _schemes(naming_schemes, group_indices, self, caller=None):
    from molsysmt.native._group_naming import NAMES

    if naming_schemes is None or isinstance(naming_schemes, str):
        # Validate a scalar even when the selected axis is empty.
        if naming_schemes not in NAMES:
            raise ArgumentError("naming_schemes", value=naming_schemes, caller=caller)
        return naming_schemes
    elif (
        isinstance(naming_schemes, (list, tuple, np.ndarray))
        and not np.ma.isMaskedArray(naming_schemes)
        and not _has_units(naming_schemes)
    ):
        values = np.asarray(naming_schemes, dtype=object)
        if values.ndim != 1:
            raise ArgumentError("naming_schemes", value=naming_schemes, caller=caller)
    else:
        raise ArgumentError("naming_schemes", value=naming_schemes, caller=caller)
    if any(
        value is not None and (not isinstance(value, str) or value not in NAMES)
        for value in values
    ):
        raise ArgumentError("naming_schemes", value=naming_schemes, caller=caller)
    expected = self.n_groups if is_all(group_indices) else len(group_indices)
    if len(values) != expected:
        raise ArgumentLengthError(
            "naming_schemes",
            expected=expected,
            actual=len(values),
            caller=caller,
        )
    return tuple(values)


ARGUMENT_DIGESTERS = {
    "self": _self,
    "group_indices": _indices,
    "naming_schemes": _schemes,
    "skip_digestion": digest_skip_digestion,
}
