def is_form(item):

    output = False

    class_name = str(type(item))
    if 'Bio.PDB.Structure.Structure' in class_name:
        output = True

    return output
