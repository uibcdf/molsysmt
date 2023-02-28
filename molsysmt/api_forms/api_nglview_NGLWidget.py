def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_molsysmt_Topology as nglview_NGLWidget_to_molsysmt_Topology

    return nglview_NGLWidget_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_molsysmt_Structures as nglview_NGLWidget_to_molsysmt_Structures

    return nglview_NGLWidget_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_molsysmt_MolSys as nglview_NGLWidget_to_molsysmt_MolSys

    return nglview_NGLWidget_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_openmm_Topology as nglview_NGLWidget_to_openmm_Topology

    return nglview_NGLWidget_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_string_pdb_text as nglview_NGLWidget_to_string_pdb_text

    return nglview_NGLWidget_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_string_aminoacids1 as nglview_NGLWidget_to_aminoacids1

    return nglview_NGLWidget_to_aminoacids1(item, atom_indices=atom_indices)


def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_string_aminoacids3 as nglview_NGLWidget_to_aminoacids3

    return nglview_NGLWidget_to_aminoacids3(item, atom_indices=atom_indices)
