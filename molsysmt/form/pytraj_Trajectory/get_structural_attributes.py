from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='pytraj.Trajectory'


@arg_digest(form=form)
def get_coordinates_from_atom(
    item,
    indices='all',
    structure_indices='all',
    skip_digestion=False,
):
    """Getting coordinates from a PyTraj trajectory in canonical units."""

    coordinates = item.xyz
    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices, :, :]
    if not is_all(indices):
        coordinates = coordinates[:, indices, :]

    coordinates = puw.quantity(coordinates, 'angstrom')
    return puw.standardize(coordinates)


@arg_digest(form=form)
def get_n_structures_from_system(
    item,
    structure_indices='all',
    skip_digestion=False,
):
    """Getting the number of selected structures from a PyTraj trajectory."""

    if is_all(structure_indices):
        return item.n_frames
    return len(structure_indices)


@arg_digest(form=form)
def get_box_from_system(
    item,
    structure_indices='all',
    skip_digestion=False,
):
    """Getting periodic boxes from a PyTraj trajectory in canonical units."""

    unitcells = item.unitcells
    if unitcells is None:
        return None
    if not is_all(structure_indices):
        unitcells = unitcells[structure_indices, :]

    from molsysmt.pbc import get_box_from_lengths_and_angles

    box_lengths = puw.quantity(np.asarray(unitcells[:, :3]), 'angstrom')
    box_angles = puw.quantity(np.asarray(unitcells[:, 3:]), 'degree')
    return get_box_from_lengths_and_angles(
        box_lengths,
        box_angles,
        skip_digestion=True,
    )


@arg_digest(form=form)
def get_time_from_system(
    item,
    structure_indices='all',
    skip_digestion=False,
):
    """Getting time from a PyTraj trajectory in picoseconds when available."""

    if item.time is None:
        return None
    time = item.time
    if not is_all(structure_indices):
        time = time[structure_indices]
    return puw.standardize(puw.quantity(time, 'picosecond'))


@arg_digest(form=form)
def get_structure_id_from_system(
    item,
    structure_indices='all',
    skip_digestion=False,
):
    """Getting structure identifiers unavailable in PyTraj trajectories."""

    return None


# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
