def is_file_mdcrd(item):

    output = False

    if type(item)==str:
        output = item.endswith('.mdcrd')

    return output

