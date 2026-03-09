from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'mdtraj.XTCTrajectoryFile'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        tmp_item = item.read(atom_indices=indices if not is_all(indices) else None)
        output = tmp_item[0] # coordinates
    else:
        tmp_item = item.read(atom_indices=indices if not is_all(indices) else None)
        output = tmp_item[0][structure_indices, :, :]

    output = output * puw.unit('nanometer')
    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    tmp_item = item.read()
    if tmp_item[2] is not None and len(tmp_item[2]) > 0: # cell_lengths
        from molsysmt.pbc import get_box_from_lengths_and_angles
        lengths = tmp_item[2] * puw.unit('nanometer')
        if tmp_item[3] is not None:
            angles = tmp_item[3] * puw.unit('degree')
        else:
            angles = None
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

    tmp_item = item.read()
    if tmp_item[1] is not None: # times
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
