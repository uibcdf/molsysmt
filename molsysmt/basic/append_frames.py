from molsysmt.forms import dict_append_frames
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt.tools.molecular_systems import is_a_single_molecular_system

def append_frames(to_molecular_system, from_molecular_systems, selections='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.basic import get

    to_molecular_system = digest_molecular_system(to_molecular_system)

    if is_a_single_molecular_system(from_molecular_systems):
        from_molecular_systems = [digest_molecular_system(from_molecular_systems)]
    else:
        tmp_from_molecular_systems = []
        for aux in from_molecular_systems:
            tmp_from_molecular_systems.append(digest_molecular_system(aux))
        from_molecular_systems = tmp_from_molecular_systems

    n_from_molecular_systems = len(from_molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_from_molecular_systems)]
    elif len(selections)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(frame_indices):
        frame_indices = [digest_frame_indices(frame_indices) for ii in range(n_from_molecular_systems)]
    elif len(frame_indices)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and frame_indices need to be equal.")

    box_in_diff_item=False
    if to_molecular_system.coordinates_item != to_molecular_system.box_item:
        box_in_diff_item=True

    for aux_molecular_system, aux_selection, aux_frame_indices in zip(from_molecular_systems, selections, frame_indices):

        step, time, coordinates, box = get(aux_molecular_system, target='atom', selection=aux_selection, frame_indices=aux_frame_indices, frame=True)

        if box_in_diff_item:
            dict_append_frames[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=None)
            dict_append_frames[to_molecular_system.box_form](to_molecular_system.box_item, step=None, time=None, coordinates=None, box=box)
        else:
            dict_append_frames[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=box)

    pass

