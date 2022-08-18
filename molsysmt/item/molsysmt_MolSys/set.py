from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

###### Set

## Atom

@digest(form='molsysmt.MolSys')
def set_atom_name_to_atom(item, indices='all', structure_indices='all', value=None):

    from ..molsysmt_Topology import set_atom_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None):

    if is_all(indices):
        if item.structures.coordinates.shape[1]!=value.shape[1]:
            raise ValueError('New coordinates array has different number of atoms')

    if is_all(structure_indices):
        if item.structures.coordinates.shape[0]!=value.shape[0]:
            raise ValueError('New coordinates array has different number of frames')

    if is_all(indices):
        if is_all(structure_indices):
            item.structures.coordinates[:,:,:] = value[:,:,:]
        else:
            item.structures.coordinates[structure_indices,:,:] = value[:,:,:]
    else:
        if is_all(structure_indices):
            item.structures.coordinates[:,indices,:] = value[:,:,:]
        else:
            item.structures.coordinates[np.ix_(structure_indices, indices)]=value[:,:,:]

## System

@digest(form='molsysmt.MolSys')
def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    item.trajectory.box = value

    pass

@digest(form='molsysmt.MolSys')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value)

