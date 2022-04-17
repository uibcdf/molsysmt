from molsysmt._private.exceptions import *

from molsysmt.form.string_pdb_id.is_string_pdb_id import is_string_pdb_id as is_form
from molsysmt.form.string_pdb_id.extract import extract
from molsysmt.form.string_pdb_id.add import add
from molsysmt.form.string_pdb_id.append_structures import append_structures
from molsysmt.form.string_pdb_id.get import *
from molsysmt.form.string_pdb_id.set import *

form_name='string:pdb_id'
form_type='string'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : False,
    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,
    'bond_order' : False,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : False,
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


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.string_pdb_id import to_file_pdb as string_pdb_id_to_file_pdb

    tmp_item = string_pdb_id_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filaname=output_filanme, check=False)

    return tmp_item

def to_file_mmtf(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.string_pdb_id import to_file_mmtf as string_pdb_id_to_file_mmtf

    tmp_item = string_pdb_id_to_file_mmtf(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filaname=output_filanme, check=False)

    return tmp_item

def to_file_msmpk(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.string_pdb_id import to_file_mmtf as string_pdb_id_to_file_msmpk

    tmp_item = string_pdb_id_to_file_msmpk(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filaname=output_filanme, check=False)

    return tmp_item

def to_file_fasta(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from sabueso.tools.string_pdb_id import to_file_fasta as string_pdb_id_to_file_fasta
    from sabueso.tools.file_fasta import extract as extract_file_fasta
    from sabueso.basic import get
    import numpy as np

    tmp_item = string_pdb_id_to_file_fasta(item, check=False)
    group_indices = get(molecular_system, target='atom', indices=atom_indices, group_index=True)
    group_indices = np.unique(group_indices)
    tmp_item = extract_file_fasta(tmp_item, group_indices=group_indices, output_filename=output_filename, copy_if_all=False)

    return tmp_item

def to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_mmtf_MMTFDecoder as string_pdb_id_to_mmtf_MMTFDecoder

    tmp_item = string_pdb_id_to_mmtf_MMTFDecoder(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_molsysmt_MolSys as string_pdb_id_to_molsysmt_MolSys

    tmp_item = string_pdb_id_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_molsysmt_Topology as string_pdb_id_to_molsysmt_Topology

    tmp_item = string_pdb_id_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_molsysmt_Structures as string_pdb_id_to_molsysmt_Structures

    tmp_item = string_pdb_id_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_mdtraj_Trajectory as string_pdb_id_to_mdtraj_Trajectory

    tmp_item = string_pdb_id_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_mdtraj_Topology as string_pdb_id_to_mdtraj_Topology

    tmp_item = string_pdb_id_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_parmed_Structure as string_pdb_id_to_parmed_Structure

    tmp_item = string_pdb_id_to_parmed_Structure(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_pdbfixer_PDBFixer as string_pdb_id_to_pdbfixer_PDBFixer

    tmp_item = string_pdb_id_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_openmm_Modeller as string_pdb_id_to_openmm_Modeller

    tmp_item = string_pdb_id_to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_openmm_Topology as string_pdb_id_to_openmm_Topology

    tmp_item = string_pdb_id_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_PDBFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_openmm_PDBFile as string_pdb_id_to_openmm_PDBFile

    tmp_item = string_pdb_id_to_openmm_PDBFile(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_mdanalysis_Universe as string_pdb_id_to_mdanalysis_Universe

    tmp_item = string_pdb_id_to_mdanalysis_Universe(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pytraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_pytraj_Trajectory as string_pdb_id_to_pytraj_Trajectory

    tmp_item = string_pdb_id_to_pytraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.string_pdb_id import to_nglview_NGLWidget as string_pdb_id_to_nglview_NGLWidget

    tmp_item = string_pdb_id_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

