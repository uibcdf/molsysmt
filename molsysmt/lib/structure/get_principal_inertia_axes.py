"""Compatibility exports for the bundled Rust kernels."""

from molsysmt._private.rust_backend import (
    get_principal_inertia_axes_single_structure,
    get_principal_inertia_axes,
)

__all__ = ["get_principal_inertia_axes_single_structure", "get_principal_inertia_axes"]
