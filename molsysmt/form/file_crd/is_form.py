def is_form(item):

    output = False

    if type(item)==str:
        if item.endswith('.crd'):
            output = True

    return output

