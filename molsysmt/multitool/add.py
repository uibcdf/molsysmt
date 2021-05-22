from molsysmt.forms import dict_add
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt.tools.molecular_systems import is_a_single_molecular_system
from molsysmt.multitool.convert import convert
from molsysmt.multitool.select import select

def add(to_molecular_system, from_molecular_systems, selections='all', frame_indices='all', syntaxis='MolSysMT'):

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


    to_already_added=[]

    for aux_molecular_system, aux_selection, aux_frame_indices in zip(from_molecular_systems, selections, frame_indices):

        atom_indices = select(aux_molecular_system, selection=aux_selection, syntaxis=syntaxis)

        # topology

        to_form = to_molecular_system.elements_form
        to_item = to_molecular_system.elements_item

        if to_form is not None:
            from_item = convert(aux_molecular_system, selection=atom_indices, frame_indices=aux_frame_indices, syntaxis=syntaxis, to_form=to_form)
            dict_add[to_form](to_item, from_item)
            to_already_added.append(to_item)

        # ff_parameters

        to_form = to_molecular_system.ff_parameters_form
        to_item = to_molecular_system.ff_parameters_item

        if to_form is not None:
            if to_item not in to_already_added:
                from_item = convert(aux_molecular_system, selection=atom_indices, frame_indices=aux_frame_indices, syntaxis=syntaxis, to_form=to_form)
                dict_add[to_form](to_item, from_item)
                to_already_added.append(to_item)

        # bonds

        to_form = to_molecular_system.bonds_form
        to_item = to_molecular_system.bonds_item

        if to_form is not None:
            if to_item not in to_already_added:
                from_item = convert(aux_molecular_system, selection=atom_indices, frame_indices=aux_frame_indices, syntaxis=syntaxis, to_form=to_form)
                dict_add[to_form](to_item, from_item)
                to_already_added.append(to_item)

        # coordinates

        to_form = to_molecular_system.coordinates_form
        to_item = to_molecular_system.coordinates_item

        if to_form is not None:
            if to_item not in to_already_added:
                from_item = convert(aux_molecular_system, selection=atom_indices, frame_indices=aux_frame_indices, syntaxis=syntaxis, to_form=to_form)
                dict_add[to_form](to_item, from_item)
                to_already_added.append(to_item)

        # The box info is taken from the first molecular_system

    pass

