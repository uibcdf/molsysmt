import numpy as np

def complementary_structure_indices(molecular_system, structure_indices):

    from molsysmt.basic import get

    n_structures = get(molecular_system, element='system', n_structures=True)

    structure_indices = np.array(structure_indices)
    structure_indices = structure_indices[structure_indices < n_structures]

    mask = np.ones(n_structures, dtype=bool)
    mask[structure_indices] = False
    return list(np.where(mask)[0])

