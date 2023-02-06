from molsysmt._private.digestion import digest

@digest()
def append_structures(to_molecular_system, from_molecular_systems, selections='all',
        structure_indices='all', syntax='MolSysMT'):

    from . import get_form, convert, extract, get, are_multiple_molecular_systems, is_a_molecular_system
    from molsysmt.api_forms import dict_append_structures

    if not isinstance(to_molecular_system, (list, tuple)):
        to_molecular_system = [to_molecular_system]

    to_forms = get_form(to_molecular_system)

    if is_a_molecular_system(from_molecular_systems):
        from_molecular_systems = [from_molecular_systems]

    n_from_molecular_systems = len(from_molecular_systems)

    if not isinstance(selections, (list, tuple)):
        selections = [selections for ii in range(n_from_molecular_systems)]
    elif len(selections)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not isinstance(structure_indices, (list, tuple)):
        structure_indices = [structure_indices for ii in range(n_from_molecular_systems)]
    elif len(structure_indices)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and structure_indices need to be equal.")


    for aux_molecular_system, aux_selection, aux_structure_indices in zip(from_molecular_systems, selections, structure_indices):


        coordinates = get(aux_molecular_system, element='atom', selection=aux_selection,
                          structure_indices=aux_structure_indices, coordinates=True)

        structure_id, time, box = get(aux_molecular_system, element='system', structure_indices=aux_structure_indices,
                              structure_id=True, time=True, box=True)

        for aux_to_item, aux_to_form in zip(to_molecular_system, to_forms):

            dict_append_structures[aux_to_form](aux_to_item, structure_id=structure_id, time=time, coordinates=coordinates, box=box,
                    )

    pass

