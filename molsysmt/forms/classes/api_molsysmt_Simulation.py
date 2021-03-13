from molsysmt._private_tools.exceptions import *
from molsysmt.native.simulation import Simulation as _molsysmt_Simulation

form_name='molsysmt.Simulation'

is_form={
    _molsysmt_Simulation : form_name,
}

info=["",""]
with_topology=False
with_coordinates=False
with_box=False
with_bonds=False
with_parameters=False
with_simulation=True

def extract(item, atom_indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def copy(item):

    return item.copy()

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotWithThisFormError()

###### Get

## system

