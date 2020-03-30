from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from networkx import Graph as _networkx_Graph

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'networkx.Graph': form_name,
    _networkx_Graph : form_name
}

info=["",""]

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.subgraph(atom_indices).copy()

def duplicate(item):

    return item.copy()

