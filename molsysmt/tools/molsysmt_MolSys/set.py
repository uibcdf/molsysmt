from molsysmt._private_tools.exceptions import *
from molsysmt import puw
import numpy as np

###### Set

## Atom

def set_atom_name_to_atom(item, indices='all', frame_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check_form=check_form)

    from .api_molsysmt_Topology import set_atom_name_to_atom as _set

    return _set(item.topology, indices=indices, frame_indices=frame_indices, value=value, check_form=True)

def set_coordinates_to_atom(item, indices='all', frame_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check_form=check_form)

    value = puw.standardize(value)

    if indices is 'all':
        if item.trajectory.coordinates.shape[1]!=value.shape[1]:
            raise ValueError('New coordinates array has different number of atoms')

    if frame_indices is 'all':
        if item.trajectory.coordinates.shape[0]!=value.shape[0]:
            raise ValueError('New coordinates array has different number of frames')

    if indices is 'all':
        if frame_indices is 'all':
            item.trajectory.coordinates[:,:,:] = value[:,:,:]
        else:
            item.trajectory.coordinates[frame_indices,:,:] = value[:,:,:]
    else:
        if frame_indices is 'all':
            item.trajectory.coordinates[:,indices,:] = value[:,:,:]
        else:
            item.trajectory.coordinates[np.ix_(frame_indices, indices)]=value[:,:,:]

## System

def set_box_to_system(item, indices='all', frame_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check_form=check_form)

    item.trajectory.box = value
    pass

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check_form=check_form)

    return set_coordinates_to_atom(item, indices='all', frame_indices=frame_indices, value=value)

