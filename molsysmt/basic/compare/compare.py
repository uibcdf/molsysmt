from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
from .arguments import digest_argument
from .compare_all_eq import compare_all_eq
from .compare_all_in import compare_all_in
from .compare_molecules_eq import compare_molecules_eq
from .compare_molecules_in import compare_molecules_in

dict_compare_eq={
        'all' : compare_all_eq,
        'molecules' : compare_molecules_eq,
        }

dict_compare_in={
        'all' : compare_all_in,
        'molecules' : compare_molecules_in,
        }

def comparison(molecular_system_A, molecular_system_B, selection_A='all', frame_indices_A='all',
        selection_B='all', frame_indices_B='all', rule='A_eq_B', syntaxis='MolSysMT', **kwargs):

    # rule in ['A_eq_B', 'A_neq_B', 'A_in_B', 'B_in_A']

    molecular_system_A = digest_molecular_system(molecular_system_A)
    molecular_system_B = digest_molecular_system(molecular_system_B)

    arguments = [ digest_argument(key) for key in kwargs.keys() if kwargs[key] ]

    output = []

    if rule in ['A_eq_B', 'A_neq_B']:

        for argument in arguments:

            result = dict_compare_eq[argument](molecular_system_A, molecular_system_B,
                     selection_A=selection_A, frame_indices_A=frame_indices_A,
                     selection_B=selection_B, frame_indices_B=frame_indices_B,
                     rule=rule, syntaxis=syntaxis)

            if rule == 'A_neq_B':

                result = not result

            output.append(result)

    elif rule in ['A_in_B', 'B_in_A']:

        for argument in arguments:

            if rule == 'A_in_B':

                result = dict_compare_in[argument](molecular_system_A, molecular_system_B,
                        selection_A=selection_A, frame_indices_A=frame_indices_A,
                        selection_B=selection_B, frame_indices_B=frame_indices_B,
                        syntaxis=syntaxis)

            else:

                result = dict_compare_in[argument](molecular_system_B, molecular_system_A,
                        selection_A=selection_B, frame_indices_A=frame_indices_B,
                        selection_B=selection_A, frame_indices_B=frame_indices_A,
                        syntaxis=syntaxis)

            output.append(result)

    else:

        raise ValueError()

    output=digest_output(output)

    return output

