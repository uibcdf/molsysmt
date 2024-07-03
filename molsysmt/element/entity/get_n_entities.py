from molsysmt._private.digestion import digest


@digest()
def get_n_entities(molecular_system, selection='all', redefine_entities=False,
                     syntax='MolSysMT'):

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

