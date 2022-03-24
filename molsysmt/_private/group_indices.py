import numpy as np

def complementary_group_indices(molecular_system, group_indices):

    from molsysmt.basic import get

    n_groups = get(molecular_system, target='system', n_groups=True)

    mask = np.ones(n_groups,dtype=bool)
    mask[atom_indices]=False
    return list(np.where(mask)[0])

def group_indices_to_csv(group_indices):

    return ",".join([str(ii) for ii in group_indices])

