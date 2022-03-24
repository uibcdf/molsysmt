from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .arguments import digest_argument
from .compare_all import compare_all_eq, compare_all_in
from .compare_info import compare_info_eq, compare_info_in
from .compare_info_no_form import compare_info_no_form_eq, compare_info_no_form_in
from .compare_n_elements import compare_n_elements_eq, compare_n_elements_in
from .compare_n_molecules import compare_n_molecules_eq, compare_n_molecules_in
from .compare_n_structures import compare_n_structures_eq, compare_n_structures_in
from .compare_form import compare_form_eq, compare_form_in

dict_compare_eq={
        'all' : compare_all_eq,
        'info' : compare_info_eq,
        'info_no_form' : compare_info_no_form_eq,
        'n_elements' : compare_n_elements_eq,
        'n_molecules' : compare_n_molecules_eq,
        'n_structures' : compare_n_structures_eq,
        'form' : compare_form_eq,
        }

dict_compare_in={
        'all' : compare_all_in,
        'info' : compare_info_in,
        'info_no_form' : compare_info_no_form_in,
        'n_elements' : compare_n_elements_in,
        'n_molecules' : compare_n_molecules_in,
        'n_structures' : compare_n_structures_in,
        'form' : compare_form_in,
        }

def compare(molecular_system_A, molecular_system_B, selection_A='all', structure_indices_A='all',
        selection_B='all', structure_indices_B='all', comparison='all', rule='A_eq_B',
        syntaxis='MolSysMT', report=False, check=True):

    # rule in ['A_eq_B', 'A_neq_B', 'A_in_B', 'B_in_A']

    if check:

        if not is_molecular_system(molecular_system_A):
            raise MolecularSystemNeededError()

        if not is_molecular_system(molecular_system_B):
            raise MolecularSystemNeededError()

        try:
            target=digest_target(target)
        except:
            raise WrongTargetError(target)

        try:
            syntaxis=digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError(syntaxis)

        try:
            selection=digest_selection(selection_A, syntaxis)
        except:
            raise WrongSelectionError(selection_A)

        try:
            selection=digest_selection(selection_B, syntaxis)
        except:
            raise WrongSelectionError(selection_B)

        try:
            structure_indices_A = digest_structure_indices(structure_indices_A)
        except:
            raise WrongStructureIndicesError(structure_indices_A)

        try:
            structure_indices_B = digest_structure_indices(structure_indices_B)
        except:
            raise WrongStructureIndicesError(structure_indices_B)

        try:
            comparison = digest_argument(comparison)
        except:
            raise WrongComparisonError(comparison)

    if rule == 'A_eq_B':

        result, dict_report = dict_compare_eq[comparison](molecular_system_A, molecular_system_B,
                 selection_A=selection_A, structure_indices_A=structure_indices_A,
                 selection_B=selection_B, structure_indices_B=structure_indices_B,
                 syntaxis=syntaxis)

    elif rule in ['A_in_B', 'B_in_A']:

        if rule == 'A_in_B':

            result, dict_report = dict_compare_in[argument](molecular_system_A, molecular_system_B,
                    selection_A=selection_A, structure_indices_A=structure_indices_A,
                    selection_B=selection_B, structure_indices_B=structure_indices_B,
                    syntaxis=syntaxis)

        else:

            result, dict_report = dict_compare_in[argument](molecular_system_B, molecular_system_A,
                    selection_A=selection_B, structure_indices_A=structure_indices_B,
                    selection_B=selection_A, structure_indices_B=structure_indices_A,
                    syntaxis=syntaxis)

    else:

        raise ValueError()

    if report:

        return result, dict_report

    else:

        return result


