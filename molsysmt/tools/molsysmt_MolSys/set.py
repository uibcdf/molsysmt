from molsysmt._private_tools.exceptions import *
from molsysmt import puw
import numpy as np

###### Set

## Atom

def set_atom_name_to_atom(item, indices='all', structure_indices='all', value=None, check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check=check)

    from .api_molsysmt_Topology import set_atom_name_to_atom as _set

    return _set(item.topology, indices=indices, structure_indices=structure_indices, value=value, check=True)

def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check=check)

    value = puw.standardize(value)

    if indices is 'all':
        if item.trajectory.coordinates.shape[1]!=value.shape[1]:
            raise ValueError('New coordinates array has different number of atoms')

    if structure_indices is 'all':
        if item.trajectory.coordinates.shape[0]!=value.shape[0]:
            raise ValueError('New coordinates array has different number of frames')

    if indices is 'all':
        if structure_indices is 'all':
            item.trajectory.coordinates[:,:,:] = value[:,:,:]
        else:
            item.trajectory.coordinates[structure_indices,:,:] = value[:,:,:]
    else:
        if structure_indices is 'all':
            item.trajectory.coordinates[:,indices,:] = value[:,:,:]
        else:
            item.trajectory.coordinates[np.ix_(structure_indices, indices)]=value[:,:,:]

## System

def set_box_to_system(item, indices='all', structure_indices='all', value=None, check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check=check)

    item.trajectory.box = value
    pass

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check=check)

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices, value=value)

