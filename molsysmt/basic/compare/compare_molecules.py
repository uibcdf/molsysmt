from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *

def comparison_molecules(molecular_system_A, molecular_system_B, selection_A='all',
        frame_indices_A='all', selection_B='all', frame_indices_B='all', type='A_eq_B',
        syntaxis=syntaxis):

    molecular_system_A = digest_molecular_system(molecular_system_A)
    molecular_system_B = digest_molecular_system(molecular_system_B)

    

    pass
