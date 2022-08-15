def is_item(item):

    from molsysmt.basic import get_form

    try:
        form = get_form(item)
        output = True
    except:
        output = False

    return output

