from molsysmt._private.exceptions import *
from molsysmt._private.digestion import digest, digest_structure_indices
from molsysmt._private.lists_and_tuples import is_list_or_tuple


@digest
def concatenate_structures(molecular_systems, selections='all', structure_indices='all', to_form=None):

    from . import convert, extract, get, get_form
    from molsysmt.api_forms import dict_append_structures

    n_molecular_systems = len(molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections)!=n_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(structure_indices):
        structure_indices = [digest_structure_indices(structure_indices) for ii in range(n_molecular_systems)]
    elif len(structure_indices)!=n_molecular_systems:
        raise ValueError("The length of the lists items and structure_indices need to be equal.")

    if to_form is None:
        to_molecular_system = extract(molecular_systems[0], selection=selections[0],
                structure_indices=structure_indices[0], check=False)
        to_form = get_form(to_molecular_system)
    else:
        to_molecular_system = convert(molecular_systems[0], selection=selections[0],
                structure_indices=structure_indices[0], to_form=to_form, check=False)

    for aux_molecular_system, aux_selection, aux_structure_indices in zip(molecular_systems[1:], selections[1:], structure_indices[1:]):

        coordinates = get(aux_molecular_system, element='atom', selection=aux_selection,
                          structure_indices=aux_structure_indices, coordinates=True)
        step, time, box = get(aux_molecular_system, structure_indices=aux_structure_indices, step=True, time=True,
                              box=True)

        dict_append_structures[to_form](to_molecular_system, step=step, time=time, coordinates=coordinates, box=box)

    output = to_molecular_system

    return output

