"""Validate flat positional populations at the new correspondence boundaries."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError

CALLERS = {
    "molsysmt.form.read_pdbqt_poses.read_pdbqt_poses",
    "molsysmt.topology.get_atom_correspondences.get_atom_correspondences",
    "molsysmt.structure.get_symmetry_corrected_rmsd.get_symmetry_corrected_rmsd",
}


def flat_axis(value, argument, caller):
    """Reject booleans, fractional values and nested populations before casting."""
    if value is None:
        return value
    if isinstance(value, str):
        if argument == "selection" or value.lower() == "all":
            return value
        raise ArgumentError(argument, value=value, caller=caller)
    if isinstance(value, (list, tuple)) and any(
        isinstance(item, (bool, np.bool_)) for item in value
    ):
        raise ArgumentError(argument, value=value, caller=caller)
    try:
        array = np.asarray(value)
        if array.ndim == 0:
            array = array.reshape(1)
        if array.ndim == 1 and array.size == 0:
            return np.empty(0, dtype=np.int64)
        if (
            array.ndim == 1
            and array.dtype.kind in "iu"
            and np.all(array >= 0)
            and np.all(array <= np.iinfo(np.int64).max)
        ):
            return array.astype(np.int64)
    except (TypeError, ValueError, OverflowError):
        pass
    raise ArgumentError(argument, value=value, caller=caller)
