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

form_elements = {
    'atoms' : True,
    'bonds' : True,
    'groups' : True,
    'component' : False,
    'molecule' : True,
    'chain' : True,
    'entity' : True,
        }

form_attributes = {

    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,

    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

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


def to_file_mmtf(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from mmtf.api.default_api import write_mmtf, MMTFDecoder

    tmp_item, tmp_molecular_system = to_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    write_mmtf(output_filename, tmp_item, MMTFDecoder.pass_data_on)
    tmp_item = output_filename
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.api_molsysmt_MolSys import to_file_pdb as molsysmt_MolSys_to_file_pdb

    tmp_item, tmp_molecular_system = to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_file_pdb(tmp_item, molecular_system=tmp_molecular_system, output_filename=output_filename)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys import from_mmtf_MMTFDecoder as molsysmt_MolSys_from_mmtf_MMTFDecoder

    tmp_item, tmp_molecular_system = molsysmt_MolSys_from_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology import from_mmtf_MMTFDecoder as molsysmt_Topology_from_mmtf_MMTFDecoder

    tmp_item, tmp_molecular_system = molsysmt_Topology_from_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory import from_mmtf_MMTFDecoder as molsysmt_Trajectory_from_mmtf_MMTFDecoder

    tmp_item, tmp_molecular_system = molsysmt_Trajectory_from_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_molsysmt_MolSys import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item, tmp_molecular_system = to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_mdtraj_Trajectory(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system


