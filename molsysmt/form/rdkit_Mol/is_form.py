def is_form(item):

    output = False

    class_name = str(type(item))
    if 'rdkit.Chem.rdchem.Mol' in class_name:
        output = True

    return output
