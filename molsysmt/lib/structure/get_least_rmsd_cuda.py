"""
CUDA kernels for Kabsch least-RMSD calculation.

Requires: numba with CUDA support (``numba[cuda]``) and a CUDA-capable GPU.

The kernels share a Jacobi iterative eigensolver for 4×4 symmetric matrices
(thread-local, no shared memory required).

Kernels
-------
get_least_rmsd(coordinates, reference_coordinates) -> least_rmsd
    Per-frame least-RMSD (Kabsch), query frames vs. reference frames (1-to-1).

get_least_rmsd_with_single_reference_structure(coordinates, reference_coordinates) -> least_rmsd
    Per-frame least-RMSD against a single reference frame (broadcast).
"""

from __future__ import annotations

import math
import numpy as np


try:
    from numba import cuda
    import numba as nb

    # -----------------------------------------------------------------------
    # Jacobi 4×4 symmetric eigensolver (device function)
    # -----------------------------------------------------------------------
    #
    # On entry  : A[0..3][0..3]  — symmetric matrix (modified in place)
    #             V[0..3][0..3]  — overwritten with eigenvectors (columns)
    # On exit   : A diagonal = eigenvalues (sorted ascending)
    #             V columns  = eigenvectors (sorted ascending)
    # -----------------------------------------------------------------------

    @cuda.jit(device=True)
    def _jacobi_eigh4(A, V):
        """In-place Jacobi diagonalisation of a 4×4 symmetric matrix A."""
        # Initialise V as identity
        for i in range(4):
            for j in range(4):
                V[i, j] = 1.0 if i == j else 0.0

        for _ in range(64):  # typically converges in < 10 sweeps
            # Find largest off-diagonal element
            max_val = 0.0
            p = 0
            q = 1
            for i in range(4):
                for j in range(i + 1, 4):
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

            App = A[p, p]
            Aqq = A[q, q]
            Apq = A[p, q]

            # Update diagonal and (p,q) element
            A[p, p] = c * c * App - 2.0 * c * s * Apq + s * s * Aqq
            A[q, q] = s * s * App + 2.0 * c * s * Apq + c * c * Aqq
            A[p, q] = 0.0
            A[q, p] = 0.0

            # Update other off-diagonal elements symmetrically
            for r in range(4):
                if r != p and r != q:
                    arp = A[r, p]
                    arq = A[r, q]
                    A[r, p] = c * arp - s * arq
                    A[p, r] = A[r, p]
                    A[r, q] = s * arp + c * arq
                    A[q, r] = A[r, q]

            # Accumulate rotation into V
            for k in range(4):
                Vkp = c * V[k, p] - s * V[k, q]
                Vkq = s * V[k, p] + c * V[k, q]
                V[k, p] = Vkp
                V[k, q] = Vkq

        # Extract diagonal as eigenvalues and sort ascending (insertion sort)
        for i in range(1, 4):
            key = A[i, i]
            v0 = V[0, i]; v1 = V[1, i]; v2 = V[2, i]; v3 = V[3, i]
            j = i - 1
            while j >= 0 and A[j, j] > key:
                A[j + 1, j + 1] = A[j, j]
                V[0, j + 1] = V[0, j]
                V[1, j + 1] = V[1, j]
                V[2, j + 1] = V[2, j]
                V[3, j + 1] = V[3, j]
                j -= 1
            A[j + 1, j + 1] = key
            V[0, j + 1] = v0; V[1, j + 1] = v1; V[2, j + 1] = v2; V[3, j + 1] = v3

    # -----------------------------------------------------------------------
    # CUDA kernels
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_least_rmsd_kernel(coords, ref_coords, out):
        """
        Thread assignment: one thread per frame.
        """
        ii = cuda.grid(1)
        if ii >= coords.shape[0]:
            return

        n_atoms = coords.shape[1]

        # Compute centroids without storing centered coordinates
        c_ref = cuda.local.array(3, dtype=nb.float64)
        c_query = cuda.local.array(3, dtype=nb.float64)
        for a in range(3):
            c_ref[a] = 0.0
            c_query[a] = 0.0

        for j in range(n_atoms):
            for a in range(3):
                c_ref[a] += ref_coords[ii, j, a]
                c_query[a] += coords[ii, j, a]

        for a in range(3):
            c_ref[a] /= n_atoms
            c_query[a] /= n_atoms

        # Compute x_norm and y_norm
        x_norm = 0.0
        y_norm = 0.0
        for j in range(n_atoms):
            for a in range(3):
                dx = ref_coords[ii, j, a] - c_ref[a]
                dy = coords[ii, j, a] - c_query[a]
                x_norm += dx * dx
                y_norm += dy * dy

        # Compute R matrix (3x3)
        R = cuda.local.array((3, 3), dtype=nb.float64)
        for ll in range(3):
            for mm in range(3):
                val = 0.0
                for j in range(n_atoms):
                    dx = ref_coords[ii, j, ll] - c_ref[ll]
                    dy = coords[ii, j, mm] - c_query[mm]
                    val += dx * dy
                R[ll, mm] = val

        # Construct F matrix (4x4)
        F = cuda.local.array((4, 4), dtype=nb.float64)
        F[0,0] = R[0,0] + R[1,1] + R[2,2]
        F[1,0] = R[1,2] - R[2,1]
        F[2,0] = R[2,0] - R[0,2]
        F[3,0] = R[0,1] - R[1,0]
        F[0,1] = F[1,0]
        F[1,1] = R[0,0] - R[1,1] - R[2,2]
        F[2,1] = R[0,1] + R[1,0]
        F[3,1] = R[0,2] + R[2,0]
        F[0,2] = F[2,0]
        F[1,2] = F[2,1]
        F[2,2] = -R[0,0] + R[1,1] - R[2,2]
        F[3,2] = R[1,2] + R[2,1]
        F[0,3] = F[3,0]
        F[1,3] = F[3,1]
        F[2,3] = F[3,2]
        F[3,3] = -R[0,0] - R[1,1] + R[2,2]

        V = cuda.local.array((4, 4), dtype=nb.float64)
        _jacobi_eigh4(F, V)

        # RMSD
        msd = max(0.0, (x_norm + y_norm) - 2.0 * F[3, 3]) / n_atoms
        out[ii] = math.sqrt(msd)

    @cuda.jit
    def _get_least_rmsd_single_ref_kernel(coords, ref_coords, out):
        """
        Thread assignment: one thread per frame.
        """
        ii = cuda.grid(1)
        if ii >= coords.shape[0]:
            return

        n_atoms = coords.shape[1]

        # Compute centroids
        c_ref = cuda.local.array(3, dtype=nb.float64)
        c_query = cuda.local.array(3, dtype=nb.float64)
        for a in range(3):
            c_ref[a] = 0.0
            c_query[a] = 0.0

        for j in range(n_atoms):
            for a in range(3):
                c_ref[a] += ref_coords[j, a]
                c_query[a] += coords[ii, j, a]

        for a in range(3):
            c_ref[a] /= n_atoms
            c_query[a] /= n_atoms

        # Compute x_norm and y_norm
        x_norm = 0.0
        y_norm = 0.0
        for j in range(n_atoms):
            for a in range(3):
                dx = ref_coords[j, a] - c_ref[a]
                dy = coords[ii, j, a] - c_query[a]
                x_norm += dx * dx
                y_norm += dy * dy

        # Compute R matrix (3x3)
        R = cuda.local.array((3, 3), dtype=nb.float64)
        for ll in range(3):
            for mm in range(3):
                val = 0.0
                for j in range(n_atoms):
                    dx = ref_coords[j, ll] - c_ref[ll]
                    dy = coords[ii, j, mm] - c_query[mm]
                    val += dx * dy
                R[ll, mm] = val

        # Construct F matrix (4x4)
        F = cuda.local.array((4, 4), dtype=nb.float64)
        F[0,0] = R[0,0] + R[1,1] + R[2,2]
        F[1,0] = R[1,2] - R[2,1]
        F[2,0] = R[2,0] - R[0,2]
        F[3,0] = R[0,1] - R[1,0]
        F[0,1] = F[1,0]
        F[1,1] = R[0,0] - R[1,1] - R[2,2]
        F[2,1] = R[0,1] + R[1,0]
        F[3,1] = R[0,2] + R[2,0]
        F[0,2] = F[2,0]
        F[1,2] = F[2,1]
        F[2,2] = -R[0,0] + R[1,1] - R[2,2]
        F[3,2] = R[1,2] + R[2,1]
        F[0,3] = F[3,0]
        F[1,3] = F[3,1]
        F[2,3] = F[3,2]
        F[3,3] = -R[0,0] - R[1,1] + R[2,2]

        V = cuda.local.array((4, 4), dtype=nb.float64)
        _jacobi_eigh4(F, V)

        # RMSD
        msd = max(0.0, (x_norm + y_norm) - 2.0 * F[3, 3]) / n_atoms
        out[ii] = math.sqrt(msd)

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Python-level entry points
# ---------------------------------------------------------------------------

def get_least_rmsd(coordinates: np.ndarray, reference_coordinates: np.ndarray) -> np.ndarray:
    """
    Per-frame least-RMSD (Kabsch superposition) on GPU.
    """
    if not _CUDA_AVAILABLE:
        raise RuntimeError("Numba CUDA is not available.")

    n_structures = coordinates.shape[0]
    out = np.zeros(n_structures, dtype=np.float64)

    threads_per_block = 256
    blocks_per_grid = (n_structures + threads_per_block - 1) // threads_per_block

    _get_least_rmsd_kernel[blocks_per_grid, threads_per_block](coordinates, reference_coordinates, out)
    return out


def get_least_rmsd_with_single_reference_structure(coordinates: np.ndarray, reference_coordinates: np.ndarray) -> np.ndarray:
    """
    Per-frame least-RMSD against a single reference structure on GPU.
    """
    if not _CUDA_AVAILABLE:
        raise RuntimeError("Numba CUDA is not available.")

    n_structures = coordinates.shape[0]
    out = np.zeros(n_structures, dtype=np.float64)

    threads_per_block = 256
    blocks_per_grid = (n_structures + threads_per_block - 1) // threads_per_block

    _get_least_rmsd_single_ref_kernel[blocks_per_grid, threads_per_block](coordinates, reference_coordinates, out)
    return out
