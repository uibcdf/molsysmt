"""Construct empty, evaluated hydrogen-bond results."""

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
