from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.Structure')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from parmed.Structure to nglview.NGLWidget.

    Parameters
    ----------
    item : parmed.Structure
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    nglview.NGLWidget
        Converted molecular system representation.
    """

    from nglview import show_parmed
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)
    tmp_item = show_parmed(tmp_item)

    return tmp_item

