"""
Experimental Taichi Lang backend for Kabsch least-RMSD fit (rigid superposition).

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


class TaichiLeastRmsdKernels:
    """Encapsulation of JIT compiled Taichi kernels for Kabsch least-RMSD alignment."""

    def __init__(self, ti):
        self.ti = ti

        @ti.func
        def _jacobi_eigh4(A, V):
            for i in range(4):
                for j in range(4):
                    V[i, j] = 1.0 if i == j else 0.0

            for _ in range(64):
                max_val = 0.0
                p = 0
                q = 1
                for i in range(4):
                    for j in range(i + 1, 4):
                        aij = ti.abs(A[i, j])
                        if aij > max_val:
                            max_val = aij
                            p = i
                            q = j

                if max_val < 1e-14:
                    break

                theta = 0.5 * ti.atan2(2.0 * A[p, q], A[q, q] - A[p, p])
                c = ti.cos(theta)
                s = ti.sin(theta)

                App = A[p, p]
                Aqq = A[q, q]
                Apq = A[p, q]

                A[p, p] = c * c * App - 2.0 * c * s * Apq + s * s * Aqq
                A[q, q] = s * s * App + 2.0 * c * s * Apq + c * c * Aqq
                A[p, q] = 0.0
                A[q, p] = 0.0

                for r in range(4):
                    if r != p and r != q:
                        arp = A[r, p]
                        arq = A[r, q]
                        A[r, p] = c * arp - s * arq
                        A[p, r] = A[r, p]
                        A[r, q] = s * arp + c * arq
                        A[q, r] = A[r, q]

                for k in range(4):
                    Vkp = c * V[k, p] - s * V[k, q]
                    Vkq = s * V[k, p] + c * V[k, q]
                    V[k, p] = Vkp
                    V[k, q] = Vkq

            for i in range(1, 4):
                key = A[i, i]
                v0 = V[0, i]
                v1 = V[1, i]
                v2 = V[2, i]
                v3 = V[3, i]
                j = i - 1
                while j >= 0 and A[j, j] > key:
                    A[j + 1, j + 1] = A[j, j]
                    V[0, j + 1] = V[0, j]
                    V[1, j + 1] = V[1, j]
                    V[2, j + 1] = V[2, j]
                    V[3, j + 1] = V[3, j]
                    j -= 1
                A[j + 1, j + 1] = key
                V[0, j + 1] = v0
                V[1, j + 1] = v1
                V[2, j + 1] = v2
                V[3, j + 1] = v3

        @ti.func
        def _quaternion_to_rotation_matrix(q, U):
            q0 = q[0]
            q1 = q[1]
            q2 = q[2]
            q3 = q[3]

            q00 = 2.0 * q0 * q0
            q11 = 2.0 * q1 * q1
            q22 = 2.0 * q2 * q2
            q33 = 2.0 * q3 * q3

            q01 = 2.0 * q0 * q1
            q02 = 2.0 * q0 * q2
            q03 = 2.0 * q0 * q3
            q12 = 2.0 * q1 * q2
            q13 = 2.0 * q1 * q3
            q23 = 2.0 * q2 * q3

            U[0, 0] = q00 + q11 - 1.0
            U[1, 1] = q00 + q22 - 1.0
            U[2, 2] = q00 + q33 - 1.0

            U[0, 1] = q12 - q03
            U[1, 0] = q12 + q03

            U[0, 2] = q13 + q02
            U[2, 0] = q13 - q02

            U[1, 2] = q23 - q01
            U[2, 1] = q23 + q01

        @ti.kernel
        def least_rmsd_fit_kernel(
            coords_to_move: ti.template(),
            fit_coords: ti.template(),
            ref_coords: ti.template(),
            ref_is_single: int
        ):
            ti.loop_config(serialize=False)
            for ii in range(coords_to_move.shape[0]):
                n_fit_atoms = fit_coords.shape[1]
                n_move_atoms = coords_to_move.shape[1]

                # Compute query centroid
                c_query_x = 0.0
                c_query_y = 0.0
                c_query_z = 0.0
                for j in range(n_fit_atoms):
                    c_query_x += fit_coords[ii, j, 0]
                    c_query_y += fit_coords[ii, j, 1]
                    c_query_z += fit_coords[ii, j, 2]
                c_query_x /= n_fit_atoms
                c_query_y /= n_fit_atoms
                c_query_z /= n_fit_atoms

                # Compute reference centroid
                c_ref_x = 0.0
                c_ref_y = 0.0
                c_ref_z = 0.0
                ref_idx = 0 if ref_is_single == 1 else ii
                for j in range(n_fit_atoms):
                    c_ref_x += ref_coords[ref_idx, j, 0]
                    c_ref_y += ref_coords[ref_idx, j, 1]
                    c_ref_z += ref_coords[ref_idx, j, 2]
                c_ref_x /= n_fit_atoms
                c_ref_y /= n_fit_atoms
                c_ref_z /= n_fit_atoms

                # Compute covariance matrix R (3x3)
                R00 = 0.0; R01 = 0.0; R02 = 0.0
                R10 = 0.0; R11 = 0.0; R12 = 0.0
                R20 = 0.0; R21 = 0.0; R22 = 0.0
                for j in range(n_fit_atoms):
                    dx = ref_coords[ref_idx, j, 0] - c_ref_x
                    dy = fit_coords[ii, j, 0] - c_query_x
                    R00 += dx * dy
                    dy = fit_coords[ii, j, 1] - c_query_y
                    R01 += dx * dy
                    dy = fit_coords[ii, j, 2] - c_query_z
                    R02 += dx * dy

                    dx = ref_coords[ref_idx, j, 1] - c_ref_y
                    dy = fit_coords[ii, j, 0] - c_query_x
                    R10 += dx * dy
                    dy = fit_coords[ii, j, 1] - c_query_y
                    R11 += dx * dy
                    dy = fit_coords[ii, j, 2] - c_query_z
                    R12 += dx * dy

                    dx = ref_coords[ref_idx, j, 2] - c_ref_z
                    dy = fit_coords[ii, j, 0] - c_query_x
                    R20 += dx * dy
                    dy = fit_coords[ii, j, 1] - c_query_y
                    R21 += dx * dy
                    dy = fit_coords[ii, j, 2] - c_query_z
                    R22 += dx * dy

                # Construct F matrix (4x4)
                F = ti.Matrix.zero(ti.f64, 4, 4)
                F[0, 0] = R00 + R11 + R22
                F[1, 0] = R12 - R21
                F[2, 0] = R20 - R02
                F[3, 0] = R01 - R10
                F[0, 1] = F[1, 0]
                F[1, 1] = R00 - R11 - R22
                F[2, 1] = R01 + R10
                F[3, 1] = R02 + R20
                F[0, 2] = F[2, 0]
                F[1, 2] = F[2, 1]
                F[2, 2] = -R00 + R11 - R22
                F[3, 2] = R12 + R21
                F[0, 3] = F[3, 0]
                F[1, 3] = F[3, 1]
                F[2, 3] = F[3, 2]
                F[3, 3] = -R00 - R11 + R22

                V = ti.Matrix.zero(ti.f64, 4, 4)
                _jacobi_eigh4(F, V)

                # Quaternion q
                q = ti.Vector([V[0, 3], V[1, 3], V[2, 3], V[3, 3]])

                # Rotation matrix U (3x3)
                U = ti.Matrix.zero(ti.f64, 3, 3)
                _quaternion_to_rotation_matrix(q, U)

                # Rotate and translate coords_to_move in-place
                for j in range(n_move_atoms):
                    dx = coords_to_move[ii, j, 0] - c_query_x
                    dy = coords_to_move[ii, j, 1] - c_query_y
                    dz = coords_to_move[ii, j, 2] - c_query_z

                    coords_to_move[ii, j, 0] = U[0, 0] * dx + U[0, 1] * dy + U[0, 2] * dz + c_ref_x
                    coords_to_move[ii, j, 1] = U[1, 0] * dx + U[1, 1] * dy + U[1, 2] * dz + c_ref_y
                    coords_to_move[ii, j, 2] = U[2, 0] * dx + U[2, 1] * dy + U[2, 2] * dz + c_ref_z

        self.least_rmsd_fit_kernel = least_rmsd_fit_kernel


def least_rmsd_fit(coords_to_move: np.ndarray, fit_coords: np.ndarray, ref_coords: np.ndarray) -> np.ndarray:
    """
    Align a set of coordinates entirely on the GPU via Taichi.
    """
    global _KERNELS_CACHE
    ti = _get_taichi()

    if _KERNELS_CACHE is None:
        _KERNELS_CACHE = TaichiLeastRmsdKernels(ti)

    ref_is_single = 1 if ref_coords.shape[0] == 1 else 0

    # Allocate fields
    t_move = ti.field(dtype=ti.f64, shape=coords_to_move.shape)
    t_fit = ti.field(dtype=ti.f64, shape=fit_coords.shape)
    t_ref = ti.field(dtype=ti.f64, shape=ref_coords.shape)

    # Transfer host data to JIT fields
    t_move.from_numpy(coords_to_move.astype(np.float64))
    t_fit.from_numpy(fit_coords.astype(np.float64))
    t_ref.from_numpy(ref_coords.astype(np.float64))

    # Run kernel
    _KERNELS_CACHE.least_rmsd_fit_kernel(t_move, t_fit, t_ref, ref_is_single)
    ti.sync()

    # Transfer data back to host array
    out_coords = t_move.to_numpy().astype(coords_to_move.dtype)
    return out_coords
