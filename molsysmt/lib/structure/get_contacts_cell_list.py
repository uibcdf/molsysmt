"""
CPU JIT periodic 3D Cell-Lists for O(N) spatial contact searches.
"""

from __future__ import annotations
import numpy as np
import numba as nb
import math


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
def get_contacts_cell_list_vacuum(coords, ref_coords, threshold):
    """Spatial cell-list search in vacuum (no PBC)."""
    n_query = coords.shape[0]
    n_ref = ref_coords.shape[0]

    # Find bounding box
    xmin = min(coords[:, 0].min(), ref_coords[:, 0].min())
    xmax = max(coords[:, 0].max(), ref_coords[:, 0].max())
    ymin = min(coords[:, 1].min(), ref_coords[:, 1].min())
    ymax = max(coords[:, 1].max(), ref_coords[:, 1].max())
    zmin = min(coords[:, 2].min(), ref_coords[:, 2].min())
    zmax = max(coords[:, 2].max(), ref_coords[:, 2].max())

    lx = max(threshold, xmax - xmin + 1e-5)
    ly = max(threshold, ymax - ymin + 1e-5)
    lz = max(threshold, zmax - zmin + 1e-5)

    nx = max(1, int(math.floor(lx / threshold)))
    ny = max(1, int(math.floor(ly / threshold)))
    nz = max(1, int(math.floor(lz / threshold)))

    dx = lx / nx
    dy = ly / ny
    dz = lz / nz

    n_cells = nx * ny * nz
    head = np.full((n_cells), -1, dtype=np.int32)
    next_ref = np.full((n_ref), -1, dtype=np.int32)

    # Populate cell list with ref_coords
    for j in range(n_ref):
        cx = min(nx - 1, max(0, int(math.floor((ref_coords[j, 0] - xmin) / dx))))
        cy = min(ny - 1, max(0, int(math.floor((ref_coords[j, 1] - ymin) / dy))))
        cz = min(nz - 1, max(0, int(math.floor((ref_coords[j, 2] - zmin) / dz))))
        c = cx + nx * (cy + ny * cz)
        next_ref[j] = head[c]
        head[c] = j

    # Query neighbors
    contacts = []
    threshold_sq = threshold * threshold

    for i in range(n_query):
        qx = coords[i, 0]
        qy = coords[i, 1]
        qz = coords[i, 2]

        cx = min(nx - 1, max(0, int(math.floor((qx - xmin) / dx))))
        cy = min(ny - 1, max(0, int(math.floor((qy - ymin) / dy))))
        cz = min(nz - 1, max(0, int(math.floor((qz - zmin) / dz))))

        for ox in range(max(0, cx - 1), min(nx, cx + 2)):
            for oy in range(max(0, cy - 1), min(ny, cy + 2)):
                for oz in range(max(0, cz - 1), min(nz, cz + 2)):
                    c = ox + nx * (oy + ny * oz)
                    j = head[c]
                    while j != -1:
                        rx = ref_coords[j, 0] - qx
                        ry = ref_coords[j, 1] - qy
                        rz = ref_coords[j, 2] - qz
                        d_sq = rx * rx + ry * ry + rz * rz
                        if d_sq <= threshold_sq:
                            contacts.append((i, j))
                        j = next_ref[j]

    return contacts


@nb.njit(cache=True)
def get_contacts_cell_list_pbc(coords, ref_coords, box_s, threshold):
    """Spatial cell-list search with orthogonal or triclinic periodic boundaries."""
    n_query = coords.shape[0]
    n_ref = ref_coords.shape[0]

    # Matrix inverse via Cramer's rule to compute fractional coordinates
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

    nx = max(1, int(math.floor(lx / threshold)))
    ny = max(1, int(math.floor(ly / threshold)))
    nz = max(1, int(math.floor(lz / threshold)))

    n_cells = nx * ny * nz
    head = np.full((n_cells), -1, dtype=np.int32)
    next_ref = np.full((n_ref), -1, dtype=np.int32)

    # Populate cell list with ref_coords fractional mappings
    for j in range(n_ref):
        rx = ref_coords[j, 0]
        ry = ref_coords[j, 1]
        rz = ref_coords[j, 2]
        
        # Fractional coordinates
        sx = inv00 * rx + inv01 * ry + inv02 * rz
        sy = inv10 * rx + inv11 * ry + inv12 * rz
        sz = inv20 * rx + inv21 * ry + inv22 * rz

        # Wrapping to [0, 1)
        sx -= math.floor(sx)
        sy -= math.floor(sy)
        sz -= math.floor(sz)

        cx = int(math.floor(sx * nx)) % nx
        cy = int(math.floor(sy * ny)) % ny
        cz = int(math.floor(sz * nz)) % nz
        c = cx + nx * (cy + ny * cz)

        next_ref[j] = head[c]
        head[c] = j

    # Query neighbors
    contacts = []
    threshold_sq = threshold * threshold

    for i in range(n_query):
        qx = coords[i, 0]
        qy = coords[i, 1]
        qz = coords[i, 2]

        sx = inv00 * qx + inv01 * qy + inv02 * qz
        sy = inv10 * qx + inv11 * qy + inv12 * qz
        sz = inv20 * qx + inv21 * qy + inv22 * qz

        sx -= math.floor(sx)
        sy -= math.floor(sy)
        sz -= math.floor(sz)

        cx = int(math.floor(sx * nx)) % nx
        cy = int(math.floor(sy * ny)) % ny
        cz = int(math.floor(sz * nz)) % nz

        # Loop 27 cells wrapping periodic cells
        for ox in range(cx - 1, cx + 2):
            w_cx = (ox + nx) % nx
            for oy in range(cy - 1, cy + 2):
                w_cy = (oy + ny) % ny
                for oz in range(cz - 1, cz + 2):
                    w_cz = (oz + nz) % nz

                    c = w_cx + nx * (w_cy + ny * w_cz)
                    j = head[c]
                    while j != -1:
                        dx = ref_coords[j, 0] - qx
                        dy = ref_coords[j, 1] - qy
                        dz = ref_coords[j, 2] - qz

                        dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box_s)
                        d_sq = dx * dx + dy * dy + dz * dz
                        if d_sq <= threshold_sq:
                            contacts.append((i, j))
                        j = next_ref[j]

    return contacts
