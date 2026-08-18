
def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.StructuresDict.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form molsysmt.StructuresDict, False otherwise.
    """

    output = False

    if type(item) is dict:

        from molsysmt.native.structures_dict import structures_parameters

        keys = set(item.keys())
        output = (keys <= structures_parameters)

    return output

