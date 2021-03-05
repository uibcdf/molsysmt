from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from networkx import Graph as _networkx_Graph

form_name='networkx.Graph'

is_form={
    _networkx_Graph : form_name
}

info=["",""]
with_topology=True
with_coordinates=False
with_box=False
with_bonds=True
with_parameters=False

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.subgraph(atom_indices).copy()

def copy(item):

    return item.copy()

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate_frames(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append_frames(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

###### Get

## system

