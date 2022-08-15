def is_file_dcd(item):

    output = False

    if type(item)==str:
        output = item.endswith('.dcd')

    return output

