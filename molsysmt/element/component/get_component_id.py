from molsysmt._private.digestion import digest


@digest()
def get_component_id(molecular_system, element='atom', selection='all', redefine_components=False,
                     redefine_ids=False, syntax='MolSysMT'):

    if redefine_components:
        from .get_component_index import get_component_index
        output = get_component_index(molecular_system, element=element, selection=selection,
                                     redefine_indices=True, syntax=syntax)
    elif redefine_ids:
        from .get_component_index import get_component_index
        output = get_component_index(molecular_system, element=element, selection=selection,
                                     redefine_indices=False, syntax=syntax)
    else:
        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_id=True)

    return output
