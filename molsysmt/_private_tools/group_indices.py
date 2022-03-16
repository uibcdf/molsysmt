import numpy as np

def digest_group_indices(group_indices):

    if type(group_indices)==str:
        if group_indices in ['all', 'All', 'ALL']:
            group_indices = 'all'
        else:
            raise ValueError()
    elif type(group_indices) in [int, np.int64, np.int32]:
        group_indices = np.array([group_indices], dtype='int64')
    elif hasattr(group_indices, '__iter__'):
        group_indices = np.array(group_indices, dtype='int64')

    return group_indices

def complementary_group_indices(molecular_system, group_indices):

    from molsysmt.basic import get

    n_groups = get(molecular_system, target='system', n_groups=True)

    mask = np.ones(n_groups,dtype=bool)
    mask[atom_indices]=False
    return list(np.where(mask)[0])

def group_indices_to_csv(group_indices):

    return ",".join([str(ii) for ii in group_indices])

