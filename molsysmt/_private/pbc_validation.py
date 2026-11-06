"""Internal validation helpers for periodic boxes."""

from __future__ import annotations

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError


def validate_box_array(box, n_structures, *, caller):
    """Validate finite, nonsingular box matrices independent of length units.

    Numerical singularity uses a dimensionless determinant after per-cell
    maximum-entry normalization, compared with float64 machine epsilon.
    """

    if box is None:
        raise StructuralInconsistencyError(
            reason="Periodic coordinates require box vectors.",
            caller=caller,
        )
    box = np.asarray(box, dtype=np.float64)
    if box.ndim != 3 or box.shape[1:] != (3, 3):
        raise StructuralInconsistencyError(
            reason=f"Box vectors must have shape (n_structures, 3, 3), not {box.shape}.",
            caller=caller,
        )
    if box.shape[0] == 1 and n_structures > 1:
        box = np.repeat(box, n_structures, axis=0)
    elif box.shape[0] != n_structures:
        raise StructuralInconsistencyError(
            reason=(
                f"Coordinates contain {n_structures} structures but box vectors "
                f"contain {box.shape[0]}."
            ),
            caller=caller,
        )
    if not np.all(np.isfinite(box)):
        raise StructuralInconsistencyError(
            reason="Box vectors must contain only finite values.",
            caller=caller,
        )
    scale = np.max(np.abs(box), axis=(1, 2))
    if np.any(scale == 0) or np.any(
        np.abs(np.linalg.det(box / scale[:, None, None])) <= np.finfo(np.float64).eps
    ):
        raise StructuralInconsistencyError(
            reason="Periodic box matrices must be non-singular.",
            caller=caller,
        )
    return np.ascontiguousarray(box, dtype=np.float64)
