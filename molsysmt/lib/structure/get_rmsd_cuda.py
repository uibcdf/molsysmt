"""
CUDA kernels for RMSD calculation.

Requires: numba with CUDA support (``numba[cuda]``) and a CUDA-capable GPU.

Kernels
-------
get_rmsd(coordinates, reference_coordinates) -> rmsd
    Per-frame RMSD, many query frames vs. many reference frames (1-to-1).
    Equivalent to the CPU ``@lazy_njit`` version in ``get_rmsd.py``.

get_rmsd_with_single_reference_structure(coordinates, reference_coordinates) -> rmsd
    Per-frame RMSD against a single reference frame (broadcast).

Both functions accept/return plain numpy float64 arrays (units are handled
by the public wrapper layer, not here).
"""

from __future__ import annotations

import math
import numpy as np


# ---------------------------------------------------------------------------
# CUDA kernels
# ---------------------------------------------------------------------------

try:
    from numba import cuda

    @cuda.jit
    def _get_rmsd_kernel(coords, ref_coords, out):
        """
        Thread assignment: one thread per frame.

        coords     : (n_structures, n_atoms, 3)  float64
        ref_coords : (n_structures, n_atoms, 3)  float64
        out        : (n_structures,)              float64
        """
        ii = cuda.grid(1)
        if ii >= coords.shape[0]:
            return
        n_atoms = coords.shape[1]
        val = 0.0
        for jj in range(n_atoms):
            dx = ref_coords[ii, jj, 0] - coords[ii, jj, 0]
            dy = ref_coords[ii, jj, 1] - coords[ii, jj, 1]
            dz = ref_coords[ii, jj, 2] - coords[ii, jj, 2]
            val += dx * dx + dy * dy + dz * dz
        out[ii] = math.sqrt(val / n_atoms)

    @cuda.jit
    def _get_rmsd_single_ref_kernel(coords, ref_coords, out):
        """
        Thread assignment: one thread per frame.

        coords     : (n_structures, n_atoms, 3)  float64
        ref_coords : (n_atoms, 3)                float64
        out        : (n_structures,)              float64
        """
        ii = cuda.grid(1)
        if ii >= coords.shape[0]:
            return
        n_atoms = coords.shape[1]
        val = 0.0
        for jj in range(n_atoms):
            dx = ref_coords[jj, 0] - coords[ii, jj, 0]
            dy = ref_coords[jj, 1] - coords[ii, jj, 1]
            dz = ref_coords[jj, 2] - coords[ii, jj, 2]
            val += dx * dx + dy * dy + dz * dz
        out[ii] = math.sqrt(val / n_atoms)

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Python-level entry points  (same signatures as CPU counterparts)
# ---------------------------------------------------------------------------

def get_rmsd(coordinates: np.ndarray, reference_coordinates: np.ndarray) -> np.ndarray:
    """
    Per-frame RMSD on GPU.

    Parameters
    ----------
    coordinates : np.ndarray, shape (n_structures, n_atoms, 3), float64
    reference_coordinates : np.ndarray, shape (n_structures, n_atoms, 3), float64

    Returns
    -------
    np.ndarray, shape (n_structures,), float64
    """
    n_structures = coordinates.shape[0]
    out = np.zeros(n_structures, dtype=np.float64)

    threads_per_block = 256
    blocks = math.ceil(n_structures / threads_per_block)

    d_c = cuda.to_device(coordinates)
    d_r = cuda.to_device(reference_coordinates)
    d_out = cuda.to_device(out)

    _get_rmsd_kernel[blocks, threads_per_block](d_c, d_r, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out


def get_rmsd_with_single_reference_structure(
    coordinates: np.ndarray, reference_coordinates: np.ndarray
) -> np.ndarray:
    """
    Per-frame RMSD against a single reference frame on GPU.

    Parameters
    ----------
    coordinates : np.ndarray, shape (n_structures, n_atoms, 3), float64
    reference_coordinates : np.ndarray, shape (n_atoms, 3), float64

    Returns
    -------
    np.ndarray, shape (n_structures,), float64
    """
    n_structures = coordinates.shape[0]
    out = np.zeros(n_structures, dtype=np.float64)

    threads_per_block = 256
    blocks = math.ceil(n_structures / threads_per_block)

    d_c = cuda.to_device(coordinates)
    d_r = cuda.to_device(reference_coordinates)
    d_out = cuda.to_device(out)

    _get_rmsd_single_ref_kernel[blocks, threads_per_block](d_c, d_r, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out
