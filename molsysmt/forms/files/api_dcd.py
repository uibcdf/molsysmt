from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='dcd'

is_form = {
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

    raise NotImplementedError

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

## system

