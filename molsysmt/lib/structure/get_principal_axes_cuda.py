"""
CUDA kernels for principal axes (inertia and geometric).

Requires: numba with CUDA support (``numba[cuda]``) and a CUDA-capable GPU.

The kernels share a Jacobi iterative eigensolver for 3×3 symmetric matrices
(thread-local, no shared memory required).

Kernels
-------
get_principal_inertia_axes(coordinates, weights) -> (eigenvalues, eigenvectors)
    Per-frame inertia tensor eigendecomposition.

get_principal_geometric_axes(coordinates, weights) -> (eigenvalues, eigenvectors)
    Per-frame covariance tensor eigendecomposition (geometric principal axes).

Both accept/return plain numpy float64 arrays (units handled by the public
wrapper).
"""

from __future__ import annotations

import math
import numpy as np


try:
    from numba import cuda
    import numba as nb

    # -----------------------------------------------------------------------
    # Jacobi 3×3 symmetric eigensolver (device function)
    # -----------------------------------------------------------------------
    #
    # On entry  : A[0..2][0..2]  — symmetric matrix (modified in place)
    #             V[0..2][0..2]  — overwritten with eigenvectors (columns)
    # On exit   : A diagonal = eigenvalues (unsorted)
    #             V columns  = eigenvectors (unsorted)
    #
    # Sorting (ascending by eigenvalue) is performed after convergence.
    # -----------------------------------------------------------------------

    @cuda.jit(device=True)
    def _jacobi_eigh3(A, V):
        """In-place Jacobi diagonalisation of a 3×3 symmetric matrix A."""
        # Initialise V as identity
        for i in range(3):
            for j in range(3):
                V[i, j] = 1.0 if i == j else 0.0

        for _ in range(64):  # typically converges in < 10 iterations
            # Find largest off-diagonal element
            max_val = 0.0
            p = 0
            q = 1
            for i in range(3):
                for j in range(i + 1, 3):
                    aij = A[i, j] if A[i, j] >= 0.0 else -A[i, j]
                    if aij > max_val:
                        max_val = aij
                        p = i
                        q = j

            if max_val < 1e-14:
                break

            # Givens rotation angle
            theta = 0.5 * math.atan2(2.0 * A[p, q], A[q, q] - A[p, p])
            c = math.cos(theta)
            s = math.sin(theta)

            # Third index (the one not equal to p or q)
            r = 3 - p - q   # works: {0,1}→2, {0,2}→1, {1,2}→0

            # Save off-diagonal element involving r
            Arp = A[min(r, p), max(r, p)]
            Arq = A[min(r, q), max(r, q)]

            # Update diagonal and (p,q) element
            App = A[p, p]
            Aqq = A[q, q]
            Apq = A[p, q]

            A[p, p] = c * c * App - 2.0 * c * s * Apq + s * s * Aqq
            A[q, q] = s * s * App + 2.0 * c * s * Apq + c * c * Aqq
            A[p, q] = 0.0
            A[q, p] = 0.0

            # Update off-diagonal elements involving r
            new_rp = c * Arp - s * Arq
            new_rq = s * Arp + c * Arq
            A[min(r, p), max(r, p)] = new_rp
            A[max(r, p), min(r, p)] = new_rp
            A[min(r, q), max(r, q)] = new_rq
            A[max(r, q), min(r, q)] = new_rq

            # Accumulate rotation into V
            for k in range(3):
                Vkp = c * V[k, p] - s * V[k, q]
                Vkq = s * V[k, p] + c * V[k, q]
                V[k, p] = Vkp
                V[k, q] = Vkq

        # Extract diagonal as eigenvalues and sort ascending (insertion sort)
        # (V columns are the corresponding eigenvectors)
        for i in range(1, 3):
            key = A[i, i]
            v0  = V[0, i];  v1 = V[1, i];  v2 = V[2, i]
            j = i - 1
            while j >= 0 and A[j, j] > key:
                A[j + 1, j + 1] = A[j, j]
                V[0, j + 1] = V[0, j]
                V[1, j + 1] = V[1, j]
                V[2, j + 1] = V[2, j]
                j -= 1
            A[j + 1, j + 1] = key
            V[0, j + 1] = v0;  V[1, j + 1] = v1;  V[2, j + 1] = v2

    # -----------------------------------------------------------------------
    # Inertia-tensor kernel  (one thread per frame)
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_principal_inertia_axes_kernel(coords, weights, eigenvalues, eigenvectors):
        """
        Thread assignment: one thread per frame.

        coords       : (n_structures, n_atoms, 3)    float64
        weights      : (n_atoms,)                    float64
        eigenvalues  : (n_structures, 3)             float64
        eigenvectors : (n_structures, 3, 3)          float64   rows = eigenvectors
        """
        ii = cuda.grid(1)
        if ii >= coords.shape[0]:
            return

        n_atoms = coords.shape[1]

        # --- weighted centre ---
        total_w = 0.0
        cx = 0.0;  cy = 0.0;  cz = 0.0
        for jj in range(n_atoms):
            w = weights[jj]
            cx += w * coords[ii, jj, 0]
            cy += w * coords[ii, jj, 1]
            cz += w * coords[ii, jj, 2]
            total_w += w
        cx /= total_w;  cy /= total_w;  cz /= total_w

        # --- build inertia tensor ---
        A = cuda.local.array((3, 3), nb.float64)
        for i in range(3):
            for j in range(3):
                A[i, j] = 0.0

        for jj in range(n_atoms):
            w = weights[jj]
            dx = coords[ii, jj, 0] - cx
            dy = coords[ii, jj, 1] - cy
            dz = coords[ii, jj, 2] - cz
            A[0, 0] += w * (dy * dy + dz * dz)
            A[1, 1] += w * (dx * dx + dz * dz)
            A[2, 2] += w * (dx * dx + dy * dy)
            A[0, 1] -= w * dx * dy
            A[0, 2] -= w * dx * dz
            A[1, 2] -= w * dy * dz
        A[1, 0] = A[0, 1]
        A[2, 0] = A[0, 2]
        A[2, 1] = A[1, 2]

        # --- Jacobi eigendecomposition ---
        V = cuda.local.array((3, 3), nb.float64)
        _jacobi_eigh3(A, V)

        # --- write output (transpose V so rows = eigenvectors) ---
        eigenvalues[ii, 0] = A[0, 0]
        eigenvalues[ii, 1] = A[1, 1]
        eigenvalues[ii, 2] = A[2, 2]
        for r in range(3):
            for c in range(3):
                eigenvectors[ii, r, c] = V[c, r]   # transpose

    # -----------------------------------------------------------------------
    # Geometric-axes kernel  (one thread per frame)
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_principal_geometric_axes_kernel(coords, weights, eigenvalues, eigenvectors):
        """
        Thread assignment: one thread per frame.

        coords       : (n_structures, n_atoms, 3)    float64
        weights      : (n_atoms,)                    float64
        eigenvalues  : (n_structures, 3)             float64
        eigenvectors : (n_structures, 3, 3)          float64
        """
        ii = cuda.grid(1)
        if ii >= coords.shape[0]:
            return

        n_atoms = coords.shape[1]

        # --- weighted centre ---
        total_w = 0.0
        cx = 0.0;  cy = 0.0;  cz = 0.0
        for jj in range(n_atoms):
            w = weights[jj]
            cx += w * coords[ii, jj, 0]
            cy += w * coords[ii, jj, 1]
            cz += w * coords[ii, jj, 2]
            total_w += w
        cx /= total_w;  cy /= total_w;  cz /= total_w

        # --- build covariance tensor ---
        A = cuda.local.array((3, 3), nb.float64)
        for i in range(3):
            for j in range(3):
                A[i, j] = 0.0

        for jj in range(n_atoms):
            w = weights[jj]
            dx = coords[ii, jj, 0] - cx
            dy = coords[ii, jj, 1] - cy
            dz = coords[ii, jj, 2] - cz
            A[0, 0] += w * dx * dx
            A[1, 1] += w * dy * dy
            A[2, 2] += w * dz * dz
            A[0, 1] += w * dx * dy
            A[0, 2] += w * dx * dz
            A[1, 2] += w * dy * dz
        A[1, 0] = A[0, 1]
        A[2, 0] = A[0, 2]
        A[2, 1] = A[1, 2]
        for i in range(3):
            for j in range(3):
                A[i, j] /= total_w

        # --- Jacobi eigendecomposition ---
        V = cuda.local.array((3, 3), nb.float64)
        _jacobi_eigh3(A, V)

        eigenvalues[ii, 0] = A[0, 0]
        eigenvalues[ii, 1] = A[1, 1]
        eigenvalues[ii, 2] = A[2, 2]
        for r in range(3):
            for c in range(3):
                eigenvectors[ii, r, c] = V[c, r]

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Python-level entry points  (same signatures as CPU counterparts)
# ---------------------------------------------------------------------------

def get_principal_inertia_axes(
    coordinates: np.ndarray, weights: np.ndarray
):
    """
    Per-frame inertia-tensor eigendecomposition on GPU.

    Parameters
    ----------
    coordinates : np.ndarray, shape (n_structures, n_atoms, 3), float64
    weights     : np.ndarray, shape (n_atoms,), float64

    Returns
    -------
    eigenvalues  : np.ndarray, shape (n_structures, 3), float64
    eigenvectors : np.ndarray, shape (n_structures, 3, 3), float64
        Rows are eigenvectors, matching the CPU kernel convention.
    """
    n_structures = coordinates.shape[0]
    eigenvalues  = np.zeros((n_structures, 3),    dtype=np.float64)
    eigenvectors = np.zeros((n_structures, 3, 3), dtype=np.float64)

    threads_per_block = 256
    blocks = math.ceil(n_structures / threads_per_block)

    d_c   = cuda.to_device(coordinates)
    d_w   = cuda.to_device(weights)
    d_ev  = cuda.to_device(eigenvalues)
    d_evv = cuda.to_device(eigenvectors)

    _get_principal_inertia_axes_kernel[blocks, threads_per_block](d_c, d_w, d_ev, d_evv)
    cuda.synchronize()

    d_ev.copy_to_host(eigenvalues)
    d_evv.copy_to_host(eigenvectors)
    return eigenvalues, eigenvectors


def get_principal_geometric_axes(
    coordinates: np.ndarray, weights: np.ndarray
):
    """
    Per-frame geometric-axis eigendecomposition on GPU.

    Parameters
    ----------
    coordinates : np.ndarray, shape (n_structures, n_atoms, 3), float64
    weights     : np.ndarray, shape (n_atoms,), float64

    Returns
    -------
    eigenvalues  : np.ndarray, shape (n_structures, 3), float64
    eigenvectors : np.ndarray, shape (n_structures, 3, 3), float64
    """
    n_structures = coordinates.shape[0]
    eigenvalues  = np.zeros((n_structures, 3),    dtype=np.float64)
    eigenvectors = np.zeros((n_structures, 3, 3), dtype=np.float64)

    threads_per_block = 256
    blocks = math.ceil(n_structures / threads_per_block)

    d_c   = cuda.to_device(coordinates)
    d_w   = cuda.to_device(weights)
    d_ev  = cuda.to_device(eigenvalues)
    d_evv = cuda.to_device(eigenvectors)

    _get_principal_geometric_axes_kernel[blocks, threads_per_block](d_c, d_w, d_ev, d_evv)
    cuda.synchronize()

    d_ev.copy_to_host(eigenvalues)
    d_evv.copy_to_host(eigenvectors)
    return eigenvalues, eigenvectors
