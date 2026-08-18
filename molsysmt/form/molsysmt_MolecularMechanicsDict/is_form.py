def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form molsysmt.MolecularMechanicsDict, False otherwise.
    """

    output = False

    if type(item) is dict:

        from molsysmt.native.molecular_mechanics_dict import molecular_mechanics_parameters

        keys = set(item.keys())
        output = (keys <= molecular_mechanics_parameters)

    return output

