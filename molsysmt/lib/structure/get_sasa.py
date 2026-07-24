"""
Parallel CPU JIT compiled Shrake-Rupley SASA calculations.

Accelerated using Numba JIT and multi-threaded ``nb.prange`` loops.
"""

from __future__ import annotations

import math
import numpy as np
import numba as nb
from molsysmt._private.jit import lazy_njit
from .get_sasa_cuda import get_fibonacci_sphere_points


# ---------------------------------------------------------------------------
# JIT CPU helpers
# ---------------------------------------------------------------------------

@nb.njit(cache=True)
def _is_orthogonal(box_s):
    tol = 1e-10
    return (
        abs(box_s[0, 1]) < tol and abs(box_s[0, 2]) < tol and
        abs(box_s[1, 0]) < tol and abs(box_s[1, 2]) < tol and
        abs(box_s[2, 0]) < tol and abs(box_s[2, 2]) < tol
    )

@nb.njit(cache=True)
def _mic_wrap_vector_orthogonal(dx, dy, dz, lx, ly, lz):
    rx = dx - lx * math.floor(dx / lx + 0.5)
    ry = dy - ly * math.floor(dy / ly + 0.5)
    rz = dz - lz * math.floor(dz / lz + 0.5)
    return rx, ry, rz

@nb.njit(cache=True)
def _mic_wrap_vector_triclinic(dx, dy, dz, box_s):
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

@nb.njit(cache=True)
def _mic_wrap_vector(dx, dy, dz, box_s):
    if _is_orthogonal(box_s):
        return _mic_wrap_vector_orthogonal(
            dx, dy, dz,
            box_s[0, 0], box_s[1, 1], box_s[2, 2]
        )
    else:
        return _mic_wrap_vector_triclinic(dx, dy, dz, box_s)


# ---------------------------------------------------------------------------
# Parallel CPU Shrake-Rupley Implementations
# ---------------------------------------------------------------------------

@lazy_njit(
    nb.float64[:,:](nb.float64[:,:,:], nb.float64[:], nb.float64[:,:], nb.float64),
    parallel=True,
    cache=True
)
def get_sasa(
    coordinates: np.ndarray,
    radii: np.ndarray,
    sphere_points: np.ndarray,
    probe_radius: float = 0.14
) -> np.ndarray:
    """SASA JIT CPU loop parallelized over frames and atoms."""
    n_structures = coordinates.shape[0]
    n_atoms = coordinates.shape[1]
    n_points = sphere_points.shape[0]
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)

    for ii in nb.prange(n_structures):
        for jj in nb.prange(n_atoms):
            r_i_ext = radii[jj] + probe_radius
            if r_i_ext <= probe_radius:
                out[ii, jj] = 0.0
                continue

            accessible_count = 0
            for kk in range(n_points):
                px = coordinates[ii, jj, 0] + r_i_ext * sphere_points[kk, 0]
                py = coordinates[ii, jj, 1] + r_i_ext * sphere_points[kk, 1]
                pz = coordinates[ii, jj, 2] + r_i_ext * sphere_points[kk, 2]

                is_accessible = True
                for ll in range(n_atoms):
                    if ll == jj:
                        continue
                    r_l_ext = radii[ll] + probe_radius
                    if r_l_ext <= probe_radius:
                        continue

                    dx = px - coordinates[ii, ll, 0]
                    dy = py - coordinates[ii, ll, 1]
                    dz = pz - coordinates[ii, ll, 2]

                    dist_sq = dx*dx + dy*dy + dz*dz
                    if dist_sq < r_l_ext * r_l_ext:
                        is_accessible = False
                        break

                if is_accessible:
                    accessible_count += 1

            out[ii, jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    return out


@lazy_njit(
    nb.float64[:,:](nb.float64[:,:,:], nb.float64[:,:,:], nb.float64[:], nb.float64[:,:], nb.float64),
    parallel=True,
    cache=True
)
def get_mic_sasa(
    coordinates: np.ndarray,
    box: np.ndarray,
    radii: np.ndarray,
    sphere_points: np.ndarray,
    probe_radius: float = 0.14
) -> np.ndarray:
    """SASA JIT CPU loop with MIC parallelized over frames and atoms."""
    n_structures = coordinates.shape[0]
    n_atoms = coordinates.shape[1]
    n_points = sphere_points.shape[0]
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)

    for ii in nb.prange(n_structures):
        box_s = box[ii]
        for jj in nb.prange(n_atoms):
            r_i_ext = radii[jj] + probe_radius
            if r_i_ext <= probe_radius:
                out[ii, jj] = 0.0
                continue

            accessible_count = 0
            for kk in range(n_points):
                px = coordinates[ii, jj, 0] + r_i_ext * sphere_points[kk, 0]
                py = coordinates[ii, jj, 1] + r_i_ext * sphere_points[kk, 1]
                pz = coordinates[ii, jj, 2] + r_i_ext * sphere_points[kk, 2]

                is_accessible = True
                for ll in range(n_atoms):
                    if ll == jj:
                        continue
                    r_l_ext = radii[ll] + probe_radius
                    if r_l_ext <= probe_radius:
                        continue

                    dx = px - coordinates[ii, ll, 0]
                    dy = py - coordinates[ii, ll, 1]
                    dz = pz - coordinates[ii, ll, 2]
                    dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box_s)

                    dist_sq = dx*dx + dy*dy + dz*dz
                    if dist_sq < r_l_ext * r_l_ext:
                        is_accessible = False
                        break

                if is_accessible:
                    accessible_count += 1

            out[ii, jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    return out


# ---------------------------------------------------------------------------
# Cell-list accelerated Shrake-Rupley (multi-structure, flattened parallelism)
# ---------------------------------------------------------------------------
#
# Each structure gets its own linked-cell grid; the occlusion scan is restricted
# to candidate neighbours within ``cutoff = 2*max_radius + 2*probe_radius`` of each
# atom, turning the per-structure cost from O(N**2 * n_points) into ~O(N * n_points).
# The grids are built in parallel over structures, and the SASA compute runs a
# ``prange`` over the flattened (structure, atom) space, so both a single large
# structure (many atoms) and many structures parallelise well. Results are
# numerically identical to the brute-force kernels above.

@lazy_njit(
    nb.float64[:,:](nb.float64[:,:,:], nb.float64[:], nb.float64[:,:], nb.float64, nb.float64),
    parallel=True,
    cache=True
)
def get_sasa_cell_list(
    coordinates: np.ndarray,
    radii: np.ndarray,
    sphere_points: np.ndarray,
    probe_radius: float,
    cutoff: float,
) -> np.ndarray:
    """Multi-structure SASA with per-structure cell lists (vacuum)."""
    n_structures = coordinates.shape[0]
    n_atoms = coordinates.shape[1]
    n_points = sphere_points.shape[0]
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)
    cutoff_sq = cutoff * cutoff

    g_nx = np.empty(n_structures, dtype=np.int64)
    g_ny = np.empty(n_structures, dtype=np.int64)
    g_nz = np.empty(n_structures, dtype=np.int64)
    g_xmin = np.empty(n_structures, dtype=np.float64)
    g_ymin = np.empty(n_structures, dtype=np.float64)
    g_zmin = np.empty(n_structures, dtype=np.float64)
    g_cdx = np.empty(n_structures, dtype=np.float64)
    g_cdy = np.empty(n_structures, dtype=np.float64)
    g_cdz = np.empty(n_structures, dtype=np.float64)
    cell_offsets = np.zeros(n_structures + 1, dtype=np.int64)

    # Grid parameters and cell offsets (serial prefix sum).
    for ss in range(n_structures):
        coords = coordinates[ss]
        xmin = coords[0, 0]; xmax = coords[0, 0]
        ymin = coords[0, 1]; ymax = coords[0, 1]
        zmin = coords[0, 2]; zmax = coords[0, 2]
        for a in range(1, n_atoms):
            if coords[a, 0] < xmin: xmin = coords[a, 0]
            if coords[a, 0] > xmax: xmax = coords[a, 0]
            if coords[a, 1] < ymin: ymin = coords[a, 1]
            if coords[a, 1] > ymax: ymax = coords[a, 1]
            if coords[a, 2] < zmin: zmin = coords[a, 2]
            if coords[a, 2] > zmax: zmax = coords[a, 2]
        lx = max(cutoff, xmax - xmin + 1e-5)
        ly = max(cutoff, ymax - ymin + 1e-5)
        lz = max(cutoff, zmax - zmin + 1e-5)
        nx = max(1, int(math.floor(lx / cutoff)))
        ny = max(1, int(math.floor(ly / cutoff)))
        nz = max(1, int(math.floor(lz / cutoff)))
        g_nx[ss] = nx; g_ny[ss] = ny; g_nz[ss] = nz
        g_xmin[ss] = xmin; g_ymin[ss] = ymin; g_zmin[ss] = zmin
        g_cdx[ss] = lx / nx; g_cdy[ss] = ly / ny; g_cdz[ss] = lz / nz
        cell_offsets[ss + 1] = cell_offsets[ss] + nx * ny * nz

    head = np.full(cell_offsets[n_structures], -1, dtype=np.int64)
    nxt = np.empty((n_structures, n_atoms), dtype=np.int64)

    # Phase 1: build linked cell lists (parallel over structures).
    for ss in nb.prange(n_structures):
        coords = coordinates[ss]
        nx = g_nx[ss]; ny = g_ny[ss]
        xmin = g_xmin[ss]; ymin = g_ymin[ss]; zmin = g_zmin[ss]
        cdx = g_cdx[ss]; cdy = g_cdy[ss]; cdz = g_cdz[ss]
        base = cell_offsets[ss]
        for a in range(n_atoms):
            cx = min(nx - 1, max(0, int(math.floor((coords[a, 0] - xmin) / cdx))))
            cy = min(ny - 1, max(0, int(math.floor((coords[a, 1] - ymin) / cdy))))
            cz = min(g_nz[ss] - 1, max(0, int(math.floor((coords[a, 2] - zmin) / cdz))))
            c = base + cx + nx * (cy + ny * cz)
            nxt[ss, a] = head[c]
            head[c] = a

    # Phase 2: SASA over the flattened (structure, atom) space.
    for w in nb.prange(n_structures * n_atoms):
        ss = w // n_atoms
        jj = w % n_atoms
        r_i_ext = radii[jj] + probe_radius
        if r_i_ext <= probe_radius:
            out[ss, jj] = 0.0
            continue

        coords = coordinates[ss]
        nx = g_nx[ss]; ny = g_ny[ss]; nz = g_nz[ss]
        xmin = g_xmin[ss]; ymin = g_ymin[ss]; zmin = g_zmin[ss]
        cdx = g_cdx[ss]; cdy = g_cdy[ss]; cdz = g_cdz[ss]
        base = cell_offsets[ss]

        qx = coords[jj, 0]; qy = coords[jj, 1]; qz = coords[jj, 2]
        cx = min(nx - 1, max(0, int(math.floor((qx - xmin) / cdx))))
        cy = min(ny - 1, max(0, int(math.floor((qy - ymin) / cdy))))
        cz = min(nz - 1, max(0, int(math.floor((qz - zmin) / cdz))))

        cand = np.empty(n_atoms, dtype=np.int64)
        ncand = 0
        for ox in range(max(0, cx - 1), min(nx, cx + 2)):
            for oy in range(max(0, cy - 1), min(ny, cy + 2)):
                for oz in range(max(0, cz - 1), min(nz, cz + 2)):
                    c = base + ox + nx * (oy + ny * oz)
                    j = head[c]
                    while j != -1:
                        if j != jj:
                            rx = coords[j, 0] - qx
                            ry = coords[j, 1] - qy
                            rz = coords[j, 2] - qz
                            if rx * rx + ry * ry + rz * rz <= cutoff_sq:
                                cand[ncand] = j
                                ncand += 1
                        j = nxt[ss, j]

        accessible_count = 0
        for kk in range(n_points):
            px = qx + r_i_ext * sphere_points[kk, 0]
            py = qy + r_i_ext * sphere_points[kk, 1]
            pz = qz + r_i_ext * sphere_points[kk, 2]

            is_accessible = True
            for cc in range(ncand):
                ll = cand[cc]
                r_l_ext = radii[ll] + probe_radius
                if r_l_ext <= probe_radius:
                    continue
                dx = px - coords[ll, 0]
                dy = py - coords[ll, 1]
                dz = pz - coords[ll, 2]
                if dx * dx + dy * dy + dz * dz < r_l_ext * r_l_ext:
                    is_accessible = False
                    break

            if is_accessible:
                accessible_count += 1

        out[ss, jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    return out


@lazy_njit(
    nb.float64[:,:](nb.float64[:,:,:], nb.float64[:,:,:], nb.float64[:], nb.float64[:,:],
                    nb.float64, nb.float64),
    parallel=True,
    cache=True
)
def get_mic_sasa_cell_list(
    coordinates: np.ndarray,
    box: np.ndarray,
    radii: np.ndarray,
    sphere_points: np.ndarray,
    probe_radius: float,
    cutoff: float,
) -> np.ndarray:
    """Multi-structure SASA with per-structure cell lists and minimum-image PBC."""
    n_structures = coordinates.shape[0]
    n_atoms = coordinates.shape[1]
    n_points = sphere_points.shape[0]
    out = np.zeros((n_structures, n_atoms), dtype=np.float64)
    cutoff_sq = cutoff * cutoff

    g_nx = np.empty(n_structures, dtype=np.int64)
    g_ny = np.empty(n_structures, dtype=np.int64)
    g_nz = np.empty(n_structures, dtype=np.int64)
    cell_offsets = np.zeros(n_structures + 1, dtype=np.int64)

    for ss in range(n_structures):
        nx = max(1, int(math.floor(box[ss, 0, 0] / cutoff)))
        ny = max(1, int(math.floor(box[ss, 1, 1] / cutoff)))
        nz = max(1, int(math.floor(box[ss, 2, 2] / cutoff)))
        g_nx[ss] = nx; g_ny[ss] = ny; g_nz[ss] = nz
        cell_offsets[ss + 1] = cell_offsets[ss] + nx * ny * nz

    head = np.full(cell_offsets[n_structures], -1, dtype=np.int64)
    nxt = np.empty((n_structures, n_atoms), dtype=np.int64)

    # Phase 1: build linked cell lists (parallel over structures).
    for ss in nb.prange(n_structures):
        coords = coordinates[ss]
        box_s = box[ss]
        nx = g_nx[ss]; ny = g_ny[ss]; nz = g_nz[ss]
        base = cell_offsets[ss]

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

        for a in range(n_atoms):
            rx = coords[a, 0]; ry = coords[a, 1]; rz = coords[a, 2]
            sx = inv00 * rx + inv01 * ry + inv02 * rz
            sy = inv10 * rx + inv11 * ry + inv12 * rz
            sz = inv20 * rx + inv21 * ry + inv22 * rz
            sx -= math.floor(sx); sy -= math.floor(sy); sz -= math.floor(sz)
            cx = int(math.floor(sx * nx)) % nx
            cy = int(math.floor(sy * ny)) % ny
            cz = int(math.floor(sz * nz)) % nz
            c = base + cx + nx * (cy + ny * cz)
            nxt[ss, a] = head[c]
            head[c] = a

    # Phase 2: SASA over the flattened (structure, atom) space.
    for w in nb.prange(n_structures * n_atoms):
        ss = w // n_atoms
        jj = w % n_atoms
        r_i_ext = radii[jj] + probe_radius
        if r_i_ext <= probe_radius:
            out[ss, jj] = 0.0
            continue

        coords = coordinates[ss]
        box_s = box[ss]
        nx = g_nx[ss]; ny = g_ny[ss]; nz = g_nz[ss]
        base = cell_offsets[ss]

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

        qx = coords[jj, 0]; qy = coords[jj, 1]; qz = coords[jj, 2]
        sx = inv00 * qx + inv01 * qy + inv02 * qz
        sy = inv10 * qx + inv11 * qy + inv12 * qz
        sz = inv20 * qx + inv21 * qy + inv22 * qz
        sx -= math.floor(sx); sy -= math.floor(sy); sz -= math.floor(sz)
        cx = int(math.floor(sx * nx)) % nx
        cy = int(math.floor(sy * ny)) % ny
        cz = int(math.floor(sz * nz)) % nz

        cand = np.empty(n_atoms, dtype=np.int64)
        ncand = 0
        for ox in range(cx - 1, cx + 2):
            w_cx = (ox + nx) % nx
            for oy in range(cy - 1, cy + 2):
                w_cy = (oy + ny) % ny
                for oz in range(cz - 1, cz + 2):
                    w_cz = (oz + nz) % nz
                    c = base + w_cx + nx * (w_cy + ny * w_cz)
                    j = head[c]
                    while j != -1:
                        if j != jj:
                            dx = coords[j, 0] - qx
                            dy = coords[j, 1] - qy
                            dz = coords[j, 2] - qz
                            dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box_s)
                            if dx * dx + dy * dy + dz * dz <= cutoff_sq:
                                cand[ncand] = j
                                ncand += 1
                        j = nxt[ss, j]

        accessible_count = 0
        for kk in range(n_points):
            px = qx + r_i_ext * sphere_points[kk, 0]
            py = qy + r_i_ext * sphere_points[kk, 1]
            pz = qz + r_i_ext * sphere_points[kk, 2]

            is_accessible = True
            for cc in range(ncand):
                ll = cand[cc]
                r_l_ext = radii[ll] + probe_radius
                if r_l_ext <= probe_radius:
                    continue
                dx = px - coords[ll, 0]
                dy = py - coords[ll, 1]
                dz = pz - coords[ll, 2]
                dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box_s)
                if dx * dx + dy * dy + dz * dz < r_l_ext * r_l_ext:
                    is_accessible = False
                    break

            if is_accessible:
                accessible_count += 1

        out[ss, jj] = 4.0 * math.pi * r_i_ext * r_i_ext * (accessible_count / n_points)

    return out
