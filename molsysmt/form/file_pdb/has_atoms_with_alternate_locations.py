def has_atoms_with_alternate_locations(filename):
    """
    Performing has atoms with alternate locations on form file:pdb.

    Parameters
    ----------
    filename : object
        Argument filename.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import PDBFileHandler

    handler = PDBFileHandler(filename)
    try:
        return any(
            atom.alternate_location
            for model in handler.content.models
            for atom in model.atoms
        )
    finally:
        handler.close()
