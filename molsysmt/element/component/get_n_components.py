from molsysmt._private.arg_digestion import arg_digest


@arg_digest()
def get_n_components(molecular_system, selection='all', redefine_components=False,
                     syntax='MolSysMT'):

    if redefine_components:

        from .get_component_index import get_component_index

        aux = get_component_index(molecular_system, element='component', selection=selection,
                                  redefine_indices=True, syntax=syntax)
        output = len(aux)

        del aux

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                     n_components=True)

    return output

