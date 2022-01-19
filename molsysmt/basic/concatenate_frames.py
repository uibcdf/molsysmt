from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt.api_forms import dict_append_frames, dict_concatenate_frames

def concatenate_frames(molecular_systems, selections='all', frame_indices='all', syntaxis='MolSysMT', to_form=None):

    from molsysmt.basic import convert, extract, get, is_a_molecular_system

    if is_a_single_molecular_system(molecular_systems):
        raise NeedsMultipleMolecularSystemsError()

    tmp_molecular_systems = []
    for aux in molecular_systems:
        tmp_molecular_systems.append([digest_molecular_system(aux)])
    molecular_systems = tmp_molecular_systems

    n_molecular_systems = len(molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections)!=n_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(frame_indices):
        frame_indices = [digest_frame_indices(frame_indices) for ii in range(n_molecular_systems)]
    elif len(frame_indices)!=n_molecular_systems:
        raise ValueError("The length of the lists items and frame_indices need to be equal.")

    if to_form is None:
        to_molecular_system = extract(molecular_systems[0], selection=selections[0], frame_indices=frame_indices[0])
    else:
        to_molecular_system = convert(molecular_systems[0], selection=selections[0], frame_indices=frame_indices[0], to_form=to_form)

    to_molecular_system = digest_molecular_system(to_molecular_system)

    box_in_diff_item=False
    if to_molecular_system.coordinates_item != to_molecular_system.box_item:
        box_in_diff_item=True

    for aux_molecular_system, aux_selection, aux_frame_indices in zip(molecular_systems[1:], selections[1:], frame_indices[1:]):

        step, time, coordinates, box = get(aux_molecular_system, target='atom', selection=aux_selection, frame_indices=aux_frame_indices, frame=True)

        try:
            if box_in_diff_item:
                dict_append_frames[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=None)
                dict_append_frames[to_molecular_system.box_form](to_molecular_system.box_item, step=None, time=None, coordinates=None, box=box)
            else:
                dict_append_frames[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=box)
        except:
            if box_in_diff_item:
                tmp_item = dict_concatenate_frames[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=None)
                to_molecular_system._replace_object(to_molecular_system.coordinates_item, tmp_item)
                tmp_item = dict_concatenate_append_frames[to_molecular_system.box_form](to_molecular_system.box_item, step=None, time=None, coordinates=None, box=box)
                to_molecular_system._replace_object(to_molecular_system.box_form, tmp_item)
            else:
                tmp_item = dict_concatenate_frames[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=box)
                to_molecular_system._replace_object(to_molecular_system.coordinates_item, tmp_item)

    output_items, output_forms = to_molecular_system.get_items()
    if len(output_items)==1:
        output = output_items[0]
    else:
        output = output_items

    return output

