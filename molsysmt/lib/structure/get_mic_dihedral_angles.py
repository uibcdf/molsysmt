"""Compatibility exports for the bundled Rust kernels."""

from molsysmt._private.rust_backend import (
    get_mic_dihedral_angles_single_structure,
    get_mic_dihedral_angles,
)

__all__ = ["get_mic_dihedral_angles_single_structure", "get_mic_dihedral_angles"]
