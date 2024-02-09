from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

###### Set

## Atom

@digest(form='XYZ')
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        if is_all(structure_indices):
            item[:,:,:]=value[:,:,:]
        else:
            item[structure_indices,:,:] = value[:,:,:]
    else:
        if is_all(structure_indices):
            item[:,indices,:] = value[:,:,:]
        else:
            item[np.ix_(structure_indices, indices)]=value[:,:,:]

    pass

## System

@digest(form='XYZ')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value)


