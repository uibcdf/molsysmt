from molsysmt._private.digestion import digest


@digest()
def get_molecule_index(molecular_system, element='atom', selection='all',
        redefine_components=False, redefine_indices=False, syntax='MolSysMT'):

    if redefine_indices:

        from ..component import get_component_index
        component_indices = get_component_index(molecular_system, element=element, selection=selection,
                            redefine_indices=redefine_components, syntax=syntax)
        if element in ['atom', 'group', 'component']:
            output = component_indices
        else:
            output = [ii[0] for ii in component_indices]

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_index=True)

    return output
