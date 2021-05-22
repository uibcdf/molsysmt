from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt.tools.molecular_systems import is_a_single_molecular_system
from molsysmt.multitool.convert import convert
from molsysmt.multitool.extract import extract
from molsysmt.multitool.append_frames import append_frames

def concatenate_frames(molecular_systems, selections='all', frame_indices='all', syntaxis='MolSysMT', to_form=None):

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
        tmp_molecular_system = extract(molecular_systems[0], selection=selections[0], frame_indices=frame_indices[0])
    else:
        tmp_molecular_system = convert(molecular_systems[0], selection=selections[0], frame_indices=frame_indices[0], to_form=to_form)

    append_frames(tmp_molecular_system, molecular_systems[1:], selections=selections[1:], frame_indices=frame_indices[1:])

    return tmp_molecular_system

