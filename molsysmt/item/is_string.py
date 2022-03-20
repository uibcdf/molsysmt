def is_string(item, check=True):

    from molsysmt.basic import get_form
    from molsysmt.tools.form import is_string as form_is_string

    if check:
        from molsysmt.tools.item import is_item
        if not is_item(item):
            raise WrongItemError()

    form = get_form(item, check=False)

    return form_is_string(form)

