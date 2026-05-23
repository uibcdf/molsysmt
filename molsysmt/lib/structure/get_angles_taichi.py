"""
Experimental Taichi Lang backend for 3-body valence angle calculations.

Compiles JIT to Vulkan, Metal, CUDA, or CPU depending on hardware availability.
Avoids any top-level import of `taichi` to conform with lazy-loading invariants.
"""

from __future__ import annotations
import numpy as np


_KERNELS_CACHE = None


def _get_taichi():
    """Import and lazily initialize Taichi Lang on the optimal hardware backend."""
    import taichi as ti
    try:
        ti.lang.impl.current_cfg().arch
    except Exception:
        ti.init(arch=ti.gpu)
    return ti


class TaichiAnglesKernels:
    """Encapsulation of JIT compiled Taichi kernels for valence angles."""

    def __init__(self, ti):
        self.ti = ti

        @ti.func
        def _angle(vx, vy, vz, wx, wy, wz):
            dot = vx * wx + vy * wy + vz * wz
            norm_v = ti.sqrt(vx * vx + vy * vy + vz * vz)
            norm_w = ti.sqrt(wx * wx + wy * wy + wz * wz)
            cosa = 0.0
            if norm_v > 1e-10 and norm_w > 1e-10:
                cosa = dot / (norm_v * norm_w)
            if cosa >= 1.0:
                cosa = 1.0
            elif cosa <= -1.0:
                cosa = -1.0
            return ti.acos(cosa)

        @ti.func
        def is_orthogonal(box_s):
            tol = 1e-10
            return (
                ti.abs(box_s[0, 1]) < tol and ti.abs(box_s[0, 2]) < tol and
                ti.abs(box_s[1, 0]) < tol and ti.abs(box_s[1, 2]) < tol and
                ti.abs(box_s[2, 0]) < tol and ti.abs(box_s[2, 1]) < tol
            )

        @ti.func
        def mic_wrap_vector_orthogonal(dx, dy, dz, lx, ly, lz):
            rx = dx - lx * ti.floor(dx / lx + 0.5)
            ry = dy - ly * ti.floor(dy / ly + 0.5)
            rz = dz - lz * ti.floor(dz / lz + 0.5)
            return rx, ry, rz

        @ti.func
        def mic_wrap_vector_triclinic(dx, dy, dz, box_s):
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

            sx -= ti.floor(sx + 0.5)
            sy -= ti.floor(sy + 0.5)
            sz -= ti.floor(sz + 0.5)

            cx = b00 * sx + b01 * sy + b02 * sz
            cy = b10 * sx + b11 * sy + b12 * sz
            cz = b20 * sx + b21 * sy + b22 * sz

            return cx, cy, cz

        @ti.func
        def mic_wrap_vector(dx, dy, dz, box_s):
            rx, ry, rz = 0.0, 0.0, 0.0
            if is_orthogonal(box_s):
                rx, ry, rz = mic_wrap_vector_orthogonal(
                    dx, dy, dz,
                    box_s[0, 0], box_s[1, 1], box_s[2, 2]
                )
            else:
                rx, ry, rz = mic_wrap_vector_triclinic(dx, dy, dz, box_s)
            return rx, ry, rz

        # -------------------------------------------------------------------
        # JIT Kernels
        # -------------------------------------------------------------------

        @ti.kernel
        def _get_angles_kernel(
            coords: ti.types.ndarray(),
            triplets: ti.types.ndarray(),
            out: ti.types.ndarray()
        ):
            for ii, jj in out:
                at0 = triplets[jj, 0]
                at1 = triplets[jj, 1]
                at2 = triplets[jj, 2]

                v0x = coords[ii, at0, 0] - coords[ii, at1, 0]
                v0y = coords[ii, at0, 1] - coords[ii, at1, 1]
                v0z = coords[ii, at0, 2] - coords[ii, at1, 2]

                v1x = coords[ii, at2, 0] - coords[ii, at1, 0]
                v1y = coords[ii, at2, 1] - coords[ii, at1, 1]
                v1z = coords[ii, at2, 2] - coords[ii, at1, 2]

                out[ii, jj] = _angle(v0x, v0y, v0z, v1x, v1y, v1z)

        self.get_angles = _get_angles_kernel

        @ti.kernel
        def _get_mic_angles_kernel(
            coords: ti.types.ndarray(),
            box: ti.types.ndarray(),
            triplets: ti.types.ndarray(),
            out: ti.types.ndarray()
        ):
            for ii, jj in out:
                at0 = triplets[jj, 0]
                at1 = triplets[jj, 1]
                at2 = triplets[jj, 2]

                v0x = coords[ii, at0, 0] - coords[ii, at1, 0]
                v0y = coords[ii, at0, 1] - coords[ii, at1, 1]
                v0z = coords[ii, at0, 2] - coords[ii, at1, 2]

                v1x = coords[ii, at2, 0] - coords[ii, at1, 0]
                v1y = coords[ii, at2, 1] - coords[ii, at1, 1]
                v1z = coords[ii, at2, 2] - coords[ii, at1, 2]

                box_s = ti.Matrix([
                    [box[ii, 0, 0], box[ii, 0, 1], box[ii, 0, 2]],
                    [box[ii, 1, 0], box[ii, 1, 1], box[ii, 1, 2]],
                    [box[ii, 2, 0], box[ii, 2, 1], box[ii, 2, 2]]
                ])
                v0x, v0y, v0z = mic_wrap_vector(v0x, v0y, v0z, box_s)
                v1x, v1y, v1z = mic_wrap_vector(v1x, v1y, v1z, box_s)

                out[ii, jj] = _angle(v0x, v0y, v0z, v1x, v1y, v1z)

        self.get_mic_angles = _get_mic_angles_kernel


def _get_kernels():
    """Retrieve or compile the cached Taichi angles kernels."""
    global _KERNELS_CACHE
    if _KERNELS_CACHE is None:
        ti = _get_taichi()
        _KERNELS_CACHE = TaichiAnglesKernels(ti)
    return _KERNELS_CACHE


# ---------------------------------------------------------------------------
# Public Entrypoints
# ---------------------------------------------------------------------------

def get_angles(coordinates: np.ndarray, triplets: np.ndarray) -> np.ndarray:
    """3-body valence angles under vacuum using Taichi."""
    n_structures, _, _ = coordinates.shape
    n_angles = triplets.shape[0]
    out = np.zeros((n_structures, n_angles), dtype=np.float64)
    kernels = _get_kernels()
    kernels.get_angles(coordinates, triplets.astype(np.int64), out)
    return out


def get_mic_angles(coordinates: np.ndarray, box: np.ndarray, triplets: np.ndarray) -> np.ndarray:
    """3-body valence angles under PBC/MIC using Taichi."""
    n_structures, _, _ = coordinates.shape
    n_angles = triplets.shape[0]
    out = np.zeros((n_structures, n_angles), dtype=np.float64)
    kernels = _get_kernels()
    kernels.get_mic_angles(coordinates, box, triplets.astype(np.int64), out)
    return out
