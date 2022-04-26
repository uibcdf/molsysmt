from molsysmt._private.exceptions import *

from molsysmt.form.molsysmt_MolSys.is_molsysmt_MolSys import is_molsysmt_MolSys as is_form
from molsysmt.form.molsysmt_MolSys.extract import extract
from molsysmt.form.molsysmt_MolSys.add import add
from molsysmt.form.molsysmt_MolSys.append_structures import append_structures
from molsysmt.form.molsysmt_MolSys.get import *
from molsysmt.form.molsysmt_MolSys.set import *

import numpy as np

form_name='molsysmt.MolSys'
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
    'bonded_atoms' : True,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : True,
    'component_name' : True,
    'component_type' : True,

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
    'time' : True,
    'step' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_molsysmt_Structures as molsysmt_MolSys_to_molsysmt_Structures

    tmp_item = molsysmt_MolSys_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_XYZ(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_XYZ as molsysmt_MolSys_to_XYZ

    tmp_item = molsysmt_MolSys_to_XYZ(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_string_aminoacids3 as molsysmt_MolSys_to_string_aminoacids3
    from molsysmt.form.molsysmt_MolSys import get_group_index_from_atom as get_group_index_from_atom_molsysmt_MolSys

    group_indices = get_group_index_from_atom_molsysmt_MolSys(item, indices=atom_indices, check=False)
    group_indices = np.unique(group_indices)

    tmp_item = molsysmt_MolSys_to_string_aminoacids3(item, group_indices=group_indices, check=False)

    return tmp_item

def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_string_aminoacids1 as molsysmt_MolSys_to_string_aminoacids1
    from molsysmt.form.molsysmt_MolSys import get_group_index_from_atom as get_group_index_from_atom_molsysmt_MolSys

    group_indices = get_group_index_from_atom_molsysmt_MolSys(item, indices=atom_indices, check=False)
    group_indices = np.unique(group_indices)

    tmp_item = molsysmt_MolSys_to_string_aminoacids1(item, group_indices=group_indices, check=False)

    return tmp_item

def to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_biopython_Seq as molsysmt_MolSys_to_biopython_Seq
    from molsysmt.form.molsysmt_MolSys import get_group_index_from_atom as get_group_index_from_atom_molsysmt_MolSys

    group_indices = get_group_index_from_atom_molsysmt_MolSys(item, indices=atom_indices, check=False)
    group_indices = np.unique(group_indices)

    tmp_item = molsysmt_MolSys_to_biopython_Seq(item, group_indices=group_indices, check=False)

    return tmp_item

def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_biopython_SeqRecord as molsysmt_MolSys_to_biopython_SeqRecord
    from molsysmt.form.molsysmt_MolSys import get_group_index_from_atom as get_group_index_from_atom_molsysmt_MolSys

    group_indices = get_group_index_from_atom_molsysmt_MolSys(item, indices=atom_indices, check=False)
    group_indices = np.unique(group_indices)

    tmp_item = molsysmt_MolSys_to_biopython_SeqRecord(item, group_indices=group_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item = molsysmt_MolSys_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_mdtraj_Topology as molsysmt_MolSys_to_mdtraj_Topology

    tmp_item = molsysmt_MolSys_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_openmm_Modeller as molsysmt_MolSys_to_openmm_Modeller

    tmp_item = molsysmt_MolSys_to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_openmm_System as molsysmt_MolSys_to_openmm_System

    tmp_item = molsysmt_MolSys_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Context(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_openmm_Context as molsysmt_MolSys_to_openmm_Context

    tmp_item = molsysmt_MolSys_to_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_openmm_Simulation as molsysmt_MolSys_to_openmm_Simulation

    tmp_item = molsysmt_MolSys_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.molsysmt_MolSys import to_file_pdb as molsysmt_MolSys_to_file_pdb

    tmp_item = molsysmt_MolSys_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item

def to_file_msmpk(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk

    tmp_item = molsysmt_MolSys_to_file_msmpk(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item

def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text

    tmp_item = molsysmt_MolSys_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_pdbfixer_PDBFixer as molsysmt_MolSys_to_pdbfixer_PDBFixer

    tmp_item = molsysmt_MolSys_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_pytraj_Topology as molsysmt_MolSys_to_pytraj_Topology

    tmp_item = molsysmt_MolSys_to_pytraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

