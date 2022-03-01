import numpy as np

def complementary_structure_indices(molecular_system, structure_indices):

    from molsysmt.basic import get

    n_frames = get(molecular_system, target='system', n_frames=True)

    mask = np.ones(n_frames, dtype=bool)
    mask[structure_indices] = False
    return list(np.where(mask)[0])

def digest_structure_indices(structure_indices):

    if type(structure_indices)==str:
        if structure_indices in ['all', 'All', 'ALL']:
            structure_indices = 'all'
        else:
            raise ValueError()
    elif type(structure_indices) in [int, np.int64, np.int32]:
        structure_indices = np.array([structure_indices], dtype='int64')
    elif hasattr(structure_indices, '__iter__'):
        structure_indices = np.array(structure_indices, dtype='int64')

    return structure_indices

