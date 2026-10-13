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

    # A declared form name describes a target; it is not an instantiated item.
    # Avoid importing every string/file detector to reject such a name.
    if isinstance(item, str):
        from molsysmt.form import catalogue

        if item.lower() in catalogue.forms_lowercase():
            return False

    try:
        get_form(item)
        output = True
    except Exception:
        output = False

    return output
