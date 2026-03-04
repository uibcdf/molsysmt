from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'mdtraj.HDF5TrajectoryFile'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    item.seek(0)
    if is_all(structure_indices):
        if is_all(indices):
            tmp_item = item.read(atom_indices=None)
        else:
            tmp_item = item.read(atom_indices=indices)
        output = tmp_item.coordinates
    else:
        # MDTraj file handles usually support sequential reading or seeking.
        # HDF5TrajectoryFile specifically might be more flexible.
        # But for now, let's use the standard read and slice.
        item.seek(0)
        if is_all(indices):
            tmp_item = item.read(atom_indices=None)
        else:
            tmp_item = item.read(atom_indices=indices)
        output = tmp_item.coordinates[structure_indices, :, :]

    output = output * puw.unit('nanometer')
    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    item.seek(0)
    tmp_item = item.read()
    if tmp_item.cell_lengths is not None and tmp_item.cell_angles is not None:
        from molsysmt.pbc import get_box_from_lengths_and_angles
        lengths = tmp_item.cell_lengths * puw.unit('nanometer')
        angles = tmp_item.cell_angles * puw.unit('degree')
        output = get_box_from_lengths_and_angles(lengths, angles)
        if not is_all(structure_indices):
            output = output[structure_indices, :, :]
        return output
    return None

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        return len(item)
    else:
        return len(structure_indices)

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    item.seek(0)
    tmp_item = item.read()
    if tmp_item.time is not None:
        output = tmp_item.time * puw.unit('picosecond')
        if not is_all(structure_indices):
            output = output[structure_indices]
        return output
    return None

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    return None

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
