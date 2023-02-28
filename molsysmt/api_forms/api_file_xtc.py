def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_xtc import to_molsysmt_Structures as file_xtc_to_molsysmt_Structures

    return file_xtc_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_XTCTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_xtc import to_mdtraj_XTCTrajectoryFile as file_xtc_to_mdtraj_XTCTrajectoryFile

    return file_xtc_to_mdtraj_XTCTrajectoryFile(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_xtc import to_mdtraj_Trajectory as file_xtc_to_mdtraj_Trajectory

    return file_xtc_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)
