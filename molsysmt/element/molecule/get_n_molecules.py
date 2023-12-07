from molsysmt._private.digestion import digest


@digest()
def get_n_molecules(molecular_system, selection='all', redefine_molecules=False,
                     syntax='MolSysMT'):

    if redefine_molecules:

        from ..component import get_component_index

        aux = get_component_index(molecular_system, element='component', selection=selection,
                                  redefine_indices=True, syntax=syntax)
        output = len(aux)

        del aux

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                     n_molecules=True)

    return output

