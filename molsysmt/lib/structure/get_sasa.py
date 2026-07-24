"""
Parallel CPU JIT compiled Shrake-Rupley SASA calculations.

Accelerated using Numba JIT and multi-threaded ``nb.prange`` loops.
"""

from __future__ import annotations

import math
import numpy as np
import numba as nb
from molsysmt._private.jit import lazy_njit
from .get_sasa_cuda import get_fibonacci_sphere_points


# ---------------------------------------------------------------------------
# JIT CPU helpers
# ---------------------------------------------------------------------------

@nb.njit(cache=True)
def _is_orthogonal(box_s):
    tol = 1e-10
    return (
        abs(box_s[0, 1]) < tol and abs(box_s[0, 2]) < tol and
        abs(box_s[1, 0]) < tol and abs(box_s[1, 2]) < tol and
        abs(box_s[2, 0]) < tol and abs(box_s[2, 2]) < tol
    )

@nb.njit(cache=True)
def _mic_wrap_vector_orthogonal(dx, dy, dz, lx, ly, lz):
    rx = dx - lx * math.floor(dx / lx + 0.5)
    ry = dy - ly * math.floor(dy / ly + 0.5)
    rz = dz - lz * math.floor(dz / lz + 0.5)
    return rx, ry, rz

@nb.njit(cache=True)
def _mic_wrap_vector_triclinic(dx, dy, dz, box_s):
    b00 = box_s[0, 0]; b01 = box_s[0, 1]; b02 = box_s[0, 2]
    b10 = box_s[1, 0]; b11 = box_s[1, 1]; b12 = box_s[1, 2]
    b20 = box_s[2, 0]; b21 = box_s[2, 1]; b22 = box_s[2, 2]

    det = (b00 * (b11 * b22 - b12 * b21)
         - b01 * (b10 * b22 - b12 * b20)
         + b02 * (b10 * b21 - b11 * b20))

    inv00 = (b11 * b22 - b12 * b21) / det
    inv01 = (b02 * b21 - b01 * b22) / det
    inv02 = (b01 * b12 - b02 * b11) / det
    inv10 = (b12 * b20 - b10 * b22) / det
    inv11 = (b00 * b22 - b02 * b20) / det
    inv12 = (b02 * b10 - b00 * b12) / det
    inv20 = (b10 * b21 - b11 * b20) / det
    inv21 = (b01 * b20 - b00 * b21) / det
    inv22 = (b00 * b11 - b01 * b10) / det

    sx = inv00 * dx + inv01 * dy + inv02 * dz
    sy = inv10 * dx + inv11 * dy + inv12 * dz
    sz = inv20 * dx + inv21 * dy + inv22 * dz

    sx -= math.floor(sx + 0.5)
    sy -= math.floor(sy + 0.5)
    sz -= math.floor(sz + 0.5)

    cx = b00 * sx + b01 * sy + b02 * sz
    cy = b10 * sx + b11 * sy + b12 * sz
    cz = b20 * sx + b21 * sy + b22 * sz

    return cx, cy, cz

@nb.njit(cache=True)
def _mic_wrap_vector(dx, dy, dz, box_s):
    if _is_orthogonal(box_s):
        return _mic_wrap_vector_orthogonal(
            dx, dy, dz,
            box_s[0, 0], box_s[1, 1], box_s[2, 2]
        )
    else:
        return _mic_wrap_vector_triclinic(dx, dy, dz, box_s)


# ---------------------------------------------------------------------------
# Parallel CPU Shrake-Rupley Implementations
# ---------------------------------------------------------------------------

@lazy_njit(
    nb.float64[:,:](nb.float64[:,:,:], nb.float64[:], nb.float64[:,:], nb.float64),
    parallel=True,
    cache=True
)
def get_sasa(
    coordinates: np.ndarray,
    radii: np.ndarray,
    sphere_points: np.ndarray,
    probe_radius: float = 0.14
) -> np.ndarray:
    """SASA JIT CPU loop parallelized over frames and atoms."""
    n_structures = coordinates.shape[0]
    n_atoms = coordinates.shape[1]
    n_points = sphere_points.shape[0]
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)

    for ii in nb.prange(n_structures):
        for jj in nb.prange(n_atoms):
            r_i_ext = radii[jj] + probe_radius
            if r_i_ext <= probe_radius:
                out[ii, jj] = 0.0
                continue

            accessible_count = 0
            for kk in range(n_points):
                px = coordinates[ii, jj, 0] + r_i_ext * sphere_points[kk, 0]
                py = coordinates[ii, jj, 1] + r_i_ext * sphere_points[kk, 1]
                pz = coordinates[ii, jj, 2] + r_i_ext * sphere_points[kk, 2]

                is_accessible = True
                for ll in range(n_atoms):
                    if ll == jj:
                        continue
                    r_l_ext = radii[ll] + probe_radius
                    if r_l_ext <= probe_radius:
                        continue

                    dx = px - coordinates[ii, ll, 0]
                    dy = py - coordinates[ii, ll, 1]
                    dz = pz - coordinates[ii, ll, 2]

                    dist_sq = dx*dx + dy*dy + dz*dz
                    if dist_sq < r_l_ext * r_l_ext:
                        is_accessible = False
                        break

                if is_accessible:
                    accessible_count += 1

            out[ii, jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    return out


@lazy_njit(
    nb.float64[:,:](nb.float64[:,:,:], nb.float64[:,:,:], nb.float64[:], nb.float64[:,:], nb.float64),
    parallel=True,
    cache=True
)
def get_mic_sasa(
    coordinates: np.ndarray,
    box: np.ndarray,
    radii: np.ndarray,
    sphere_points: np.ndarray,
    probe_radius: float = 0.14
) -> np.ndarray:
    """SASA JIT CPU loop with MIC parallelized over frames and atoms."""
    n_structures = coordinates.shape[0]
    n_atoms = coordinates.shape[1]
    n_points = sphere_points.shape[0]
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)

    for ii in nb.prange(n_structures):
        box_s = box[ii]
        for jj in nb.prange(n_atoms):
            r_i_ext = radii[jj] + probe_radius
            if r_i_ext <= probe_radius:
                out[ii, jj] = 0.0
                continue

            accessible_count = 0
            for kk in range(n_points):
                px = coordinates[ii, jj, 0] + r_i_ext * sphere_points[kk, 0]
                py = coordinates[ii, jj, 1] + r_i_ext * sphere_points[kk, 1]
                pz = coordinates[ii, jj, 2] + r_i_ext * sphere_points[kk, 2]

                is_accessible = True
                for ll in range(n_atoms):
                    if ll == jj:
                        continue
                    r_l_ext = radii[ll] + probe_radius
                    if r_l_ext <= probe_radius:
                        continue

                    dx = px - coordinates[ii, ll, 0]
                    dy = py - coordinates[ii, ll, 1]
                    dz = pz - coordinates[ii, ll, 2]
                    dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box_s)

                    dist_sq = dx*dx + dy*dy + dz*dz
                    if dist_sq < r_l_ext * r_l_ext:
                        is_accessible = False
                        break

                if is_accessible:
                    accessible_count += 1

            out[ii, jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    return out


# ---------------------------------------------------------------------------
# Cell-list accelerated Shrake-Rupley (single frame, CSR candidate neighbours)
# ---------------------------------------------------------------------------
#
# The occlusion scan is restricted to the CSR candidate neighbours of each atom
# (built with a safe cutoff of ``2*max_radius + 2*probe_radius``), turning the
# per-frame cost from O(N**2 * n_points) into ~O(N * n_points). Results are
# numerically identical to the brute-force kernels above.

@lazy_njit(
    nb.float64[:](nb.float64[:,:], nb.float64[:], nb.float64[:,:], nb.float64,
                  nb.int64[:], nb.int64[:]),
    parallel=True,
    cache=True
)
def get_sasa_cell_list(
    coordinates: np.ndarray,
    radii: np.ndarray,
    sphere_points: np.ndarray,
    probe_radius: float,
    neighbor_offsets: np.ndarray,
    neighbor_indices: np.ndarray,
) -> np.ndarray:
    """Single-frame SASA over CSR candidate neighbours (vacuum)."""
    n_atoms = coordinates.shape[0]
    n_points = sphere_points.shape[0]
    out = np.zeros(n_atoms, dtype=np.float64)

    for jj in nb.prange(n_atoms):
        r_i_ext = radii[jj] + probe_radius
        if r_i_ext <= probe_radius:
            out[jj] = 0.0
            continue

        start = neighbor_offsets[jj]
        end = neighbor_offsets[jj + 1]

        accessible_count = 0
        for kk in range(n_points):
            px = coordinates[jj, 0] + r_i_ext * sphere_points[kk, 0]
            py = coordinates[jj, 1] + r_i_ext * sphere_points[kk, 1]
            pz = coordinates[jj, 2] + r_i_ext * sphere_points[kk, 2]

            is_accessible = True
            for p in range(start, end):
                ll = neighbor_indices[p]
                r_l_ext = radii[ll] + probe_radius
                if r_l_ext <= probe_radius:
                    continue

                dx = px - coordinates[ll, 0]
                dy = py - coordinates[ll, 1]
                dz = pz - coordinates[ll, 2]

                if dx*dx + dy*dy + dz*dz < r_l_ext * r_l_ext:
                    is_accessible = False
                    break

            if is_accessible:
                accessible_count += 1

        out[jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    return out


@lazy_njit(
    nb.float64[:](nb.float64[:,:], nb.float64[:,:], nb.float64[:], nb.float64[:,:],
                  nb.float64, nb.int64[:], nb.int64[:]),
    parallel=True,
    cache=True
)
def get_mic_sasa_cell_list(
    coordinates: np.ndarray,
    box_s: np.ndarray,
    radii: np.ndarray,
    sphere_points: np.ndarray,
    probe_radius: float,
    neighbor_offsets: np.ndarray,
    neighbor_indices: np.ndarray,
) -> np.ndarray:
    """Single-frame SASA over CSR candidate neighbours with minimum-image PBC."""
    n_atoms = coordinates.shape[0]
    n_points = sphere_points.shape[0]
    out = np.zeros(n_atoms, dtype=np.float64)

    for jj in nb.prange(n_atoms):
        r_i_ext = radii[jj] + probe_radius
        if r_i_ext <= probe_radius:
            out[jj] = 0.0
            continue

        start = neighbor_offsets[jj]
        end = neighbor_offsets[jj + 1]

        accessible_count = 0
        for kk in range(n_points):
            px = coordinates[jj, 0] + r_i_ext * sphere_points[kk, 0]
            py = coordinates[jj, 1] + r_i_ext * sphere_points[kk, 1]
            pz = coordinates[jj, 2] + r_i_ext * sphere_points[kk, 2]

            is_accessible = True
            for p in range(start, end):
                ll = neighbor_indices[p]
                r_l_ext = radii[ll] + probe_radius
                if r_l_ext <= probe_radius:
                    continue

                dx = px - coordinates[ll, 0]
                dy = py - coordinates[ll, 1]
                dz = pz - coordinates[ll, 2]
                dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box_s)

                if dx*dx + dy*dy + dz*dz < r_l_ext * r_l_ext:
                    is_accessible = False
                    break

            if is_accessible:
                accessible_count += 1

        out[jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    return out
