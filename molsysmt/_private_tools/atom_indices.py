import numpy as np

def complementary_atom_indices(molecular_system, atom_indices):

    from molsysmt.multitool import get

    n_atoms = get(molecular_system, target='system', n_atoms=True)

    mask = np.ones(n_atoms,dtype=bool)
    mask[atom_indices]=False
    return list(np.where(mask)[0])

def atom_indices_to_AmberMask(molecular_system, atom_indices):

    from molsysmt.multitool import get

    n_atoms = get(molecular_system, element='system', n_atoms=True)
    mask = np.zeros(n_atoms,dtype=int)
    mask[atom_indices]=1
    return list(mask)

def digest_atom_indices(atom_indices):

    if type(atom_indices)==str:
        if atom_indices in ['all', 'All', 'ALL']:
            atom_indices = 'all'
        else:
            raise ValueError()
    elif type(atom_indices) in [int, np.int64, np.int]:
        atom_indices = np.array([atom_indices], dtype='int64')
    elif hasattr(atom_indices, '__iter__'):
        atom_indices = np.array(atom_indices, dtype='int64')

    return atom_indices

def atom_indices_to_string(atom_indices):

    return ",".join([str(ii) for ii in atom_indices])

