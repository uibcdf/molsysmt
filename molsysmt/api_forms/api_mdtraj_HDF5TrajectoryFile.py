def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_mdtraj_Topology as mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology

    return mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology(item, atom_indices=atom_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_openmm_Topology as mdtraj_HDF5TrajectoryFile_to_openmm_Topology

    return mdtraj_HDF5TrajectoryFile_to_openmm_Topology(item, atom_indices=atom_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_molsysmt_MolSys as mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys

    return mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                        structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_molsysmt_Topology as mdtraj_HDF5TrajectoryFile_to_molsysmt_Topology

    return mdtraj_HDF5TrajectoryFile_to_molsysmt_Topology(item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_molsysmt_Structures as mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures

    return mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                            structure_indices=structure_indices)
