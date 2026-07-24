"""Reusable cell-list neighbour search producing CSR neighbour lists (CPU).

This is the CPU (Numba ``njit``) implementation. The CSR output layout is
GPU-portable, so a future GPU neighbour-list build could feed the same
consumers; see ``devguide/pending_proposals/sasa_methodologies_and_acceleration_post_1_0.md``.

A general spatial neighbour-search primitive meant to be shared across MolSysMT
(SASA occlusion candidates, contacts, neighbours, h-bond candidate generation,
...). It builds a linked-cell grid in ``O(N)`` and returns a **CSR**
(compressed-sparse-row) neighbour list: the neighbours of query atom ``i`` are

    indices[offsets[i] : offsets[i + 1]]

From CSR every other useful shape is trivially derived (pair array, per-atom
counts, per-atom slices), and the per-atom contiguous layout is safe to read
from a parallel ``prange`` kernel without cross-thread contention.

Two spatial regimes are supported, mirroring the rest of the structure kernels:
- **vacuum** (``box=None``): a bounding-box grid;
- **periodic** (``box`` a 3x3 matrix): orthogonal or triclinic minimum-image,
  reusing the shared MIC helpers.

The list is a *candidate* list within ``cutoff``: consumers that need a tighter,
value-dependent test (e.g. per-atom SASA occlusion with per-atom radii) pass a
safe upper-bound ``cutoff`` and apply their exact predicate over the candidates.
"""

from __future__ import annotations
import numpy as np
import numba as nb
import math


# ---------------------------------------------------------------------------
# Minimum-image-convention helpers (shared periodic-wrap primitives)
# ---------------------------------------------------------------------------

@nb.njit(inline='always')
def _is_orthogonal(box_s):
    tol = 1e-10
    return (
        abs(box_s[0, 1]) < tol and abs(box_s[0, 2]) < tol and
        abs(box_s[1, 0]) < tol and abs(box_s[1, 2]) < tol and
        abs(box_s[2, 0]) < tol and abs(box_s[2, 1]) < tol
    )


@nb.njit(inline='always')
def _mic_wrap_vector_orthogonal(dx, dy, dz, lx, ly, lz):
    rx = dx - lx * math.floor(dx / lx + 0.5)
    ry = dy - ly * math.floor(dy / ly + 0.5)
    rz = dz - lz * math.floor(dz / lz + 0.5)
    return rx, ry, rz


@nb.njit(inline='always')
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


@nb.njit(inline='always')
def _mic_wrap_vector(dx, dy, dz, box_s):
    if _is_orthogonal(box_s):
        return _mic_wrap_vector_orthogonal(
            dx, dy, dz,
            box_s[0, 0], box_s[1, 1], box_s[2, 2]
        )
    else:
        return _mic_wrap_vector_triclinic(dx, dy, dz, box_s)


@nb.njit(cache=True)
def _neighbor_csr_vacuum(query, ref, cutoff, exclude_self, half):
    n_q = query.shape[0]
    n_r = ref.shape[0]

    xmin = min(query[:, 0].min(), ref[:, 0].min())
    xmax = max(query[:, 0].max(), ref[:, 0].max())
    ymin = min(query[:, 1].min(), ref[:, 1].min())
    ymax = max(query[:, 1].max(), ref[:, 1].max())
    zmin = min(query[:, 2].min(), ref[:, 2].min())
    zmax = max(query[:, 2].max(), ref[:, 2].max())

    lx = max(cutoff, xmax - xmin + 1e-5)
    ly = max(cutoff, ymax - ymin + 1e-5)
    lz = max(cutoff, zmax - zmin + 1e-5)

    nx = max(1, int(math.floor(lx / cutoff)))
    ny = max(1, int(math.floor(ly / cutoff)))
    nz = max(1, int(math.floor(lz / cutoff)))

    dx = lx / nx
    dy = ly / ny
    dz = lz / nz

    n_cells = nx * ny * nz
    head = np.full((n_cells), -1, dtype=np.int32)
    next_ref = np.full((n_r), -1, dtype=np.int32)

    for j in range(n_r):
        cx = min(nx - 1, max(0, int(math.floor((ref[j, 0] - xmin) / dx))))
        cy = min(ny - 1, max(0, int(math.floor((ref[j, 1] - ymin) / dy))))
        cz = min(nz - 1, max(0, int(math.floor((ref[j, 2] - zmin) / dz))))
        c = cx + nx * (cy + ny * cz)
        next_ref[j] = head[c]
        head[c] = j

    cutoff_sq = cutoff * cutoff
    counts = np.zeros(n_q, dtype=np.int64)

    # Pass 1: count neighbours per query atom.
    for i in range(n_q):
        qx = query[i, 0]
        qy = query[i, 1]
        qz = query[i, 2]
        cx = min(nx - 1, max(0, int(math.floor((qx - xmin) / dx))))
        cy = min(ny - 1, max(0, int(math.floor((qy - ymin) / dy))))
        cz = min(nz - 1, max(0, int(math.floor((qz - zmin) / dz))))

        cnt = 0
        for ox in range(max(0, cx - 1), min(nx, cx + 2)):
            for oy in range(max(0, cy - 1), min(ny, cy + 2)):
                for oz in range(max(0, cz - 1), min(nz, cz + 2)):
                    c = ox + nx * (oy + ny * oz)
                    j = head[c]
                    while j != -1:
                        if (not (exclude_self and j == i)) and (not (half and j <= i)):
                            rx = ref[j, 0] - qx
                            ry = ref[j, 1] - qy
                            rz = ref[j, 2] - qz
                            if rx * rx + ry * ry + rz * rz <= cutoff_sq:
                                cnt += 1
                        j = next_ref[j]
        counts[i] = cnt

    offsets = np.zeros(n_q + 1, dtype=np.int64)
    for i in range(n_q):
        offsets[i + 1] = offsets[i] + counts[i]

    indices = np.empty(offsets[n_q], dtype=np.int64)
    sqdist = np.empty(offsets[n_q], dtype=np.float64)
    pos = offsets[:-1].copy()

    # Pass 2: fill neighbour indices and squared distances (same enumeration).
    for i in range(n_q):
        qx = query[i, 0]
        qy = query[i, 1]
        qz = query[i, 2]
        cx = min(nx - 1, max(0, int(math.floor((qx - xmin) / dx))))
        cy = min(ny - 1, max(0, int(math.floor((qy - ymin) / dy))))
        cz = min(nz - 1, max(0, int(math.floor((qz - zmin) / dz))))

        for ox in range(max(0, cx - 1), min(nx, cx + 2)):
            for oy in range(max(0, cy - 1), min(ny, cy + 2)):
                for oz in range(max(0, cz - 1), min(nz, cz + 2)):
                    c = ox + nx * (oy + ny * oz)
                    j = head[c]
                    while j != -1:
                        if (not (exclude_self and j == i)) and (not (half and j <= i)):
                            rx = ref[j, 0] - qx
                            ry = ref[j, 1] - qy
                            rz = ref[j, 2] - qz
                            d2 = rx * rx + ry * ry + rz * rz
                            if d2 <= cutoff_sq:
                                indices[pos[i]] = j
                                sqdist[pos[i]] = d2
                                pos[i] += 1
                        j = next_ref[j]

    return offsets, indices, sqdist


@nb.njit(cache=True)
def _neighbor_csr_pbc(query, ref, box_s, cutoff, exclude_self, half):
    n_q = query.shape[0]
    n_r = ref.shape[0]

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

    lx = box_s[0, 0]
    ly = box_s[1, 1]
    lz = box_s[2, 2]

    nx = max(1, int(math.floor(lx / cutoff)))
    ny = max(1, int(math.floor(ly / cutoff)))
    nz = max(1, int(math.floor(lz / cutoff)))

    n_cells = nx * ny * nz
    head = np.full((n_cells), -1, dtype=np.int32)
    next_ref = np.full((n_r), -1, dtype=np.int32)

    for j in range(n_r):
        rx = ref[j, 0]; ry = ref[j, 1]; rz = ref[j, 2]
        sx = inv00 * rx + inv01 * ry + inv02 * rz
        sy = inv10 * rx + inv11 * ry + inv12 * rz
        sz = inv20 * rx + inv21 * ry + inv22 * rz
        sx -= math.floor(sx)
        sy -= math.floor(sy)
        sz -= math.floor(sz)
        cx = int(math.floor(sx * nx)) % nx
        cy = int(math.floor(sy * ny)) % ny
        cz = int(math.floor(sz * nz)) % nz
        c = cx + nx * (cy + ny * cz)
        next_ref[j] = head[c]
        head[c] = j

    cutoff_sq = cutoff * cutoff
    counts = np.zeros(n_q, dtype=np.int64)

    for i in range(n_q):
        qx = query[i, 0]; qy = query[i, 1]; qz = query[i, 2]
        sx = inv00 * qx + inv01 * qy + inv02 * qz
        sy = inv10 * qx + inv11 * qy + inv12 * qz
        sz = inv20 * qx + inv21 * qy + inv22 * qz
        sx -= math.floor(sx)
        sy -= math.floor(sy)
        sz -= math.floor(sz)
        cx = int(math.floor(sx * nx)) % nx
        cy = int(math.floor(sy * ny)) % ny
        cz = int(math.floor(sz * nz)) % nz

        cnt = 0
        for ox in range(cx - 1, cx + 2):
            w_cx = (ox + nx) % nx
            for oy in range(cy - 1, cy + 2):
                w_cy = (oy + ny) % ny
                for oz in range(cz - 1, cz + 2):
                    w_cz = (oz + nz) % nz
                    c = w_cx + nx * (w_cy + ny * w_cz)
                    j = head[c]
                    while j != -1:
                        if (not (exclude_self and j == i)) and (not (half and j <= i)):
                            dx = ref[j, 0] - qx
                            dy = ref[j, 1] - qy
                            dz = ref[j, 2] - qz
                            dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box_s)
                            if dx * dx + dy * dy + dz * dz <= cutoff_sq:
                                cnt += 1
                        j = next_ref[j]
        counts[i] = cnt

    offsets = np.zeros(n_q + 1, dtype=np.int64)
    for i in range(n_q):
        offsets[i + 1] = offsets[i] + counts[i]

    indices = np.empty(offsets[n_q], dtype=np.int64)
    sqdist = np.empty(offsets[n_q], dtype=np.float64)
    pos = offsets[:-1].copy()

    for i in range(n_q):
        qx = query[i, 0]; qy = query[i, 1]; qz = query[i, 2]
        sx = inv00 * qx + inv01 * qy + inv02 * qz
        sy = inv10 * qx + inv11 * qy + inv12 * qz
        sz = inv20 * qx + inv21 * qy + inv22 * qz
        sx -= math.floor(sx)
        sy -= math.floor(sy)
        sz -= math.floor(sz)
        cx = int(math.floor(sx * nx)) % nx
        cy = int(math.floor(sy * ny)) % ny
        cz = int(math.floor(sz * nz)) % nz

        for ox in range(cx - 1, cx + 2):
            w_cx = (ox + nx) % nx
            for oy in range(cy - 1, cy + 2):
                w_cy = (oy + ny) % ny
                for oz in range(cz - 1, cz + 2):
                    w_cz = (oz + nz) % nz
                    c = w_cx + nx * (w_cy + ny * w_cz)
                    j = head[c]
                    while j != -1:
                        if (not (exclude_self and j == i)) and (not (half and j <= i)):
                            dx = ref[j, 0] - qx
                            dy = ref[j, 1] - qy
                            dz = ref[j, 2] - qz
                            dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box_s)
                            d2 = dx * dx + dy * dy + dz * dz
                            if d2 <= cutoff_sq:
                                indices[pos[i]] = j
                                sqdist[pos[i]] = d2
                                pos[i] += 1
                        j = next_ref[j]

    return offsets, indices, sqdist


@nb.njit(cache=True)
def _csr_to_pairs(offsets, indices):
    n = offsets.shape[0] - 1
    pairs = np.empty((indices.shape[0], 2), dtype=np.int64)
    k = 0
    for i in range(n):
        for p in range(offsets[i], offsets[i + 1]):
            pairs[k, 0] = i
            pairs[k, 1] = indices[p]
            k += 1
    return pairs


def neighbor_list_csr(query_coords, ref_coords=None, box=None, cutoff=None,
                      exclude_self=True, half=False, return_distances=False):
    """CSR neighbour list of query atoms within ``cutoff`` of reference atoms.

    Parameters
    ----------
    query_coords : (n_query, 3) array
        Coordinates of the query atoms, in the same length unit as ``cutoff``.
    ref_coords : (n_ref, 3) array or None, default None
        Reference atoms searched for neighbours. ``None`` means ``ref == query``
        (self neighbour list); in that case ``exclude_self`` / ``half`` refer to
        the shared indexing.
    box : (3, 3) array or None, default None
        Periodic box matrix (rows are lattice vectors). ``None`` selects the
        vacuum (bounding-box) search.
    cutoff : float
        Neighbour cutoff distance (a safe upper bound for the consumer's exact
        predicate), same unit as the coordinates.
    exclude_self : bool, default True
        Drop the ``j == i`` self entry (only meaningful when ``ref`` is ``query``).
    half : bool, default False
        Keep only ``j > i`` (unique unordered pairs; only meaningful when ``ref``
        is ``query``). Useful to avoid double-counting in symmetric consumers.
    return_distances : bool, default False
        If ``True``, also return the neighbour distances (same length unit as the
        coordinates, minimum-image when ``box`` is given), aligned with ``indices``.

    Returns
    -------
    offsets : (n_query + 1,) int64 array
    indices : (n_neighbours,) int64 array
        Neighbours of query ``i`` are ``indices[offsets[i]:offsets[i + 1]]``.
    distances : (n_neighbours,) float64 array
        Only when ``return_distances=True``; the distance for each entry of
        ``indices``.
    """
    if cutoff is None:
        raise ValueError("neighbor_list_csr requires a cutoff.")
    query = np.ascontiguousarray(query_coords, dtype=np.float64)
    ref = query if ref_coords is None else np.ascontiguousarray(ref_coords, dtype=np.float64)
    cutoff = float(cutoff)
    if box is None:
        offsets, indices, sqdist = _neighbor_csr_vacuum(query, ref, cutoff, exclude_self, half)
    else:
        box_s = np.ascontiguousarray(box, dtype=np.float64)
        offsets, indices, sqdist = _neighbor_csr_pbc(query, ref, box_s, cutoff, exclude_self, half)
    if return_distances:
        return offsets, indices, np.sqrt(sqdist)
    return offsets, indices


def neighbor_pairs(query_coords, ref_coords=None, box=None, cutoff=None,
                   half=True, exclude_self=True):
    """Neighbour pairs ``[[i, j], ...]`` within ``cutoff``, derived from CSR.

    See :func:`neighbor_list_csr` for the parameters. ``half=True`` (the default)
    yields unique unordered pairs (``j > i``) for symmetric consumers such as
    contact maps.
    """
    offsets, indices = neighbor_list_csr(query_coords, ref_coords, box, cutoff,
                                         exclude_self=exclude_self, half=half)
    return _csr_to_pairs(offsets, indices)
