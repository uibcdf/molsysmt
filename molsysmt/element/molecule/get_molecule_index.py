from molsysmt._private.digestion import digest


@digest()
def get_molecule_index(molecular_system, element='atom', selection='all',
        redefine_components=False, redefine_indices=False, syntax='MolSysMT'):

    if redefine_indices:

        from ..component import get_component_index
        output = get_component_index(molecular_system, element=element, selection=selection,
                redefine_indices=redefine_components, syntax=syntax)

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_index=True)

    return output
