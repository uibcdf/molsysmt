from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.Universe')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from MDAnalysis.Universe to nglview.NGLWidget.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    nglview.NGLWidget
        Converted molecular system representation.
    """

    from . import extract
    from nglview import show_mdanalysis

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)
    tmp_item = show_mdanalysis(tmp_item)

    return tmp_item

