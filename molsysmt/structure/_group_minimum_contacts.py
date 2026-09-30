"""Reducing sparse atom neighbors to minimum-distance group observations."""

import numpy as np

from molsysmt._private.rust_backend import (
    get_mic_pair_observations,
    neighbor_list_csr_multi,
)
from molsysmt._private.smonitor import InternalAlgorithmError


def bounded_group_minimum_contacts(
    coordinates_a, groups_a, coordinates_b, groups_b, threshold, box,
    max_candidate_bytes,
):
    """Bound source batches using a conservative dense-neighbor upper estimate.

    A batch reserves 128 bytes per possible atom pair for neighbor, grouping,
    and sort workspace. Group minima retained across batches have the same
    estimate. This is a numeric-workspace policy, not a process RSS limit.
    """
    from molsysmt._private.smonitor import MemoryBudgetExceededError

    if not len(coordinates_a) or not len(coordinates_b):
        return (
            np.empty((0, 2), dtype=np.int64), np.empty(0, dtype=np.float64),
            np.empty((0, 3), dtype=np.int32),
        )
    per_source = len(coordinates_b) * 128
    batch_size = max_candidate_bytes // (2 * per_source)
    if batch_size < 1:
        raise MemoryBudgetExceededError(
            reason="One source-atom neighbor batch exceeds the candidate memory estimate.",
            predicted_bytes=2 * per_source, available_bytes=max_candidate_bytes,
        )
    blocks = []
    retained_rows = 0
    for start in range(0, len(coordinates_a), batch_size):
        stop = min(start + batch_size, len(coordinates_a))
        block = group_minimum_contacts(
            coordinates_a[start:stop], groups_a[start:stop],
            coordinates_b, groups_b, threshold, box,
        )
        retained_rows += len(block[0])
        if retained_rows * 128 > max_candidate_bytes // 2:
            raise MemoryBudgetExceededError(
                reason="Retained group candidates exceed the candidate memory estimate.",
                predicted_bytes=retained_rows * 256,
                available_bytes=max_candidate_bytes,
            )
        blocks.append(block)
    pairs, distances, images = [np.concatenate(parts) for parts in zip(*blocks)]
    # Batches follow source-index order; the stable tie key preserves the
    # original lowest-source/lowest-target convention across batch boundaries.
    order = np.lexsort((np.arange(len(pairs)), distances, pairs[:, 1], pairs[:, 0]))
    pairs, distances, images = pairs[order], distances[order], images[order]
    keep = np.ones(len(pairs), dtype=bool)
    if len(pairs) > 1:
        keep[1:] = np.any(pairs[1:] != pairs[:-1], axis=1)
    return pairs[keep], distances[keep], images[keep]


def group_minimum_contacts(
    coordinates_a, groups_a, coordinates_b, groups_b, threshold, box=None
):
    """Return group pairs, minimum distances, and target MIC images for one structure.

    Coordinates and threshold share a length unit. Group labels are arbitrary
    int64 indices aligned with reference atoms; no charge or chemistry is inferred.
    Equal minima choose reference indices deterministically. At most one winning
    image per group pair is returned; this is not an all-images enumeration.
    """
    csr, targets, distances = neighbor_list_csr_multi(
        coordinates_a[None],
        coordinates_b[None],
        box=None if box is None else box[None],
        cutoff=np.nextafter(threshold, np.inf),
        exclude_self=False,
    )
    sources = np.repeat(np.arange(len(coordinates_a)), np.diff(csr))
    pairs = np.column_stack((groups_a[sources], groups_b[targets]))
    order = np.lexsort((targets, sources, distances, pairs[:, 1], pairs[:, 0]))
    pairs, sources, targets, distances = (
        pairs[order],
        sources[order],
        targets[order],
        distances[order],
    )
    keep = np.ones(len(pairs), dtype=bool)
    if len(pairs) > 1:
        keep[1:] = np.any(pairs[1:] != pairs[:-1], axis=1)
    pairs, sources, targets, distances = (
        pairs[keep],
        sources[keep],
        targets[keep],
        distances[keep],
    )
    images = np.zeros((len(pairs), 3), dtype=np.int32)
    if box is not None and len(pairs):
        observed, images = get_mic_pair_observations(
            coordinates_a[sources],
            coordinates_b[targets],
            box[None],
            np.zeros(len(pairs), dtype=np.int64),
        )
        if not np.allclose(observed, distances, atol=1e-8, rtol=1e-8):
            raise InternalAlgorithmError(
                reason="MIC images disagree with sparse neighbor distances",
                caller="molsysmt.structure._group_minimum_contacts",
            )
    return pairs, distances, images
