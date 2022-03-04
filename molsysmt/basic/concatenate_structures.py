from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt.api_forms import dict_append_structures, dict_concatenate_structures
from molsysmt.tools.molecular_system import are_multiple_molecular_systems

def concatenate_structures(molecular_systems, selections='all', structure_indices='all',
        syntaxis='MolSysMT', to_form=None, check=True):

    from molsysmt.basic import convert, extract, get

    if check:

        if not are_multiple_molecular_systems(molecular_systems):
            raise MultipleMolecularSystemsNeededError()

        raise NotImplementedError()

        try:
            syntaxis = digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError(syntaxis)

        try:
            selection = digest_selection(selection, syntaxis)
        except:
            raise WrongSelectionError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

        try:
            to_form = digest_to_form(to_form)
        except:
            raise WrongToFormError(to_form)

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
    else:
        to_molecular_system = convert(molecular_systems[0], selection=selections[0],
                structure_indices=structure_indices[0], to_form=to_form, check=False)


    box_in_diff_item=False
    if to_molecular_system.coordinates_item != to_molecular_system.box_item:
        box_in_diff_item=True

    for aux_molecular_system, aux_selection, aux_structure_indices in zip(molecular_systems[1:], selections[1:], structure_indices[1:]):

        step, time, coordinates, box = get(aux_molecular_system, target='atom',
                selection=aux_selection, structure_indices=aux_structure_indices, frame=True,
                check=False)

        try:
            if box_in_diff_item:
                dict_append_structures[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=None)
                dict_append_structures[to_molecular_system.box_form](to_molecular_system.box_item, step=None, time=None, coordinates=None, box=box)
            else:
                dict_append_structures[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=box)
        except:
            if box_in_diff_item:
                tmp_item = dict_concatenate_structures[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=None)
                to_molecular_system._replace_object(to_molecular_system.coordinates_item, tmp_item)
                tmp_item = dict_concatenate_append_structures[to_molecular_system.box_form](to_molecular_system.box_item, step=None, time=None, coordinates=None, box=box)
                to_molecular_system._replace_object(to_molecular_system.box_form, tmp_item)
            else:
                tmp_item = dict_concatenate_structures[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=box)
                to_molecular_system._replace_object(to_molecular_system.coordinates_item, tmp_item)

    output_items, output_forms = to_molecular_system.get_items()
    if len(output_items)==1:
        output = output_items[0]
    else:
        output = output_items

    return output

