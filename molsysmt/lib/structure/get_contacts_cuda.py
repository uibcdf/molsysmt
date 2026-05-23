"""
CUDA kernels for pairwise contact calculations under vacuum and Periodic Boundary Conditions (MIC).

Requires: numba with CUDA support (``numba[cuda]``) and a CUDA-capable GPU.
"""

from __future__ import annotations

import math
import numpy as np


try:
    from numba import cuda

    # ---------------------------------------------------------------------------
    # CUDA device helpers
    # ---------------------------------------------------------------------------

    @cuda.jit(device=True)
    def _dist3d(ax, ay, az, bx, by, bz):
        """Euclidean distance between two 3-D points (device function)."""
        dx = bx - ax
        dy = by - ay
        dz = bz - az
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    @cuda.jit(device=True)
    def _is_orthogonal(box_s):
        """Return True when all off-diagonal box elements are essentially zero."""
        tol = 1e-10
        return (
            abs(box_s[0, 1]) < tol and abs(box_s[0, 2]) < tol and
            abs(box_s[1, 0]) < tol and abs(box_s[1, 2]) < tol and
            abs(box_s[2, 0]) < tol and abs(box_s[2, 1]) < tol
        )

    @cuda.jit(device=True)
    def _mic_dist_orthogonal(ax, ay, az, bx, by, bz, lx, ly, lz):
        """MIC distance for an orthogonal box with edge lengths lx, ly, lz."""
        dx = bx - ax
        dy = by - ay
        dz = bz - az
        dx -= lx * math.floor(dx / lx + 0.5)
        dy -= ly * math.floor(dy / ly + 0.5)
        dz -= lz * math.floor(dz / lz + 0.5)
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    @cuda.jit(device=True)
    def _mic_dist_triclinic(ax, ay, az, bx, by, bz, box_s):
        """
        MIC distance for a triclinic box.

        Converts displacement to fractional coordinates, applies minimum-image
        rounding, then converts back to Cartesian.
        """
        dx = bx - ax
        dy = by - ay
        dz = bz - az

        # 3×3 matrix inverse via Cramer's rule
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

        # Fractional coordinates
        sx = inv00 * dx + inv01 * dy + inv02 * dz
        sy = inv10 * dx + inv11 * dy + inv12 * dz
        sz = inv20 * dx + inv21 * dy + inv22 * dz

        # Minimum-image rounding
        sx -= math.floor(sx + 0.5)
        sy -= math.floor(sy + 0.5)
        sz -= math.floor(sz + 0.5)

        # Back to Cartesian
        cx = b00 * sx + b01 * sy + b02 * sz
        cy = b10 * sx + b11 * sy + b12 * sz
        cz = b20 * sx + b21 * sy + b22 * sz

        return math.sqrt(cx * cx + cy * cy + cz * cz)

    @cuda.jit(device=True)
    def _mic_dist(ax, ay, az, bx, by, bz, box_s):
        """MIC distance: dispatches to orthogonal or triclinic helper."""
        if _is_orthogonal(box_s):
            return _mic_dist_orthogonal(
                ax, ay, az, bx, by, bz,
                box_s[0, 0], box_s[1, 1], box_s[2, 2]
            )
        else:
            return _mic_dist_triclinic(ax, ay, az, bx, by, bz, box_s)

    # -----------------------------------------------------------------------
    # Vacuum Contact Kernels
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_contacts_single_system_kernel(coords, threshold, out):
        """Thread grid: (frame, atom_i, atom_j)."""
        ii, jj, kk = cuda.grid(3)
        n_structures = coords.shape[0]
        n_atoms = coords.shape[1]

        if ii >= n_structures or jj >= n_atoms or kk >= n_atoms:
            return

        d = _dist3d(
            coords[ii, jj, 0], coords[ii, jj, 1], coords[ii, jj, 2],
            coords[ii, kk, 0], coords[ii, kk, 1], coords[ii, kk, 2],
        )
        out[ii, jj, kk] = (d <= threshold)

    @cuda.jit
    def _get_contacts_kernel(coords1, coords2, threshold, out):
        """Thread grid: (frame, atom_i, atom_j)."""
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
        out[ii, jj, kk] = (d <= threshold)

    @cuda.jit
    def _get_contacts_pairs_kernel(coords1, coords2, threshold, out):
        """Thread grid: (frame, pair_idx)."""
        ii, jj = cuda.grid(2)
        n_structures = coords1.shape[0]
        n_pairs = coords1.shape[1]

        if ii >= n_structures or jj >= n_pairs:
            return

        d = _dist3d(
            coords1[ii, jj, 0], coords1[ii, jj, 1], coords1[ii, jj, 2],
            coords2[ii, jj, 0], coords2[ii, jj, 1], coords2[ii, jj, 2],
        )
        out[ii, jj] = (d <= threshold)

    # -----------------------------------------------------------------------
    # PBC/MIC Contact Kernels
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_mic_contacts_single_system_kernel(coords, box, threshold, out):
        """Thread grid: (frame, atom_i, atom_j)."""
        ii, jj, kk = cuda.grid(3)
        n_structures = coords.shape[0]
        n_atoms = coords.shape[1]

        if ii >= n_structures or jj >= n_atoms or kk >= n_atoms:
            return

        d = _mic_dist(
            coords[ii, jj, 0], coords[ii, jj, 1], coords[ii, jj, 2],
            coords[ii, kk, 0], coords[ii, kk, 1], coords[ii, kk, 2],
            box[ii],
        )
        out[ii, jj, kk] = (d <= threshold)

    @cuda.jit
    def _get_mic_contacts_kernel(coords1, coords2, box, threshold, out):
        """Thread grid: (frame, atom_i, atom_j)."""
        ii, jj, kk = cuda.grid(3)
        n_structures = coords1.shape[0]
        n_atoms1 = coords1.shape[1]
        n_atoms2 = coords2.shape[1]

        if ii >= n_structures or jj >= n_atoms1 or kk >= n_atoms2:
            return

        d = _mic_dist(
            coords1[ii, jj, 0], coords1[ii, jj, 1], coords1[ii, jj, 2],
            coords2[ii, kk, 0], coords2[ii, kk, 1], coords2[ii, kk, 2],
            box[ii],
        )
        out[ii, jj, kk] = (d <= threshold)

    @cuda.jit
    def _get_mic_contacts_pairs_kernel(coords1, coords2, box, threshold, out):
        """Thread grid: (frame, pair_idx)."""
        ii, jj = cuda.grid(2)
        n_structures = coords1.shape[0]
        n_pairs = coords1.shape[1]

        if ii >= n_structures or jj >= n_pairs:
            return

        d = _mic_dist(
            coords1[ii, jj, 0], coords1[ii, jj, 1], coords1[ii, jj, 2],
            coords2[ii, jj, 0], coords2[ii, jj, 1], coords2[ii, jj, 2],
            box[ii],
        )
        out[ii, jj] = (d <= threshold)

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Entrypoints
# ---------------------------------------------------------------------------

def get_contacts_single_system(coordinates: np.ndarray, threshold: float) -> np.ndarray:
    """All-vs-all contacts within a single system (vacuum)."""
    n_structures, n_atoms, _ = coordinates.shape
    out = np.zeros((n_structures, n_atoms, n_atoms), dtype=bool)

    threads_per_block = (4, 8, 8)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_atoms      / threads_per_block[1]),
        math.ceil(n_atoms      / threads_per_block[2]),
    )

    d_coords = cuda.to_device(coordinates)
    d_out    = cuda.to_device(out)

    _get_contacts_single_system_kernel[blocks, threads_per_block](d_coords, threshold, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out


def get_contacts(coordinates1: np.ndarray, coordinates2: np.ndarray, threshold: float) -> np.ndarray:
    """Cross-system contacts (vacuum)."""
    n_structures, n_atoms1, _ = coordinates1.shape
    n_atoms2 = coordinates2.shape[1]
    out = np.zeros((n_structures, n_atoms1, n_atoms2), dtype=bool)

    threads_per_block = (4, 8, 8)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_atoms1     / threads_per_block[1]),
        math.ceil(n_atoms2     / threads_per_block[2]),
    )

    d_c1  = cuda.to_device(coordinates1)
    d_c2  = cuda.to_device(coordinates2)
    d_out = cuda.to_device(out)

    _get_contacts_kernel[blocks, threads_per_block](d_c1, d_c2, threshold, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out


def get_contacts_pairs(coordinates1: np.ndarray, coordinates2: np.ndarray, threshold: float) -> np.ndarray:
    """Specific pair-wise contacts (vacuum)."""
    n_structures, n_pairs, _ = coordinates1.shape
    out = np.zeros((n_structures, n_pairs), dtype=bool)

    threads_per_block = (16, 16)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_pairs      / threads_per_block[1]),
    )

    d_c1  = cuda.to_device(coordinates1)
    d_c2  = cuda.to_device(coordinates2)
    d_out = cuda.to_device(out)

    _get_contacts_pairs_kernel[blocks, threads_per_block](d_c1, d_c2, threshold, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out


def get_mic_contacts_single_system(coordinates: np.ndarray, box: np.ndarray, threshold: float) -> np.ndarray:
    """All-vs-all contacts within a single system under PBC/MIC."""
    n_structures, n_atoms, _ = coordinates.shape
    out = np.zeros((n_structures, n_atoms, n_atoms), dtype=bool)

    threads_per_block = (4, 8, 8)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_atoms      / threads_per_block[1]),
        math.ceil(n_atoms      / threads_per_block[2]),
    )

    d_coords = cuda.to_device(coordinates)
    d_box    = cuda.to_device(box)
    d_out    = cuda.to_device(out)

    _get_mic_contacts_single_system_kernel[blocks, threads_per_block](d_coords, d_box, threshold, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out


def get_mic_contacts(coordinates1: np.ndarray, coordinates2: np.ndarray, box: np.ndarray, threshold: float) -> np.ndarray:
    """Cross-system contacts under PBC/MIC."""
    n_structures, n_atoms1, _ = coordinates1.shape
    n_atoms2 = coordinates2.shape[1]
    out = np.zeros((n_structures, n_atoms1, n_atoms2), dtype=bool)

    threads_per_block = (4, 8, 8)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_atoms1     / threads_per_block[1]),
        math.ceil(n_atoms2     / threads_per_block[2]),
    )

    d_c1  = cuda.to_device(coordinates1)
    d_c2  = cuda.to_device(coordinates2)
    d_box = cuda.to_device(box)
    d_out = cuda.to_device(out)

    _get_mic_contacts_kernel[blocks, threads_per_block](d_c1, d_c2, d_box, threshold, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out


def get_mic_contacts_pairs(coordinates1: np.ndarray, coordinates2: np.ndarray, box: np.ndarray, threshold: float) -> np.ndarray:
    """Specific pair-wise contacts under PBC/MIC."""
    n_structures, n_pairs, _ = coordinates1.shape
    out = np.zeros((n_structures, n_pairs), dtype=bool)

    threads_per_block = (16, 16)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_pairs      / threads_per_block[1]),
    )

    d_c1  = cuda.to_device(coordinates1)
    d_c2  = cuda.to_device(coordinates2)
    d_box = cuda.to_device(box)
    d_out = cuda.to_device(out)

    _get_mic_contacts_pairs_kernel[blocks, threads_per_block](d_c1, d_c2, d_box, threshold, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out
