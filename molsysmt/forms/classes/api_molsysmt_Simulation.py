from molsysmt._private_tools.exceptions import *
from molsysmt.native.simulation import Simulation as _molsysmt_Simulation
from molsysmt.molecular_system import molecular_system_components

form_name='molsysmt.Simulation'

is_form={
    _molsysmt_Simulation : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['thermo_state', 'simulation']:
    has[ii]=True

def to_SimulationDict(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    tmp_item = item.to_dict()
    tmp_molecular_system = molecular_system

    return tmp_item, tmp_molecular_system

def to_molsysmt_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        tmp_item = item.copy()
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        raise NotWithThisFormError()

    return tmp_item, tmp_molecular_system

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotWithThisFormError()


