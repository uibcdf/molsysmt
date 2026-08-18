from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:mol2 to nglview.NGLWidget.

    Parameters
    ----------
    item : file:mol2
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    nglview.NGLWidget
        Converted molecular system representation.
    """

    from nglview import show_file as nglview_show_file

    tmp_item = nglview_show_file(item)

    return tmp_item

