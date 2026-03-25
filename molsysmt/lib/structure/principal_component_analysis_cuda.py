"""
Hybrid GPU/CPU principal component analysis.

Requires: numba with CUDA support (``numba[cuda]``) and a CUDA-capable GPU.

Strategy
--------
The CPU bottleneck in PCA is building the (n_features × n_features) covariance
matrix, which costs O(n_structures × n_features²).  This module offloads that
step to the GPU while keeping the final eigendecomposition (``np.linalg.eigh``)
on the CPU:

1. CPU  — flatten and mean-subtract coordinates; apply sqrt(weights) per feature.
2. GPU  — compute cov = flat_weighted^T @ flat_weighted / n_structures.
3. CPU  — symmetrize upper triangle, call ``np.linalg.eigh``, transpose eigenvectors.

Accepts/returns plain numpy float64 arrays (units handled by the public wrapper).
"""

from __future__ import annotations

import math
import numpy as np


try:
    from numba import cuda

    # -----------------------------------------------------------------------
    # Covariance kernel
    # -----------------------------------------------------------------------

    @cuda.jit
    def _cov_kernel(flat_w, cov):
        """
        Compute the upper triangle of the covariance matrix.

        flat_w : (n_structures, n_features)  float64  — mean-subtracted, weighted
        cov    : (n_features, n_features)    float64  — output (upper triangle)

        Thread assignment: one thread per (ii, jj) pair with jj >= ii.
        """
        ii, jj = cuda.grid(2)
        n_structures = flat_w.shape[0]
        n_features   = flat_w.shape[1]

        if ii >= n_features or jj >= n_features or jj < ii:
            return

        acc = 0.0
        for ll in range(n_structures):
            acc += flat_w[ll, ii] * flat_w[ll, jj]

        cov[ii, jj] = acc / n_structures
        if ii != jj:
            cov[jj, ii] = cov[ii, jj]

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Python-level entry point
# ---------------------------------------------------------------------------

def principal_component_analysis(
    coordinates: np.ndarray, weights: np.ndarray
):
    """
    PCA with GPU-accelerated covariance matrix construction.

    Parameters
    ----------
    coordinates : np.ndarray, shape (n_structures, n_atoms, 3), float64
    weights     : np.ndarray, shape (n_atoms,), float64

    Returns
    -------
    eigenvalues  : np.ndarray, shape (n_features,), float64
    eigenvectors : np.ndarray, shape (n_features, n_features), float64
        Each row is an eigenvector (transposed from np.linalg.eigh convention),
        matching the CPU kernel output.
    """
    n_structures, n_atoms, _ = coordinates.shape
    n_features = n_atoms * 3

    # ----- 1. CPU: flatten, mean-subtract, apply sqrt(weights) -----
    # Feature ordering: (x0,y0,z0, x1,y1,z1, ...) — same as CPU kernel
    # aux_ind maps (atom, coord) → feature index: feature = atom*3 + coord
    # But the CPU kernel uses a different ordering: (all-x, all-y, all-z)
    # Replicate exactly: feature = coord*n_atoms + atom
    flat = np.empty((n_structures, n_features), dtype=np.float64)
    for jj in range(3):
        for ii in range(n_atoms):
            feat = jj * n_atoms + ii
            flat[:, feat] = coordinates[:, ii, jj]

    mean = flat.mean(axis=0)
    flat -= mean

    weight_per_feature = np.empty(n_features, dtype=np.float64)
    for jj in range(3):
        for ii in range(n_atoms):
            feat = jj * n_atoms + ii
            weight_per_feature[feat] = math.sqrt(weights[ii])

    flat_w = flat * weight_per_feature[np.newaxis, :]   # broadcast

    # ----- 2. GPU: cov = flat_w^T @ flat_w / n_structures -----
    cov = np.zeros((n_features, n_features), dtype=np.float64)

    tile = 16
    threads_per_block = (tile, tile)
    blocks = (
        math.ceil(n_features / tile),
        math.ceil(n_features / tile),
    )

    d_flat_w = cuda.to_device(np.ascontiguousarray(flat_w))
    d_cov    = cuda.to_device(cov)

    _cov_kernel[blocks, threads_per_block](d_flat_w, d_cov)
    cuda.synchronize()

    d_cov.copy_to_host(cov)

    # ----- 3. CPU: eigendecomposition -----
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    eigenvectors = eigenvectors.T   # match CPU kernel: rows = eigenvectors

    return eigenvalues, eigenvectors
