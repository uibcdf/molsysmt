from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_nglview_NGLWidget(item, atom_indices='all', coordinates=None, skip_digestion=False):
    """
    Converting from openmm.Topology to nglview.NGLWidget.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
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

    from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text as to_string_pdb_text
    from molsysmt.form.string_pdb_text.to_nglview_NGLWidget import to_nglview_NGLWidget as string_pdb_text_to_nglview_NGLWidget

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, skip_digestion=True)
    tmp_item = string_pdb_text_to_nglview_NGLWidget(tmp_item, skip_digestion=True)

    return tmp_item

