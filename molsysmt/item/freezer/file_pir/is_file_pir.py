def is_file_pir(item):

    output = False

    if type(item)==str:
        output = item.endswith('.pir')

    return output

