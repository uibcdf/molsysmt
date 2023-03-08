def is_form(item):

    output = False

    if type(item)==str:
        output = (item.endswith('.prmtop') or item.endswith('.parm7'))

    return output

