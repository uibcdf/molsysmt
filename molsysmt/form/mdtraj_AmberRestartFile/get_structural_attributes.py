from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'mdtraj.AmberRestartFile'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.read(atom_indices=indices if not is_all(indices) else None)
    output = tmp_item[0]  # shape (1, n_atoms, 3), angstroms

    if not is_all(structure_indices):
        output = output[structure_indices, :, :]

    output = puw.quantity(output, 'angstrom', standardized=True)
    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    tmp_item = item.read()
    cell_lengths = tmp_item[2]  # shape (3,) angstroms or None
    cell_angles = tmp_item[3]   # shape (3,) degrees or None

    if cell_lengths is not None:
        from molsysmt.pbc import get_box_from_lengths_and_angles
        lengths = puw.quantity(cell_lengths[np.newaxis, :], 'angstrom', standardized=True)
        angles = puw.quantity(cell_angles[np.newaxis, :], 'degree', standardized=True)
        output = get_box_from_lengths_and_angles(lengths, angles)
        if not is_all(structure_indices):
            output = output[structure_indices, :, :]
        return output
    return None

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        return 1
    else:
        return len(structure_indices)

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    tmp_item = item.read()
    if tmp_item[1] is not None:
        time = tmp_item[1]
        if np.ndim(time) == 0:
            output = np.array([float(time)]) * puw.unit('picosecond')
        else:
            output = time * puw.unit('picosecond')
        if not is_all(structure_indices):
            output = output[structure_indices]
        return output
    return None

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
