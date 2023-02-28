def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_GromacsGroFile import to_openmm_Topology as openmm_GromacsGroFile_to_openmm_Topology

    return openmm_GromacsGroFile_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_GromacsGroFile import to_openmm_Modeller as openmm_GromacsGroFile_to_openmm_Modeller

    return openmm_GromacsGroFile_to_openmm_Modeller(item, atom_indices=atom_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_GromacsGroFile import to_molsysmt_MolSys as openmm_GromacsGroFile_to_molsysmt_MolSys

    return openmm_GromacsGroFile_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_GromacsGroFile import to_molsysmt_Topology as openmm_GromacsGroFile_to_molsysmt_Topology

    return openmm_GromacsGroFile_to_molsysmt_Topology(item, atom_indices=atom_indices,
                                                      structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_GromacsGroFile import \
        to_molsysmt_Structures as openmm_GromacsGroFile_to_molsysmt_Structures

    return openmm_GromacsGroFile_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                        structure_indices=structure_indices)
