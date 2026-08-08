# This method must not be digested
def is_string(item_or_form):
    """Whether a molecular system, or a form name, is one of the string forms.

    Mirrors :func:`molsysmt.form.is_file`: it takes either an item or the name of a form,
    and it answers rather than raising. It used to index the form registry with whatever it
    was given, so anything that was not already a form name -- an actual molecular system
    included -- raised `KeyError` or `TypeError` instead of returning False.

    Parameters
    ----------
    item_or_form : object or str
        A molecular system, or the name of a form in any capitalization.

    Returns
    -------
    bool
        True when the input is, or names, a form whose items are strings.
    """

    from molsysmt.form import catalogue

    if isinstance(item_or_form, str):
        form = catalogue.forms_lowercase().get(item_or_form.lower())
        if form is not None:
            return catalogue.form_type(form) == 'string'

    try:
        from molsysmt.basic import get_form

        return catalogue.form_type(get_form(item_or_form)) == 'string'
    except Exception:
        return False
