def is_form(item):

    output = False

    if type(item)==str:
        output = item.endswith('.msmpk')

    return output

