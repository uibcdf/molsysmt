def is_form(item):
    """
    Checking whether an item is an instance of form biopython.PDBStructure.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form biopython.PDBStructure, False otherwise.
    """

    output = False

    class_name = str(type(item))
    if 'Bio.PDB.Structure.Structure' in class_name:
        output = True

    return output
