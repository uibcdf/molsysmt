from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'mdtraj.XTCTrajectoryFile'


def _read_from_start(item, atom_indices=None):
    """Read an XTC payload without changing the caller's file position."""

    position = item.tell()
    try:
        item.seek(0)
        return item.read(atom_indices=atom_indices)
    finally:
        item.seek(position)

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    atom_indices = indices if not is_all(indices) else None
    tmp_item = _read_from_start(item, atom_indices=atom_indices)
    if is_all(structure_indices):
        output = tmp_item[0] # coordinates
    else:
        output = tmp_item[0][structure_indices, :, :]

    output = output * puw.unit('nanometer')
    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    tmp_item = _read_from_start(item)
    if tmp_item[3] is not None and len(tmp_item[3]) > 0:  # box vectors
        output = tmp_item[3] * puw.unit('nanometer')
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

    tmp_item = _read_from_start(item)
    if tmp_item[1] is not None: # times
        output = tmp_item[1] * puw.unit('picosecond')
        if not is_all(structure_indices):
            output = output[structure_indices]
        return output
    return None

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    tmp_item = _read_from_start(item)
    if tmp_item[2] is not None:
        output = tmp_item[2]
        if not is_all(structure_indices):
            output = output[structure_indices]
        return output
    return None

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
