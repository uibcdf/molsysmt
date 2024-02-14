from molsysmt._private.digestion import digest

@digest(form='pytraj.Trajectory')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from nglview import show_pytraj
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False,
                       skip_digestion=True)
    tmp_item = show_pytraj(tmp_item)

    return tmp_item

