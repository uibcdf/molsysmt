from molsysmt._private_tools.exceptions import *
from molsysmt.api_forms.common_gets import *
import numpy as np
from molsysmt import puw
from molsysmt.native.molecular_system import molecular_system_components

form_name='openmm.System'
from_type='class'

is_form={
    'openmm.System' : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['box', 'ff_parameters', 'mm_parameters']:
    has[ii]=True

def to_openmm_Context(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import convert, get
    from openmm import Context

    positions = get(molecular_system, target='atom', selection=atom_indices, structure_indices=structure_indices, coordinates=True)
    positions = puw.convert(positions[0], to_unit='nm', to_form='openmm.unit')
    simulation = convert(molecular_system, to_form='molsysmt.Simulation')

    integrator = simulation.to_openmm_Integrator()
    platform = simulation.to_openmm_Platform()

    properties = simulation.get_openmm_Context_parameters()

    tmp_item = Context(item, integrator, platform, properties)
    tmp_item.setPositions(positions)
    if simulation.initial_velocities_to_temperature:
        temperature = puw.convert(simulation.temperature, to_unit='K', to_form='openmm.unit')
        tmp_item.setVelocitiesToTemperature(temperature)

    if molecular_system is not None:
        tmp_molecular_simulation=molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_simulation=None

    return tmp_item, tmp_molecular_simulation

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import convert, get
    from openmm.app import Simulation

    topology = convert(molecular_system, to_form='openmm.Topology', selection=atom_indices)
    positions = get(molecular_system, target='atom', selection=atom_indices, structure_indices=structure_indices, coordinates=True)
    positions = puw.convert(positions[0], to_unit='nm', to_form='openmm.unit')
    simulation = convert(molecular_system, to_form='molsysmt.Simulation')

    integrator = simulation.to_openmm_Integrator()
    platform = simulation.to_openmm_Platform()

    properties = simulation.get_openmm_Simulation_parameters()

    tmp_item = Simulation(topology, item, integrator, platform, properties)
    tmp_item.context.setPositions(positions)
    if simulation.initial_velocities_to_temperature:
        temperature = puw.convert(simulation.temperature, to_unit='K', to_form='openmm.unit')
        tmp_item.context.setVelocitiesToTemperature(temperature)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_System(item, molecular_system=None, atom_indices='all', structure_indices='all', copy_if_all=True):

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
        tmp_item = item.__copy__()
    else:
        raise NotImplementedError

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

##### Get

## Atom

def get_n_atoms_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_n_atoms_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_atom_name_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_atom_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_atom_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_atom_type_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_groups_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_n_groups_from_atom as _get
    _get(item.topology, indices=indices)

def get_group_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_n_group_from_atom as _get
    _get(item.topology, indices=indices)

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_group_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_group_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_group_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_chain_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_chain_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_chain_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_aminoacids_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_n_aminoacids_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_nucleotides_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_n_nucleotides_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_waters_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_n_waters_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_ions_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_n_ions_from_atom as _get
    _get(item.topology, indices=indices)

def get_mass_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt import get_mass as _get
    return _get(item, indices=indices)

def get_net_mass_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt import get_net_mass as _get
    return _get(item, indices=indices)

def get_charge_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt import get_charge as _get
    return _get(item, indices=indices)
def get_net_charge_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt import get_degrees_of_freedom_charge as _get
    return _get(item, indices=indices)

def get_molecule_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_atom as _get
    return _get(item, indices=indices)

def get_coordinates_from_atom (item, indices='all', structure_indices='all'):

    from .api_openmm_Positions import get_coordinates_from_atom as _get
    return _get(item, indices=indices)

## group

def get_n_groups_from_group (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_n_groups_from_group as _get
    return _get(item, indices=indices)

def get_group_name_from_group (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_group_name_from_group as _get
    return _get(item, indices=indices)

def get_group_index_from_group (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_group_index_from_group as _get
    return _get(item, indices=indices)

def get_group_id_from_group (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_group_id_from_group as _get
    return _get(item, indices=indices)

def get_chain_index_from_group (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_chain_index_from_group as _get
    return _get(item, indices=indices)

def get_chain_id_from_group (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_chain_id_from_group as _get
    return _get(item, indices=indices)

def get_molecule_type_from_group (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_group as _get
    return _get(item, indices=indices)

## chain

def get_chain_index_from_chain (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_chain_index_from_chain as _get
    return _get(item, indices=indices)

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_chain_id_from_chain as _get
    return _get(item, indices=indices)

def get_molecule_type_from_chain (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_chain as _get
    return _get(item, indices=indices)

## system

def get_n_atoms_from_system (item, indices='all', structure_indices='all'):

    from .api_openmm_Topology import get_n_atoms_from_system as _get
    return _get(item, indices=indices)

def get_charge_from_system (item, indices='all', structure_indices='all'):

    from molsysmt import get_charge as _get
    return _get(item, indices=indices)

def get_net_charge_from_system (item, indices='all', structure_indices='all'):

    from molsysmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_system (item, indices='all', structure_indices='all'):

    from molsysmt import get_degrees_of_freedom as _get
    return _get(item, indices=indices)

