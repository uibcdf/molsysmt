def is_file_crd(item):

    output = False

    if type(item)==str:
        if item.endswith('.crd'):
            output = True

    return output

