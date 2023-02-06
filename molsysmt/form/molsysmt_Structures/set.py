from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

###### Set

## Atom

@digest(form='molsysmt.Structures')
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None):

    if is_all(indices):
        if is_all(structure_indices):
            item.coordinates = value              
            item.n_structures = value.shape[0]
            item.n_atoms = value.shape[1]
        else:
            item.coordinates[structure_indices,:,:] = value[:,:,:]
    else:
        if is_all(structure_indices):
            item.coordinates[:,indices,:] = value[:,:,:]
        else:
            item.coordinates[np.ix_(structure_indices, indices)]=value[:,:,:]

    pass


## System

@digest(form='molsysmt.Structures')
def set_structure_id_to_system(item, structure_indices='all', value=None):

    if is_all(structure_indices):
        item.structure_id = value
    else:
        item.structure_id[structure_indices,:,:] = value[:,:,:]

    pass

@digest(form='molsysmt.Structures')
def set_time_to_system(item, structure_indices='all', value=None):

    if is_all(structure_indices):
        item.time = value
    else:
        item.time[structure_indices,:,:] = value[:,:,:]

    pass

@digest(form='molsysmt.Structures')
def set_box_to_system(item, structure_indices='all', value=None):

    if is_all(structure_indices):
        item.box = value
    else:
        item.box[structure_indices,:,:] = value[:,:,:]

    pass

@digest(form='molsysmt.Structures')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value)


