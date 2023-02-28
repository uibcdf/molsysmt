def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_XTCTrajectoryFile import \
        to_molsysmt_Structures as mdtraj_XTCTrajectoryFile_to_molsysmt_Structures

    return mdtraj_XTCTrajectoryFile_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                           structure_indices=structure_indices,
                                                           )
