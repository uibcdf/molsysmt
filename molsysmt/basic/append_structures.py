from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.lists_and_tuples import is_list_or_tuple

def append_structures(to_molecular_system, from_molecular_systems, selections='all',
        structure_indices='all', syntaxis='MolSysMT', check=True):

    from . import get_form, convert, extract, get, are_multiple_molecular_systems, is_molecular_system
    from molsysmt.api_forms import dict_append_structures

    if check:

        if not is_molecular_system(to_molecular_system):
            raise MolecularSystemNeededError()

        if not is_molecular_system(from_molecular_systems):
            if not are_multiple_molecular_systems(from_molecular_systems):
                raise MolecularSystemNeededError()

        try:
            syntaxis = digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError(syntaxis)

        try:
            selection = digest_selection(selections, syntaxis)
        except:
            raise WrongSelectionError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    if not is_list_or_tuple(to_molecular_system):
        to_molecular_system = [to_molecular_system]

    to_forms = get_form(to_molecular_system)

    if is_molecular_system(from_molecular_systems):
        from_molecular_systems = [from_molecular_systems]

    n_from_molecular_systems = len(from_molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_from_molecular_systems)]
    elif len(selections)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(structure_indices):
        structure_indices = [digest_structure_indices(structure_indices) for ii in range(n_from_molecular_systems)]
    elif len(structure_indices)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and structure_indices need to be equal.")


    for aux_molecular_system, aux_selection, aux_structure_indices in zip(from_molecular_systems, selections, structure_indices):


        coordinates = get(aux_molecular_system, target='atom', selection=aux_selection, structure_indices=aux_structure_indices,
                          coordinates=True, check=False)

        step, time, box = get(aux_molecular_system, target='system', structure_indices=aux_structure_indices, step=True,
                              time=True, box=True, check=False)

        for aux_to_item, aux_to_form in zip(to_molecular_system, to_forms):

            dict_append_structures[aux_to_form](aux_to_item, step=step, time=time, coordinates=coordinates, box=box)

    pass

