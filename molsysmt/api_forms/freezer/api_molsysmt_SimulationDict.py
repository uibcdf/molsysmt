import numpy as np
from molsysmt._private_tools.exceptions import *
from molsysmt import puw
from molsysmt.native.molecular_system import molecular_system_components

form_name='molsysmt.SimulationDict'
from_type='class'

is_form={
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['thermo_state','simulation']:
    has[ii]=True

def this_dict_is_SimulationDict(item):

    from molsysmt.native.simulation_dict import is_simulation_dict

    return is_simulation_dict(item)

def to_molsysmt_Simulation(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.simulation import Simulation as molsysmt_Simulation

    tmp_item = molsysmt_Simulation(**item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_molsysmt_SimulationDict(item, molecular_system=None, atom_indices='all', structure_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (structure_indices is 'all'):
        if copy_if_all:
            tmp_item = extract(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def extract(item, atom_indices='all', structure_indices='all'):

    if (atom_indices is 'all') and (structure_indices is 'all'):
        tmp_item = item.copy()
    else:
        raise NotImplementedError()

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

