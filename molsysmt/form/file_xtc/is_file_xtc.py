def is_file_xtc(item):

    output = False

    if type(item)==str:
        output = item.endswith('.xtc')

    return output

