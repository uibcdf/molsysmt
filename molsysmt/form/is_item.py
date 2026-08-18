def is_item(item):
    """
    Checking whether an object is a recognized molecular system item.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    bool
        True if the object is an instanced item of any supported form in MolSysMT, False otherwise.


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get_form

    try:
        form = get_form(item)
        output = True
    except Exception:
        output = False

    return output
