"""Compatibility exports for the bundled Rust kernels."""

from molsysmt._private.rust_backend import (
    set_mic_dihedral_angles,
    set_mic_dihedral_angles_single_structure,
)

__all__ = ["set_mic_dihedral_angles_single_structure", "set_mic_dihedral_angles"]
