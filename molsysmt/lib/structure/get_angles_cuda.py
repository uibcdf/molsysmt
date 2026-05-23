"""
CUDA kernels for 3-body valence angle calculations.

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
    def _angle(vx, vy, vz, wx, wy, wz):
        """Angle in radians between two 3-D vectors (device function)."""
        dot = vx * wx + vy * wy + vz * wz
        norm_v = math.sqrt(vx * vx + vy * vy + vz * vz)
        norm_w = math.sqrt(wx * wx + wy * wy + wz * wz)
        if norm_v < 1e-10 or norm_w < 1e-10:
            return 0.0
        cosa = dot / (norm_v * norm_w)
        if cosa >= 1.0:
            cosa = 1.0
        elif cosa <= -1.0:
            cosa = -1.0
        return math.acos(cosa)

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
    def _mic_wrap_vector_orthogonal(dx, dy, dz, lx, ly, lz):
        """MIC vector wrap for an orthogonal box."""
        rx = dx - lx * math.floor(dx / lx + 0.5)
        ry = dy - ly * math.floor(dy / ly + 0.5)
        rz = dz - lz * math.floor(dz / lz + 0.5)
        return rx, ry, rz

    @cuda.jit(device=True)
    def _mic_wrap_vector_triclinic(dx, dy, dz, box_s):
        """MIC vector wrap for a triclinic box."""
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

        return cx, cy, cz

    @cuda.jit(device=True)
    def _mic_wrap_vector(dx, dy, dz, box_s):
        """MIC vector wrap: dispatches to orthogonal or triclinic helper."""
        if _is_orthogonal(box_s):
            return _mic_wrap_vector_orthogonal(
                dx, dy, dz,
                box_s[0, 0], box_s[1, 1], box_s[2, 2]
            )
        else:
            return _mic_wrap_vector_triclinic(dx, dy, dz, box_s)

    # -----------------------------------------------------------------------
    # Valence Angle CUDA Kernels
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_angles_kernel(coords, triplets, out):
        """Thread grid: (frame, angle_idx)."""
        ii, jj = cuda.grid(2)
        n_structures = coords.shape[0]
        n_angles = triplets.shape[0]

        if ii >= n_structures or jj >= n_angles:
            return

        at0 = triplets[jj, 0]
        at1 = triplets[jj, 1]
        at2 = triplets[jj, 2]

        # Vector 0: at0 - at1
        v0x = coords[ii, at0, 0] - coords[ii, at1, 0]
        v0y = coords[ii, at0, 1] - coords[ii, at1, 1]
        v0z = coords[ii, at0, 2] - coords[ii, at1, 2]

        # Vector 1: at2 - at1
        v1x = coords[ii, at2, 0] - coords[ii, at1, 0]
        v1y = coords[ii, at2, 1] - coords[ii, at1, 1]
        v1z = coords[ii, at2, 2] - coords[ii, at1, 2]

        out[ii, jj] = _angle(v0x, v0y, v0z, v1x, v1y, v1z)

    @cuda.jit
    def _get_mic_angles_kernel(coords, box, triplets, out):
        """Thread grid: (frame, angle_idx)."""
        ii, jj = cuda.grid(2)
        n_structures = coords.shape[0]
        n_angles = triplets.shape[0]

        if ii >= n_structures or jj >= n_angles:
            return

        at0 = triplets[jj, 0]
        at1 = triplets[jj, 1]
        at2 = triplets[jj, 2]

        # Vector 0: at0 - at1
        v0x = coords[ii, at0, 0] - coords[ii, at1, 0]
        v0y = coords[ii, at0, 1] - coords[ii, at1, 1]
        v0z = coords[ii, at0, 2] - coords[ii, at1, 2]

        # Vector 1: at2 - at1
        v1x = coords[ii, at2, 0] - coords[ii, at1, 0]
        v1y = coords[ii, at2, 1] - coords[ii, at1, 1]
        v1z = coords[ii, at2, 2] - coords[ii, at1, 2]

        # Wrap vectors to MIC
        box_s = box[ii]
        v0x, v0y, v0z = _mic_wrap_vector(v0x, v0y, v0z, box_s)
        v1x, v1y, v1z = _mic_wrap_vector(v1x, v1y, v1z, box_s)

        out[ii, jj] = _angle(v0x, v0y, v0z, v1x, v1y, v1z)

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Entrypoints
# ---------------------------------------------------------------------------

def get_angles(coordinates: np.ndarray, triplets: np.ndarray) -> np.ndarray:
    """3-body valence angles under vacuum."""
    n_structures, _, _ = coordinates.shape
    n_angles = triplets.shape[0]
    out = np.zeros((n_structures, n_angles), dtype=np.float64)

    threads_per_block = (16, 16)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_angles     / threads_per_block[1]),
    )

    d_coords = cuda.to_device(coordinates)
    d_trip   = cuda.to_device(triplets.astype(np.int64))
    d_out    = cuda.to_device(out)

    _get_angles_kernel[blocks, threads_per_block](d_coords, d_trip, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out


def get_mic_angles(coordinates: np.ndarray, box: np.ndarray, triplets: np.ndarray) -> np.ndarray:
    """3-body valence angles under PBC/MIC."""
    n_structures, _, _ = coordinates.shape
    n_angles = triplets.shape[0]
    out = np.zeros((n_structures, n_angles), dtype=np.float64)

    threads_per_block = (16, 16)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_angles     / threads_per_block[1]),
    )

    d_coords = cuda.to_device(coordinates)
    d_box    = cuda.to_device(box)
    d_trip   = cuda.to_device(triplets.astype(np.int64))
    d_out    = cuda.to_device(out)

    _get_mic_angles_kernel[blocks, threads_per_block](d_coords, d_box, d_trip, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out
