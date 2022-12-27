from molsysmt.form.molsysmt_MolSys.is_molsysmt_MolSys import is_molsysmt_MolSys as is_form
from molsysmt.form.molsysmt_MolSys.extract import extract
from molsysmt.form.molsysmt_MolSys.add import add
from molsysmt.form.molsysmt_MolSys.append_structures import append_structures
from molsysmt.form.molsysmt_MolSys.get import *
from molsysmt.form.molsysmt_MolSys.set import *
from molsysmt.form.molsysmt_MolSys.iterators import StructuresIterator, TopologyIterator
import numpy as np
from .form_attributes import form_attributes

form_name = 'molsysmt.MolSys'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['bonded_atoms'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['component_id'] = True
form_attributes['component_name'] = True
form_attributes['component_type'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['entity_index'] = True
form_attributes['entity_id'] = True
form_attributes['entity_name'] = True
form_attributes['entity_type'] = True
form_attributes['coordinates'] = True
form_attributes['box'] = True
form_attributes['time'] = True
form_attributes['structure_id'] = True
form_attributes['occupancy'] = True
form_attributes['alternate_location'] = True
form_attributes['b_factor'] = True
form_attributes['formal_charge'] = True
form_attributes['partial_charge'] = True


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    return molsysmt_MolSys_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_molsysmt_Structures as molsysmt_MolSys_to_molsysmt_Structures

    return molsysmt_MolSys_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_XYZ(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_XYZ as molsysmt_MolSys_to_XYZ

    return molsysmt_MolSys_to_XYZ(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_string_aminoacids3 as molsysmt_MolSys_to_string_aminoacids3
    from molsysmt.form.molsysmt_MolSys import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return molsysmt_MolSys_to_string_aminoacids3(item, group_indices=group_indices)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_string_aminoacids1 as molsysmt_MolSys_to_string_aminoacids1
    from molsysmt.form.molsysmt_MolSys import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return molsysmt_MolSys_to_string_aminoacids1(item, group_indices=group_indices)


def to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_biopython_Seq as molsysmt_MolSys_to_biopython_Seq
    from molsysmt.form.molsysmt_MolSys import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return molsysmt_MolSys_to_biopython_Seq(item, group_indices=group_indices)


def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_biopython_SeqRecord as molsysmt_MolSys_to_biopython_SeqRecord

    from molsysmt.form.molsysmt_MolSys import get_group_index_from_atom as get_group_index_from_atom_molsysmt_MolSys

    group_indices = get_group_index_from_atom_molsysmt_MolSys(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return molsysmt_MolSys_to_biopython_SeqRecord(item, group_indices=group_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    return molsysmt_MolSys_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_mdtraj_Topology as molsysmt_MolSys_to_mdtraj_Topology

    return molsysmt_MolSys_to_mdtraj_Topology(item, atom_indices=atom_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology

    return molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_openmm_Modeller as molsysmt_MolSys_to_openmm_Modeller

    return molsysmt_MolSys_to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_openmm_System as molsysmt_MolSys_to_openmm_System

    return molsysmt_MolSys_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Context(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_openmm_Context as molsysmt_MolSys_to_openmm_Context

    return molsysmt_MolSys_to_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_openmm_Simulation as molsysmt_MolSys_to_openmm_Simulation

    return molsysmt_MolSys_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.molsysmt_MolSys import to_file_pdb as molsysmt_MolSys_to_file_pdb

    return molsysmt_MolSys_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                       output_filename=output_filename)


def to_file_msmpk(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk

    return molsysmt_MolSys_to_file_msmpk(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                         output_filename=output_filename)


def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text

    return molsysmt_MolSys_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_pdbfixer_PDBFixer as molsysmt_MolSys_to_pdbfixer_PDBFixer

    return molsysmt_MolSys_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_pytraj_Topology as molsysmt_MolSys_to_pytraj_Topology

    return molsysmt_MolSys_to_pytraj_Topology(item, atom_indices=atom_indices)


def to_pytraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_pytraj_Trajectory as molsysmt_MolSys_to_pytraj_Trajectory

    return molsysmt_MolSys_to_pytraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    return molsysmt_MolSys_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices)
