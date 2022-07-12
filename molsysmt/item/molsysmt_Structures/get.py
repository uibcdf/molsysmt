from molsysmt._private.exceptions import NotWithThisFormError as _NotWithThisFormError
from molsysmt._private.exceptions import NotImplementedMethodError as _NotImplementedMethodError
from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_indices as _digest_indices
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices
from molsysmt._private.variables import is_all as _is_all
from molsysmt import puw as _puw
import numpy as _np
from networkx import Graph as _Graph

_form='molsysmt.Structures'

## atom

def get_coordinates_from_atom(item, indices='all', structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)
        structure_indices = _digest_structure_indices(structure_indices)

    tmp_coordinates = item.coordinates

    if not _is_all(structure_indices):
        tmp_coordinates = tmp_coordinates[structure_indices,:,:]

    if not _is_all(indices):
        tmp_coordinates = tmp_coordinates[:,indices,:]

    return tmp_coordinates

def get_n_atoms_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if _is_all(indices):
        output=item.coordinates.shape[1]
    else:
        output=indices.shape[0]

    return output

## system

def get_n_atoms_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    output=item.coordinates.shape[1]

    return output

def get_coordinates_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    if _is_all(structure_indices):
        output=item.coordinates
    else:
        output=item.coordinates[structure_indices,:,:]
    return output

def get_box_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    output=None
    if item.box is not None:
        if _is_all(structure_indices):
            output=item.box
        else:
            output=item.box[structure_indices,:,:]
    return output

def get_box_shape_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    from molsysmt.pbc import box_shape_from_box_vectors
    output = None
    box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    if box is not None:
        output = box_shape_from_box_vectors(box)
    return output

def get_box_lengths_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    tmp_box_lengths = item.get_box_lengths()
    if _is_all(structure_indices):
        output = tmp_box_lengths
    else:
        output = tmp_box_lengths[structure_indices,:]
    return output

def get_box_angles_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    tmp_box_angles = item.get_box_angles()
    if _is_all(structure_indices):
        output = tmp_box_angles
    else:
        output = tmp_box_angles[structure_indices,:]
    return output

def get_box_volume_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    from molsysmt.pbc import box_volume_from_box_vectors
    output = None
    box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    if box is not None:
        output = box_volume_from_box_vectors(box)
    return output

def get_time_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    if _is_all(structure_indices):
        output = item.time
    else:
        output = item.time[structure_indices]
    return output

def get_step_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    if _is_all(structure_indices):
        output = item.step
    else:
        output = item.step[structure_indices]
    return output

def get_n_structures_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    output=item.coordinates.shape[0]

    return output

