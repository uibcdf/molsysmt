def is_form(item):
    """
    Checking whether an item is an instance of form rdkit.Mol.

    Parameters
    ----------
    item : rdkit.Mol
        Source item in rdkit.Mol form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    output = False

    class_name = str(type(item))
    if 'rdkit.Chem.rdchem.Mol' in class_name:
        output = True

    return output
