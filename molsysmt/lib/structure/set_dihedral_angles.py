"""Compatibility exports for the bundled Rust kernels."""

from molsysmt._private.rust_backend import (
    set_dihedral_angles_single_structure,
    set_dihedral_angles,
)

__all__ = ["set_dihedral_angles_single_structure", "set_dihedral_angles"]
