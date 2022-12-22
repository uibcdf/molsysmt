from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', digest=True):

    from . import extract
    from nglview import show_mdtraj as show_mdtraj

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, digest=False)
    tmp_item = show_mdtraj(tmp_item, digest=False)

    return tmp_item

