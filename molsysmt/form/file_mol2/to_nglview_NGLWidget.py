from molsysmt._private.digestion import digest

@digest(form='file:mol2')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all'):

    from nglview import show_file as nglview_show_file

    tmp_item = nglview_show_file(item)

    return tmp_item

