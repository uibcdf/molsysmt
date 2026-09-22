"""Compatibility exports for the bundled Rust kernels."""

from molsysmt._private.rust_backend import (
    get_radius_of_gyration,
    get_radius_of_gyration_single_structure,
)

__all__ = ["get_radius_of_gyration_single_structure", "get_radius_of_gyration"]
