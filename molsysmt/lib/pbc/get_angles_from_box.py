"""Compatibility exports for the bundled Rust kernels."""

from molsysmt._private.rust_backend import (
    get_angles_from_box_single_structure,
    get_angles_from_box,
)

__all__ = ["get_angles_from_box_single_structure", "get_angles_from_box"]
