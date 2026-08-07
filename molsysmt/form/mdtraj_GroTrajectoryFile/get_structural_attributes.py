from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'mdtraj.GroTrajectoryFile'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    item._file.seek(0)
    tmp_item = item.read(atom_indices=indices if not is_all(indices) else None)
    output = tmp_item[0]  # shape (n_frames, n_atoms, 3), nanometers

    if not is_all(structure_indices):
        output = output[structure_indices, :, :]

    output = output * puw.unit('nanometer')
    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    item._file.seek(0)
    tmp_item = item.read()
    unitcell_vectors = tmp_item[2]  # shape (n_frames, 3, 3), nanometers

    if unitcell_vectors is not None and len(unitcell_vectors) > 0:
        output = unitcell_vectors * puw.unit('nanometer')
        if not is_all(structure_indices):
            output = output[structure_indices, :, :]
        return output
    return None

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        item._file.seek(0)
        tmp_item = item.read()
        return tmp_item[0].shape[0]
    else:
        return len(structure_indices)

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    item._file.seek(0)
    tmp_item = item.read()
    if tmp_item[1] is not None:
        output = tmp_item[1] * puw.unit('picosecond')
        if not is_all(structure_indices):
            output = output[structure_indices]
        return output
    return None

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
