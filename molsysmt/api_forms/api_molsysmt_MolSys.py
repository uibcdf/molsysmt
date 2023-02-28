import numpy as np

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    return molsysmt_MolSys_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_molsysmt_Structures as molsysmt_MolSys_to_molsysmt_Structures

    return molsysmt_MolSys_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_MolecularMechanics(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolSys import to_molsysmt_MolecularMechanics as molsysmt_MolSys_to_molsysmt_MolecularMechanics

    return molsysmt_MolSys_to_molsysmt_MolecularMechanics(item, atom_indices=atom_indices, structure_indices=structure_indices)


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
