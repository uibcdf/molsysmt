from molsysmt._private_tools.exceptions import *

from molsysmt.tools.biopython_Seq.is_biopython_Seq import is_biopython_Seq as is_form
from molsysmt.tools.biopython_Seq.extract import extract
from molsysmt.tools.biopython_Seq.add import add
from molsysmt.tools.biopython_Seq.merge import merge
from molsysmt.tools.biopython_Seq.append_structures import append_structures
from molsysmt.tools.biopython_Seq.concatenate_structures import concatenate_structures
from molsysmt.tools.biopython_Seq.get import *
from molsysmt.tools.biopython_Seq.set import *

form_name='biopython.Seq'
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

    'entity_index' : True,
    'entity_id' : True,
    'entity_name' : True,
    'entity_type' : True,

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


def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all',
                           id=None, name=None, description=None):

    from molsysmt.tools.biopython_Seq import to_biopython_SeqRecord as biopython_Seq_to_biopython_SeqRecord

    tmp_item = biopython_Seq_to_biopython_SeqRecord(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_fasta(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.tools.biopython_Seq import to_file_fasta as biopython_Seq_to_file_fasta

    tmp_item = biopython_Seq_to_file_fasta(item, atom_indices=atom_indices,
                                           structure_indices=structure_indices,
                                           output_filename=output_filename, check=False)

    return tmp_item

###### Get

## atom

def get_atom_id_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_atom_name_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_atom_type_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_component_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_entity_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_inner_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_inner_bonds_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_frame_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

## group

def get_group_id_from_group(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_group_name_from_group(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_group_type_from_group(item, indices='all', structure_indices='all'):

    raise NotImplementedError

## component

def get_component_id_from_component (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_component_name_from_component (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_component_type_from_component (item, indices='all', structure_indices='all'):

    raise NotImplementedError

## molecule

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all'):

    raise NotImplementedError

## chain

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', structure_indices='all'):

    raise NotImplementedError

## entity

def get_entity_id_from_entity (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_entity_name_from_entity (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_entity_type_from_entity (item, indices='all', structure_indices='all'):

    raise NotImplementedError

## system

def get_n_atoms_from_system(item, indices='all', structure_indices='all'):

    return None

def get_n_groups_from_system(item, indices='all', structure_indices='all'):

    return len(item)

def get_n_components_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_chains_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_entities_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_coordinates_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_shape_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_volume_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_step_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_structures_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_bond_type_from_bond(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_atom_index_from_bond(item, indices='all', structure_indices='all'):

    raise NotImplementedError

###### Set

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

