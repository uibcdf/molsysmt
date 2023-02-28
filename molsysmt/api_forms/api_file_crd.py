def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_molsysmt_MolSys as file_crd_to_molsysmt_MolSys

    tmp_item = file_crd_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_molsysmt_Topology as file_crd_to_molsysmt_Topology

    tmp_item = file_crd_to_molsysmt_Topology(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_molsysmt_Structures as file_crd_to_molsysmt_Structures

    tmp_item = file_crd_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_openmm_CharmmCrdFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_openmm_CharmmCrdFile as file_crd_to_openmm_CharmmCrdFile

    tmp_item = file_crd_to_openmm_CharmmCrdFile(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item


