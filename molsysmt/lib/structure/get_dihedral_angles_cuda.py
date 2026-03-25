"""
CUDA kernel for dihedral angle calculation.

Requires: numba with CUDA support (``numba[cuda]``) and a CUDA-capable GPU.

Kernels
-------
get_dihedral_angles(coordinates, quartets) -> angles
    Per-frame, per-quartet dihedral angles.
    Equivalent to the CPU ``@lazy_njit`` version in ``get_dihedral_angles.py``.

Accepts/returns plain numpy float64 arrays (unit conversion handled by the
public wrapper layer).
"""

from __future__ import annotations

import math
import numpy as np


try:
    from numba import cuda

    # -----------------------------------------------------------------------
    # Device helpers
    # -----------------------------------------------------------------------

    @cuda.jit(device=True)
    def _cross_x(ax, ay, az, bx, by, bz):
        return ay * bz - az * by

    @cuda.jit(device=True)
    def _cross_y(ax, ay, az, bx, by, bz):
        return az * bx - ax * bz

    @cuda.jit(device=True)
    def _cross_z(ax, ay, az, bx, by, bz):
        return ax * by - ay * bx

    @cuda.jit(device=True)
    def _norm3(x, y, z):
        return math.sqrt(x * x + y * y + z * z)

    @cuda.jit(device=True)
    def _dot3(ax, ay, az, bx, by, bz):
        return ax * bx + ay * by + az * bz

    @cuda.jit(device=True)
    def _dihedral(v0x, v0y, v0z, v1x, v1y, v1z, v2x, v2y, v2z):
        """
        Dihedral angle from three bond vectors v0, v1, v2.
        Equivalent to the CPU dihedral_angle(vect0, vect1, vect2).
        """
        # aux0 = v0 × v1,  aux1 = v1 × v2
        a0x = _cross_x(v0x, v0y, v0z, v1x, v1y, v1z)
        a0y = _cross_y(v0x, v0y, v0z, v1x, v1y, v1z)
        a0z = _cross_z(v0x, v0y, v0z, v1x, v1y, v1z)

        a1x = _cross_x(v1x, v1y, v1z, v2x, v2y, v2z)
        a1y = _cross_y(v1x, v1y, v1z, v2x, v2y, v2z)
        a1z = _cross_z(v1x, v1y, v1z, v2x, v2y, v2z)

        norm_a0 = _norm3(a0x, a0y, a0z)
        norm_a1 = _norm3(a1x, a1y, a1z)

        cosa = _dot3(a0x, a0y, a0z, a1x, a1y, a1z) / (norm_a0 * norm_a1)
        if cosa > 1.0:
            cosa = 1.0
        if cosa < -1.0:
            cosa = -1.0

        ang = math.acos(cosa)

        # Sign correction: aux2 = aux0 × aux1; sign = dot(aux2, v1)
        a2x = _cross_x(a0x, a0y, a0z, a1x, a1y, a1z)
        a2y = _cross_y(a0x, a0y, a0z, a1x, a1y, a1z)
        a2z = _cross_z(a0x, a0y, a0z, a1x, a1y, a1z)

        if _dot3(a2x, a2y, a2z, v1x, v1y, v1z) <= 0.0:
            ang = -ang

        return ang

    # -----------------------------------------------------------------------
    # Main kernel
    # -----------------------------------------------------------------------

    @cuda.jit
    def _get_dihedral_angles_kernel(coords, quartets, out):
        """
        Thread assignment: (frame, quartet_index).

        coords   : (n_structures, n_atoms_subset, 3)  float64
        quartets : (n_quartets, 4)                    int64
        out      : (n_structures, n_quartets)         float64
        """
        ii, jj = cuda.grid(2)
        n_structures = coords.shape[0]
        n_quartets   = quartets.shape[0]

        if ii >= n_structures or jj >= n_quartets:
            return

        at0 = quartets[jj, 0]
        at1 = quartets[jj, 1]
        at2 = quartets[jj, 2]
        at3 = quartets[jj, 3]

        # Bond vectors
        v0x = coords[ii, at1, 0] - coords[ii, at0, 0]
        v0y = coords[ii, at1, 1] - coords[ii, at0, 1]
        v0z = coords[ii, at1, 2] - coords[ii, at0, 2]

        v1x = coords[ii, at2, 0] - coords[ii, at1, 0]
        v1y = coords[ii, at2, 1] - coords[ii, at1, 1]
        v1z = coords[ii, at2, 2] - coords[ii, at1, 2]

        v2x = coords[ii, at3, 0] - coords[ii, at2, 0]
        v2y = coords[ii, at3, 1] - coords[ii, at2, 1]
        v2z = coords[ii, at3, 2] - coords[ii, at2, 2]

        out[ii, jj] = _dihedral(v0x, v0y, v0z, v1x, v1y, v1z, v2x, v2y, v2z)

    _CUDA_AVAILABLE = True

except Exception:
    _CUDA_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public Python-level entry point  (same signature as CPU counterpart)
# ---------------------------------------------------------------------------

def get_dihedral_angles(coordinates: np.ndarray, quartets: np.ndarray) -> np.ndarray:
    """
    Per-frame, per-quartet dihedral angles on GPU.

    Parameters
    ----------
    coordinates : np.ndarray, shape (n_structures, n_atoms_subset, 3), float64
    quartets    : np.ndarray, shape (n_quartets, 4), int64
        Local atom indices into the coordinates array.

    Returns
    -------
    np.ndarray, shape (n_structures, n_quartets), float64
        Angles in radians.
    """
    n_structures = coordinates.shape[0]
    n_quartets   = quartets.shape[0]
    out = np.empty((n_structures, n_quartets), dtype=np.float64)

    threads_per_block = (16, 16)
    blocks = (
        math.ceil(n_structures / threads_per_block[0]),
        math.ceil(n_quartets   / threads_per_block[1]),
    )

    d_coords   = cuda.to_device(coordinates)
    d_quartets = cuda.to_device(quartets)
    d_out      = cuda.to_device(out)

    _get_dihedral_angles_kernel[blocks, threads_per_block](d_coords, d_quartets, d_out)
    cuda.synchronize()

    d_out.copy_to_host(out)
    return out
