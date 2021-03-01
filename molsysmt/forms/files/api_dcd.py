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

