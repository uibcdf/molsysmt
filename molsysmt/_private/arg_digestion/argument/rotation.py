import numpy as np
from molsysmt._private.smonitor import ArgumentError


def _is_rotation_like(rotation):
    """Return whether an object provides SciPy's rotation application protocol."""

    return callable(getattr(rotation, "apply", None))


def _validated_matrices(rotation, caller):
    matrices = np.asarray(rotation, dtype=np.float64)
    identity = np.eye(3)
    gram = matrices @ np.swapaxes(matrices, -1, -2)
    determinants = np.linalg.det(matrices)
    if not np.all(np.isfinite(matrices)):
        raise ArgumentError(
            "rotation", value=rotation, caller=caller,
            message="Rotation matrices must contain only finite values.",
        )
    if not np.allclose(gram, identity, rtol=0.0, atol=1.0e-10):
        raise ArgumentError(
            "rotation", value=rotation, caller=caller,
            message="Rotation matrices must be orthonormal.",
        )
    if not np.allclose(determinants, 1.0, rtol=0.0, atol=1.0e-10):
        raise ArgumentError(
            "rotation", value=rotation, caller=caller,
            message="Rotation matrices must be proper rotations with determinant +1.",
        )
    return matrices

def digest_rotation(rotation, caller=None):

    if isinstance(rotation, (list, tuple)):
        rotation = np.array(rotation)

    if isinstance(rotation, np.ndarray):
        if rotation.shape == (3,3):
            rotation = rotation[np.newaxis,np.newaxis,:,:]
        elif len(rotation.shape)==3 and rotation.shape[1:]==(3,3):
            rotation = rotation[:,np.newaxis,:,:]
        elif len(rotation.shape)==4 and rotation.shape[2:]==(3,3):
            pass
        else:
            raise ArgumentError('rotation', value=rotation, caller=caller, message=None)
        return _validated_matrices(rotation, caller)

    if _is_rotation_like(rotation):
        return rotation

    raise ArgumentError('rotation', value=rotation, caller=caller, message=None)
