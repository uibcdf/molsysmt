from molsysmt._private.exceptions import *

from molsysmt.item.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder as is_form
from molsysmt.item.mmtf_MMTFDecoder.extract import extract
from molsysmt.item.mmtf_MMTFDecoder.add import add
from molsysmt.item.mmtf_MMTFDecoder.append_structures import append_structures
from molsysmt.item.mmtf_MMTFDecoder.get import *
from molsysmt.item.mmtf_MMTFDecoder.set import *

form_name='mmtf.MMTFDecoder'
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
    'bond_order' : True,

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


def to_file_mmtf(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.item.mmtf_MMTFDecoder import to_file_mmtf as mmtf_MMTFDecoder_to_file_mmtf

    tmp_item = mmtf_MMTFDecoder_to_file_mmtf(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.item.mmtf_MMTFDecoder import to_file_pdb as mmtf_MMTFDecoder_to_file_pdb

    tmp_item = mmtf_MMTFDecoder_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.mmtf_MMTFDecoder import to_molsysmt_Structures as mmtf_MMTFDecoder_to_molsysmt_Structures

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.mmtf_MMTFDecoder import to_mdtraj_Trajectory as mmtf_MMTFDecoder_to_mdtraj_Trajectory

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.mmtf_MMTFDecoder import to_string_aminoacids1 as mmtf_MMTFDecoder_to_string_aminoacids1
    from molsysmt.item.mmtf_MMTFDecoder import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)

    tmp_item = mmtf_MMTFDecoder_to_string_aminoacids1(item, group_indices=group_indices, check=False)

    return tmp_item

def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.mmtf_MMTFDecoder import to_string_aminoacids3 as mmtf_MMTFDecoder_to_string_aminoacids3
    from molsysmt.item.mmtf_MMTFDecoder import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)

    tmp_item = mmtf_MMTFDecoder_to_string_aminoacids3(item, group_indices=group_indices, check=False)

    return tmp_item

