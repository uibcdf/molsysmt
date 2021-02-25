from molsysmt._private_tools.exceptions import *
import numpy as np
from molsysmt.native.trajectory_file import TrajectoryFile as _molsysmt_TrajectoryFile

form_name='molsysmt.TrajectoryFile'

is_form={
    _molsysmt_TrajectoryFile : form_name,
}

info=["",""]
with_topology=False
with_trajectory=True
with_coordinates=True
with_box=True
with_bonds=False
with_parameters=False

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    return item.copy()

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

