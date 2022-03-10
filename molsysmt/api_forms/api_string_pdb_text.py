from molsysmt._private_tools.exceptions import *

from molsysmt.tools.string_pdb_text.is_string_pdb_text import is_string_pdb_text as is_form
from molsysmt.tools.string_pdb_text.extract import extract
from molsysmt.tools.string_pdb_text.add import add
from molsysmt.tools.string_pdb_text.merge import merge
from molsysmt.tools.string_pdb_text.append_structures import append_structures
from molsysmt.tools.string_pdb_text.concatenate_structures import concatenate_structures
from molsysmt.tools.string_pdb_text.get import *
from molsysmt.tools.string_pdb_text.set import *

form_name='string:pdb_text'
from_type='string'
info = ["Protein Data Bank file format","https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

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

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_molsysmt_MolSys as string_pdb_text_to_molsysmt_MolSys

    tmp_item = string_pdb_text_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_molsysmt_Topology as string_pdb_text_to_molsysmt_Topology

    tmp_item = string_pdb_text_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_molsysmt_Structures as string_pdb_text_to_molsysmt_Structures

    tmp_item = string_pdb_text_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_mdtraj_Topology as string_pdb_text_to_mdtraj_Topology

    tmp_item = string_pdb_text_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_mdtraj_Trajectory as string_pdb_text_to_mdtraj_Trajectory

    tmp_item = string_pdb_text_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_openmm_Topology as string_pdb_text_to_openmm_Topology

    tmp_item = string_pdb_text_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_openmm_Topology as string_pdb_text_to_openmm_Topology

    tmp_item = string_pdb_text_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_System(item, molecular_system=None, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from molsysmt.tools.string_pdb_text import to_openmm_System as string_pdb_text_to_openmm_System

    tmp_item = string_pdb_text_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):

    from molsysmt.tools.string_pdb_text import to_openmm_System as string_pdb_text_to_openmm_System

    tmp_item = string_pdb_text_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_PDBFile(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_openmm_PDBFile as string_pdb_text_to_openmm_PDBFile

    tmp_item = string_pdb_text_to_openmm_PDBFile(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_pdbfixer_PDBFixer as string_pdb_text_to_pdbfixer_PDBFixer

    tmp_item = string_pdb_text_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_pdb_text import to_nglview_NGLWidget as string_pdb_text_to_nglview_NGLWidget

    tmp_item = string_pdb_text_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.tools.string_pdb_text import to_file_pdb as string_pdb_text_to_file_pdb

    tmp_item = string_pdb_text_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=output_filename, check=False)

    return tmp_item

###### Get


def aux_get_coors(item, indices='all', structure_indices='all'):

    from molsysmt.api_forms import forms

    method_name = sys._getframe(1).f_code.co_name

    if 'openmm.PDBFile' in forms:

        tmp_item, _ = to_openmm_PDBFile(item)
        module = importlib.import_module('molsysmt.api_forms.api_openmm_PDBFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, structure_indices=structure_indices)

    elif 'pdbfixer.PDBFixer' in forms:

        tmp_item, _ = to_pdbfixer_PDBFixer(item)
        module = importlib.import_module('molsysmt.api_forms.api_pdbfixer_PDBFixer')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, structure_indices=structure_indices)

    elif 'mdtraj.PDBTrajectoryFile' in forms:

        tmp_item = to_mdtraj_PDBTrajectoryFile(item)
        module = importlib.import_module('molsysmt.api_forms.api_mdtraj_PDBTrajectoryFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, structure_indices=structure_indices)

    else:

        raise NotImplementedError

    return output


## atom

def get_atom_index_from_atom(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_atom_id_from_atom(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_atom_name_from_atom(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_atom_type_from_atom(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_component_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_molecule_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_entity_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_n_inner_bonds_from_atom (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_frame_from_atom(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

## group

def get_group_id_from_group(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_group_name_from_group(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_group_type_from_group(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

## component

def get_component_id_from_component (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_component_name_from_component (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_component_type_from_component (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

## chain

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_chain_name_from_chain (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_chain_type_from_chain (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

## entity

def get_entity_id_from_entity (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_entity_name_from_entity (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_entity_type_from_entity (item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

## system

def get_n_atoms_from_system(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_system(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_n_components_from_system(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_system(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_system(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_system(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_system(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_coordinates_from_system(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_box_from_system(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_box_shape_from_system(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_box_volume_from_system(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_time_from_system(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_step_from_system(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_n_structures_from_system(item, indices='all', structure_indices='all'):

    return aux_get_coors(item, indices=indices, structure_indices=structure_indices)

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_bond_type_from_bond(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_bond(item, indices='all', structure_indices='all'):

    return aux_get_top(item, indices=indices, structure_indices=structure_indices)

###### Set

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

