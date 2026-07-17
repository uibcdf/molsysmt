"""Delivering ParmEd coordinate frames, unit cells, and B factors."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

form = 'parmed.Structure'


def _selected_frame_indices(item, structure_indices):
    coordinates = item.get_coordinates('all')
    n_structures = 0 if coordinates is None else coordinates.shape[0]
    if is_all(structure_indices):
        return np.arange(n_structures, dtype=np.int64)
    return np.asarray(structure_indices, dtype=np.int64)


@arg_digest(form=form)
def get_coordinates_from_atom(
    item, indices='all', structure_indices='all', skip_digestion=False
):
    """Returning coordinate frames in nanometers."""

    coordinates = item.get_coordinates('all')
    if coordinates is None:
        return None
    frame_indices = _selected_frame_indices(item, structure_indices)
    coordinates = np.asarray(coordinates[frame_indices], dtype=np.float64)
    if not is_all(indices):
        coordinates = coordinates[:, indices, :]
    return puw.standardize(puw.quantity(coordinates, 'angstrom'))


@arg_digest(form=form)
def get_structure_id_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """Returning positional identifiers for ParmEd coordinate frames."""

    return _selected_frame_indices(item, structure_indices)


@arg_digest(form=form)
def get_structure_index_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """Returning selected positional frame indices."""

    return _selected_frame_indices(item, structure_indices)


@arg_digest(form=form)
def get_n_structures_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """Returning the number of selected coordinate frames."""

    return len(_selected_frame_indices(item, structure_indices))


@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    """Returning no time because ParmEd coordinate frames do not store it."""

    return None


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    """Returning unit-cell vectors in nanometers."""

    boxes = item.get_box('all')
    if boxes is None:
        return None
    if is_all(structure_indices):
        structure_indices = np.arange(len(boxes), dtype=np.int64)
    boxes = np.asarray(boxes, dtype=np.float64)[structure_indices]
    from molsysmt.pbc import get_box_from_lengths_and_angles

    return get_box_from_lengths_and_angles(
        puw.quantity(boxes[:, :3], 'angstrom'),
        puw.quantity(boxes[:, 3:], 'degree'),
        skip_digestion=True,
    )


@arg_digest(form=form)
def get_b_factor_from_atom(
    item, indices='all', structure_indices='all', skip_digestion=False
):
    """Returning atom B factors in squared nanometers."""

    frame_indices = _selected_frame_indices(item, structure_indices)
    if len(frame_indices) == 0:
        return None
    values = np.asarray([atom.bfactor for atom in item.atoms], dtype=np.float64)
    if not np.any(values):
        return None
    if not is_all(indices):
        values = values[indices]
    values = np.repeat(values[None, :], len(frame_indices), axis=0)
    return puw.standardize(puw.quantity(values, 'angstrom**2'))
