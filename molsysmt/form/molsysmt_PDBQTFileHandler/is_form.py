def is_form(item):
    """Checking the registered PDBQT handler class.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler with resident snapshot or source-bound indexed storage.

    Returns
    -------
    bool
        Whether this input matches the registered handler class.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native import PDBQTFileHandler

    return isinstance(item, PDBQTFileHandler)
