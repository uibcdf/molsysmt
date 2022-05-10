from molsysmt._private.exceptions import *

from molsysmt.item.pdbfixer_PDBFixer.is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer as is_form
from molsysmt.item.pdbfixer_PDBFixer.extract import extract
from molsysmt.item.pdbfixer_PDBFixer.add import add
from molsysmt.item.pdbfixer_PDBFixer.append_structures import append_structures
from molsysmt.item.pdbfixer_PDBFixer.get import *
from molsysmt.item.pdbfixer_PDBFixer.set import *

form_name='pdbfixer.PDBFixer'
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

def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_string_aminoacids3 as pdbfixer_PDBFixer_to_string_aminoacids3

    tmp_item = pdbfixer_PDBFixer_to_string_aminoacids3(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_string_aminoacids1 as pdbfixer_PDBFixer_to_string_aminoacids1

    tmp_item = pdbfixer_PDBFixer_to_string_aminoacids1(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_biopython_Seq as pdbfixer_PDBFixer_to_biopython_Seq

    tmp_item = pdbfixer_PDBFixer_to_biopython_Seq(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_biopython_Seq as pdbfixer_PDBFixer_to_biopython_Seq

    tmp_item = pdbfixer_PDBFixer_to_biopython_SeqRecord(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_mdtraj_Topology as pdbfixer_PDBFixer_to_mdtraj_Topology

    tmp_item = pdbfixer_PDBFixer_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_mdtraj_Trajectory as pdbfixer_PDBFixer_to_mdtraj_Trajectory

    tmp_item = pdbfixer_PDBFixer_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_openmm_Modeller as pdbfixer_PDBFixer_to_openmm_Modeller

    tmp_item = pdbfixer_PDBFixer_to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_openmm_Topology as pdbfixer_PDBFixer_to_openmm_Topology

    tmp_item = pdbfixer_PDBFixer_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_molsysmt_Topology as pdbfixer_PDBFixer_to_molsysmt_Topology

    tmp_item = pdbfixer_PDBFixer_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_molsysmt_MolSys as pdbfixer_PDBFixer_to_molsysmt_MolSys

    tmp_item = pdbfixer_PDBFixer_to_molsysmt_MolSys(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_parmed_Structure as pdbfixer_PDBFixer_to_parmed_Structure

    tmp_item = pdbfixer_PDBFixer_to_parmed_Structure(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.item.pdbfixer_PDBFixer import to_file_pdb as pdbfixer_PDBFixer_to_file_pdb

    tmp_item = pdbfixer_PDBFixer_to_file_pdb(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.item.pdbfixer_PDBFixer import to_nglview_NLGWidget as pdbfixer_PDBFixer_to_nglview_NGLWidget

    tmp_item = pdbfixer_PDBFixer_to_nglview_NGLWidget(item, atom_indices=atom_indices, check=False)

    return tmp_item

