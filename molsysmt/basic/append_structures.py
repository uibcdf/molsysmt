from molsysmt._private.digestion import digest

@digest()
def append_structures(to_molecular_system, from_molecular_system, selection='all',
        structure_indices='all', syntax='MolSysMT'):

    from . import get_form, convert, extract, get
    from molsysmt.form import _dict_modules

    if not isinstance(to_molecular_system, (list, tuple)):
        to_molecular_system = [to_molecular_system]

    to_forms = get_form(to_molecular_system)

    coordinates, velocities = get(from_molecular_system, element='atom', selection=selection,
                      structure_indices=structure_indices, coordinates=True, velocities=True)

    structure_id, time, box = get(from_molecular_system, element='system', structure_indices=structure_indices,
                          structure_id=True, time=True, box=True)

    for aux_to_item, aux_to_form in zip(to_molecular_system, to_forms):

        _dict_modules[aux_to_form].append_structures(aux_to_item, structure_id=structure_id, time=time, coordinates=coordinates, box=box,
                velocities=velocities)

    pass

