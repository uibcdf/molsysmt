def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_pytraj_Topology as pytraj_Trajectory_to_pytraj_Topology

    return pytraj_Trajectory_to_pytraj_Topology(item, atom_indices=atom_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_molsysmt_MolSys as pytraj_Trajectory_to_molsysmt_MolSys

    return pytraj_Trajectory_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_molsysmt_Topology as pytraj_Trajectory_to_molsysmt_Topology

    return pytraj_Trajectory_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_molsysmt_Structures as pytraj_Trajectory_to_molsysmt_Structures

    return pytraj_Trajectory_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_nglview_NGLWidget as pytraj_Trajectory_to_nglview_NGLWidget

    return pytraj_Trajectory_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)

