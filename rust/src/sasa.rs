//! Rusterized cell-list Shrake–Rupley SASA (multi-structure).
//!
//! Faithful port of `molsysmt.lib.structure.get_sasa.{get_sasa_cell_list,
//! get_mic_sasa_cell_list}`: per-structure linked-cell grid, candidate gather within
//! `cutoff = 2*max_radius + 2*probe`, then the sphere-point occlusion test.
//!
//! DELIBERATE CORRECTION of an upstream typo: `get_sasa.py::_is_orthogonal` tests
//! `box_s[2,2]` where it means `box_s[2,1]`. `box_s[2,2]` is a box length, so the check
//! can never be true and the MIC path always takes the (more expensive) triclinic
//! branch, even for cubic boxes. This port uses the intended check.
//!
//! Consequence, measured and documented: for an orthogonal box the two branches are
//! mathematically identical but not bit-identical (the orthogonal one divides, the
//! triclinic one multiplies by a Cramer reciprocal) — 11094/20000 probe samples differ,
//! max |diff| ~ 1.78e-15. So on orthogonal boxes this kernel is compared to the Numba
//! oracle at scientific tolerance rather than bit-for-bit. Reported upstream in
//! `devguide/pending_bugs/sasa_is_orthogonal_typo.md`.
//!
//! The cell-list SASA is correct on triclinic boxes (it equals the brute-force SASA
//! exactly): reduced-cell minimum image, perpendicular-thickness grid, and lattice
//! fractional binning `inv^T . p` — same fixes as the neighbour list.

use numpy::ndarray::{Array2, ArrayView1, ArrayView2, ArrayView3};
use numpy::{IntoPyArray, PyArray2, PyReadonlyArray1, PyReadonlyArray2, PyReadonlyArray3};
use pyo3::prelude::*;

use crate::mathlib::fast_floor;
use crate::mathlib::inverse_matrix_3x3_full as inv3;
use rayon::prelude::*;

type Mat3 = [[f64; 3]; 3];

/// The check `get_sasa.py::_is_orthogonal` *intends* (upstream tests `b[2][2]`, a box
/// length, which can never be below the tolerance — see the module docs).
#[cfg(test)]
fn is_orthogonal(b: &Mat3) -> bool {
    let tol = 1e-10;
    b[0][1].abs() < tol
        && b[0][2].abs() < tol
        && b[1][0].abs() < tol
        && b[1][2].abs() < tol
        && b[2][0].abs() < tol
        && b[2][1].abs() < tol
}

fn mic_wrap(dx: f64, dy: f64, dz: f64, cell: &Mat3, inv: &Mat3, ortho: bool) -> (f64, f64, f64) {
    let w = crate::mic::mic_vector([dx, dy, dz], cell, inv, ortho);
    (w[0], w[1], w[2])
}

/// [`mic_wrap`] with the box shape as a const parameter, for the occlusion loops.
#[inline(always)]
fn mic_wrap_const<const ORTHO: bool>(
    dx: f64,
    dy: f64,
    dz: f64,
    cell: &Mat3,
    inv: &Mat3,
) -> (f64, f64, f64) {
    let w = crate::mic::mic_vector_const::<ORTHO>([dx, dy, dz], cell, inv);
    (w[0], w[1], w[2])
}

struct Grid {
    nx: i64,
    ny: i64,
    nz: i64,
    xmin: f64,
    ymin: f64,
    zmin: f64,
    cdx: f64,
    cdy: f64,
    cdz: f64,
    head: Vec<i64>,
    nxt: Vec<i64>,
}

impl Grid {
    fn cell(&self, x: f64, y: f64, z: f64) -> (i64, i64, i64) {
        (
            (((x - self.xmin) / self.cdx) as i64).clamp(0, self.nx - 1),
            (((y - self.ymin) / self.cdy) as i64).clamp(0, self.ny - 1),
            (((z - self.zmin) / self.cdz) as i64).clamp(0, self.nz - 1),
        )
    }
}

/// Bounding-box grid over one structure's atoms (vacuum regime; the periodic regime
/// uses the fractional GridP below, mirroring the Numba kernels).
fn build_grid(coords: &ArrayView3<f64>, s: usize, n_atoms: usize, cutoff: f64) -> Grid {
    let (mut xmn, mut ymn, mut zmn) = (coords[[s, 0, 0]], coords[[s, 0, 1]], coords[[s, 0, 2]]);
    let (mut xmx, mut ymx, mut zmx) = (xmn, ymn, zmn);
    for a in 1..n_atoms {
        let (x, y, z) = (coords[[s, a, 0]], coords[[s, a, 1]], coords[[s, a, 2]]);
        xmn = xmn.min(x);
        xmx = xmx.max(x);
        ymn = ymn.min(y);
        ymx = ymx.max(y);
        zmn = zmn.min(z);
        zmx = zmx.max(z);
    }
    let lx = cutoff.max(xmx - xmn + 1e-5);
    let ly = cutoff.max(ymx - ymn + 1e-5);
    let lz = cutoff.max(zmx - zmn + 1e-5);
    let nx = ((lx / cutoff) as i64).max(1);
    let ny = ((ly / cutoff) as i64).max(1);
    let nz = ((lz / cutoff) as i64).max(1);
    let mut g = Grid {
        nx,
        ny,
        nz,
        xmin: xmn,
        ymin: ymn,
        zmin: zmn,
        cdx: lx / nx as f64,
        cdy: ly / ny as f64,
        cdz: lz / nz as f64,
        head: vec![-1i64; (nx * ny * nz) as usize],
        nxt: vec![-1i64; n_atoms],
    };
    for a in 0..n_atoms {
        let (cx, cy, cz) = g.cell(coords[[s, a, 0]], coords[[s, a, 1]], coords[[s, a, 2]]);
        let c = (cx + g.nx * (cy + g.ny * cz)) as usize;
        g.nxt[a] = g.head[c];
        g.head[c] = a as i64;
    }
    g
}

/// Grid cell counts sized by the perpendicular distance between opposite cell faces
/// (`V/|b_j x b_k|`), so a +-1 fractional stencil covers the cutoff on triclinic boxes.
fn grid_dims(b: &Mat3, cutoff: f64) -> (i64, i64, i64) {
    let cross = |u: &[f64; 3], v: &[f64; 3]| {
        [
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0],
        ]
    };
    let norm = |v: [f64; 3]| (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]).sqrt();
    let vol = (b[0][0] * (b[1][1] * b[2][2] - b[1][2] * b[2][1])
        - b[0][1] * (b[1][0] * b[2][2] - b[1][2] * b[2][0])
        + b[0][2] * (b[1][0] * b[2][1] - b[1][1] * b[2][0]))
        .abs();
    let perp = |bc: [f64; 3]| {
        if norm(bc) > 0.0 {
            vol / norm(bc)
        } else {
            cutoff
        }
    };
    (
        ((perp(cross(&b[1], &b[2])) / cutoff) as i64).max(1),
        ((perp(cross(&b[0], &b[2])) / cutoff) as i64).max(1),
        ((perp(cross(&b[0], &b[1])) / cutoff) as i64).max(1),
    )
}

/// Periodic (fractional) grid, mirroring get_mic_sasa_cell_list: cells come from the
/// box lengths and the 27-cell stencil wraps around.
struct GridP {
    nx: i64,
    ny: i64,
    nz: i64,
    inv: Mat3, // original-box inverse, for cell binning only
    wcell: Mat3,
    winv: Mat3,
    ortho: bool, // reduced wrap cell, for the MIC distance
    head: Vec<i64>,
    nxt: Vec<i64>,
}

impl GridP {
    fn cell(&self, x: f64, y: f64, z: f64) -> (i64, i64, i64) {
        let mut sx = self.inv[0][0] * x + self.inv[1][0] * y + self.inv[2][0] * z;
        let mut sy = self.inv[0][1] * x + self.inv[1][1] * y + self.inv[2][1] * z;
        let mut sz = self.inv[0][2] * x + self.inv[1][2] * y + self.inv[2][2] * z;
        sx -= fast_floor(sx);
        sy -= fast_floor(sy);
        sz -= fast_floor(sz);
        (
            (sx * self.nx as f64) as i64 % self.nx,
            (sy * self.ny as f64) as i64 % self.ny,
            (sz * self.nz as f64) as i64 % self.nz,
        )
    }
}

fn build_grid_p(
    coords: &ArrayView3<f64>,
    boxes: &ArrayView3<f64>,
    s: usize,
    n_atoms: usize,
    cutoff: f64,
) -> GridP {
    let b: Mat3 = [
        [boxes[[s, 0, 0]], boxes[[s, 0, 1]], boxes[[s, 0, 2]]],
        [boxes[[s, 1, 0]], boxes[[s, 1, 1]], boxes[[s, 1, 2]]],
        [boxes[[s, 2, 0]], boxes[[s, 2, 1]], boxes[[s, 2, 2]]],
    ];
    let (nx, ny, nz) = grid_dims(&b, cutoff);
    let (ortho, wcell, winv) = crate::mic::prep_dist(&b);
    let mut g = GridP {
        nx,
        ny,
        nz,
        inv: inv3(&b),
        wcell,
        winv,
        ortho,
        head: vec![-1i64; (nx * ny * nz) as usize],
        nxt: vec![-1i64; n_atoms],
    };
    for a in 0..n_atoms {
        let (cx, cy, cz) = g.cell(coords[[s, a, 0]], coords[[s, a, 1]], coords[[s, a, 2]]);
        let c = (cx + g.nx * (cy + g.ny * cz)) as usize;
        g.nxt[a] = g.head[c];
        g.head[c] = a as i64;
    }
    g
}

/// Vacuum gather (bounding-box grid, clamped stencil).
#[allow(clippy::too_many_arguments)]
fn gather_v(
    g: &Grid,
    coords: &ArrayView3<f64>,
    s: usize,
    jj: usize,
    qx: f64,
    qy: f64,
    qz: f64,
    cutoff_sq: f64,
    cand: &mut Vec<i64>,
) {
    let (cx, cy, cz) = g.cell(qx, qy, qz);
    cand.clear();
    for ox in (cx - 1).max(0)..(cx + 2).min(g.nx) {
        for oy in (cy - 1).max(0)..(cy + 2).min(g.ny) {
            for oz in (cz - 1).max(0)..(cz + 2).min(g.nz) {
                let c = (ox + g.nx * (oy + g.ny * oz)) as usize;
                let mut j = g.head[c];
                while j != -1 {
                    let ju = j as usize;
                    if ju != jj {
                        let dx = coords[[s, ju, 0]] - qx;
                        let dy = coords[[s, ju, 1]] - qy;
                        let dz = coords[[s, ju, 2]] - qz;
                        if dx * dx + dy * dy + dz * dz <= cutoff_sq {
                            cand.push(j);
                        }
                    }
                    j = g.nxt[ju];
                }
            }
        }
    }
}

/// Periodic gather (fractional grid, wrapping stencil, MIC distance).
#[allow(clippy::too_many_arguments)]
fn gather_p(
    g: &GridP,
    coords: &ArrayView3<f64>,
    s: usize,
    jj: usize,
    qx: f64,
    qy: f64,
    qz: f64,
    cutoff_sq: f64,
    cand: &mut Vec<i64>,
) {
    let (cx, cy, cz) = g.cell(qx, qy, qz);
    cand.clear();
    // Unique periodic neighbour cells per axis (see neighbors::axis_cells): ±1 for n>=3,
    // all cells once for n<3, so a small box does not gather a candidate twice.
    let (xs, nxs) = crate::neighbors::axis_cells(cx, g.nx);
    let (ys, nys) = crate::neighbors::axis_cells(cy, g.ny);
    let (zs, nzs) = crate::neighbors::axis_cells(cz, g.nz);
    for &wcx in &xs[..nxs] {
        for &wcy in &ys[..nys] {
            for &wcz in &zs[..nzs] {
                let c = (wcx + g.nx * (wcy + g.ny * wcz)) as usize;
                let mut j = g.head[c];
                while j != -1 {
                    let ju = j as usize;
                    if ju != jj {
                        let dx = coords[[s, ju, 0]] - qx;
                        let dy = coords[[s, ju, 1]] - qy;
                        let dz = coords[[s, ju, 2]] - qz;
                        let (dx, dy, dz) = mic_wrap(dx, dy, dz, &g.wcell, &g.winv, g.ortho);
                        if dx * dx + dy * dy + dz * dz <= cutoff_sq {
                            cand.push(j);
                        }
                    }
                    j = g.nxt[ju];
                }
            }
        }
    }
}

/// Squared extended radii, precomputed once per call.
///
/// `radii[ll] + probe` and its square were being recomputed inside the innermost
/// occlusion loop, i.e. `n_atoms * n_sphere_points` times per atom instead of once.
/// Atoms with a non-positive radius get `0.0`, which the `d2 < rext2[ll]` test rejects for
/// free (`d2` is a sum of squares) — that is exactly the `if r_l_ext <= probe { continue }`
/// guard the loop used to carry, now expressed as data instead of as a branch.
fn extended_radii_sq(radii: &ArrayView1<f64>, probe: f64) -> Vec<f64> {
    radii
        .iter()
        .map(|&r| {
            let ext = r + probe;
            if ext <= probe {
                0.0
            } else {
                ext * ext
            }
        })
        .collect()
}

/// Shrake–Rupley occlusion count for one atom over its candidate neighbours.
///
/// `cf` is the structure's coordinates as a flat `[x, y, z]`-per-atom slice and `spf` the
/// sphere points likewise: `ArrayView` indexing recomputes strides and bounds-checks on
/// every access, which in a loop this deep is a measurable fraction of the body. `WRAP`
/// and `ORTHO` are const parameters so neither the periodic-vs-vacuum choice nor the box
/// shape leaves a branch inside the loop (see `mic::mic_vector_const`).
#[allow(clippy::too_many_arguments)]
fn atom_sasa<const WRAP: bool, const ORTHO: bool>(
    cf: &[f64],
    spf: &[f64],
    n_points: usize,
    rext2: &[f64],
    r_i_ext: f64,
    qx: f64,
    qy: f64,
    qz: f64,
    cand: &[i64],
    cell: &Mat3,
    inv: &Mat3,
) -> f64 {
    let mut accessible = 0usize;
    for kk in 0..n_points {
        let px = qx + r_i_ext * spf[3 * kk];
        let py = qy + r_i_ext * spf[3 * kk + 1];
        let pz = qz + r_i_ext * spf[3 * kk + 2];
        let mut ok = true;
        for &cc in cand {
            let ll = cc as usize;
            let dx = px - cf[3 * ll];
            let dy = py - cf[3 * ll + 1];
            let dz = pz - cf[3 * ll + 2];
            let (dx, dy, dz) = if WRAP {
                mic_wrap_const::<ORTHO>(dx, dy, dz, cell, inv)
            } else {
                (dx, dy, dz)
            };
            if dx * dx + dy * dy + dz * dz < rext2[ll] {
                ok = false;
                break;
            }
        }
        if ok {
            accessible += 1;
        }
    }
    4.0 * std::f64::consts::PI * r_i_ext * r_i_ext * (accessible as f64 / n_points as f64)
}

/// [`atom_sasa`] with the periodic/orthogonal choice resolved from runtime flags.
#[allow(clippy::too_many_arguments)]
#[inline]
fn atom_sasa_dispatch(
    cf: &[f64],
    spf: &[f64],
    n_points: usize,
    rext2: &[f64],
    r_i_ext: f64,
    qx: f64,
    qy: f64,
    qz: f64,
    cand: &[i64],
    boxm: Option<(&Mat3, &Mat3, bool)>,
) -> f64 {
    const ZERO: Mat3 = [[0.0; 3]; 3];
    match boxm {
        None => atom_sasa::<false, false>(
            cf, spf, n_points, rext2, r_i_ext, qx, qy, qz, cand, &ZERO, &ZERO,
        ),
        Some((cell, inv, true)) => atom_sasa::<true, true>(
            cf, spf, n_points, rext2, r_i_ext, qx, qy, qz, cand, cell, inv,
        ),
        Some((cell, inv, false)) => atom_sasa::<true, false>(
            cf, spf, n_points, rext2, r_i_ext, qx, qy, qz, cand, cell, inv,
        ),
    }
}

fn core_vacuum(
    coords: &ArrayView3<f64>,
    radii: &ArrayView1<f64>,
    sphere: &ArrayView2<f64>,
    probe: f64,
    cutoff: f64,
) -> Vec<f64> {
    let ns = coords.shape()[0];
    let na = coords.shape()[1];
    let cutoff_sq = cutoff * cutoff;
    let rext2 = extended_radii_sq(radii, probe);
    let cc = coords.as_standard_layout();
    let cflat = cc.as_slice().expect("standard layout is contiguous");
    let spc = sphere.as_standard_layout();
    let spf = spc.as_slice().expect("standard layout is contiguous");
    let n_points = sphere.shape()[0];
    let grids: Vec<Grid> = (0..ns)
        .into_par_iter()
        .map(|s| build_grid(coords, s, na, cutoff))
        .collect();
    (0..ns * na)
        .into_par_iter()
        .map_init(
            || Vec::<i64>::with_capacity(256),
            |cand, w| {
                let s = w / na;
                let jj = w % na;
                let r_i_ext = radii[jj] + probe;
                if r_i_ext <= probe {
                    return 0.0;
                }
                let cf = &cflat[s * na * 3..(s + 1) * na * 3];
                let (qx, qy, qz) = (cf[3 * jj], cf[3 * jj + 1], cf[3 * jj + 2]);
                gather_v(&grids[s], coords, s, jj, qx, qy, qz, cutoff_sq, cand);
                atom_sasa_dispatch(cf, spf, n_points, &rext2, r_i_ext, qx, qy, qz, cand, None)
            },
        )
        .collect()
}

fn core_pbc(
    coords: &ArrayView3<f64>,
    boxes: &ArrayView3<f64>,
    radii: &ArrayView1<f64>,
    sphere: &ArrayView2<f64>,
    probe: f64,
    cutoff: f64,
) -> Vec<f64> {
    let ns = coords.shape()[0];
    let na = coords.shape()[1];
    let cutoff_sq = cutoff * cutoff;
    let rext2 = extended_radii_sq(radii, probe);
    let cc = coords.as_standard_layout();
    let cflat = cc.as_slice().expect("standard layout is contiguous");
    let spc = sphere.as_standard_layout();
    let spf = spc.as_slice().expect("standard layout is contiguous");
    let n_points = sphere.shape()[0];
    let grids: Vec<GridP> = (0..ns)
        .into_par_iter()
        .map(|s| build_grid_p(coords, boxes, s, na, cutoff))
        .collect();
    (0..ns * na)
        .into_par_iter()
        .map_init(
            || Vec::<i64>::with_capacity(256),
            |cand, w| {
                let s = w / na;
                let jj = w % na;
                let r_i_ext = radii[jj] + probe;
                if r_i_ext <= probe {
                    return 0.0;
                }
                let g = &grids[s];
                let cf = &cflat[s * na * 3..(s + 1) * na * 3];
                let (qx, qy, qz) = (cf[3 * jj], cf[3 * jj + 1], cf[3 * jj + 2]);
                gather_p(g, coords, s, jj, qx, qy, qz, cutoff_sq, cand);
                atom_sasa_dispatch(
                    cf,
                    spf,
                    n_points,
                    &rext2,
                    r_i_ext,
                    qx,
                    qy,
                    qz,
                    cand,
                    Some((&g.wcell, &g.winv, g.ortho)),
                )
            },
        )
        .collect()
}

#[pyfunction]
pub fn get_sasa_cell_list<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    radii: PyReadonlyArray1<'py, f64>,
    sphere_points: PyReadonlyArray2<'py, f64>,
    probe_radius: f64,
    cutoff: f64,
    num_threads: usize,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let r = radii.as_array();
    let sp = sphere_points.as_array();
    let (ns, na) = (c.shape()[0], c.shape()[1]);
    let flat = py.detach(|| {
        crate::threads::install(num_threads, || {
            core_vacuum(&c, &r, &sp, probe_radius, cutoff)
        })
    });
    Array2::from_shape_vec((ns, na), flat)
        .unwrap()
        .into_pyarray(py)
}

#[pyfunction]
#[allow(clippy::too_many_arguments)] // Stable flat Python FFI.
pub fn get_mic_sasa_cell_list<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    boxes: PyReadonlyArray3<'py, f64>,
    radii: PyReadonlyArray1<'py, f64>,
    sphere_points: PyReadonlyArray2<'py, f64>,
    probe_radius: f64,
    cutoff: f64,
    num_threads: usize,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let b = boxes.as_array();
    let r = radii.as_array();
    let sp = sphere_points.as_array();
    let (ns, na) = (c.shape()[0], c.shape()[1]);
    let flat = py.detach(|| {
        crate::threads::install(num_threads, || {
            core_pbc(&c, &b, &r, &sp, probe_radius, cutoff)
        })
    });
    Array2::from_shape_vec((ns, na), flat)
        .unwrap()
        .into_pyarray(py)
}

// ---------------------------------------------------------- brute-force Shrake–Rupley
//
// The O(N² · n_points) kernels `get_sasa` / `get_mic_sasa`, the small-system path below
// `CELL_LIST_MIN_ATOMS`. Numerically the same occlusion test as the cell-list kernels,
// just without the grid: every sphere point is checked against every other atom.
//
// The MIC wrap here matches upstream's `_mic_wrap_vector`: a centred fractional wrap using
// the *full* 3x3 inverse (no 27-image search), and the same corrected orthogonality check
// as the cell-list path (upstream's `_is_orthogonal` has the `box_s[2,2]` typo, so on a
// cubic box the two branches agree to ~1e-15 rather than bit-for-bit — see the module
// docs and `devguide/pending_bugs/sasa_is_orthogonal_typo.md`).

#[inline]
#[allow(clippy::too_many_arguments)] // Inner-loop state is passed explicitly for inlining.
fn atom_sasa_bruteforce<const WRAP: bool, const ORTHO: bool>(
    cf: &[f64],
    spf: &[f64],
    n_points: usize,
    jj: usize,
    rext2: &[f64],
    r_i_ext: f64,
    na: usize,
    cell: &Mat3,
    inv: &Mat3,
) -> f64 {
    let (ax, ay, az) = (cf[3 * jj], cf[3 * jj + 1], cf[3 * jj + 2]);
    let mut accessible = 0usize;
    for kk in 0..n_points {
        let px = ax + r_i_ext * spf[3 * kk];
        let py = ay + r_i_ext * spf[3 * kk + 1];
        let pz = az + r_i_ext * spf[3 * kk + 2];
        let mut is_accessible = true;
        for ll in 0..na {
            if ll == jj {
                continue;
            }
            let dx = px - cf[3 * ll];
            let dy = py - cf[3 * ll + 1];
            let dz = pz - cf[3 * ll + 2];
            let (dx, dy, dz) = if WRAP {
                let w = mic_wrap_bruteforce_const::<ORTHO>(dx, dy, dz, cell, inv);
                (w[0], w[1], w[2])
            } else {
                (dx, dy, dz)
            };
            if dx * dx + dy * dy + dz * dz < rext2[ll] {
                is_accessible = false;
                break;
            }
        }
        if is_accessible {
            accessible += 1;
        }
    }
    4.0 * std::f64::consts::PI * r_i_ext * r_i_ext * (accessible as f64 / n_points as f64)
}

/// [`atom_sasa_bruteforce`] with the periodic/orthogonal choice resolved from runtime flags.
#[allow(clippy::too_many_arguments)]
#[inline]
fn atom_sasa_bruteforce_dispatch(
    cf: &[f64],
    spf: &[f64],
    n_points: usize,
    jj: usize,
    rext2: &[f64],
    r_i_ext: f64,
    na: usize,
    wrap: Option<(&Mat3, &Mat3, bool)>,
) -> f64 {
    const ZERO: Mat3 = [[0.0; 3]; 3];
    match wrap {
        None => atom_sasa_bruteforce::<false, false>(
            cf, spf, n_points, jj, rext2, r_i_ext, na, &ZERO, &ZERO,
        ),
        Some((cell, inv, true)) => {
            atom_sasa_bruteforce::<true, true>(cf, spf, n_points, jj, rext2, r_i_ext, na, cell, inv)
        }
        Some((cell, inv, false)) => atom_sasa_bruteforce::<true, false>(
            cf, spf, n_points, jj, rext2, r_i_ext, na, cell, inv,
        ),
    }
}

/// Centred minimum-image wrap via the full inverse, matching `_mic_wrap_vector`, with the
/// box shape as a const parameter so the occlusion loop carries no branch on it.
#[inline(always)]
fn mic_wrap_bruteforce_const<const ORTHO: bool>(
    dx: f64,
    dy: f64,
    dz: f64,
    b: &Mat3,
    inv: &Mat3,
) -> [f64; 3] {
    crate::mic::mic_vector_const::<ORTHO>([dx, dy, dz], b, inv)
}

#[pyfunction]
pub fn get_sasa<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    radii: PyReadonlyArray1<'py, f64>,
    sphere_points: PyReadonlyArray2<'py, f64>,
    probe_radius: f64,
    num_threads: usize,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let r = radii.as_array();
    let sp = sphere_points.as_array();
    let (ns, na) = (c.shape()[0], c.shape()[1]);
    let rext2 = extended_radii_sq(&r, probe_radius);
    let cc = c.as_standard_layout();
    let cflat = cc.as_slice().expect("standard layout is contiguous");
    let spc = sp.as_standard_layout();
    let spf = spc.as_slice().expect("standard layout is contiguous");
    let n_points = sp.shape()[0];
    let flat: Vec<f64> = py.detach(|| {
        crate::threads::install(num_threads, || {
            (0..ns * na)
                .into_par_iter()
                .map(|idx| {
                    let (s, jj) = (idx / na, idx % na);
                    let r_i_ext = r[jj] + probe_radius;
                    if r_i_ext <= probe_radius {
                        return 0.0;
                    }
                    let cf = &cflat[s * na * 3..(s + 1) * na * 3];
                    atom_sasa_bruteforce_dispatch(cf, spf, n_points, jj, &rext2, r_i_ext, na, None)
                })
                .collect()
        })
    });
    Array2::from_shape_vec((ns, na), flat)
        .unwrap()
        .into_pyarray(py)
}

#[pyfunction]
pub fn get_mic_sasa<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    boxes: PyReadonlyArray3<'py, f64>,
    radii: PyReadonlyArray1<'py, f64>,
    sphere_points: PyReadonlyArray2<'py, f64>,
    probe_radius: f64,
    num_threads: usize,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let bx = boxes.as_array();
    let r = radii.as_array();
    let sp = sphere_points.as_array();
    let (ns, na) = (c.shape()[0], c.shape()[1]);
    // one box per structure; precompute inverse and orthogonality once each
    let parts: Vec<(Mat3, Mat3, bool)> = (0..ns)
        .map(|s| {
            let b = [
                [bx[[s, 0, 0]], bx[[s, 0, 1]], bx[[s, 0, 2]]],
                [bx[[s, 1, 0]], bx[[s, 1, 1]], bx[[s, 1, 2]]],
                [bx[[s, 2, 0]], bx[[s, 2, 1]], bx[[s, 2, 2]]],
            ];
            let (ortho, cell, inv) = crate::mic::prep_dist(&b);
            (cell, inv, ortho)
        })
        .collect();
    let rext2 = extended_radii_sq(&r, probe_radius);
    let cc = c.as_standard_layout();
    let cflat = cc.as_slice().expect("standard layout is contiguous");
    let spc = sp.as_standard_layout();
    let spf = spc.as_slice().expect("standard layout is contiguous");
    let n_points = sp.shape()[0];
    let flat: Vec<f64> = py.detach(|| {
        crate::threads::install(num_threads, || {
            (0..ns * na)
                .into_par_iter()
                .map(|idx| {
                    let (s, jj) = (idx / na, idx % na);
                    let r_i_ext = r[jj] + probe_radius;
                    if r_i_ext <= probe_radius {
                        return 0.0;
                    }
                    let (b, inv, ortho) = &parts[s];
                    let cf = &cflat[s * na * 3..(s + 1) * na * 3];
                    atom_sasa_bruteforce_dispatch(
                        cf,
                        spf,
                        n_points,
                        jj,
                        &rext2,
                        r_i_ext,
                        na,
                        Some((b, inv, *ortho)),
                    )
                })
                .collect()
        })
    });
    Array2::from_shape_vec((ns, na), flat)
        .unwrap()
        .into_pyarray(py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_sasa_cell_list, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_sasa_cell_list, m)?)?;
    m.add_function(wrap_pyfunction!(get_sasa, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_sasa, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const ORTHO: Mat3 = [[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]];
    const TRIC: Mat3 = [[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]];

    /// The corrected check: a cubic box is orthogonal, a triclinic one is not.
    /// Upstream returns false for both because it tests `b[2][2]` (a box length).
    #[test]
    fn orthogonality_check_is_correct_unlike_upstream() {
        assert!(is_orthogonal(&ORTHO));
        assert!(!is_orthogonal(&TRIC));
        // What upstream computes, for the record: `b[2][2] < tol` is never true.
        let upstream_would_say = ORTHO[2][2].abs() < 1e-10;
        assert!(
            !upstream_would_say,
            "upstream can never report a real box as orthogonal"
        );
    }

    #[test]
    fn mic_wrap_returns_the_nearest_image() {
        let (x, _, _) = mic_wrap(5.0, 0.0, 0.0, &ORTHO, &[[0.0; 3]; 3], true);
        assert!((x - (-1.0)).abs() < 1e-12, "got {x}");
    }

    #[test]
    fn full_inverse_round_trips() {
        let inv = inv3(&TRIC);
        for i in 0..3 {
            let mut acc = 0.0;
            for k in 0..3 {
                acc += inv[i][k] * TRIC[k][i];
            }
            assert!((acc - 1.0).abs() < 1e-12);
        }
    }
}

#[cfg(test)]
mod branch_divergence {
    use super::*;

    /// Quantifies the cost of correcting the `_is_orthogonal` typo (see module docs).
    ///
    /// For an orthogonal box the two branches are mathematically identical, but the
    /// orthogonal one divides (`dx / L`) while the triclinic one multiplies by a
    /// reciprocal built from Cramer's rule (`dx * inv00`). This pins the size of the
    /// resulting divergence so that a future change cannot enlarge it unnoticed: the
    /// parity gate for this kernel is a tolerance, and this test is what justifies it.
    #[test]
    fn orthogonal_vs_triclinic_branch_on_a_cubic_box() {
        let b: Mat3 = [[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]];
        let inv = inv3(&b);
        let mut max_diff = 0.0f64;
        let mut differing = 0usize;
        let n = 20000;
        for i in 0..n {
            // spread over several box lengths, including near +/- L/2 boundaries
            let dx = -18.0 + 36.0 * (i as f64) / (n as f64);
            let ortho_branch = dx - b[0][0] * fast_floor(dx / b[0][0] + 0.5);
            let mut sx = inv[0][0] * dx;
            sx -= fast_floor(sx + 0.5);
            let tric_branch = b[0][0] * sx;
            let d = (ortho_branch - tric_branch).abs();
            if d > 0.0 {
                differing += 1;
            }
            max_diff = max_diff.max(d);
        }
        // Measured: 11094/20000 samples differ, max |diff| ~ 1.78e-15 — pure floating-
        // point noise, propagating to ~4.4e-16 in SASA values with no occlusion decision
        // flipping. The port takes the correct branch and the typo is reported upstream
        // (`devguide/pending_bugs/sasa_is_orthogonal_typo.md`); the price is that parity
        // against Numba is asserted at 1e-9 here rather than bit-for-bit.
        assert!(
            differing > 0 && max_diff < 1e-12,
            "expected tiny-but-nonzero divergence; got {differing}/{n}, max {max_diff:.3e}"
        );
    }
}
