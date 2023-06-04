def is_file(molecular_system):

    from molsysmt.basic import get_form
    from molsysmt.form import is_file as form_is_file

    form = get_form(molecular_system)
    output = form_is_file(form)

    return output

