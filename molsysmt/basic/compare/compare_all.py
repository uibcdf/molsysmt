from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
import numpy as np

def comparison_all_eq(molecular_system_A, molecular_system_B, selection_A='all',
        frame_indices_A='all', selection_B='all', frame_indices_B='all', syntaxis=syntaxis):

    from molsysmt.basic import select, get

    molecular_system_A = digest_molecular_system(molecular_system_A)
    molecular_system_B = digest_molecular_system(molecular_system_B)

    atom_indices_A = select(molecular_system_A, selection=selection_A, syntaxis=syntaxis)
    atom_indices_B = select(molecular_system_B, selection=selection_B, syntaxis=syntaxis)

    # Number of atoms

    n_atoms_A = atom_indices_A.shape[0]
    n_atoms_B = atom_indices_B.shape[0]

    if not n_atoms_A == n_atoms_B: return False

    # Atoms

    atom_names_A, atom_types_A, atom_ids_A = get(molecular_system_A, target='atom',
            indices=atom_indices_A, atom_name=True, atom_type=True, atom_id=True)

    atom_names_B, atom_types_B, atom_ids_B = get(molecular_system_B, target='atom',
            indices=atom_indices_B, atom_name=True, atom_type=True, atom_id=True)

    if not np.all(atom_names_A==atom_names_B): return False
    if not np.all(atom_types_A==atom_types_B): return False
    if not np.all(atom_ids_A==atom_ids_B): return False

    return True


