def is_item(item, check=True):

    from molsysmt.basic import get_form

    try:
        form = get_form(item)
        output = True
    except:
        output = False

    return output

