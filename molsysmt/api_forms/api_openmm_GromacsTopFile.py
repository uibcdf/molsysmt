def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_GromacsTopFile import to_openmm_Topology as openmm_GromacsTopFile_to_openmm_Topology

    return openmm_GromacsTopFile_to_openmm_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_GromacsTopFile import to_molsysmt_Topology as openmm_GromacsTopFile_to_molsysmt_Topology

    return openmm_GromacsTopFile_to_molsysmt_Topology(item, atom_indices=atom_indices,
                                                      structure_indices=structure_indices)
