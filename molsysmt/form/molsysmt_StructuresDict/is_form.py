
def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.StructuresDict.

    Parameters
    ----------
    item : molsysmt.StructuresDict
        Source item in molsysmt.StructuresDict form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    output = False

    if type(item) is dict:

        from molsysmt.native.structures_dict import structures_parameters

        keys = set(item.keys())
        output = (keys <= structures_parameters)

    return output

