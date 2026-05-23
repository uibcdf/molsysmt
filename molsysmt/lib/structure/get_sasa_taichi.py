"""
Experimental Taichi Lang backend for Shrake-Rupley SASA calculations.

Compiles JIT to Vulkan, Metal, CUDA, or CPU depending on hardware availability.
Avoids any top-level import of `taichi` to conform with lazy-loading invariants.
"""

from __future__ import annotations
import numpy as np
import math


_KERNELS_CACHE = None


def get_fibonacci_sphere_points(n_points: int) -> np.ndarray:
    """Generate N evenly distributed points on a unit sphere using the Fibonacci spiral."""
    points = []
    golden_ratio = (1.0 + math.sqrt(5.0)) / 2.0
    for i in range(n_points):
        theta = math.acos(1.0 - 2.0 * (i + 0.5) / n_points)
        phi = 2.0 * math.pi * i / golden_ratio
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)
        points.append([x, y, z])
    return np.array(points, dtype=np.float64)


def _get_taichi():
    """Import and lazily initialize Taichi Lang on the optimal hardware backend."""
    import taichi as ti
    try:
        ti.lang.impl.current_cfg().arch
    except Exception:
        ti.init(arch=ti.gpu)
    return ti


class TaichiSasaKernels:
    """Encapsulation of JIT compiled Taichi kernels for SASA."""

    def __init__(self, ti):
        self.ti = ti

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
        # Shrake-Rupley Taichi Kernels
        # -------------------------------------------------------------------

        @ti.kernel
        def _get_sasa_kernel(
            coords: ti.types.ndarray(),
            radii: ti.types.ndarray(),
            sphere_points: ti.types.ndarray(),
            probe_radius: float,
            out: ti.types.ndarray()
        ):
            for ii, jj in out:
                n_atoms = coords.shape[1]
                n_points = sphere_points.shape[0]

                r_i_ext = radii[jj] + probe_radius
                if r_i_ext <= probe_radius:
                    out[ii, jj] = 0.0
                else:
                    accessible_count = 0.0

                    for kk in range(n_points):
                        px = coords[ii, jj, 0] + r_i_ext * sphere_points[kk, 0]
                        py = coords[ii, jj, 1] + r_i_ext * sphere_points[kk, 1]
                        pz = coords[ii, jj, 2] + r_i_ext * sphere_points[kk, 2]

                        is_accessible = True

                        for ll in range(n_atoms):
                            if ll != jj:
                                r_l_ext = radii[ll] + probe_radius
                                if r_l_ext > probe_radius:
                                    dx = px - coords[ii, ll, 0]
                                    dy = py - coords[ii, ll, 1]
                                    dz = pz - coords[ii, ll, 2]

                                    dist_sq = dx*dx + dy*dy + dz*dz
                                    if dist_sq < r_l_ext * r_l_ext:
                                        is_accessible = False
                                        break

                        if is_accessible:
                            accessible_count += 1.0

                    out[ii, jj] = 4.0 * 3.141592653589793 * r_i_ext * r_i_ext * (accessible_count / n_points)

        self.get_sasa = _get_sasa_kernel

        @ti.kernel
        def _get_mic_sasa_kernel(
            coords: ti.types.ndarray(),
            box: ti.types.ndarray(),
            radii: ti.types.ndarray(),
            sphere_points: ti.types.ndarray(),
            probe_radius: float,
            out: ti.types.ndarray()
        ):
            for ii, jj in out:
                n_atoms = coords.shape[1]
                n_points = sphere_points.shape[0]

                r_i_ext = radii[jj] + probe_radius
                if r_i_ext <= probe_radius:
                    out[ii, jj] = 0.0
                else:
                    accessible_count = 0.0
                    box_s = ti.Matrix([
                        [box[ii, 0, 0], box[ii, 0, 1], box[ii, 0, 2]],
                        [box[ii, 1, 0], box[ii, 1, 1], box[ii, 1, 2]],
                        [box[ii, 2, 0], box[ii, 2, 1], box[ii, 2, 2]]
                    ])

                    for kk in range(n_points):
                        px = coords[ii, jj, 0] + r_i_ext * sphere_points[kk, 0]
                        py = coords[ii, jj, 1] + r_i_ext * sphere_points[kk, 1]
                        pz = coords[ii, jj, 2] + r_i_ext * sphere_points[kk, 2]

                        is_accessible = True

                        for ll in range(n_atoms):
                            if ll != jj:
                                r_l_ext = radii[ll] + probe_radius
                                if r_l_ext > probe_radius:
                                    dx = px - coords[ii, ll, 0]
                                    dy = py - coords[ii, ll, 1]
                                    dz = pz - coords[ii, ll, 2]
                                    dx, dy, dz = mic_wrap_vector(dx, dy, dz, box_s)

                                    dist_sq = dx*dx + dy*dy + dz*dz
                                    if dist_sq < r_l_ext * r_l_ext:
                                        is_accessible = False
                                        break

                        if is_accessible:
                            accessible_count += 1.0

                    out[ii, jj] = 4.0 * 3.141592653589793 * r_i_ext * r_i_ext * (accessible_count / n_points)

        self.get_mic_sasa = _get_mic_sasa_kernel


def _get_kernels():
    """Retrieve or compile the cached Taichi SASA kernels."""
    global _KERNELS_CACHE
    if _KERNELS_CACHE is None:
        ti = _get_taichi()
        _KERNELS_CACHE = TaichiSasaKernels(ti)
    return _KERNELS_CACHE


# ---------------------------------------------------------------------------
# Public Entrypoints
# ---------------------------------------------------------------------------

def get_sasa(
    coordinates: np.ndarray,
    radii: np.ndarray,
    probe_radius: float = 0.14,
    n_points: int = 100
) -> np.ndarray:
    """SASA calculation in vacuum using Taichi."""
    n_structures, n_atoms, _ = coordinates.shape
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)
    sphere_pts = get_fibonacci_sphere_points(n_points)
    kernels = _get_kernels()
    kernels.get_sasa(coordinates, radii, sphere_pts, probe_radius, out)
    return out


def get_mic_sasa(
    coordinates: np.ndarray,
    box: np.ndarray,
    radii: np.ndarray,
    probe_radius: float = 0.14,
    n_points: int = 100
) -> np.ndarray:
    """SASA calculation under PBC/MIC using Taichi."""
    n_structures, n_atoms, _ = coordinates.shape
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)
    sphere_pts = get_fibonacci_sphere_points(n_points)
    kernels = _get_kernels()
    kernels.get_mic_sasa(coordinates, box, radii, sphere_pts, probe_radius, out)
    return out
