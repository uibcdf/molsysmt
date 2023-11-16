def is_molecule_type(molecule_type):

    from molsysmt.element.molecule import _molecule_types
    from molsysmt.element.molecule import _plural_molecule_types_to_singular

    output = False

    if molecule_type in _molecule_types:
        output = True

    elif molecule_type in _plural_molecule_types_to_singular:
        output = True

    return output

