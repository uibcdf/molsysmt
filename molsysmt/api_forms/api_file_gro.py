def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_molsysmt_MolSys as file_gro_to_molsysmt_MolSys

    return file_gro_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_molsysmt_Topology as file_gro_to_molsysmt_Topology

    return file_gro_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_molsysmt_Structures as file_gro_to_molsysmt_Structures

    return file_gro_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                               structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_mdtraj_Trajectory as file_gro_to_mdtraj_Trajectory

    return file_gro_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
                                             structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_mdtraj_Topology as file_gro_to_mdtraj_Topology

    tmp_item = file_gro_to_mdtraj_Topology(item, atom_indices=atom_indices)

    return tmp_item


def to_mdtraj_GroTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_mdtraj_GroTrajectoryFile as file_gro_to_mdtraj_GroTrajectoryFile

    return file_gro_to_mdtraj_GroTrajectoryFile(item, atom_indices=atom_indices,
            structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_openmm_Topology as file_gro_to_openmm_Topology

    return file_gro_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_openmm_Modeller as file_gro_to_openmm_Modeller

    return file_gro_to_openmm_Modeller(item, atom_indices=atom_indices,
                                       structure_indices=structure_indices)


def to_openmm_GromacsGroFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_openmm_GromacsGroFile as file_gro_to_openmm_GromacsGroFile

    return file_gro_to_openmm_GromacsGroFile(item, atom_indices=atom_indices,
                                             structure_indices=structure_indices)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_nglview_NGLWidget as file_gro_to_nglview_NGLWidget

    return file_gro_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                         structure_indices=structure_indices)
