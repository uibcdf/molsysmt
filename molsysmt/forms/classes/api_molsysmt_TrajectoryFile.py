from molsysmt._private_tools.exceptions import *
import numpy as np
from molsysmt.native.trajectory_file import TrajectoryFile as _molsysmt_TrajectoryFile
from molsysmt.molecular_system import molecular_system_components

form_name='molsysmt.TrajectoryFile'

is_form={
    _molsysmt_TrajectoryFile : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['coordinates', 'box']:
    has[ii]=True

def to_molsysmt_TrajectoryFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item.copy()
    else:
        raise NotImplementedError

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

## system

