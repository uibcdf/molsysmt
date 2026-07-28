"""Low-level mathematical kernels implemented by the bundled Rust extension."""

from molsysmt import _rust
from molsysmt._private.rust_backend import (
    inverse_matrix_3x3,
    matmul,
    minimum_distance_between_coordinate_sets,
    minimum_distance_masked_not_bonded,
    normalize_vector,
    quaternion_to_rotation_matrix,
    rodrigues_rotation as _rodrigues_rotation,
    transpmatmul,
)

angle = _rust.angle
cross_product = _rust.cross_product
dihedral_angle = _rust.dihedral_angle
dot_product = _rust.dot_product
norm_vector = _rust.norm_vector


def rodrigues_rotation(vector, unit_vector, angle):
    """Rotating a vector in place with Rodrigues' formula."""
    vector[...] = _rodrigues_rotation(vector, unit_vector, angle)


__all__ = [
    "angle",
    "cross_product",
    "dihedral_angle",
    "dot_product",
    "inverse_matrix_3x3",
    "matmul",
    "minimum_distance_between_coordinate_sets",
    "minimum_distance_masked_not_bonded",
    "norm_vector",
    "normalize_vector",
    "quaternion_to_rotation_matrix",
    "rodrigues_rotation",
    "transpmatmul",
]
