"""Checking whether original participant coordinates need internal MIC images."""

import numpy as np

from molsysmt._private.rust_backend import get_mic_pair_observations
from molsysmt._private.smonitor import NotImplementedMethodError


def require_whole_participants(coordinates, box, atom_offsets, atom_indices, caller):
    """Require each member to occupy its anchor's MIC image in the source coordinates.

    This is a bounded, anchor-relative condition, not a general compactness
    test or a covalent reconstruction. It permits one image per participant.
    Inputs contain one structure and box row vectors, in the same length unit.
    """
    lengths = np.diff(atom_offsets)
    anchors = np.repeat(atom_indices[atom_offsets[:-1]], lengths)
    if len(atom_indices) == 0:
        return
    _, images = get_mic_pair_observations(
        coordinates[anchors],
        coordinates[atom_indices],
        box[None],
        np.zeros(len(atom_indices), dtype=np.int64),
    )
    if np.any(images):
        raise NotImplementedMethodError(
            method="periodic compound participants",
            arguments="source coordinates requiring different MIC images within a participant",
            caller=caller,
        )
