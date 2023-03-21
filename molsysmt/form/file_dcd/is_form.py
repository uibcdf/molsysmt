def is_form(item):

    output = False

    if type(item)==str:
        output = item.endswith('.dcd')

    return output

