"""Compatibility exports for the bundled Rust kernels."""

from molsysmt._private.rust_backend import (
    get_angles_single_structure,
    get_angles,
)

__all__ = ["get_angles_single_structure", "get_angles"]
