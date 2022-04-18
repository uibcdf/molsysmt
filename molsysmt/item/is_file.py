def is_file(item, check=True):

    from molsysmt.basic import get_form
    from molsysmt.form import is_file as form_is_file

    if check:
        from molsysmt.item import is_item
        if not is_item(item):
            raise WrongItemError()

    output = False

    if type(item) is str:
        output = form_is_file(item)

    return output

