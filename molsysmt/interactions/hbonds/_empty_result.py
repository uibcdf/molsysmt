"""Construct aligned per-structure hydrogen-bond results."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all


def empty_result(molecular_system, structure_indices, with_angles=False):
    if is_all(structure_indices):
        from molsysmt.basic import get

        n_structures = get(molecular_system, n_structures=True)
    else:
        n_structures = len(np.atleast_1d(structure_indices))

    atoms = np.empty((n_structures, 0, 3), dtype=np.int64)
    distances = puw.quantity(np.empty((n_structures, 0)), "nanometers")
    if with_angles:
        angles = puw.quantity(np.empty((n_structures, 0)), "radians")
        return atoms, distances, angles
    return atoms, distances


def pack_result(atoms, distances, angles=None):
    """Keep rectangular legacy arrays and preserve varying counts as lists."""
    triples = [np.asarray(frame, dtype=np.int64).reshape(-1, 3) for frame in atoms]
    values = [puw.get_value(frame, to_unit="nanometers") for frame in distances]
    angle_values = (
        None if angles is None else
        [puw.get_value(frame, to_unit="radians") for frame in angles]
    )
    if len({len(frame) for frame in triples}) > 1:
        result = (triples, [puw.quantity(frame, "nanometers") for frame in values])
        if angle_values is not None:
            result += ([puw.quantity(frame, "radians") for frame in angle_values],)
        return result
    result = (
        np.stack(triples) if triples else np.empty((0, 0, 3), dtype=np.int64),
        puw.quantity(np.stack(values) if values else np.empty((0, 0)), "nanometers"),
    )
    if angle_values is not None:
        result += (puw.quantity(
            np.stack(angle_values) if angle_values else np.empty((0, 0)), "radians"),)
    return result
