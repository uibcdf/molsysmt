def is_form(item):

    output = False

    if type(item)==str:
        output = item.endswith('.mol2')

    return output

