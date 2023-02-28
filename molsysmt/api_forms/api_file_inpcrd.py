
def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_inpcrd import to_molsysmt_Structures as file_inpcrd_to_molsysmt_Structures

    return file_inpcrd_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                              structure_indices=structure_indices)


def to_mdtraj_AmberRestartFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_inpcrd import to_mdtraj_AmberRestartFile as file_inpcrd_to_mdtraj_AmberRestartFile

    return file_inpcrd_to_mdtraj_AmberRestartFile(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)


def to_openmm_AmberInpcrdFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_inpcrd import to_openmm_AmberInpcrdFile as file_inpcrd_to_openmm_AmberInpcrdFile

    return file_inpcrd_to_openmm_AmberInpcrdFile(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices)
