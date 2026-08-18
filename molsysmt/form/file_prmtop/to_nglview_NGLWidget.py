from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def to_nglview_NGLWidget(item, atom_indices='all', coordinates=None, skip_digestion=False):
    """
    Converting from file:prmtop to nglview.NGLWidget.

    Parameters
    ----------
    item : file:prmtop
        Source item in file:prmtop form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    nglview.NGLWidget
        Resulting object in nglview.NGLWidget form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_nglview_NGLWidget import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item, skip_digestion=True)

    return tmp_item

