import numpy as np

def complementary_atom_indices(molecular_system, atom_indices):

    from molsysmt.basic import get

    n_atoms = get(molecular_system, target='system', n_atoms=True)

    mask = np.ones(n_atoms,dtype=bool)
    mask[atom_indices]=False
    return list(np.where(mask)[0])

def atom_indices_to_AmberMask(molecular_system, atom_indices):

    from molsysmt.basic import get

    n_atoms = get(molecular_system, element='system', n_atoms=True)
    mask = np.zeros(n_atoms,dtype=int)
    mask[atom_indices]=1
    return list(mask)

def atom_indices_to_csv(atom_indices):

    return ",".join([str(ii) for ii in atom_indices])

