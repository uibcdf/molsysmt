def is_molecule_type(molecule_type):
    """
    Checking if a string represents a valid recognized molecule type in MolSysMT.

    Parameters
    ----------
    molecule_type : str
        String to test.

    Returns
    -------
    bool
        True if recognized molecule type, False otherwise.

    .. versionadded:: 1.0.0
    """
    from molsysmt.element.molecule import _molecule_types
    return molecule_type in _molecule_types
