from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'mdtraj.PDBTrajectoryFile'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    output = item.positions  # shape (n_frames, n_atoms, 3), angstroms

    if not is_all(indices):
        output = output[:, indices, :]
    if not is_all(structure_indices):
        output = output[structure_indices, :, :]

    output = puw.quantity(output, 'angstrom', standardized=True)
    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    cell_lengths = item.unitcell_lengths  # shape (3,) angstroms or None
    cell_angles = item.unitcell_angles    # shape (3,) degrees or None

    if cell_lengths is not None:
        from molsysmt.pbc import get_box_from_lengths_and_angles
        n_structures = len(item.positions)
        lengths = np.tile(cell_lengths, (n_structures, 1))
        lengths = puw.quantity(lengths, 'angstrom', standardized=True)
        angles = np.tile(cell_angles, (n_structures, 1))
        angles = puw.quantity(angles, 'degree', standardized=True)
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
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
