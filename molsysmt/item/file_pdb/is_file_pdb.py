def is_file_pdb(item):

    output = False

    if type(item)==str:
        output = item.endswith('.pdb')

    return output

