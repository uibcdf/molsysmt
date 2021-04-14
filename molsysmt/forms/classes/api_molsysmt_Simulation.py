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

    return tmp_item

def to_molsysmt_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item.copy()
    else:
        raise NotWithThisFormError()

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotWithThisFormError()


