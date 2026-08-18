def is_form(item):
    """
    Checking whether an item is an instance of form rdkit.Mol.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form rdkit.Mol, False otherwise.
    """

    output = False

    class_name = str(type(item))
    if 'rdkit.Chem.rdchem.Mol' in class_name:
        output = True

    return output
