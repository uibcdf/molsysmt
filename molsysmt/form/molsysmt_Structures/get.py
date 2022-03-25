from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_Structures import is_molsysmt_Structures
import numpy as np
from networkx import Graph

## atom

def get_coordinates_from_atom(item, indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_coordinates = item.coordinates

    if structure_indices is not 'all':
        tmp_coordinates = tmp_coordinates[structure_indices,:,:]

    if indices is not 'all':
        tmp_coordinates = tmp_coordinates[:,indices,:]

    return tmp_coordinates

def get_n_atoms_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output=item.coordinates.shape[1]
    else:
        output=indices.shape[0]

    return output

## system

def get_n_atoms_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

    output=item.coordinates.shape[1]

    return output

def get_coordinates_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongIndicesError()

    if structure_indices is 'all':
        output=item.coordinates
    else:
        output=item.coordinates[structure_indices,:,:]
    return output

def get_box_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongIndicesError()

    output=None
    if item.box is not None:
        if structure_indices is 'all':
            output=item.box
        else:
            output=item.box[structure_indices,:,:]
    return output

def get_box_shape_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongIndicesError()

    from molsysmt.pbc import box_shape_from_box_vectors
    output = None
    box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    if box is not None:
        output = box_shape_from_box_vectors(box)
    return output

def get_box_lengths_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongIndicesError()

    tmp_box_lengths = item.get_box_lengths()
    if structure_indices is 'all':
        output = tmp_box_lengths
    else:
        output = tmp_box_lengths[structure_indices,:]
    return output

def get_box_angles_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongIndicesError()

    tmp_box_angles = item.get_box_angles()
    if structure_indices is 'all':
        output = tmp_box_angles
    else:
        output = tmp_box_angles[structure_indices,:]
    return output

def get_time_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongIndicesError()

    if structure_indices is 'all':
        output = item.time
    else:
        output = item.time[structure_indices]
    return output

def get_step_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongIndicesError()

    if structure_indices is 'all':
        output = item.step
    else:
        output = item.step[structure_indices]
    return output

def get_n_structures_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

    output=item.coordinates.shape[0]

    return output

