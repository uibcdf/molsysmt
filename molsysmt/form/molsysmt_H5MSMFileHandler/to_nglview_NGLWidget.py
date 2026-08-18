from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.H5MSMFileHandler')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.H5MSMFileHandler to nglview.NGLWidget.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    nglview.NGLWidget
        Converted molecular system representation.
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_nglview_NGLWidget import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item, skip_digestion=True)

    return tmp_item

