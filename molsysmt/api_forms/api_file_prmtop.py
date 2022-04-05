from molsysmt._private.exceptions import *

from molsysmt.form.file_prmtop.is_file_prmtop import is_file_prmtop as is_form
from molsysmt.form.file_prmtop.extract import extract
from molsysmt.form.file_prmtop.add import add
from molsysmt.form.file_prmtop.merge import merge
from molsysmt.form.file_prmtop.append_structures import append_structures
from molsysmt.form.file_prmtop.concatenate_structures import concatenate_structures
from molsysmt.form.file_prmtop.get import *
from molsysmt.form.file_prmtop.set import *

form_name='file:prmtop'
form_type='file'
form_info = ["AMBER parameter/topology file format","https://ambermd.org/FileFormats.php#topology"]

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

    'coordinates' : False,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield_parameters' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.file_prmtop import to_file_pdb as file_prmtop_to_file_pdb
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True, check=False)
    tmp_item = file_prmtop_to_file_pdb(item, atom_indices=atom_indices, coordinates=coordinates, output_filename=output_filename, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_mdtraj_Topology as file_prmtop_to_mdtraj_Topology

    tmp_item = file_prmtop_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_molsysmt_MolSys as file_prmtop_to_molsysmt_MolSys
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True, check=False)
    tmp_item  = file_prmtop_to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_molsysmt_Topology as file_prmtop_to_molsysmt_Topology

    tmp_item  = file_prmtop_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_nglview_NGLWidget as file_prmtop_to_nglview_NGLWidget
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True, check=False)
    tmp_item  = file_prmtop_to_nglview_NGLWidget(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

def to_openmm_AmberPrmtopFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_openmm_AmberPrmtopFile as file_prmtop_to_openmm_AmberPrmtopFile

    tmp_item  = file_prmtop_to_nglview_NGLWidget(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_openmm_Topology as file_prmtop_to_openmm_Topology

    tmp_item  = file_prmtop_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_openmm_Modeller as file_prmtop_to_openmm_Modeller
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True, check=False)
    tmp_item = file_prmtop_to_openmm_Modeller(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

###### Get

def aux_get(item, indices='all', structure_indices='all'):

    from molsysmt.api_forms import forms

    method_name = sys._getframe(1).f_code.co_name

    if 'openmm.AmberPrmtopFile' in forms:

        tmp_item, _ = to_openmm_AmberPrmtopFile(item)
        module = importlib.import_module('molsysmt.api_forms.api_openmm_AmberPrmtopFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, structure_indices=structure_indices)

    elif 'mdtraj.Topology' in forms:

        tmp_item, _ = to_mdtraj_Topology(item)
        module = importlib.import_module('molsysmt.api_forms.api_mdtraj_Topology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, structure_indices=structure_indices)

    else:

        raise NotImplementedError

    return output

# Atoms

def get_atom_index_from_atom(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

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

def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_frame_from_atom(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

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

# System

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

def get_coordinates_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_box_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_shape_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_volume_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_time_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError

def get_step_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError

def get_n_structures_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_bond_type_from_bond(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_bond(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

###### Set

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

