def is_file_gro(item):

    output = False

    if type(item)==str:
        output = item.endswith('.gro')

    return output

