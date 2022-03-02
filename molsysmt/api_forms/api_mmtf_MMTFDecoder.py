from molsysmt._private_tools.exceptions import *

from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder as is_form
from molsysmt.tools.mmtf_MMTFDecoder.extract import extract
from molsysmt.tools.mmtf_MMTFDecoder.add import add
from molsysmt.tools.mmtf_MMTFDecoder.merge import merge
from molsysmt.tools.mmtf_MMTFDecoder.append_frames import append_frames
from molsysmt.tools.mmtf_MMTFDecoder.concatenate_frames import concatenate_frames
from molsysmt.tools.mmtf_MMTFDecoder.get import *
from molsysmt.tools.mmtf_MMTFDecoder.set import *

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

    from molsysmt.tools.mmtf_MMTFDecoder import to_file_mmtf as mmtf_MMTFDecoder_to_file_mmtf

    tmp_item = mmtf_MMTFDecoder_to_file_mmtf(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=output_filename, check_form=False)

    return tmp_item

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.tools.mmtf_MMTFDecoder import to_file_pdb as mmtf_MMTFDecoder_to_file_pdb

    tmp_item = mmtf_MMTFDecoder_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=output_filename, check_form=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Trajectory as mmtf_MMTFDecoder_to_molsysmt_Trajectory

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.mmtf_MMTFDecoder import to_mdtraj_Trajectory as mmtf_MMTFDecoder_to_mdtraj_Trajectory

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

