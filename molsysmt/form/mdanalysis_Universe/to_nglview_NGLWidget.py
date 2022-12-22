from molsysmt._private.digestion import digest

@digest(form='mdanalysis.Universe')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', digest=True):

    from . import extract
    from nglview import show_mdanalysis

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, digest=False)
    tmp_item = show_mdanalysis(tmp_item)

    return tmp_item

