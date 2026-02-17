import numpy as np
import numba as nb

from molsysmt._private.jit import lazy_njit


@lazy_njit(nb.int64(nb.int64[:], nb.int64), cache=True)
def _find_root(parent, node):

    while parent[node] != node:
        parent[node] = parent[parent[node]]
        node = parent[node]

    return node


@lazy_njit(nb.void(nb.int64[:], nb.int64[:], nb.int64, nb.int64), cache=True)
def _union(parent, rank, node_1, node_2):

    root_1 = _find_root(parent, node_1)
    root_2 = _find_root(parent, node_2)

    if root_1 == root_2:
        return

    if rank[root_1] < rank[root_2]:
        parent[root_1] = root_2
    elif rank[root_1] > rank[root_2]:
        parent[root_2] = root_1
    else:
        parent[root_2] = root_1
        rank[root_1] += 1


@lazy_njit(nb.int64[:](nb.int64[:, :], nb.int64), cache=True)
def get_component_index_from_bonded_atom_pairs(bonded_atom_pairs, n_atoms):
    """Computing contiguous component indices from atom bonded pairs."""

    if n_atoms == 0:
        return np.empty((0,), dtype=np.int64)

    parent = np.arange(n_atoms, dtype=np.int64)
    rank = np.zeros(n_atoms, dtype=np.int64)

    for bond_index in range(bonded_atom_pairs.shape[0]):
        atom_1 = bonded_atom_pairs[bond_index, 0]
        atom_2 = bonded_atom_pairs[bond_index, 1]
        _union(parent, rank, atom_1, atom_2)

    output = np.empty((n_atoms,), dtype=np.int64)
    root_to_component = np.full((n_atoms,), -1, dtype=np.int64)
    next_component = 0

    for atom_index in range(n_atoms):
        root = _find_root(parent, atom_index)
        component_index = root_to_component[root]
        if component_index == -1:
            component_index = next_component
            root_to_component[root] = component_index
            next_component += 1
        output[atom_index] = component_index

    return output
