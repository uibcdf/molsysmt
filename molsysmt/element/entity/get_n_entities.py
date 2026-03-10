from molsysmt._private.arg_digestion import arg_digest


@arg_digest()
def get_n_entities(molecular_system, selection='all', redefine_entities=False,
                     syntax='MolSysMT'):

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from .get_entity_index import get_entity_index

        if isinstance(molecular_system, Topology):
            return len(molecular_system.entities.index) if not redefine_entities else len(
                get_entity_index(
                    molecular_system, element='entity', selection='all', redefine_indices=True, syntax=syntax
                )
            )
        if isinstance(molecular_system, MolSys):
            return len(molecular_system.topology.entities.index) if not redefine_entities else len(
                get_entity_index(
                    molecular_system, element='entity', selection='all', redefine_indices=True, syntax=syntax
                )
            )

    if redefine_entities:

        from .get_entity_index import get_entity_index

        aux = get_entity_index(molecular_system, element='entity', selection=selection,
                                  redefine_indices=True, syntax=syntax)
        output = len(aux)

        del aux

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                     n_entities=True)

    return output
