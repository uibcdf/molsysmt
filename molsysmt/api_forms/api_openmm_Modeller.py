from molsysmt._private.exceptions import *

from molsysmt.form.openmm_Modeller.is_openmm_Modeller import is_openmm_Modeller as is_form
from molsysmt.form.openmm_Modeller.extract import extract
from molsysmt.form.openmm_Modeller.add import add
from molsysmt.form.openmm_Modeller.merge import merge
from molsysmt.form.openmm_Modeller.append_structures import append_structures
from molsysmt.form.openmm_Modeller.concatenate_structures import concatenate_structures
from molsysmt.form.openmm_Modeller.get import *
from molsysmt.form.openmm_Modeller.set import *

form_name='openmm.Modeller'
form_type='class'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : True,
    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : True,
    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : True,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_mdtraj_Trajectory as openmm_Modeller_to_mdtraj_Trajectory

    tmp_item = openmm_Modeller_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_mdtraj_Topology as openmm_Modeller_to_mdtraj_Topology

    tmp_item = openmm_Modeller_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from molsysmt.form.openmm_Modeller import to_openmm_System as openmm_Modeller_to_openmm_System

    tmp_item = openmm_Modeller_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices,
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False, check=False)

    return tmp_item


def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):

    from molsysmt.form.openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    tmp_item = openmm_Modeller_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices,
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA',
                         check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_openmm_Topology as openmm_Modeller_to_openmm_Topology

    tmp_item = openmm_Modeller_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_pdbfixer_PDBFixer as openmm_Modeller_to_pdbfixer_PDBFixer

    tmp_item = openmm_Modeller_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_molsysmt_MolSys as openmm_Modeller_to_molsysmt_MolSys

    tmp_item = openmm_Modeller_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.openmm_Modeller import to_file_pdb as openmm_Modeller_to_file_pdb

    tmp_item = openmm_Modeller_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                           output_filename=output_filename, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'): 

    from .api_molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item, tmp_molecular_system  = to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system  = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', structure_indices='all', copy_if_all=True):

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

        from openmm.app import Modeller

        tmp_item = Modeller(item.topology, item.positions)

    else:

        from openmm.app import Modeller
        from molsysmt.api_forms.api_openmm_Topology import to_openmm_Topology as openmm_Topology_to_openmm_Topology

        tmp_topology = openmm_Topology_to_openmm_Topology(item.topology, atom_indices=atom_indices)
        tmp_positions = get_coordinates_from_atom(item, indices=atom_indices)
        tmp_item = Modeller(tmp_topology, tmp_positions)

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

def aux_get(item, indices='all', structure_indices='all'):

    from molsysmt.api_forms import forms

    method_name = sys._getframe(1).f_code.co_name

    if 'openmm.Topology' in forms:

        tmp_item, _ = to_openmm_Topology(item)
        module = importlib.import_module('molsysmt.api_forms.api_openmm_Topology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, structure_indices=structure_indices)

    else:

        raise NotImplementedError

    return output

## Atom

def get_atom_id_from_atom(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_atom_name_from_atom(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_atom_type_from_atom(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_component_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_molecule_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_entity_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_inner_bonds_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_coordinates_from_atom (item, indices='all', structure_indices='all'):

    unit = puw.get_unit(item.positions)
    coordinates = np.array(puw.get_value(item.positions))
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if structure_indices is not 'all':
        coordinates = coordinates[structure_indices,:,:]

    if indices is not 'all':
        coordinates = coordinates[:,indices,:]

    coordinates = coordinates * unit
    coordinates = puw.standardize(coordinates)

    return coordinates

def get_frame_from_atom (item, indices='all', structure_indices='all'):

    coordinates = get_coordinates_from_atom(item, indices=indices, structure_indices=structure_indices)
    box = get_box_from_system(item, structure_indices=structure_indices)
    step = get_step_from_system(item, structure_indices=structure_indices)
    time = get_time_from_system(item, structure_indices=structure_indices)

    return step, time, coordinates, box

## group

def get_group_id_from_group(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_group_name_from_group(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_group_type_from_group(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## component

def get_component_id_from_component (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_component_name_from_component (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_component_type_from_component (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## chain

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_chain_name_from_chain (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_chain_type_from_chain (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## entity

def get_entity_id_from_entity (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_entity_name_from_entity (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_entity_type_from_entity (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## system

def get_n_atoms_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_components_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_shape_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_time_from_system(item, indices='all', structure_indices='all'):

    return None

def get_step_from_system(item, indices='all', structure_indices='all'):

    return None

def get_n_structures_from_system(item, indices='all', structure_indices='all'):

    if structure_indices is 'all':

        return 1

    else:

        output = structure_indices.shape[0]
        if output>1:
            raise ValueError('The molecular system has a single frame')
        return output

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

###### Set

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

