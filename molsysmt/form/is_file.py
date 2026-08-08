# This method must not be digested
def is_file(item_or_form):
    """Whether a molecular system, or a form name, is one of the file forms.

    Parameters
    ----------
    item_or_form : object or str or pathlib.Path
        A molecular system, the path of a file, or the name of a form in any
        capitalization.

    Returns
    -------
    bool
        True when the input is, or names, a form whose items are files.

    Notes
    -----
    A path is recognised by its extension, read from the catalogue rather than by asking
    every form detector in turn. That keeps the question about a *name* from importing the
    libraries needed to work with the data behind it.
    """

    from pathlib import PurePath

    from molsysmt.form import catalogue

    if isinstance(item_or_form, PurePath):
        item_or_form = str(item_or_form)

    if isinstance(item_or_form, str):
        form = catalogue.forms_lowercase().get(item_or_form.lower())
        if form is not None:
            return catalogue.form_type(form) == 'file'

        if item_or_form.startswith('file:'):
            return True

        if catalogue.form_of_extension(item_or_form) is not None:
            return True

    try:
        from molsysmt.basic import get_form

        return catalogue.form_type(get_form(item_or_form)) == 'file'
    except Exception:
        return False
