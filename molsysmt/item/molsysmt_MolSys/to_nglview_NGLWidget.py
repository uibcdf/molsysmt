from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all'):

    from nglview import show_molsysmt

    tmp_item = show_molsysmt(item, selection=atom_indices, structure_indices=structure_indices)

    return tmp_item

