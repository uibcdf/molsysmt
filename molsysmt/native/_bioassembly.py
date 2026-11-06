"""Project native assembly operations onto an explicitly retained chain axis."""

from copy import deepcopy

import numpy as np


def restrict(catalogue, chain_index_map):
    """Retain complete operations and remap chains without aliasing the source."""
    retained = {}
    for assembly_id, assembly in deepcopy(catalogue).items():
        chains = assembly["chain_indices"]
        if len(chains) and isinstance(chains[0], (list, tuple, np.ndarray)):
            operations = [
                i
                for i, indices in enumerate(chains)
                if all(int(index) in chain_index_map for index in indices)
            ]
            if not operations:
                continue
            assembly["chain_indices"] = [
                [chain_index_map[int(index)] for index in chains[i]] for i in operations
            ]
            for field in ("rotations", "translations"):
                assembly[field] = assembly[field][operations]
        else:
            if not all(int(index) in chain_index_map for index in chains):
                continue
            assembly["chain_indices"] = [
                chain_index_map[int(index)] for index in chains
            ]
        retained[assembly_id] = assembly
    return retained or None
