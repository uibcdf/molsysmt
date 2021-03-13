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
with_simulation=False

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.subgraph(atom_indices).copy()

def copy(item):

    return item.copy()

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

## system


