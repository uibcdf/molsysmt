from molsysmt._private.digestion import digest


@digest()
def get_molecule_type(molecular_system, element='atom', selection='all',
        redefine_molecules=False, redefine_types=False, syntax='MolSysMT'):

    if redefine_molecules:

        from ..component import get_component_type

        molecule_types_from_molecule = get_component_type(molecular_system, element='component', selection=selection,
                redefine_components=True, syntax=syntax)

        if element == 'atom':
            aux = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'group':
            aux = get(molecular_system, element='group', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'component':
            aux = get(molecular_system, element='component', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'molecule':
            output = molecule_types_from_molecule
        else:
            raise NotImplementedError

    if redefine_types:

        from ..component import get_component_type

        molecule_types_from_molecule = get_component_type(molecular_system, element='component', selection=selection,
                redefine_components=False, redefine_types=False, syntax=syntax)

        if element == 'atom':
            aux = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'group':
            aux = get(molecular_system, element='group', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'component':
            aux = get(molecular_system, element='component', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'molecule':
            output = molecule_types_from_molecule
        else:
            raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_type=True)

    return output

