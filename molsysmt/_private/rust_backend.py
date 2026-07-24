"""Optional Rust-kernel backend (Rust-migration coexistence layer).

MolSysMT runs on pure Numba by default. When the optional ``msm_rust_kernels`` wheel is
installed *and* selected, these dispatchers route kernels to Rust — numerically equal to
within a documented scientific tolerance (not bit-for-bit; ``fastmath`` and different
eigensolvers move the last bits), with no JIT compilation and no ``warmup()``.

Selection is driven by ``molsysmt.configure.kernel`` (global) and the uniform per-call
``kernel=`` override, exactly like ``parallel``/``num_threads`` — never a bespoke argument
per function:

- ``'numba'`` (the default): always Numba.
- ``'rust'``: Rust; raises if the wheel is not installed.
- ``'auto'``: Rust if the wheel is importable, else Numba.

Each dispatcher also accepts an explicit ``backend=`` for tests and internal callers; when
left ``None`` it reads ``configure.kernel``. This module is a safe no-op when the wheel is
absent, so it lives in ``main`` without making MolSysMT depend on Rust. See
``devguide/pending_proposals/rust_numba_coexistence_and_cut_plan.md``.
"""

import warnings

try:
    import msm_rust_kernels as _rust
    HAVE_RUST = True
except Exception:  # pragma: no cover - absence is the normal, supported state
    _rust = None
    HAVE_RUST = False

_NUMBA_DEPRECATION_WARNED = False


def _resolve_backend(backend):
    """Return the effective backend, reading ``configure.kernel`` when unspecified."""
    if backend is not None:
        return backend
    from molsysmt import configure
    return getattr(configure, "kernel", "numba")


def _warn_numba_deprecation_once():
    """Warn once when the deprecated Numba path is taken explicitly while Rust is available.

    Kept quiet in the default (``kernel='numba'``, no wheel) state so it does not spam
    during normal use; it fires only when a user could have used Rust and did not, which is
    the signal the migration wants to surface. See the coexistence plan for the removal
    target.
    """
    global _NUMBA_DEPRECATION_WARNED
    if _NUMBA_DEPRECATION_WARNED or not HAVE_RUST:
        return
    _NUMBA_DEPRECATION_WARNED = True
    warnings.warn(
        "The Numba compute kernels are deprecated and will be removed after the Rust "
        "migration is complete. Set molsysmt.configure.kernel = 'rust' (or 'auto') to use "
        "the Rust kernels. See devguide/pending_proposals/"
        "rust_numba_coexistence_and_cut_plan.md.",
        DeprecationWarning,
        stacklevel=3,
    )


def _use_rust(backend):
    # Warn only when the backend was unspecified and resolved to Numba from configure —
    # i.e. the path a user actually takes. An explicit backend='numba' (tests, internal
    # callers) is a deliberate choice, not the deprecated default, and stays quiet.
    from_config = backend is None
    backend = _resolve_backend(backend)
    if backend == "numba":
        if from_config:
            _warn_numba_deprecation_once()
        return False
    if backend == "rust":
        if not HAVE_RUST:
            raise RuntimeError(
                "kernel='rust' requested but the optional 'msm_rust_kernels' package "
                "is not installed."
            )
        return True
    if backend == "auto":
        return HAVE_RUST
    raise ValueError(f"unknown kernel {backend!r} (expected 'numba', 'rust' or 'auto')")


# --------------------------------------------------------------------------- MIC distances
# Faithful 1:1 dispatch of molsysmt.lib.structure.get_mic_distances.* — the Rust and
# Numba implementations produce identical results (bit-for-bit; see tests/rust/).

def get_mic_distances_single_system(coordinates, box, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_distances_single_system(coordinates, box)
    from molsysmt.lib.structure.get_mic_distances import get_mic_distances_single_system as _nb
    return _nb(coordinates, box)


def get_mic_distances(coordinates1, coordinates2, box, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_distances(coordinates1, coordinates2, box)
    from molsysmt.lib.structure.get_mic_distances import get_mic_distances as _nb
    return _nb(coordinates1, coordinates2, box)


def get_mic_distances_pairs(coordinates1, coordinates2, box, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_distances_pairs(coordinates1, coordinates2, box)
    from molsysmt.lib.structure.get_mic_distances import get_mic_distances_pairs as _nb
    return _nb(coordinates1, coordinates2, box)


def get_mic_distances_single_system_single_structure(coordinates, box, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_distances_single_system_single_structure(coordinates, box)
    from molsysmt.lib.structure.get_mic_distances import (
        get_mic_distances_single_system_single_structure as _nb)
    return _nb(coordinates, box)


def get_mic_distances_single_structure(coordinates1, coordinates2, box, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_distances_single_structure(coordinates1, coordinates2, box)
    from molsysmt.lib.structure.get_mic_distances import get_mic_distances_single_structure as _nb
    return _nb(coordinates1, coordinates2, box)


def get_mic_distances_pairs_single_structure(coordinates1, coordinates2, box, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_distances_pairs_single_structure(coordinates1, coordinates2, box)
    from molsysmt.lib.structure.get_mic_distances import (
        get_mic_distances_pairs_single_structure as _nb)
    return _nb(coordinates1, coordinates2, box)


# --------------------------------------------------------------------------- neighbour list
# Dispatch of molsysmt.lib.structure.neighbor_list.neighbor_list_csr_multi (the hot
# kernel behind get_contacts and get_neighbors). Bit-for-bit identical results.

def neighbor_list_csr_multi(query_coords, ref_coords=None, box=None, cutoff=None,
                            exclude_self=True, sort_by_distance=False, backend=None):
    if _use_rust(backend):
        import numpy as np
        q = np.ascontiguousarray(query_coords, dtype=np.float64)
        r = q if ref_coords is None else np.ascontiguousarray(ref_coords, dtype=np.float64)
        b = None if box is None else np.ascontiguousarray(box, dtype=np.float64)
        return _rust.neighbor_list_csr_multi(q, r, b, float(cutoff), bool(exclude_self),
                                             bool(sort_by_distance))
    from molsysmt.lib.structure.neighbor_list import neighbor_list_csr_multi as _nb
    return _nb(query_coords, ref_coords, box, cutoff,
               exclude_self=exclude_self, sort_by_distance=sort_by_distance)


# --------------------------------------------------------------------------- SASA
# Dispatch of the cell-list Shrake-Rupley kernels
# (molsysmt.lib.structure.get_sasa.{get_sasa_cell_list, get_mic_sasa_cell_list}).

def get_sasa_cell_list(coordinates, radii, sphere_points, probe_radius, cutoff,
                       backend=None):
    if _use_rust(backend):
        return _rust.get_sasa_cell_list(coordinates, radii, sphere_points,
                                        float(probe_radius), float(cutoff))
    from molsysmt.lib.structure.get_sasa import get_sasa_cell_list as _nb
    return _nb(coordinates, radii, sphere_points, probe_radius, cutoff)


def get_mic_sasa_cell_list(coordinates, box, radii, sphere_points, probe_radius, cutoff,
                           backend=None):
    if _use_rust(backend):
        return _rust.get_mic_sasa_cell_list(coordinates, box, radii, sphere_points,
                                            float(probe_radius), float(cutoff))
    from molsysmt.lib.structure.get_sasa import get_mic_sasa_cell_list as _nb
    return _nb(coordinates, box, radii, sphere_points, probe_radius, cutoff)


# --------------------------------------------------------------------------- angles
# Dispatch of molsysmt.lib.structure.{get_angles, get_mic_angles}.* — on the
# hbonds.get_luzard_chandler_hbonds path.

def get_angles(coordinates, triplets, backend=None):
    if _use_rust(backend):
        return _rust.get_angles(coordinates, triplets)
    from molsysmt.lib.structure.get_angles import get_angles as _nb
    return _nb(coordinates, triplets)


def get_angles_single_structure(coordinates, triplets, backend=None):
    if _use_rust(backend):
        return _rust.get_angles_single_structure(coordinates, triplets)
    from molsysmt.lib.structure.get_angles import get_angles_single_structure as _nb
    return _nb(coordinates, triplets)


def get_mic_angles(coordinates, box, triplets, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_angles(coordinates, box, triplets)
    from molsysmt.lib.structure.get_mic_angles import get_mic_angles as _nb
    return _nb(coordinates, box, triplets)


def get_mic_angles_single_structure(coordinates, box, triplets, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_angles_single_structure(coordinates, box, triplets)
    from molsysmt.lib.structure.get_mic_angles import get_mic_angles_single_structure as _nb
    return _nb(coordinates, box, triplets)


# --------------------------------------------------------------------------- distances
# Dispatch of molsysmt.lib.structure.get_distances.* (the vacuum counterpart of the MIC
# family; the full-matrix fallback used by get_neighbors / get_contacts).

def get_distances_single_system(coordinates, backend=None):
    if _use_rust(backend):
        return _rust.get_distances_single_system(coordinates)
    from molsysmt.lib.structure.get_distances import get_distances_single_system as _nb
    return _nb(coordinates)


def get_distances(coordinates1, coordinates2, backend=None):
    if _use_rust(backend):
        return _rust.get_distances(coordinates1, coordinates2)
    from molsysmt.lib.structure.get_distances import get_distances as _nb
    return _nb(coordinates1, coordinates2)


def get_distances_pairs(coordinates1, coordinates2, backend=None):
    if _use_rust(backend):
        return _rust.get_distances_pairs(coordinates1, coordinates2)
    from molsysmt.lib.structure.get_distances import get_distances_pairs as _nb
    return _nb(coordinates1, coordinates2)


def get_distances_single_system_single_structure(coordinates, backend=None):
    if _use_rust(backend):
        return _rust.get_distances_single_system_single_structure(coordinates)
    from molsysmt.lib.structure.get_distances import (
        get_distances_single_system_single_structure as _nb)
    return _nb(coordinates)


def get_distances_single_structure(coordinates1, coordinates2, backend=None):
    if _use_rust(backend):
        return _rust.get_distances_single_structure(coordinates1, coordinates2)
    from molsysmt.lib.structure.get_distances import get_distances_single_structure as _nb
    return _nb(coordinates1, coordinates2)


def get_distances_pairs_single_structure(coordinates1, coordinates2, backend=None):
    if _use_rust(backend):
        return _rust.get_distances_pairs_single_structure(coordinates1, coordinates2)
    from molsysmt.lib.structure.get_distances import (
        get_distances_pairs_single_structure as _nb)
    return _nb(coordinates1, coordinates2)


# --------------------------------------------------------------------------- dihedrals
# Dispatch of molsysmt.lib.structure.{get_dihedral_angles, get_mic_dihedral_angles}.*

def get_dihedral_angles(coordinates, quartets, backend=None):
    if _use_rust(backend):
        return _rust.get_dihedral_angles(coordinates, quartets)
    from molsysmt.lib.structure.get_dihedral_angles import get_dihedral_angles as _nb
    return _nb(coordinates, quartets)


def get_dihedral_angles_single_structure(coordinates, quartets, backend=None):
    if _use_rust(backend):
        return _rust.get_dihedral_angles_single_structure(coordinates, quartets)
    from molsysmt.lib.structure.get_dihedral_angles import (
        get_dihedral_angles_single_structure as _nb)
    return _nb(coordinates, quartets)


def get_mic_dihedral_angles(coordinates, box, quartets, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_dihedral_angles(coordinates, box, quartets)
    from molsysmt.lib.structure.get_mic_dihedral_angles import get_mic_dihedral_angles as _nb
    return _nb(coordinates, box, quartets)


def get_mic_dihedral_angles_single_structure(coordinates, box, quartets, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_dihedral_angles_single_structure(coordinates, box, quartets)
    from molsysmt.lib.structure.get_mic_dihedral_angles import (
        get_mic_dihedral_angles_single_structure as _nb)
    return _nb(coordinates, box, quartets)


# --------------------------------------------------------------------------- math helpers
# Dispatch of molsysmt.lib.math.* (the largest njit file). Note rodrigues_rotation:
# the Numba version rotates its argument in place and returns None, the Rust one
# returns the rotated vector — the seam normalises both to "return the rotated vector".

def matmul(m, v, backend=None):
    if _use_rust(backend):
        return _rust.matmul(m, v)
    from molsysmt.lib.math import matmul as _nb
    return _nb(m, v)


def transpmatmul(m, v, backend=None):
    if _use_rust(backend):
        return _rust.transpmatmul(m, v)
    from molsysmt.lib.math import transpmatmul as _nb
    return _nb(m, v)


def normalize_vector(a, backend=None):
    if _use_rust(backend):
        return _rust.normalize_vector(a)
    from molsysmt.lib.math import normalize_vector as _nb
    return _nb(a)


def inverse_matrix_3x3(m, backend=None):
    if _use_rust(backend):
        return _rust.inverse_matrix_3x3(m)
    from molsysmt.lib.math import inverse_matrix_3x3 as _nb
    return _nb(m)


def quaternion_to_rotation_matrix(q, backend=None):
    if _use_rust(backend):
        return _rust.quaternion_to_rotation_matrix(q)
    from molsysmt.lib.math import quaternion_to_rotation_matrix as _nb
    return _nb(q)


def rodrigues_rotation(vector, unit_vector, angle, backend=None):
    """Returns the rotated vector (never mutates the caller's array)."""
    import numpy as np
    if _use_rust(backend):
        return _rust.rodrigues_rotation(vector, unit_vector, angle)
    from molsysmt.lib.math import rodrigues_rotation as _nb
    tmp = np.array(vector, dtype=np.float64, copy=True)
    _nb(tmp, np.ascontiguousarray(unit_vector, dtype=np.float64), angle)
    return tmp


# --------------------------------------------------------------------------- dihedral edits
# Dispatch of molsysmt.lib.structure.{set,shift}[_mic]_dihedral_angles.*
# These kernels MUTATE `coordinates` in place; the seam preserves that contract.

def _dihedral_edit(name, rust_fn, args, backend):
    if _use_rust(backend):
        return rust_fn(*args)
    import importlib
    mod = importlib.import_module(f"molsysmt.lib.structure.{name}")
    return getattr(mod, name if not name.endswith("_single") else name)(*args)


def shift_dihedral_angles_single_structure(coordinates, angles, quartets, blocks, backend=None):
    if _use_rust(backend):
        return _rust.shift_dihedral_angles_single_structure(coordinates, angles, quartets, blocks)
    from molsysmt.lib.structure.shift_dihedral_angles import (
        shift_dihedral_angles_single_structure as _nb)
    return _nb(coordinates, angles, quartets, blocks)


def set_dihedral_angles_single_structure(coordinates, angles, quartets, blocks, backend=None):
    if _use_rust(backend):
        return _rust.set_dihedral_angles_single_structure(coordinates, angles, quartets, blocks)
    from molsysmt.lib.structure.set_dihedral_angles import (
        set_dihedral_angles_single_structure as _nb)
    return _nb(coordinates, angles, quartets, blocks)


def shift_dihedral_angles(coordinates, angles, quartets, blocks, structure_indices, backend=None):
    if _use_rust(backend):
        return _rust.shift_dihedral_angles(coordinates, angles, quartets, blocks, structure_indices)
    from molsysmt.lib.structure.shift_dihedral_angles import shift_dihedral_angles as _nb
    return _nb(coordinates, angles, quartets, blocks, structure_indices)


def set_dihedral_angles(coordinates, angles, quartets, blocks, backend=None):
    """Upstream takes no structure_indices (it walks every structure) and is the only
    variant that broadcasts a size-1 `angles` dimension."""
    if _use_rust(backend):
        return _rust.set_dihedral_angles(coordinates, angles, quartets, blocks)
    from molsysmt.lib.structure.set_dihedral_angles import set_dihedral_angles as _nb
    return _nb(coordinates, angles, quartets, blocks)


def shift_mic_dihedral_angles_single_structure(coordinates, box, angles, quartets, blocks,
                                               backend=None):
    if _use_rust(backend):
        return _rust.shift_mic_dihedral_angles_single_structure(
            coordinates, box, angles, quartets, blocks)
    from molsysmt.lib.structure.shift_mic_dihedral_angles import (
        shift_mic_dihedral_angles_single_structure as _nb)
    return _nb(coordinates, box, angles, quartets, blocks)


def set_mic_dihedral_angles_single_structure(coordinates, box, angles, quartets, blocks,
                                             backend=None):
    if _use_rust(backend):
        return _rust.set_mic_dihedral_angles_single_structure(
            coordinates, box, angles, quartets, blocks)
    from molsysmt.lib.structure.set_mic_dihedral_angles import (
        set_mic_dihedral_angles_single_structure as _nb)
    return _nb(coordinates, box, angles, quartets, blocks)


# Multi-structure variants. NOTE the upstream signatures are asymmetric: set_* take no
# structure_indices, shift_* do. See devguide/pending_bugs/
# dihedral_angles_broadcast_mismatch_pbc.md

def set_mic_dihedral_angles(coordinates, box, angles, quartets, blocks, backend=None):
    if _use_rust(backend):
        return _rust.set_mic_dihedral_angles(coordinates, box, angles, quartets, blocks)
    from molsysmt.lib.structure.set_mic_dihedral_angles import set_mic_dihedral_angles as _nb
    return _nb(coordinates, box, angles, quartets, blocks)


def shift_mic_dihedral_angles(coordinates, box, angles, quartets, blocks, structure_indices,
                              backend=None):
    if _use_rust(backend):
        return _rust.shift_mic_dihedral_angles(coordinates, box, angles, quartets, blocks,
                                               structure_indices)
    from molsysmt.lib.structure.shift_mic_dihedral_angles import shift_mic_dihedral_angles as _nb
    return _nb(coordinates, box, angles, quartets, blocks, structure_indices)


# --------------------------------------------------------------------------------- pbc
# Block 9: molsysmt.lib.pbc — box geometry plus the wrap/unwrap family.
#
# The `*_vector_single_structure` helpers take `inv_box`/`orthogonal` as optional
# precomputed values upstream; the Rust ports always recompute them from `box` (the same
# way the whole-system kernels do), so the seam simply drops them on the Rust path.
#
# `wrap_to_pbc`, `wrap_to_pbc_center`, `wrap_to_mic` and `unwrap` mutate `coordinates`
# in place and return None, on both backends.

def box_is_orthogonal_single_structure(box, backend=None):
    if _use_rust(backend):
        return _rust.box_is_orthogonal_single_structure(box)
    from molsysmt.lib.pbc.box_is_orthogonal import box_is_orthogonal_single_structure as _nb
    return _nb(box)


def box_is_orthogonal(box, backend=None):
    if _use_rust(backend):
        return _rust.box_is_orthogonal(box)
    from molsysmt.lib.pbc.box_is_orthogonal import box_is_orthogonal as _nb
    return _nb(box)


def get_lengths_from_box_single_structure(box, backend=None):
    if _use_rust(backend):
        return _rust.get_lengths_from_box_single_structure(box)
    from molsysmt.lib.pbc.get_lengths_from_box import get_lengths_from_box_single_structure as _nb
    return _nb(box)


def get_lengths_from_box(box, backend=None):
    if _use_rust(backend):
        return _rust.get_lengths_from_box(box)
    from molsysmt.lib.pbc.get_lengths_from_box import get_lengths_from_box as _nb
    return _nb(box)


def get_angles_from_box_single_structure(box, backend=None):
    if _use_rust(backend):
        return _rust.get_angles_from_box_single_structure(box)
    from molsysmt.lib.pbc.get_angles_from_box import get_angles_from_box_single_structure as _nb
    return _nb(box)


def get_angles_from_box(box, backend=None):
    if _use_rust(backend):
        return _rust.get_angles_from_box(box)
    from molsysmt.lib.pbc.get_angles_from_box import get_angles_from_box as _nb
    return _nb(box)


def get_lengths_and_angles_from_box_single_structure(box, backend=None):
    if _use_rust(backend):
        return _rust.get_lengths_and_angles_from_box_single_structure(box)
    from molsysmt.lib.pbc.get_lengths_and_angles_from_box import (
        get_lengths_and_angles_from_box_single_structure as _nb)
    return _nb(box)


def get_lengths_and_angles_from_box(box, backend=None):
    if _use_rust(backend):
        return _rust.get_lengths_and_angles_from_box(box)
    from molsysmt.lib.pbc.get_lengths_and_angles_from_box import (
        get_lengths_and_angles_from_box as _nb)
    return _nb(box)


def get_box_from_lengths_and_angles_single_structure(lengths, angles, backend=None):
    if _use_rust(backend):
        return _rust.get_box_from_lengths_and_angles_single_structure(lengths, angles)
    from molsysmt.lib.pbc.get_box_from_lengths_and_angles import (
        get_box_from_lengths_and_angles_single_structure as _nb)
    return _nb(lengths, angles)


def get_box_from_lengths_and_angles(lengths, angles, backend=None):
    if _use_rust(backend):
        return _rust.get_box_from_lengths_and_angles(lengths, angles)
    from molsysmt.lib.pbc.get_box_from_lengths_and_angles import (
        get_box_from_lengths_and_angles as _nb)
    return _nb(lengths, angles)


def wrap_to_pbc_vector_single_structure(vector, box, inv_box=None, orthogonal=None,
                                        backend=None):
    if _use_rust(backend):
        return _rust.wrap_to_pbc_vector_single_structure(vector, box)
    from molsysmt.lib.pbc.wrap_to_pbc import wrap_to_pbc_vector_single_structure as _nb
    return _nb(vector, box, inv_box, orthogonal)


def wrap_to_pbc_center_vector_single_structure(vector, box, inv_box=None, orthogonal=None,
                                               backend=None):
    if _use_rust(backend):
        return _rust.wrap_to_pbc_center_vector_single_structure(vector, box)
    from molsysmt.lib.pbc.wrap_to_pbc import wrap_to_pbc_center_vector_single_structure as _nb
    return _nb(vector, box, inv_box, orthogonal)


def wrap_to_mic_vector_single_structure(vector, box, inv_box=None, orthogonal=None,
                                        backend=None):
    if _use_rust(backend):
        return _rust.wrap_to_mic_vector_single_structure(vector, box)
    from molsysmt.lib.pbc.wrap_to_mic import wrap_to_mic_vector_single_structure as _nb
    return _nb(vector, box, inv_box, orthogonal)


def wrap_to_pbc(coordinates, box, box_origin, backend=None):
    if _use_rust(backend):
        return _rust.wrap_to_pbc(coordinates, box, box_origin)
    from molsysmt.lib.pbc.wrap_to_pbc import wrap_to_pbc as _nb
    return _nb(coordinates, box, box_origin)


def wrap_to_pbc_center(coordinates, box, box_center, backend=None):
    if _use_rust(backend):
        return _rust.wrap_to_pbc_center(coordinates, box, box_center)
    from molsysmt.lib.pbc.wrap_to_pbc import wrap_to_pbc_center as _nb
    return _nb(coordinates, box, box_center)


def wrap_to_mic(coordinates, box, mic_origin, backend=None):
    if _use_rust(backend):
        return _rust.wrap_to_mic(coordinates, box, mic_origin)
    from molsysmt.lib.pbc.wrap_to_mic import wrap_to_mic as _nb
    return _nb(coordinates, box, mic_origin)


def unwrap(coordinates, box, backend=None):
    if _use_rust(backend):
        return _rust.unwrap(coordinates, box)
    from molsysmt.lib.pbc.unwrap import unwrap as _nb
    return _nb(coordinates, box)


# ---------------------------------------------------------------------------- geometry
# Block 10: the mechanical long tail — weighted geometry, series encoding and the
# connected-component kernel.

def get_center_single_structure(coordinates, weights, backend=None):
    if _use_rust(backend):
        return _rust.get_center_single_structure(coordinates, weights)
    from molsysmt.lib.structure.get_center import get_center_single_structure as _nb
    return _nb(coordinates, weights)


def get_center(coordinates, weights, backend=None):
    if _use_rust(backend):
        return _rust.get_center(coordinates, weights)
    from molsysmt.lib.structure.get_center import get_center as _nb
    return _nb(coordinates, weights)


def get_center_groups_of_atoms_single_structure(coordinates, atoms_per_group, weights,
                                                backend=None):
    if _use_rust(backend):
        return _rust.get_center_groups_of_atoms_single_structure(
            coordinates, atoms_per_group, weights)
    from molsysmt.lib.structure.get_center import (
        get_center_groups_of_atoms_single_structure as _nb)
    return _nb(coordinates, atoms_per_group, weights)


def get_center_groups_of_atoms(coordinates, atoms_per_group, weights, backend=None):
    if _use_rust(backend):
        return _rust.get_center_groups_of_atoms(coordinates, atoms_per_group, weights)
    from molsysmt.lib.structure.get_center import get_center_groups_of_atoms as _nb
    return _nb(coordinates, atoms_per_group, weights)


def flip_single_structure(coordinates, vector, point, backend=None):
    if _use_rust(backend):
        return _rust.flip_single_structure(coordinates, vector, point)
    from molsysmt.lib.structure.flip import flip_single_structure as _nb
    return _nb(coordinates, vector, point)


def flip(coordinates, vector, point, backend=None):
    if _use_rust(backend):
        return _rust.flip(coordinates, vector, point)
    from molsysmt.lib.structure.flip import flip as _nb
    return _nb(coordinates, vector, point)


def get_radius_of_gyration_single_structure(coordinates, weights, backend=None):
    if _use_rust(backend):
        return _rust.get_radius_of_gyration_single_structure(coordinates, weights)
    from molsysmt.lib.structure.get_radius_of_gyration import (
        get_radius_of_gyration_single_structure as _nb)
    return _nb(coordinates, weights)


def get_radius_of_gyration(coordinates, weights, backend=None):
    if _use_rust(backend):
        return _rust.get_radius_of_gyration(coordinates, weights)
    from molsysmt.lib.structure.get_radius_of_gyration import get_radius_of_gyration as _nb
    return _nb(coordinates, weights)


def get_rmsf(coordinates, backend=None):
    if _use_rust(backend):
        return _rust.get_rmsf(coordinates)
    from molsysmt.lib.structure.get_rmsf import get_rmsf as _nb
    return _nb(coordinates)


# ------------------------------------------------------------------------------ series

def serie_to_chunks(serie, backend=None):
    if _use_rust(backend):
        return _rust.serie_to_chunks(serie)
    from molsysmt.lib.series import serie_to_chunks as _nb
    return _nb(serie)


def chunks_to_serie(starts, chunk_size, backend=None):
    if _use_rust(backend):
        return _rust.chunks_to_serie(starts, chunk_size)
    from molsysmt.lib.series import chunks_to_serie as _nb
    return _nb(starts, chunk_size)


def jit_serialize(item, backend=None):
    """`item` is a sequence of integer sequences.

    Numba needs it reflected into a typed list of typed lists; the Rust port takes the
    plain Python object, so the conversion happens only on the Numba path.
    """
    if _use_rust(backend):
        return _rust.jit_serialize([list(segment) for segment in item])
    import numba as nb
    from molsysmt.lib.series import _jit_serialize as _nb

    def _typed(segment):
        # an empty nb.typed.List cannot infer its item type, so build it explicitly
        out = nb.typed.List.empty_list(nb.int64)
        for value in segment:
            out.append(int(value))
        return out

    typed = nb.typed.List.empty_list(nb.types.ListType(nb.int64))
    for segment in item:
        typed.append(_typed(segment))
    return _nb(typed)


def occurrence_order(serie, backend=None):
    if _use_rust(backend):
        return _rust.occurrence_order(serie)
    from molsysmt.lib.series import occurrence_order as _nb
    return _nb(serie)


def occurrence_order_sorted_serie(serie, backend=None):
    if _use_rust(backend):
        return _rust.occurrence_order_sorted_serie(serie)
    from molsysmt.lib.series import occurrence_order_sorted_serie as _nb
    return _nb(serie)


# ---------------------------------------------------------------------------- topology

def get_component_index_from_bonded_atom_pairs(bonded_atom_pairs, n_atoms, backend=None):
    if _use_rust(backend):
        return _rust.get_component_index_from_bonded_atom_pairs(bonded_atom_pairs, n_atoms)
    from molsysmt.lib.topology.get_component_index_from_bonded_atom_pairs import (
        get_component_index_from_bonded_atom_pairs as _nb)
    return _nb(bonded_atom_pairs, n_atoms)


def _find_root(parent, node, backend=None):
    """Path-halving find. Mutates `parent` in place on both backends."""
    if _use_rust(backend):
        return _rust._find_root(parent, node)
    from molsysmt.lib.topology.get_component_index_from_bonded_atom_pairs import _find_root as _nb
    return _nb(parent, node)


def _union(parent, rank, node_1, node_2, backend=None):
    """Union by rank. Mutates `parent` and `rank` in place on both backends."""
    if _use_rust(backend):
        return _rust._union(parent, rank, node_1, node_2)
    from molsysmt.lib.topology.get_component_index_from_bonded_atom_pairs import _union as _nb
    return _nb(parent, rank, node_1, node_2)


# -------------------------------------------------------------------------------- rmsd
# Block 11. `get_rmsd` is a plain reduction; the `least_rmsd` family superposes first via
# the quaternion (Horn/Kearsley) method, whose 4x4 eigenproblem Rust solves with
# `nalgebra` rather than LAPACK. Parity is at tolerance there -- different eigensolver,
# `fastmath`, and upstream's pairwise `np.sum` for the centroid.

def get_rmsd_single_structure(coordinates, reference_coordinates, backend=None):
    if _use_rust(backend):
        return _rust.get_rmsd_single_structure(coordinates, reference_coordinates)
    from molsysmt.lib.structure.get_rmsd import get_rmsd_single_structure as _nb
    return _nb(coordinates, reference_coordinates)


def get_rmsd(coordinates, reference_coordinates, backend=None):
    if _use_rust(backend):
        return _rust.get_rmsd(coordinates, reference_coordinates)
    from molsysmt.lib.structure.get_rmsd import get_rmsd as _nb
    return _nb(coordinates, reference_coordinates)


def get_rmsd_with_single_reference_structure(coordinates, reference_coordinates,
                                             backend=None):
    if _use_rust(backend):
        return _rust.get_rmsd_with_single_reference_structure(
            coordinates, reference_coordinates)
    from molsysmt.lib.structure.get_rmsd import (
        get_rmsd_with_single_reference_structure as _nb)
    return _nb(coordinates, reference_coordinates)


def get_least_rmsd_single_structure(coordinates, reference_coordinates, backend=None):
    if _use_rust(backend):
        return _rust.get_least_rmsd_single_structure(coordinates, reference_coordinates)
    from molsysmt.lib.structure.get_least_rmsd import get_least_rmsd_single_structure as _nb
    return _nb(coordinates, reference_coordinates)


def get_least_rmsd(coordinates, reference_coordinates, backend=None):
    if _use_rust(backend):
        return _rust.get_least_rmsd(coordinates, reference_coordinates)
    from molsysmt.lib.structure.get_least_rmsd import get_least_rmsd as _nb
    return _nb(coordinates, reference_coordinates)


def get_least_rmsd_with_single_reference_structure(coordinates, reference_coordinates,
                                                   backend=None):
    if _use_rust(backend):
        return _rust.get_least_rmsd_with_single_reference_structure(
            coordinates, reference_coordinates)
    from molsysmt.lib.structure.get_least_rmsd import (
        get_least_rmsd_with_single_reference_structure as _nb)
    return _nb(coordinates, reference_coordinates)


def get_least_rmsd_rotation_and_translation_single_structure(
        coordinates, reference_coordinates, backend=None):
    if _use_rust(backend):
        return _rust.get_least_rmsd_rotation_and_translation_single_structure(
            coordinates, reference_coordinates)
    from molsysmt.lib.structure.get_least_rmsd_rotation_and_translation import (
        get_least_rmsd_rotation_and_translation_single_structure as _nb)
    return _nb(coordinates, reference_coordinates)


def get_least_rmsd_rotation_and_translation(coordinates, reference_coordinates,
                                            backend=None):
    if _use_rust(backend):
        return _rust.get_least_rmsd_rotation_and_translation(
            coordinates, reference_coordinates)
    from molsysmt.lib.structure.get_least_rmsd_rotation_and_translation import (
        get_least_rmsd_rotation_and_translation as _nb)
    return _nb(coordinates, reference_coordinates)


def get_least_rmsd_rotation_and_translation_with_single_reference_structure(
        coordinates, reference_coordinates, backend=None):
    if _use_rust(backend):
        return _rust.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
            coordinates, reference_coordinates)
    from molsysmt.lib.structure.get_least_rmsd_rotation_and_translation import (
        get_least_rmsd_rotation_and_translation_with_single_reference_structure as _nb)
    return _nb(coordinates, reference_coordinates)


# -------------------------------------------------------------------------------- axes
# Block 12. 3x3 symmetric eigenproblems, solved with `nalgebra`.
#
# Eigenvectors are defined only up to sign. Upstream returns whatever LAPACK produces;
# the Rust port fixes the sign deterministically (largest-magnitude component positive),
# so switching backend cannot flip an axis. Compare eigenvectors up to sign.

def get_principal_inertia_axes_single_structure(coordinates, weights, backend=None):
    if _use_rust(backend):
        return _rust.get_principal_inertia_axes_single_structure(coordinates, weights)
    from molsysmt.lib.structure.get_principal_inertia_axes import (
        get_principal_inertia_axes_single_structure as _nb)
    return _nb(coordinates, weights)


def get_principal_inertia_axes(coordinates, weights, backend=None):
    if _use_rust(backend):
        return _rust.get_principal_inertia_axes(coordinates, weights)
    from molsysmt.lib.structure.get_principal_inertia_axes import (
        get_principal_inertia_axes as _nb)
    return _nb(coordinates, weights)


def get_principal_geometric_axes_single_structure(coordinates, weights, backend=None):
    if _use_rust(backend):
        return _rust.get_principal_geometric_axes_single_structure(coordinates, weights)
    from molsysmt.lib.structure.get_principal_geometric_axes import (
        get_principal_geometric_axes_single_structure as _nb)
    return _nb(coordinates, weights)


def get_principal_geometric_axes(coordinates, weights, backend=None):
    if _use_rust(backend):
        return _rust.get_principal_geometric_axes(coordinates, weights)
    from molsysmt.lib.structure.get_principal_geometric_axes import (
        get_principal_geometric_axes as _nb)
    return _nb(coordinates, weights)


# --------------------------------------------------------------------------------- pca
# Block 13, the last CPU kernel. The covariance is built as a matrix product (faer
# rank-k) rather than upstream's triple loop, and diagonalised with faer's dense
# self-adjoint eigensolver. Eigenvalues are at tolerance; eigenvectors carry a sign
# ambiguity (fixed deterministically here) and, when n_structures < n_features, a
# degenerate null space that no element-wise comparison can match.

def principal_component_analysis(coordinates, weights, backend=None):
    if _use_rust(backend):
        return _rust.principal_component_analysis(coordinates, weights)
    from molsysmt.lib.structure.principal_component_analysis import (
        principal_component_analysis as _nb)
    return _nb(coordinates, weights)


# ------------------------------------------------------------------- minimum distance
# molsysmt.lib.math brute-force minimum-distance kernels (used by build_peptide).

def minimum_distance_masked_not_bonded(coordinates, include_mask, bonded_matrix,
                                       backend=None):
    if _use_rust(backend):
        return _rust.minimum_distance_masked_not_bonded(coordinates, include_mask,
                                                        bonded_matrix)
    from molsysmt.lib.math import minimum_distance_masked_not_bonded as _nb
    return _nb(coordinates, include_mask, bonded_matrix)


def minimum_distance_between_coordinate_sets(existing_coordinates, existing_mask,
                                             candidate_coordinates, candidate_mask,
                                             candidate_start_index, bonded_matrix,
                                             backend=None):
    if _use_rust(backend):
        return _rust.minimum_distance_between_coordinate_sets(
            existing_coordinates, existing_mask, candidate_coordinates, candidate_mask,
            candidate_start_index, bonded_matrix)
    from molsysmt.lib.math import minimum_distance_between_coordinate_sets as _nb
    return _nb(existing_coordinates, existing_mask, candidate_coordinates, candidate_mask,
               candidate_start_index, bonded_matrix)


# ------------------------------------------------------------------- brute-force SASA
# The small-system Shrake-Rupley path (below configure CELL_LIST_MIN_ATOMS).

def get_sasa(coordinates, radii, sphere_points, probe_radius, backend=None):
    if _use_rust(backend):
        return _rust.get_sasa(coordinates, radii, sphere_points, probe_radius)
    from molsysmt.lib.structure.get_sasa import get_sasa as _nb
    return _nb(coordinates, radii, sphere_points, probe_radius)


def get_mic_sasa(coordinates, box, radii, sphere_points, probe_radius, backend=None):
    if _use_rust(backend):
        return _rust.get_mic_sasa(coordinates, box, radii, sphere_points, probe_radius)
    from molsysmt.lib.structure.get_sasa import get_mic_sasa as _nb
    return _nb(coordinates, box, radii, sphere_points, probe_radius)
