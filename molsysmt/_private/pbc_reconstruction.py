"""Internal covalent reconstruction helpers for periodic coordinates."""

from __future__ import annotations

import numpy as np


_NEIGHBOR_SHIFTS = np.array(
    [[i, j, k] for i in (-1.0, 0.0, 1.0) for j in (-1.0, 0.0, 1.0) for k in (-1.0, 0.0, 1.0)]
)


def _minimum_image_vector(vector, box, inverse_box):
    fractional = vector @ inverse_box
    base = fractional - np.round(fractional)
    candidates = (base[None, :] + _NEIGHBOR_SHIFTS) @ box
    return candidates[np.argmin(np.einsum("ij,ij->i", candidates, candidates))]


def _connected_blocks(n_atoms, bonded_pairs):
    adjacency = [[] for _ in range(n_atoms)]
    for atom_1, atom_2 in bonded_pairs:
        adjacency[atom_1].append(atom_2)
        adjacency[atom_2].append(atom_1)

    blocks = []
    visited = np.zeros(n_atoms, dtype=bool)
    for root in range(n_atoms):
        if visited[root]:
            continue
        visited[root] = True
        stack = [root]
        block = []
        while stack:
            atom = stack.pop()
            block.append(atom)
            for neighbor in adjacency[atom]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
        blocks.append(np.asarray(block, dtype=np.int64))
    return blocks, adjacency


def reconstruct_and_wrap_covalent_blocks(
    coordinates,
    box,
    bonded_pairs,
    *,
    origin,
    mode,
):
    """Reconstruct connected atoms and wrap every covalent block as one unit."""

    blocks, adjacency = _connected_blocks(coordinates.shape[1], bonded_pairs)

    for frame_index in range(coordinates.shape[0]):
        frame = coordinates[frame_index]
        frame_box = box[frame_index]
        inverse_box = np.linalg.inv(frame_box)

        for block in blocks:
            block_set = set(block.tolist())
            root = int(block[0])
            visited = {root}
            stack = [root]
            while stack:
                parent = stack.pop()
                for child in adjacency[parent]:
                    if child in visited or child not in block_set:
                        continue
                    displacement = frame[child] - frame[parent]
                    frame[child] = frame[parent] + _minimum_image_vector(
                        displacement, frame_box, inverse_box
                    )
                    visited.add(child)
                    stack.append(child)

            center = np.mean(frame[block], axis=0)
            relative_center = center - origin
            if mode == "pbc":
                wrapped_center = (
                    (relative_center @ inverse_box) % 1.0
                ) @ frame_box
            elif mode == "pbc_center":
                fractional = relative_center @ inverse_box
                wrapped_center = (fractional - np.floor(fractional + 0.5)) @ frame_box
            elif mode == "mic":
                wrapped_center = _minimum_image_vector(
                    relative_center, frame_box, inverse_box
                )
            else:
                raise ValueError(f"Unknown covalent wrapping mode: {mode}")
            frame[block] += origin + wrapped_center - center


def localize_bonded_pairs(atom_indices, bonded_pairs):
    """Map global bonded atom pairs onto a selected coordinate array."""

    local_index = {int(atom): index for index, atom in enumerate(atom_indices)}
    output = [
        (local_index[int(atom_1)], local_index[int(atom_2)])
        for atom_1, atom_2 in bonded_pairs
        if int(atom_1) in local_index and int(atom_2) in local_index
    ]
    return np.asarray(output, dtype=np.int64).reshape((-1, 2))
