"""Join observed images sharing an indexed anchor without changing geometry."""

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError


def join_shared_images(first, second, first_anchor, second_anchors, *, atoms, caller):
    """Translate second images onto the first shared atom, then anchor role zero.

    Inputs are integer lattice images for observations with arbitrary role counts.
    Return their concatenated images, one per singleton participant. Preserve
    both relative geometries; reject conflicting images for a repeated atom.
    """
    left = np.broadcast_to(first, (len(second), *first.shape[-2:])).astype(np.int64)
    right = second.astype(np.int64)
    shifts = (
        left[np.arange(len(left)), first_anchor]
        - right[np.arange(len(right)), second_anchors]
    )
    right += shifts[:, None]
    images = np.concatenate((left, right), axis=1)
    images -= images[:, :1]
    for a in range(images.shape[1]):
        for b in range(a + 1, images.shape[1]):
            shared = atoms[:, a] == atoms[:, b]
            if np.any(images[shared, a] != images[shared, b]):
                raise StructuralInconsistencyError(
                    reason="Joined observations assign incompatible periodic images to a shared atom.",
                    caller=caller,
                )
    limits = np.iinfo(np.int32)
    if np.any(images < limits.min) or np.any(images > limits.max):
        raise StructuralInconsistencyError(
            reason="Joined periodic images exceed int32 storage.", caller=caller
        )
    return images.astype(np.int32)
