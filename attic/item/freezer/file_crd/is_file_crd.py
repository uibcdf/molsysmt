def is_file_crd(item):

    output = False

    if type(item)==str:
        output = item.endswith('.crd')

    return output

