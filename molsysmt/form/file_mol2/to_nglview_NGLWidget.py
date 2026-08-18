from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:mol2 to nglview.NGLWidget.

    Parameters
    ----------
    item : file:mol2
        Source item in file:mol2 form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    nglview.NGLWidget
        Resulting object in nglview.NGLWidget form.

    .. versionadded:: 1.0.0
    """

    from nglview import show_file as nglview_show_file

    tmp_item = nglview_show_file(item)

    return tmp_item

