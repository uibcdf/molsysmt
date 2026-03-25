"""
CUDA kernels for pairwise distance calculations.

Requires: numba with CUDA support (``numba[cuda]``) and a CUDA-capable GPU.

Kernels
-------
get_distances_single_system(coordinates) -> distances
    All-vs-all pairwise distances for a single molecular system.
    Equivalent to the CPU ``@lazy_njit`` version in ``get_distances.py``
    but dispatched across CUDA thread blocks.

get_distances(coordinates1, coordinates2) -> distances
    Cross-system pairwise distances (atoms in system 1 vs atoms in system 2).

Both functions accept/return plain numpy float64 arrays (units are handled
by the public wrapper layer, not here).
"""

from __future__ import annotations

import math
import numpy as np


# ---------------------------------------------------------------------------
# CUDA device helpers
# ---------------------------------------------------------------------------

try:
    from numba import cuda

    @cuda.jit(device=True)
    def _dist3d(ax, ay, az, bx, by, bz):
        """Euclidean distance between two 3-D points (device function)."""
        dx = bx - ax
        dy = by - ay
        dz = bz - az
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    # -----------------------------------------------------------------------
    # Single-system all-vs-all kernel
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_distances_single_system_kernel(coords, out):
        """
        Thread assignment: (frame, atom_i, atom_j).

        coords : (n_structures, n_atoms, 3)  float64
        out    : (n_structures, n_atoms, n_atoms)  float64
        """
        ii, jj, kk = cuda.grid(3)
        n_structures = coords.shape[0]
        n_atoms = coords.shape[1]

        if ii >= n_structures or jj >= n_atoms or kk >= n_atoms:
            return

        d = _dist3d(
            coords[ii, jj, 0], coords[ii, jj, 1], coords[ii, jj, 2],
            coords[ii, kk, 0], coords[ii, kk, 1], coords[ii, kk, 2],
        )
        out[ii, jj, kk] = d

    # -----------------------------------------------------------------------
    # Cross-system kernel
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_distances_kernel(coords1, coords2, out):
        """
        Thread assignment: (frame, atom_i, atom_j).

        coords1 : (n_structures, n_atoms1, 3)  float64
        coords2 : (n_structures, n_atoms2, 3)  float64
        out     : (n_structures, n_atoms1, n_atoms2)  float64
        """
        ii, jj, kk = cuda.grid(3)
        n_structures = coords1.shape[0]
        n_atoms1 = coords1.shape[1]
        n_atoms2 = coords2.shape[1]

        if ii >= n_structures or jj >= n_atoms1 or kk >= n_atoms2:
            return

        d = _dist3d(
            coords1[ii, jj, 0], coords1[ii, jj, 1], coords1[ii, jj, 2],
            coords2[ii, kk, 0], coords2[ii, kk, 1], coords2[ii, kk, 2],
        )
        out[ii, jj, kk] = d

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Python-level entry points  (same signatures as CPU counterparts)
# ---------------------------------------------------------------------------

def get_distances_single_system(coordinates: np.ndarray) -> np.ndarray:
    """
    All-vs-all pairwise distances on GPU.

    Parameters
    ----------
    coordinates : np.ndarray, shape (n_structures, n_atoms, 3), float64
        Coordinates in any consistent length unit (nm recommended).

    Returns
    -------
    np.ndarray, shape (n_structures, n_atoms, n_atoms), float64
        Symmetric distance matrix per structure.
    """
    n_structures, n_atoms, _ = coordinates.shape
    out = np.zeros((n_structures, n_atoms, n_atoms), dtype=np.float64)

    # Grid: thread per (frame, atom_i, atom_j)
    threads_per_block = (4, 8, 8)  # 256 threads/block
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_atoms      / threads_per_block[1]),
        math.ceil(n_atoms      / threads_per_block[2]),
    )

    d_coords = cuda.to_device(coordinates)
    d_out    = cuda.to_device(out)

    _get_distances_single_system_kernel[blocks, threads_per_block](d_coords, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out


def get_distances(coordinates1: np.ndarray, coordinates2: np.ndarray) -> np.ndarray:
    """
    Cross-system pairwise distances on GPU.

    Parameters
    ----------
    coordinates1 : np.ndarray, shape (n_structures, n_atoms1, 3), float64
    coordinates2 : np.ndarray, shape (n_structures, n_atoms2, 3), float64

    Returns
    -------
    np.ndarray, shape (n_structures, n_atoms1, n_atoms2), float64
    """
    n_structures, n_atoms1, _ = coordinates1.shape
    n_atoms2 = coordinates2.shape[1]
    out = np.zeros((n_structures, n_atoms1, n_atoms2), dtype=np.float64)

    threads_per_block = (4, 8, 8)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_atoms1     / threads_per_block[1]),
        math.ceil(n_atoms2     / threads_per_block[2]),
    )

    d_c1  = cuda.to_device(coordinates1)
    d_c2  = cuda.to_device(coordinates2)
    d_out = cuda.to_device(out)

    _get_distances_kernel[blocks, threads_per_block](d_c1, d_c2, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out
