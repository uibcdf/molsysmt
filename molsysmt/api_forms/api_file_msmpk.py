def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_msmpk import to_molsysmt_MolSys as file_msmpk_to_molsysmt_MolSys

    return file_msmpk_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_msmpk import to_molsysmt_Topology as file_msmpk_to_molsysmt_Topology

    return file_msmpk_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_msmpk import to_molsysmt_Structures as file_msmpk_to_molsysmt_Structures

    return file_msmpk_to_molsysmt_Structures(item, atom_indices=atom_indices)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_msmpk import to_nglview_NGLWidget as file_msmpk_to_nglview_NGLWidget

    return file_msmpk_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                           structure_indices=structure_indices)
