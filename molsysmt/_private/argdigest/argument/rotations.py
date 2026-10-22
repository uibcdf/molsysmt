import numpy as np

from molsysmt._private.smonitor import ArgumentError

from .rotation import _validated_matrices


def digest_rotations(rotations, caller=None):

    if caller is not None:
        if caller.endswith("digest_bioassembly"):
            if isinstance(rotations, (np.ndarray, list, tuple)):
                try:
                    matrices = np.asarray(rotations)
                    if matrices.shape == (0,):
                        matrices = np.empty((0, 3, 3), dtype=np.float64)
                    if (
                        matrices.ndim != 3
                        or matrices.shape[1:] != (3, 3)
                        or np.iscomplexobj(matrices)
                        or not np.all(np.isfinite(matrices))
                    ):
                        raise ValueError("Invalid assembly rotation matrices.")
                    return _validated_matrices(matrices, caller).copy()
                except (TypeError, ValueError) as error:
                    raise ArgumentError(
                        "rotations",
                        value=rotations,
                        caller=caller,
                        message="Assembly rotations must be finite real matrices with shape (n_operations, 3, 3).",
                    ) from error

    raise ArgumentError("rotations", value=rotations, caller=caller, message=None)
