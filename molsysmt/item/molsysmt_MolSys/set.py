from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_indices as _digest_indices
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices
from molsysmt._private.variables import is_all as _is_all
from molsysmt import puw as _puw
import numpy as _np

###### Set

## Atom

def set_atom_name_to_atom(item, indices='all', structure_indices='all', value=None):

    if check:

        _digest_item(item, 'molsysmt.MolSys')
        indices = _digest_indices(indices)
        structure_indices = _digest_structure_indices(structure_indices)

    from ..molsysmt_Topology import set_atom_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, structure_indices=structure_indices, value=value)

def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None):

    if check:

        _digest_item(item, 'molsysmt.MolSys')
        indices = _digest_indices(indices)
        structure_indices = _digest_structure_indices(structure_indices)

    value = _puw.standardize(value)

    if _is_all(indices):
        if item.structures.coordinates.shape[1]!=value.shape[1]:
            raise ValueError('New coordinates array has different number of atoms')

    if _is_all(structure_indices):
        if item.structures.coordinates.shape[0]!=value.shape[0]:
            raise ValueError('New coordinates array has different number of frames')

    if _is_all(indices):
        if _is_all(structure_indices):
            item.structures.coordinates[:,:,:] = value[:,:,:]
        else:
            item.structures.coordinates[structure_indices,:,:] = value[:,:,:]
    else:
        if _is_all(structure_indices):
            item.structures.coordinates[:,indices,:] = value[:,:,:]
        else:
            item.structures.coordinates[_np.ix_(structure_indices, indices)]=value[:,:,:]

## System

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    if check:

        _digest_item(item, 'molsysmt.MolSys')
        indices = _digest_indices(indices)
        structure_indices = _digest_structure_indices(structure_indices)

    item.trajectory.box = value

    pass

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    if check:

        _digest_item(item, 'molsysmt.MolSys')
        indices = _digest_indices(indices)
        structure_indices = _digest_structure_indices(structure_indices)

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value)

