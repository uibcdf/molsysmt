def is_file_trjpk(item):

    output = False

    if type(item)==str:
        output = item.endswith('.trjpk')

    return output

