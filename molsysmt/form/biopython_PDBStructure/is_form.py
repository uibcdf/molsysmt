def is_form(item):
    """
    Checking whether an item is an instance of form biopython.PDBStructure.

    Parameters
    ----------
    item : biopython.PDBStructure
        Source item in biopython.PDBStructure form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    output = False

    class_name = str(type(item))
    if 'Bio.PDB.Structure.Structure' in class_name:
        output = True

    return output
