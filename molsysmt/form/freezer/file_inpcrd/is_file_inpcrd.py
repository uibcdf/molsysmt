def is_file_inpcrd(item):

    output = False

    if type(item)==str:
        output = item.endswith('.inpcrd')

    return output

