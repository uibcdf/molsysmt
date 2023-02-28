def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_string_aminoacids3 as mdtraj_Trajectory_to_string_aminoacids3

    from molsysmt.form.mdtraj_Trajectory import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return mdtraj_Trajectory_to_string_aminoacids3(item, group_indices=group_indices)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_string_aminoacids1 as mdtraj_Trajectory_to_string_aminoacids1

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return mdtraj_Trajectory_to_string_aminoacids1(item, group_indices=group_indices)


def to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_biopython_Seq as mdtraj_Trajectory_to_biopython_Seq

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return mdtraj_Trajectory_to_biopython_Seq(item, group_indices=group_indices)


def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_biopython_Seq as mdtraj_Trajectory_to_biopython_SeqRecord

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return mdtraj_Trajectory_to_biopython_SeqRecord(item, group_indices=group_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_molsysmt_MolSys as mdtraj_Trajectory_to_molsysmt_MolSys

    return mdtraj_Trajectory_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_molsysmt_Topology as mdtraj_Trajectory_to_molsysmt_Topology

    return mdtraj_Trajectory_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_molsysmt_Structures as mdtraj_Trajectory_to_molsysmt_Structures

    return mdtraj_Trajectory_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_mdtraj_Topology as mdtraj_Trajectory_to_mdtraj_Topology

    return mdtraj_Trajectory_to_mdtraj_Topology(item, atom_indices=atom_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_openmm_Topology as mdtraj_Trajectory_to_openmm_Topology

    return mdtraj_Trajectory_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_openmm_Modeller as mdtraj_Trajectory_to_openmm_Modeller

    return mdtraj_Trajectory_to_openmm_Modeller(item, atom_indices=atom_indices,
                                                structure_indices=structure_indices)


def to_pytraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_pytraj_Trajectory as mdtraj_Trajectory_to_pytraj_Trajectory

    return mdtraj_Trajectory_to_pytraj_Trajectory(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)


def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_pytraj_Topology as mdtraj_Trajectory_to_pytraj_Topology

    return mdtraj_Trajectory_to_pytraj_Topology(item, atom_indices=atom_indices)


def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_parmed_Structures as mdtraj_Trajectory_to_parmed_Structures

    return mdtraj_Trajectory_to_parmed_Structures(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)


def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_pdbfixer_PDBFixer as mdtraj_Trajectory_to_pdbfixer_PDBFixer

    return mdtraj_Trajectory_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.mdtraj_Trajectory import to_file_pdb as mdtraj_Trajectory_to_file_pdb

    return mdtraj_Trajectory_to_file_pdb(item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, output_filename=output_filename)


def to_file_xtc(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.mdtraj_Trajectory import to_file_xtc as mdtraj_Trajectory_to_file_xtc

    return mdtraj_Trajectory_to_file_xtc(item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, output_filename=output_filename)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Trajectory import to_nglview_NGLWidget as mdtraj_Trajectory_to_nglview_NGLWidget

    return mdtraj_Trajectory_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)
