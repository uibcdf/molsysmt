def is_file_prmtop(item):

    output = False

    if type(item)==str:
        output = item.endswith('.prmtop')

    return output

