def is_file(item, check=True):

    from molsysmt.basic import get_form
    from molsysmt.tools.form import is_file as form_is_file

    if check:
        from molsysmt.tools.item import is_item
        if not is_item(item):
            raise WrongItemError()

    output = False

    if type(item) is str:
        try:
            form = get_form(item)
            output = form_is_file(form)
        except:
            output = False

    return output

