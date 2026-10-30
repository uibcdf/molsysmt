"""Finding bounded chemical motifs on a covalent graph without property inference."""

import numpy as np


def covalent_adjacency(n_atoms, pairs):
    """Return sorted CSR neighbors and original edge indices for an undirected graph."""

    sources = np.concatenate((pairs[:, 0], pairs[:, 1]))
    targets = np.concatenate((pairs[:, 1], pairs[:, 0]))
    edge_indices = np.tile(np.arange(len(pairs), dtype=np.int64), 2)
    order = np.lexsort((targets, sources))
    offsets = np.empty(n_atoms + 1, dtype=np.int64)
    offsets[0] = 0
    np.cumsum(np.bincount(sources, minlength=n_atoms), out=offsets[1:])
    return offsets, targets[order], edge_indices[order]


def terminal_oxygen_and_guanidine_candidates(elements, pairs, bond_orders):
    """Yield carboxyl and guanidine motifs; the caller interprets their charge."""

    offsets, neighbors, edges = covalent_adjacency(len(elements), pairs)
    for carbon in np.flatnonzero(elements == "C"):
        start, stop = offsets[carbon : carbon + 2]
        adjacent = neighbors[start:stop]
        orders = bond_orders[edges[start:stop]]
        heavy = elements[adjacent] != "H"
        heavy_neighbors, heavy_orders = adjacent[heavy], orders[heavy]
        oxygens = heavy_neighbors[elements[heavy_neighbors] == "O"]
        if len(oxygens) == 2 and len(heavy_neighbors) in {2, 3}:
            oxygen_orders = heavy_orders[elements[heavy_neighbors] == "O"]
            terminal = all(offsets[atom + 1] - offsets[atom] == 1 for atom in oxygens)
            other_orders = orders[elements[adjacent] != "O"]
            if (
                terminal
                and sorted(oxygen_orders.tolist()) == [1, 2]
                and (len(other_orders) == 0 or other_orders.tolist() == [1])
            ):
                yield "carboxyl", np.sort(np.append(oxygens, carbon)), np.sort(oxygens)
        if (
            len(adjacent) == 3
            and np.all(elements[adjacent] == "N")
            and sorted(orders.tolist()) == [1, 1, 2]
        ):
            yield "guanidine", np.sort(np.append(adjacent, carbon)), np.sort(adjacent)
