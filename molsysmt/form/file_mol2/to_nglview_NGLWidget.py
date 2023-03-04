from molsysmt._private.digestion import digest

@digest(form='file:mol2')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', output_filename=None):

    from nglview import show_file as nglview_show_file

    tmp_item = nglview_show_file(item)

    return tmp_item

def _to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all'):

    return to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices)
