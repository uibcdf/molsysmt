"""
CUDA kernels for Shrake-Rupley Solvent-Accessible Surface Area (SASA) calculations.

Requires: numba with CUDA support (``numba[cuda]``) and a CUDA-capable GPU.
"""

from __future__ import annotations

import math
import numpy as np


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


try:
    from numba import cuda

    # ---------------------------------------------------------------------------
    # CUDA device helpers
    # ---------------------------------------------------------------------------

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
        # Cramer's inverse
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

        sx -= math.floor(sx + 0.5)
        sy -= math.floor(sy + 0.5)
        sz -= math.floor(sz + 0.5)

        cx = b00 * sx + b01 * sy + b02 * sz
        cy = b10 * sx + b11 * sy + b12 * sz
        cz = b20 * sx + b21 * sy + b22 * sz

        return cx, cy, cz

    @cuda.jit(device=True)
    def _mic_wrap_vector(dx, dy, dz, box_s):
        """MIC wrap helper."""
        if _is_orthogonal(box_s):
            return _mic_wrap_vector_orthogonal(
                dx, dy, dz,
                box_s[0, 0], box_s[1, 1], box_s[2, 2]
            )
        else:
            return _mic_wrap_vector_triclinic(dx, dy, dz, box_s)

    # -----------------------------------------------------------------------
    # Shrake-Rupley CUDA Kernels
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_sasa_kernel(coords, radii, sphere_points, probe_radius, out):
        """Thread grid: (frame, atom_idx)."""
        ii, jj = cuda.grid(2)
        n_structures = coords.shape[0]
        n_atoms = coords.shape[1]
        n_points = sphere_points.shape[0]

        if ii >= n_structures or jj >= n_atoms:
            return

        r_i_ext = radii[jj] + probe_radius
        if r_i_ext <= probe_radius:
            out[ii, jj] = 0.0
            return

        accessible_count = 0

        for kk in range(n_points):
            # Scale and shift sphere point
            px = coords[ii, jj, 0] + r_i_ext * sphere_points[kk, 0]
            py = coords[ii, jj, 1] + r_i_ext * sphere_points[kk, 1]
            pz = coords[ii, jj, 2] + r_i_ext * sphere_points[kk, 2]

            is_accessible = True

            for ll in range(n_atoms):
                if ll == jj:
                    continue

                r_l_ext = radii[ll] + probe_radius
                if r_l_ext <= probe_radius:
                    continue

                # Distance check
                dx = px - coords[ii, ll, 0]
                dy = py - coords[ii, ll, 1]
                dz = pz - coords[ii, ll, 2]

                dist_sq = dx*dx + dy*dy + dz*dz
                if dist_sq < r_l_ext * r_l_ext:
                    is_accessible = False
                    break

            if is_accessible:
                accessible_count += 1

        out[ii, jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    @cuda.jit
    def _get_mic_sasa_kernel(coords, box, radii, sphere_points, probe_radius, out):
        """Thread grid: (frame, atom_idx) under PBC."""
        ii, jj = cuda.grid(2)
        n_structures = coords.shape[0]
        n_atoms = coords.shape[1]
        n_points = sphere_points.shape[0]

        if ii >= n_structures or jj >= n_atoms:
            return

        r_i_ext = radii[jj] + probe_radius
        if r_i_ext <= probe_radius:
            out[ii, jj] = 0.0
            return

        accessible_count = 0
        box_s = box[ii]

        for kk in range(n_points):
            # Shift point
            px = coords[ii, jj, 0] + r_i_ext * sphere_points[kk, 0]
            py = coords[ii, jj, 1] + r_i_ext * sphere_points[kk, 1]
            pz = coords[ii, jj, 2] + r_i_ext * sphere_points[kk, 2]

            is_accessible = True

            for ll in range(n_atoms):
                if ll == jj:
                    continue

                r_l_ext = radii[ll] + probe_radius
                if r_l_ext <= probe_radius:
                    continue

                # Displacement vector under Minimum Image Convention
                dx = px - coords[ii, ll, 0]
                dy = py - coords[ii, ll, 1]
                dz = pz - coords[ii, ll, 2]
                dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box_s)

                dist_sq = dx*dx + dy*dy + dz*dz
                if dist_sq < r_l_ext * r_l_ext:
                    is_accessible = False
                    break

            if is_accessible:
                accessible_count += 1

        out[ii, jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Entrypoints
# ---------------------------------------------------------------------------

def get_sasa(
    coordinates: np.ndarray,
    radii: np.ndarray,
    probe_radius: float = 0.14,
    n_points: int = 100
) -> np.ndarray:
    """SASA calculation in vacuum."""
    n_structures, n_atoms, _ = coordinates.shape
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)

    threads_per_block = (16, 16)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_atoms      / threads_per_block[1]),
    )

    sphere_pts = get_fibonacci_sphere_points(n_points)

    d_coords = cuda.to_device(coordinates)
    d_radii  = cuda.to_device(radii)
    d_pts    = cuda.to_device(sphere_pts)
    d_out    = cuda.to_device(out)

    _get_sasa_kernel[blocks, threads_per_block](d_coords, d_radii, d_pts, probe_radius, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out


def get_mic_sasa(
    coordinates: np.ndarray,
    box: np.ndarray,
    radii: np.ndarray,
    probe_radius: float = 0.14,
    n_points: int = 100
) -> np.ndarray:
    """SASA calculation under PBC/MIC."""
    n_structures, n_atoms, _ = coordinates.shape
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)

    threads_per_block = (16, 16)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_atoms      / threads_per_block[1]),
    )

    sphere_pts = get_fibonacci_sphere_points(n_points)

    d_coords = cuda.to_device(coordinates)
    d_box    = cuda.to_device(box)
    d_radii  = cuda.to_device(radii)
    d_pts    = cuda.to_device(sphere_pts)
    d_out    = cuda.to_device(out)

    _get_mic_sasa_kernel[blocks, threads_per_block](d_coords, d_box, d_radii, d_pts, probe_radius, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out
