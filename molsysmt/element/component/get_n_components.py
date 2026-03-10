from molsysmt._private.arg_digestion import arg_digest


@arg_digest()
def get_n_components(molecular_system, selection='all', redefine_components=False,
                     syntax='MolSysMT'):

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from .get_component_index import get_component_index

        if isinstance(molecular_system, Topology):
            return len(molecular_system.components.index) if not redefine_components else len(
                get_component_index(
                    molecular_system, element='component', selection='all', redefine_indices=True, syntax=syntax
                )
            )
        if isinstance(molecular_system, MolSys):
            return len(molecular_system.topology.components.index) if not redefine_components else len(
                get_component_index(
                    molecular_system, element='component', selection='all', redefine_indices=True, syntax=syntax
                )
            )

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
