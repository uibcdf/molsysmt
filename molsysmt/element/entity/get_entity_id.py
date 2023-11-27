from molsysmt._private.digestion import digest


@digest()
def get_entity_id(molecular_system, element='atom', selection='all', redefine_entities=False,
                     redefine_ids=False, syntax='MolSysMT'):

    if redefine_entities:
        from .get_entity_index import get_entity_index
        output = get_entity_index(molecular_system, element=element, selection=selection,
                                     redefine_molecules=True, syntax=syntax)
    elif redefine_ids:
        from .get_entity_index import get_entity_index
        output = get_entity_index(molecular_system, element=element, selection=selection,
                                     redefine_molecules=False, redefine_indices=False, syntax=syntax)
    else:
        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_id=True)

    return output

