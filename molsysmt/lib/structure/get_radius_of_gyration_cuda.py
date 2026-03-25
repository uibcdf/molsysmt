"""
CUDA kernel for radius of gyration.

Requires: numba with CUDA support (``numba[cuda]``) and a CUDA-capable GPU.

Kernels
-------
get_radius_of_gyration(coordinates, weights) -> rg
    Per-frame radius of gyration (weighted).
    Equivalent to the CPU ``@lazy_njit`` version in ``get_radius_of_gyration.py``.

Accepts/returns plain numpy float64 arrays (units handled by the public
wrapper layer).
"""

from __future__ import annotations

import math
import numpy as np


# ---------------------------------------------------------------------------
# CUDA kernel
# ---------------------------------------------------------------------------

try:
    from numba import cuda

    @cuda.jit
    def _get_radius_of_gyration_kernel(coords, weights, out):
        """
        Thread assignment: one thread per frame.

        coords  : (n_structures, n_atoms, 3)  float64
        weights : (n_atoms,)                  float64
        out     : (n_structures,)             float64
        """
        ii = cuda.grid(1)
        if ii >= coords.shape[0]:
            return

        n_atoms = coords.shape[1]

        # --- pass 1: weighted centre ---
        total_w = 0.0
        cx = 0.0
        cy = 0.0
        cz = 0.0
        for jj in range(n_atoms):
            w = weights[jj]
            cx += w * coords[ii, jj, 0]
            cy += w * coords[ii, jj, 1]
            cz += w * coords[ii, jj, 2]
            total_w += w
        cx /= total_w
        cy /= total_w
        cz /= total_w

        # --- pass 2: weighted sum of squared deviations ---
        sum_sq = 0.0
        for jj in range(n_atoms):
            dx = coords[ii, jj, 0] - cx
            dy = coords[ii, jj, 1] - cy
            dz = coords[ii, jj, 2] - cz
            sum_sq += weights[jj] * (dx * dx + dy * dy + dz * dz)

        out[ii] = math.sqrt(sum_sq / total_w)

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Python-level entry point  (same signature as CPU counterpart)
# ---------------------------------------------------------------------------

def get_radius_of_gyration(coordinates: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """
    Per-frame radius of gyration on GPU.

    Parameters
    ----------
    coordinates : np.ndarray, shape (n_structures, n_atoms, 3), float64
    weights : np.ndarray, shape (n_atoms,), float64
        Per-atom weights (equal weights → geometric Rg; masses → mass-weighted Rg).

    Returns
    -------
    np.ndarray, shape (n_structures,), float64
    """
    n_structures = coordinates.shape[0]
    out = np.zeros(n_structures, dtype=np.float64)

    threads_per_block = 256
    blocks = math.ceil(n_structures / threads_per_block)

    d_c = cuda.to_device(coordinates)
    d_w = cuda.to_device(weights)
    d_out = cuda.to_device(out)

    _get_radius_of_gyration_kernel[blocks, threads_per_block](d_c, d_w, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out
