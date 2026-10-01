"""Construct coherent observed images for sparse indexed atom triplets."""

import numpy as np

from molsysmt._private.rust_backend import get_mic_pair_observations
from molsysmt._private.smonitor import StructuralInconsistencyError


def observed_chains(coordinates, chains, box, *, caller):
    """Image indexed chains coherently from adjacent MIC displacements.

    Return observed coordinates and integer shifts anchored at the first atom.
    All lengths share the input unit. This reconstructs the listed chain only,
    not other bonds, ring closure or a whole molecular component.
    """
    observed = coordinates[chains].copy()
    images = np.zeros(observed.shape, dtype=np.int64)
    if box is not None and len(chains):
        frames = np.zeros(len(chains), dtype=np.int64)
        for column in range(1, chains.shape[1]):
            _, shift = get_mic_pair_observations(
                observed[:, column - 1], observed[:, column], box[None], frames)
            images[:, column] = images[:, column - 1] + shift
        limits = np.iinfo(np.int32)
        if np.any(images < limits.min) or np.any(images > limits.max):
            raise StructuralInconsistencyError(reason="Observed periodic chain images exceed int32 storage.", caller=caller)
        observed += images @ box
    return observed, images.astype(np.int32)


def observed_triplets(coordinates, triplets, box, *, anchor, require_whole_first_pair, caller):
    """Anchor atom 0 and image via atom 0 or atom 1 according to the angle vertex.

    Inputs are one numeric coordinate frame, local triplets and row box vectors.
    Return observed coordinates, int32 images and independent atom0/atom2 MIC
    distances. The latter can reveal incompatible independent image choices.
    """
    observed = coordinates[triplets].copy()
    images = np.zeros((len(triplets), 3, 3), dtype=np.int64)
    if box is None or not len(triplets):
        return observed, images.astype(np.int32), np.linalg.norm(observed[:, 2] - observed[:, 0], axis=1)
    frames = np.zeros(len(triplets), dtype=np.int64)
    first, second, third = observed[:, 0], observed[:, 1], observed[:, 2]
    if anchor == 1:
        result, shifts = observed_chains(coordinates, triplets, box, caller=caller)
        if require_whole_first_pair and np.any(shifts[:, 1]):
            raise StructuralInconsistencyError(reason="This reference profile requires whole donor-H coordinates under PBC.", caller=caller)
        distances, _ = get_mic_pair_observations(first, third, box[None], frames)
        return result, shifts, distances
    _, pair_image = get_mic_pair_observations(first, second, box[None], frames)
    if require_whole_first_pair and np.any(pair_image):
        raise StructuralInconsistencyError(reason="This reference profile requires whole donor-H coordinates under PBC.", caller=caller)
    images[:, 1] = pair_image
    distances, third_image = get_mic_pair_observations(first, third, box[None], frames)
    images[:, 2] = third_image
    limits = np.iinfo(np.int32)
    if np.any(images < limits.min) or np.any(images > limits.max):
        raise StructuralInconsistencyError(reason="Observed periodic triplet images exceed int32 storage.", caller=caller)
    observed += images @ box
    return observed, images.astype(np.int32), distances
