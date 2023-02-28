def to_mdtraj_DCDTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_dcd import to_mdtraj_DCDTrajectoryFile as file_dcd_to_mdtraj_DCDTrajectoryFile

    return file_dcd_to_mdtraj_DCDTrajectoryFile(item, atom_indices=atom_indices, structure_indices=structure_indices)

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_dcd import to_molsysmt_Structures as file_dcd_to_molsysmt_Structures

    return file_dcd_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_dcd import to_molsysmt_MolSys as file_dcd_to_molsysmt_MolSys

    return file_dcd_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


