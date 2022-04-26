def is_file_mmtf(item):

    output = False

    if type(item)==str:
        output = item.endswith('.mmtf')

    return output

