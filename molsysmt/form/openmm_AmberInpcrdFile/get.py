#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from .is_openmm_AmberInpcrdFile import is_openmm_AmberInpcrdFile
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np
from networkx import Graph
from molsysmt import puw

## From atom

def get_coordinates_from_atom(item, indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    xyz = item.getPositions(asNumpy=True)

    unit = puw.get_unit(xyz)

    xyz = np.expand_dims(xyz, axis=0)

    if structure_indices is not 'all':
        xyz = xyz[structure_indices, :, :]
    if indices is not 'all':
        xyz = xyz[:, indices, :]


    xyz = puw.standardize(xyz*unit)

    return xyz

## From system

def get_n_atoms_from_system(item, check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

    n_atoms = item.getPositions(asNumpy=True).shape[0]

    return n_atoms

def get_box_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    box = getBoxVectors(asNumpy=True)
    unit = puw.get_unit(box)
    box = np.expand_dims(box, axis=0)
    box = puw.standardize(box*unit)

    return box

def get_box_shape_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.pbc import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    output = box_shape_from_box_vectors(tmp_box, check=False)

    return output

def get_box_lengths_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.pbc import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    output = box_lengths_from_box_vectors(tmp_box, check=False)

    return output


def get_box_angles_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.pbc import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    output = box_angles_from_box_vectors(tmp_box, check=False)

    return output

def get_box_volume_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.pbc import box_volume_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    if tmp_box is None:
        output=None
    else:
        output = box_volume_from_box_vectors(tmp_box, check=False)

    return output


def get_n_structures_from_system(item, check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

    return 1

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

## From atom

def get_n_atoms_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

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
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    return get_coordinates_from_atom(item, structure_indices=structure_indices, check=False)

