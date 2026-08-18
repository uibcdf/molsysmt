from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to nglview.NGLWidget.

    Parameters
    ----------
    item : file:pdb
        Source item in file:pdb form.
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

    from .to_string_pdb_text import to_string_pdb_text
    from molsysmt.form.string_pdb_text.to_nglview_NGLWidget import to_nglview_NGLWidget as string_pdb_text_to_nglview_NGLWidget

    tmp_item = to_string_pdb_text(item, skip_digestion=True)
    tmp_item = string_pdb_text_to_nglview_NGLWidget(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

