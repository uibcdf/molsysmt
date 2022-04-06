#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from .is_file_inpcrd import is_file_inpcrd
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np
from networkx import Graph

## From atom

def get_coordinates_from_atom(item, indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_coordinates_from_atom as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

## From system

def get_n_atoms_from_system(item, check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_n_atoms_from_system as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, check=False)

    return output

def get_box_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_box_from_system as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, check=False)

    return output

def get_box_shape_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_box_shape_from_system as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, check=False)

    return output

def get_box_lengths_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_box_lengths_from_system as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, check=False)

    return output

def get_box_angles_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_box_angles_from_system as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, check=False)

    return output

def get_box_volume_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_box_volume_from_system as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, check=False)

    return output

def get_time_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_time_from_system as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, check=False)

    return output

def get_step_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_step_from_system as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, check=False)

    return output

def get_n_structures_from_system(item, check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import get_n_structures_from_system as aux_get

    tmp_item = to_openmm_AmberInpcrdFile(item, check=False)
    output = aux_get(tmp_item, check=False)

    return output

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

## From atom

def get_n_atoms_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_atoms_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

## From system

def get_coordinates_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    return get_coordinates_from_atom(item, structure_indices=structure_indices, check=False)

