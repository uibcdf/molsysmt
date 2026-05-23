"""
Experimental Taichi Lang backend for contact calculations (multi-vendor GPU / CPU).

Compiles JIT to Vulkan, Metal, CUDA, or CPU depending on hardware availability.
Avoids any top-level import of `taichi` to conform with lazy-loading invariants.
"""

from __future__ import annotations
import numpy as np


_KERNELS_CACHE = None


def _get_taichi():
    """Import and lazily initialize Taichi Lang on the optimal hardware backend."""
    import taichi as ti
    # Check if already initialized, otherwise initialize with GPU preference
    try:
        ti.lang.impl.current_cfg().arch
    except Exception:
        # Prefers Vulkan/Metal/CUDA depending on platform; falls back to CPU
        ti.init(arch=ti.gpu)
    return ti


class TaichiContactsKernels:
    """Encapsulation of JIT compiled Taichi kernels to prevent early imports."""

    def __init__(self, ti):
        self.ti = ti

        # -------------------------------------------------------------------
        # Vacuum Kernels
        # -------------------------------------------------------------------

        @ti.kernel
        def _get_contacts_single_system_kernel(
            coords: ti.types.ndarray(),
            threshold: float,
            out: ti.types.ndarray()
        ):
            for ii, jj, kk in out:
                ax = coords[ii, jj, 0]
                ay = coords[ii, jj, 1]
                az = coords[ii, jj, 2]
                bx = coords[ii, kk, 0]
                by = coords[ii, kk, 1]
                bz = coords[ii, kk, 2]
                dx = bx - ax
                dy = by - ay
                dz = bz - az
                dist = ti.sqrt(dx*dx + dy*dy + dz*dz)
                out[ii, jj, kk] = (dist <= threshold)

        self.get_contacts_single_system = _get_contacts_single_system_kernel

        @ti.kernel
        def _get_contacts_kernel(
            coords1: ti.types.ndarray(),
            coords2: ti.types.ndarray(),
            threshold: float,
            out: ti.types.ndarray()
        ):
            for ii, jj, kk in out:
                ax = coords1[ii, jj, 0]
                ay = coords1[ii, jj, 1]
                az = coords1[ii, jj, 2]
                bx = coords2[ii, kk, 0]
                by = coords2[ii, kk, 1]
                bz = coords2[ii, kk, 2]
                dx = bx - ax
                dy = by - ay
                dz = bz - az
                dist = ti.sqrt(dx*dx + dy*dy + dz*dz)
                out[ii, jj, kk] = (dist <= threshold)

        self.get_contacts = _get_contacts_kernel

        @ti.kernel
        def _get_contacts_pairs_kernel(
            coords1: ti.types.ndarray(),
            coords2: ti.types.ndarray(),
            threshold: float,
            out: ti.types.ndarray()
        ):
            for ii, jj in out:
                ax = coords1[ii, jj, 0]
                ay = coords1[ii, jj, 1]
                az = coords1[ii, jj, 2]
                bx = coords2[ii, jj, 0]
                by = coords2[ii, jj, 1]
                bz = coords2[ii, jj, 2]
                dx = bx - ax
                dy = by - ay
                dz = bz - az
                dist = ti.sqrt(dx*dx + dy*dy + dz*dz)
                out[ii, jj] = (dist <= threshold)

        self.get_contacts_pairs = _get_contacts_pairs_kernel

        # -------------------------------------------------------------------
        # MIC / PBC Device Functions
        # -------------------------------------------------------------------

        @ti.func
        def is_orthogonal(box_s):
            tol = 1e-10
            return (
                ti.abs(box_s[0, 1]) < tol and ti.abs(box_s[0, 2]) < tol and
                ti.abs(box_s[1, 0]) < tol and ti.abs(box_s[1, 2]) < tol and
                ti.abs(box_s[2, 0]) < tol and ti.abs(box_s[2, 1]) < tol
            )

        @ti.func
        def mic_dist_orthogonal(ax, ay, az, bx, by, bz, lx, ly, lz):
            dx = bx - ax
            dy = by - ay
            dz = bz - az
            dx -= lx * ti.floor(dx / lx + 0.5)
            dy -= ly * ti.floor(dy / ly + 0.5)
            dz -= lz * ti.floor(dz / lz + 0.5)
            return ti.sqrt(dx*dx + dy*dy + dz*dz)

        @ti.func
        def mic_dist_triclinic(ax, ay, az, bx, by, bz, box_s):
            dx = bx - ax
            dy = by - ay
            dz = bz - az

            # Matrix inverse via Cramer's rule
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

            sx -= ti.floor(sx + 0.5)
            sy -= ti.floor(sy + 0.5)
            sz -= ti.floor(sz + 0.5)

            # Back to Cartesian
            cx = b00 * sx + b01 * sy + b02 * sz
            cy = b10 * sx + b11 * sy + b12 * sz
            cz = b20 * sx + b21 * sy + b22 * sz

            return ti.sqrt(cx*cx + cy*cy + cz*cz)

        @ti.func
        def mic_dist(ax, ay, az, bx, by, bz, box_s):
            d = 0.0
            if is_orthogonal(box_s):
                d = mic_dist_orthogonal(
                    ax, ay, az, bx, by, bz,
                    box_s[0, 0], box_s[1, 1], box_s[2, 2]
                )
            else:
                d = mic_dist_triclinic(ax, ay, az, bx, by, bz, box_s)
            return d

        # -------------------------------------------------------------------
        # MIC / PBC Kernels
        # -------------------------------------------------------------------

        @ti.kernel
        def _get_mic_contacts_single_system_kernel(
            coords: ti.types.ndarray(),
            box: ti.types.ndarray(),
            threshold: float,
            out: ti.types.ndarray()
        ):
            for ii, jj, kk in out:
                box_s = ti.Matrix([
                    [box[ii, 0, 0], box[ii, 0, 1], box[ii, 0, 2]],
                    [box[ii, 1, 0], box[ii, 1, 1], box[ii, 1, 2]],
                    [box[ii, 2, 0], box[ii, 2, 1], box[ii, 2, 2]]
                ])
                d = mic_dist(
                    coords[ii, jj, 0], coords[ii, jj, 1], coords[ii, jj, 2],
                    coords[ii, kk, 0], coords[ii, kk, 1], coords[ii, kk, 2],
                    box_s
                )
                out[ii, jj, kk] = (d <= threshold)

        self.get_mic_contacts_single_system = _get_mic_contacts_single_system_kernel

        @ti.kernel
        def _get_mic_contacts_kernel(
            coords1: ti.types.ndarray(),
            coords2: ti.types.ndarray(),
            box: ti.types.ndarray(),
            threshold: float,
            out: ti.types.ndarray()
        ):
            for ii, jj, kk in out:
                box_s = ti.Matrix([
                    [box[ii, 0, 0], box[ii, 0, 1], box[ii, 0, 2]],
                    [box[ii, 1, 0], box[ii, 1, 1], box[ii, 1, 2]],
                    [box[ii, 2, 0], box[ii, 2, 1], box[ii, 2, 2]]
                ])
                d = mic_dist(
                    coords1[ii, jj, 0], coords1[ii, jj, 1], coords1[ii, jj, 2],
                    coords2[ii, kk, 0], coords2[ii, kk, 1], coords2[ii, kk, 2],
                    box_s
                )
                out[ii, jj, kk] = (d <= threshold)

        self.get_mic_contacts = _get_mic_contacts_kernel

        @ti.kernel
        def _get_mic_contacts_pairs_kernel(
            coords1: ti.types.ndarray(),
            coords2: ti.types.ndarray(),
            box: ti.types.ndarray(),
            threshold: float,
            out: ti.types.ndarray()
        ):
            for ii, jj in out:
                box_s = ti.Matrix([
                    [box[ii, 0, 0], box[ii, 0, 1], box[ii, 0, 2]],
                    [box[ii, 1, 0], box[ii, 1, 1], box[ii, 1, 2]],
                    [box[ii, 2, 0], box[ii, 2, 1], box[ii, 2, 2]]
                ])
                d = mic_dist(
                    coords1[ii, jj, 0], coords1[ii, jj, 1], coords1[ii, jj, 2],
                    coords2[ii, jj, 0], coords2[ii, jj, 1], coords2[ii, jj, 2],
                    box_s
                )
                out[ii, jj] = (d <= threshold)

        self.get_mic_contacts_pairs = _get_mic_contacts_pairs_kernel


def _get_kernels():
    """Retrieve or compile the cached Taichi contacts kernels."""
    global _KERNELS_CACHE
    if _KERNELS_CACHE is None:
        ti = _get_taichi()
        _KERNELS_CACHE = TaichiContactsKernels(ti)
    return _KERNELS_CACHE


# ---------------------------------------------------------------------------
# Public Python Entrypoints
# ---------------------------------------------------------------------------

def get_contacts_single_system(coordinates: np.ndarray, threshold: float) -> np.ndarray:
    """All-vs-all contacts within a single system (vacuum) using Taichi."""
    n_structures, n_atoms, _ = coordinates.shape
    out = np.zeros((n_structures, n_atoms, n_atoms), dtype=bool)
    kernels = _get_kernels()
    kernels.get_contacts_single_system(coordinates, threshold, out)
    return out


def get_contacts(coordinates1: np.ndarray, coordinates2: np.ndarray, threshold: float) -> np.ndarray:
    """Cross-system contacts (vacuum) using Taichi."""
    n_structures, n_atoms1, _ = coordinates1.shape
    n_atoms2 = coordinates2.shape[1]
    out = np.zeros((n_structures, n_atoms1, n_atoms2), dtype=bool)
    kernels = _get_kernels()
    kernels.get_contacts(coordinates1, coordinates2, threshold, out)
    return out


def get_contacts_pairs(coordinates1: np.ndarray, coordinates2: np.ndarray, threshold: float) -> np.ndarray:
    """Specific pair-wise contacts (vacuum) using Taichi."""
    n_structures, n_pairs, _ = coordinates1.shape
    out = np.zeros((n_structures, n_pairs), dtype=bool)
    kernels = _get_kernels()
    kernels.get_contacts_pairs(coordinates1, coordinates2, threshold, out)
    return out


def get_mic_contacts_single_system(coordinates: np.ndarray, box: np.ndarray, threshold: float) -> np.ndarray:
    """All-vs-all contacts within a single system under PBC/MIC using Taichi."""
    n_structures, n_atoms, _ = coordinates.shape
    out = np.zeros((n_structures, n_atoms, n_atoms), dtype=bool)
    kernels = _get_kernels()
    kernels.get_mic_contacts_single_system(coordinates, box, threshold, out)
    return out


def get_mic_contacts(coordinates1: np.ndarray, coordinates2: np.ndarray, box: np.ndarray, threshold: float) -> np.ndarray:
    """Cross-system contacts under PBC/MIC using Taichi."""
    n_structures, n_atoms1, _ = coordinates1.shape
    n_atoms2 = coordinates2.shape[1]
    out = np.zeros((n_structures, n_atoms1, n_atoms2), dtype=bool)
    kernels = _get_kernels()
    kernels.get_mic_contacts(coordinates1, coordinates2, box, threshold, out)
    return out


def get_mic_contacts_pairs(coordinates1: np.ndarray, coordinates2: np.ndarray, box: np.ndarray, threshold: float) -> np.ndarray:
    """Specific pair-wise contacts under PBC/MIC using Taichi."""
    n_structures, n_pairs, _ = coordinates1.shape
    out = np.zeros((n_structures, n_pairs), dtype=bool)
    kernels = _get_kernels()
    kernels.get_mic_contacts_pairs(coordinates1, coordinates2, box, threshold, out)
    return out
