"""Neighbour-list compatibility helpers backed by Rust."""

import numpy as np

from molsysmt._private.rust_backend import (
    neighbor_list_csr_multi,
    wrap_to_mic_vector_single_structure,
)


def _mic_wrap_vector(dx, dy, dz, box):
    """Returning one minimum-image displacement as a tuple."""
    vector = np.array([dx, dy, dz], dtype=np.float64)
    wrapped = wrap_to_mic_vector_single_structure(vector, box)
    return tuple(wrapped)


def neighbor_list_csr(
    query_coords,
    ref_coords=None,
    box=None,
    cutoff=None,
    exclude_self=True,
    half=False,
    return_distances=False,
):
    """Returning a CSR neighbour list for one structure."""
    if cutoff is None:
        raise ValueError("neighbor_list_csr requires a cutoff.")

    query = np.asarray(query_coords, dtype=np.float64)[None, :, :]
    ref = None
    if ref_coords is not None:
        ref = np.asarray(ref_coords, dtype=np.float64)[None, :, :]
    periodic_box = None
    if box is not None:
        periodic_box = np.asarray(box, dtype=np.float64)[None, :, :]

    offsets, indices, distances = neighbor_list_csr_multi(
        query,
        ref,
        periodic_box,
        cutoff,
        exclude_self=exclude_self,
        sort_by_distance=False,
    )

    if half:
        kept_indices = []
        kept_distances = []
        new_offsets = np.zeros_like(offsets)
        for query_index in range(query.shape[1]):
            start, stop = offsets[query_index : query_index + 2]
            mask = indices[start:stop] > query_index
            kept_indices.extend(indices[start:stop][mask])
            kept_distances.extend(distances[start:stop][mask])
            new_offsets[query_index + 1] = len(kept_indices)
        offsets = new_offsets
        indices = np.asarray(kept_indices, dtype=np.int64)
        distances = np.asarray(kept_distances, dtype=np.float64)

    if return_distances:
        return offsets, indices, distances
    return offsets, indices


def neighbor_pairs(
    query_coords,
    ref_coords=None,
    box=None,
    cutoff=None,
    half=True,
    exclude_self=True,
):
    """Returning neighbour pairs derived from a CSR list."""
    offsets, indices = neighbor_list_csr(
        query_coords,
        ref_coords,
        box,
        cutoff,
        exclude_self=exclude_self,
        half=half,
    )
    counts = np.diff(offsets)
    query_indices = np.repeat(np.arange(counts.shape[0], dtype=np.int64), counts)
    return np.column_stack((query_indices, indices))


__all__ = ["neighbor_list_csr", "neighbor_list_csr_multi", "neighbor_pairs"]
