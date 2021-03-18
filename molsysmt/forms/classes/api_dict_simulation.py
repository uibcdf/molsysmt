import numpy as np
from molsysmt._private_tools.exceptions import *
import pyunitwizard as puw
from molsysmt.molecular_system import molecular_system_components

form_name='SimulationDict'

is_form={
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['thermo_state','simulation']:
    has[ii]=True

def this_dict_is_SimulationDict(item):

    from molsysmt._private_tools.simulation import is_simulation_dict

    return is_simulation_dict(item)

def to_molsysmt_Simulation(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.simulation import Simulation as molsysmt_Simulation

    tmp_item = molsysmt_Simulation(**item)

    return tmp_item

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

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
