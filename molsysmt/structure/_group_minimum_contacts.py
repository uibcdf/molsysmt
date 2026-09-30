"""Reducing sparse atom neighbors to minimum-distance group observations."""

import numpy as np

from molsysmt._private.rust_backend import (
    get_mic_pair_observations,
    neighbor_list_csr_multi,
)
from molsysmt._private.smonitor import InternalAlgorithmError


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
