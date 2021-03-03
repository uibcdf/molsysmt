from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from simtk.openmm import System as _openmm_System

form_name='openmm.System'

is_form={
    _openmm_System : form_name,
}

info=["",""]
with_topology=True
with_coordinates=False
with_box=True
with_bonds=True
with_parameters=True

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all',
                         integrator='Langevin', temperature='300.0 K', collisions_rate='1.0 1/ps',
                         integration_timestep='2.0 fs', platform='CUDA', constraint_tolerance=None):

    # constraint_tolerance 0.00001

    from molsysmt.multitool import convert, get
    from simtk.openmm import app, LangevinIntegrator
    from simtk.openmm import Platform

    topology= convert(topology_item, selection=atom_indices, to_form='openmm.Topology')
    positions = get(trajectory_item, target='atom', selection=atom_indices,
            frame_indices=frame_indices, coordinates=True)[0]

    if integrator=='Langevin':
        integrator_aux = LangevinIntegrator(temperature, collisions_rate, integration_timestep)
        if constraint_tolerance is not None:
            integrator_aux.setConstraintTolerance(constraint_tolerance)
    else:
        raise NotImplementedError('The integrator was not implemented yet in the conversion method.')

    platform_aux = Platform.getPlatformByName(platform)
    simulation_properties = {}
    if platform=='CUDA':
        simulation_properties['CudaPrecision']='mixed'

    tmp_item = app.Simulation(topology, item, integrator_aux, platform_aux, simulation_properties)
    tmp_item.context.setPositions(positions)
    tmp_item.context.setVelocitiesToTemperature(temperature)

    return tmp_item

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

##### Get

## Atom

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_atoms_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_atom_name_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_atom_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_atom_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_atom_type_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_groups_from_atom as _get
    _get(item.topology, indices=indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_group_from_atom as _get
    _get(item.topology, indices=indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_aminoacids_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_nucleotides_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_waters_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_ions_from_atom as _get
    _get(item.topology, indices=indices)

def get_mass_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_mass as _get
    return _get(item, indices=indices)

def get_net_mass_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_net_mass as _get
    return _get(item, indices=indices)

def get_charge_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_charge as _get
    return _get(item, indices=indices)
def get_net_charge_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_degrees_of_freedom_charge as _get
    return _get(item, indices=indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_atom as _get
    return _get(item, indices=indices)

def get_coordinates_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Positions import get_coordinates_from_atom as _get
    return _get(item, indices=indices)

## group

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_groups_from_group as _get
    return _get(item, indices=indices)

def get_group_name_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_name_from_group as _get
    return _get(item, indices=indices)

def get_group_index_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_index_from_group as _get
    return _get(item, indices=indices)

def get_group_id_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_id_from_group as _get
    return _get(item, indices=indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_index_from_group as _get
    return _get(item, indices=indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_id_from_group as _get
    return _get(item, indices=indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_group as _get
    return _get(item, indices=indices)

## chain

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_index_from_chain as _get
    return _get(item, indices=indices)

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_id_from_chain as _get
    return _get(item, indices=indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_chain as _get
    return _get(item, indices=indices)

## system

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_atoms_from_system as _get
    return _get(item, indices=indices)

def get_charge_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get_charge as _get
    return _get(item, indices=indices)

def get_net_charge_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get_degrees_of_freedom as _get
    return _get(item, indices=indices)

