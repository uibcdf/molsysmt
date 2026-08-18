def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.MolecularMechanicsDict.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.


    .. versionadded:: 1.0.0
    """

    output = False

    if type(item) is dict:

        from molsysmt.native.molecular_mechanics_dict import molecular_mechanics_parameters

        keys = set(item.keys())
        output = (keys <= molecular_mechanics_parameters)

    return output

