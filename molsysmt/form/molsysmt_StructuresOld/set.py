from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

###### Set

## Atom

@digest(form='molsysmt.StructuresOld')
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

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

@digest(form='molsysmt.StructuresOld')
def set_velocities_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        if is_all(structure_indices):
            item.velocities = value
            item.n_structures = value.shape[0]
            item.n_atoms = value.shape[1]
        else:
            item.velocities[structure_indices,:,:] = value[:,:,:]
    else:
        if is_all(structure_indices):
            item.velocities[:,indices,:] = value[:,:,:]
        else:
            item.velocities[np.ix_(structure_indices, indices)]=value[:,:,:]

    pass

@digest(form='molsysmt.StructuresOld')
def set_occupancy_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        if is_all(structure_indices):
            item.occupancy = value
        else:
            item.occupancy[structure_indices,:] = value[:,:]
    else:
        if is_all(structure_indices):
            item.occupancy[:,indices] = value[:,:]
        else:
            item.occupancy[np.ix_(structure_indices, indices)]=value[:,:]

    pass

@digest(form='molsysmt.StructuresOld')
def set_b_factor_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        if is_all(structure_indices):
            item.b_factor = value
        else:
            item.b_factor[structure_indices,:] = value[:,:]
    else:
        if is_all(structure_indices):
            item.b_factor[:,indices] = value[:,:]
        else:
            item.b_factor[np.ix_(structure_indices, indices)]=value[:,:]

    pass


## System

@digest(form='molsysmt.StructuresOld')
def set_structure_id_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    if is_all(structure_indices):
        item.structure_id = value
    else:
        item.structure_id[structure_indices,:,:] = value[:,:,:]

    pass

@digest(form='molsysmt.StructuresOld')
def set_time_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    if is_all(structure_indices):
        item.time = value
    else:
        item.time[structure_indices,:,:] = value[:,:,:]

    pass

@digest(form='molsysmt.StructuresOld')
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    if is_all(structure_indices):
        item.box = value
    else:
        item.box[structure_indices,:,:] = value[:,:,:]

    pass

@digest(form='molsysmt.StructuresOld')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, skip_digestion=True)


@digest(form='molsysmt.StructuresOld')
def set_velocities_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    return set_velocities_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, skip_digestion=True)

