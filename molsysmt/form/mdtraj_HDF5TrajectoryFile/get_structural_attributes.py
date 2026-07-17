from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'mdtraj.HDF5TrajectoryFile'


def _read_from_start(item, atom_indices=None):
    """Reading HDF5 frames without changing the caller's file position."""

    position = item.tell()
    try:
        item.seek(0)
        return item.read(atom_indices=atom_indices)
    finally:
        item.seek(position)


def _slice_structures(value, structure_indices):
    """Selecting structures from an optional frame field."""

    if value is None or is_all(structure_indices):
        return value
    return value[structure_indices]


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = _read_from_start(
        item,
        atom_indices=None if is_all(indices) else indices,
    )
    output = _slice_structures(tmp_item.coordinates, structure_indices)

    output = output * puw.unit('nanometer')
    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    tmp_item = _read_from_start(item)
    if tmp_item.cell_lengths is not None and tmp_item.cell_angles is not None:
        from molsysmt.pbc import get_box_from_lengths_and_angles
        lengths = tmp_item.cell_lengths * puw.unit('nanometer')
        angles = tmp_item.cell_angles * puw.unit('degree')
        output = get_box_from_lengths_and_angles(lengths, angles)
        return _slice_structures(output, structure_indices)
    return None

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        return len(item)
    else:
        return len(structure_indices)

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    output = _slice_structures(_read_from_start(item).time, structure_indices)
    if output is not None:
        return output * puw.unit('picosecond')
    return None


@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    tmp_item = _read_from_start(
        item,
        atom_indices=None if is_all(indices) else indices,
    )
    output = _slice_structures(tmp_item.velocities, structure_indices)
    if output is None:
        return None
    return output * puw.unit('nanometer/picosecond')


@arg_digest(form=form)
def get_temperature_from_system(item, structure_indices='all', skip_digestion=False):
    output = _slice_structures(_read_from_start(item).temperature, structure_indices)
    if output is None:
        return None
    return output * puw.unit('kelvin')


@arg_digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all', skip_digestion=False):
    output = _slice_structures(_read_from_start(item).potentialEnergy, structure_indices)
    if output is None:
        return None
    return output * puw.unit('kilojoule/mole')


@arg_digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all', skip_digestion=False):
    output = _slice_structures(_read_from_start(item).kineticEnergy, structure_indices)
    if output is None:
        return None
    return output * puw.unit('kilojoule/mole')


@arg_digest(form=form)
def get_total_energy_from_system(item, structure_indices='all', skip_digestion=False):
    potential = get_potential_energy_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    kinetic = get_kinetic_energy_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    if potential is None or kinetic is None:
        return None
    return potential + kinetic

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
