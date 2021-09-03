from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
from .arguments import digest_argument
from .compare_all import compare_all_eq, compare_all_in
from .compare_info import compare_info_eq, compare_info_in
from .compare_n_elements import compare_n_elements_eq, compare_n_elements_in
from .compare_n_molecules import compare_n_molecules_eq, compare_n_molecules_in
from .compare_n_frames import compare_n_frames_eq, compare_n_frames_in
from .compare_form import compare_form_eq, compare_form_in

dict_compare_eq={
        'all' : compare_all_eq,
        'info' : compare_info_eq,
        'n_elements' : compare_n_elements_eq,
        'n_molecules' : compare_n_molecules_eq,
        'n_frames' : compare_n_frames_eq,
        'form' : compare_form_eq,
        }

dict_compare_in={
        'all' : compare_all_in,
        'info' : compare_info_in,
        'n_elements' : compare_n_elements_in,
        'n_molecules' : compare_n_molecules_in,
        'n_frames' : compare_n_frames_in,
        'form' : compare_form_in,
        }

def compare(molecular_system_A, molecular_system_B, selection_A='all', frame_indices_A='all',
        selection_B='all', frame_indices_B='all', comparison='all', rule='A_eq_B',
        syntaxis='MolSysMT', report=False):

    # rule in ['A_eq_B', 'A_neq_B', 'A_in_B', 'B_in_A']

    molecular_system_A = digest_molecular_system(molecular_system_A)
    molecular_system_B = digest_molecular_system(molecular_system_B)

    comparison = digest_argument(comparison)

    if rule == 'A_eq_B':

        result, dict_report = dict_compare_eq[comparison](molecular_system_A, molecular_system_B,
                 selection_A=selection_A, frame_indices_A=frame_indices_A,
                 selection_B=selection_B, frame_indices_B=frame_indices_B,
                 syntaxis=syntaxis)

    elif rule in ['A_in_B', 'B_in_A']:

        if rule == 'A_in_B':

            result, dict_report = dict_compare_in[argument](molecular_system_A, molecular_system_B,
                    selection_A=selection_A, frame_indices_A=frame_indices_A,
                    selection_B=selection_B, frame_indices_B=frame_indices_B,
                    syntaxis=syntaxis)

        else:

            result, dict_report = dict_compare_in[argument](molecular_system_B, molecular_system_A,
                    selection_A=selection_B, frame_indices_A=frame_indices_B,
                    selection_B=selection_A, frame_indices_B=frame_indices_A,
                    syntaxis=syntaxis)

    else:

        raise ValueError()

    if report:

        return result, dict_report

    else:

        return result


