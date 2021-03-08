from molsysmt._private_tools.exceptions import *
import numpy as np
from molsysmt.native.trajectory_file import TrajectoryFile as _molsysmt_TrajectoryFile

form_name='molsysmt.TrajectoryFile'

is_form={
    _molsysmt_TrajectoryFile : form_name,
}

info=["",""]
with_topology=False
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

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

## system


