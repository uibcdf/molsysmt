//! Rusterized multi-structure CSR neighbour list.
//!
//! Multi-structure CSR neighbour list (the hot kernel behind get_contacts and
//! get_neighbors), parallel over the flattened work with the GIL released.
//!
//! **Correct on triclinic boxes**, unlike the Numba original it was ported from. Three
//! things make it so: the grid is sized by the *perpendicular* distance between cell faces
//! (so the +-1 stencil covers the cutoff on a skewed box), cells are binned by the true
//! lattice fractional coordinate `inv^T . p` (not `inv . p`, which only agrees for
//! orthogonal boxes), and the distance is the reduced-cell minimum image (`mic::mic_vector`,
//! correct where the single centred wrap is not). Validated against an all-pairs +-2
//! ground truth; on orthogonal boxes it stays bit-for-bit with Numba.

use numpy::ndarray::ArrayView3;
use numpy::{IntoPyArray, PyArray1, PyReadonlyArray3};
use pyo3::prelude::*;

use crate::mathlib::fast_floor;
use crate::mathlib::inverse_matrix_3x3_full as inv3;
use rayon::prelude::*;

type Mat3 = [[f64; 3]; 3];

#[cfg(test)]
fn is_orthogonal(b: &Mat3) -> bool {
    let tol = 1e-10;
    b[0][1].abs() < tol && b[0][2].abs() < tol && b[1][0].abs() < tol
        && b[1][2].abs() < tol && b[2][0].abs() < tol && b[2][1].abs() < tol
}

/// Minimum-image displacement via the unified reduced-cell mechanism (`mic::mic_vector`),
/// so the distance is the true minimum image even on skewed boxes. `cell`/`inv` are the
/// reduced wrap cell + inverse from `prep_dist`.
fn mic_wrap(dx: f64, dy: f64, dz: f64, cell: &Mat3, inv: &Mat3, ortho: bool) -> (f64, f64, f64) {
    let w = crate::mic::mic_vector([dx, dy, dz], cell, inv, ortho);
    (w[0], w[1], w[2])
}

/// Grid cell counts sized by the **perpendicular** distance between opposite cell faces
/// (`V / |b_j × b_k|`), not the box-vector lengths. This is what makes the ±1 fractional
/// stencil sufficient on a triclinic box: with each cell at least `cutoff` thick
/// perpendicular, every atom within `cutoff` of a query lies within ±1 cell per axis.
/// Sizing by the vector lengths (the old code) makes cells too thin perpendicular on a
/// skewed box, so the ±1 stencil misses candidates.
fn grid_dims(b: &Mat3, cutoff: f64) -> (i64, i64, i64) {
    let cross = |u: &[f64; 3], v: &[f64; 3]| {
        [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
    };
    let norm = |v: [f64; 3]| (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]).sqrt();
    let vol = (b[0][0] * (b[1][1] * b[2][2] - b[1][2] * b[2][1])
        - b[0][1] * (b[1][0] * b[2][2] - b[1][2] * b[2][0])
        + b[0][2] * (b[1][0] * b[2][1] - b[1][1] * b[2][0]))
        .abs();
    let perp = |bc: [f64; 3]| if norm(bc) > 0.0 { vol / norm(bc) } else { cutoff };
    (
        ((perp(cross(&b[1], &b[2])) / cutoff) as i64).max(1),
        ((perp(cross(&b[0], &b[2])) / cutoff) as i64).max(1),
        ((perp(cross(&b[0], &b[1])) / cutoff) as i64).max(1),
    )
}

/// Unique periodic neighbour cells along one axis: the ±1 wrap for `n >= 3`, or all `n`
/// cells (each once) for `n < 3`, avoiding the double-count a ±1 wrap causes on a small box.
#[inline]
pub(crate) fn axis_cells(c: i64, n: i64) -> ([i64; 3], usize) {
    if n >= 3 {
        ([(c - 1).rem_euclid(n), c.rem_euclid(n), (c + 1).rem_euclid(n)], 3)
    } else if n == 2 {
        ([0, 1, 0], 2)
    } else {
        ([0, 0, 0], 1)
    }
}

/// Emit the exact-size output for one query atom from reusable scratch buffers.
/// `order` is scratch too, so the only allocations left are the two output vectors.
fn emit_from(cand: &[i64], csq: &[f64], sort: bool, order: &mut Vec<usize>) -> (Vec<i64>, Vec<f64>) {
    let m = cand.len();
    let mut idx = Vec::with_capacity(m);
    let mut dist = Vec::with_capacity(m);
    if sort {
        order.clear();
        order.extend(0..m);
        order.sort_by(|&a, &b| csq[a].partial_cmp(&csq[b]).unwrap());
        for &p in order.iter() {
            idx.push(cand[p]);
            dist.push(csq[p].sqrt());
        }
    } else {
        for p in 0..m {
            idx.push(cand[p]);
            dist.push(csq[p].sqrt());
        }
    }
    (idx, dist)
}

/// Per-thread scratch reused across query atoms (rayon `map_init`), so the gather
/// loop stops reallocating. Purely structural: results are unchanged.
type Scratch = (Vec<i64>, Vec<f64>, Vec<usize>);

fn new_scratch() -> Scratch {
    (Vec::with_capacity(256), Vec::with_capacity(256), Vec::with_capacity(256))
}

/// Assemble a flat CSR from per-query (indices, distances), preserving work order.
fn flatten(per_work: Vec<(Vec<i64>, Vec<f64>)>) -> (Vec<i64>, Vec<i64>, Vec<f64>) {
    let mut offsets = vec![0i64; per_work.len() + 1];
    let mut total = 0usize;
    for (w, (idx, _)) in per_work.iter().enumerate() {
        total += idx.len();
        offsets[w + 1] = total as i64;
    }
    let mut indices = Vec::with_capacity(total);
    let mut distances = Vec::with_capacity(total);
    for (idx, dist) in per_work {
        indices.extend(idx);
        distances.extend(dist);
    }
    (offsets, indices, distances)
}

struct GridV {
    nx: i64, ny: i64, nz: i64,
    xmin: f64, ymin: f64, zmin: f64,
    cdx: f64, cdy: f64, cdz: f64,
    head: Vec<i64>,
    nxt: Vec<i64>,
}

impl GridV {
    fn cell(&self, x: f64, y: f64, z: f64) -> (i64, i64, i64) {
        (
            (((x - self.xmin) / self.cdx) as i64).clamp(0, self.nx - 1),
            (((y - self.ymin) / self.cdy) as i64).clamp(0, self.ny - 1),
            (((z - self.zmin) / self.cdz) as i64).clamp(0, self.nz - 1),
        )
    }
}

fn build_grid_v(query: &ArrayView3<f64>, refc: &ArrayView3<f64>, s: usize, cutoff: f64) -> GridV {
    let nq = query.shape()[1];
    let nr = refc.shape()[1];
    let (mut xmn, mut ymn, mut zmn) = (query[[s, 0, 0]], query[[s, 0, 1]], query[[s, 0, 2]]);
    let (mut xmx, mut ymx, mut zmx) = (xmn, ymn, zmn);
    for a in 0..nq {
        let (x, y, z) = (query[[s, a, 0]], query[[s, a, 1]], query[[s, a, 2]]);
        xmn = xmn.min(x); xmx = xmx.max(x);
        ymn = ymn.min(y); ymx = ymx.max(y);
        zmn = zmn.min(z); zmx = zmx.max(z);
    }
    for a in 0..nr {
        let (x, y, z) = (refc[[s, a, 0]], refc[[s, a, 1]], refc[[s, a, 2]]);
        xmn = xmn.min(x); xmx = xmx.max(x);
        ymn = ymn.min(y); ymx = ymx.max(y);
        zmn = zmn.min(z); zmx = zmx.max(z);
    }
    let lx = cutoff.max(xmx - xmn + 1e-5);
    let ly = cutoff.max(ymx - ymn + 1e-5);
    let lz = cutoff.max(zmx - zmn + 1e-5);
    let nx = ((lx / cutoff) as i64).max(1);
    let ny = ((ly / cutoff) as i64).max(1);
    let nz = ((lz / cutoff) as i64).max(1);
    let mut g = GridV {
        nx, ny, nz, xmin: xmn, ymin: ymn, zmin: zmn,
        cdx: lx / nx as f64, cdy: ly / ny as f64, cdz: lz / nz as f64,
        head: vec![-1i64; (nx * ny * nz) as usize],
        nxt: vec![-1i64; nr],
    };
    for a in 0..nr {
        let (cx, cy, cz) = g.cell(refc[[s, a, 0]], refc[[s, a, 1]], refc[[s, a, 2]]);
        let c = (cx + g.nx * (cy + g.ny * cz)) as usize;
        g.nxt[a] = g.head[c];
        g.head[c] = a as i64;
    }
    g
}

#[allow(clippy::too_many_arguments)]
fn gather_v(g: &GridV, refc: &ArrayView3<f64>, s: usize, qx: f64, qy: f64, qz: f64,
            iq: usize, excl: bool, cutoff_sq: f64,
            cand: &mut Vec<i64>, csq: &mut Vec<f64>) {
    let (cx, cy, cz) = g.cell(qx, qy, qz);
    cand.clear();
    csq.clear();
    for ox in (cx - 1).max(0)..(cx + 2).min(g.nx) {
        for oy in (cy - 1).max(0)..(cy + 2).min(g.ny) {
            for oz in (cz - 1).max(0)..(cz + 2).min(g.nz) {
                let c = (ox + g.nx * (oy + g.ny * oz)) as usize;
                let mut j = g.head[c];
                while j != -1 {
                    let ju = j as usize;
                    if !(excl && j == iq as i64) {
                        let rx = refc[[s, ju, 0]] - qx;
                        let ry = refc[[s, ju, 1]] - qy;
                        let rz = refc[[s, ju, 2]] - qz;
                        let d2 = rx * rx + ry * ry + rz * rz;
                        if d2 <= cutoff_sq {
                            cand.push(j);
                            csq.push(d2);
                        }
                    }
                    j = g.nxt[ju];
                }
            }
        }
    }
}

struct GridP {
    nx: i64, ny: i64, nz: i64,
    inv: Mat3, ortho: bool,     // inv: original-box inverse, for cell binning only
    wcell: Mat3, winv: Mat3,    // reduced wrap cell + inverse, for the MIC distance
    head: Vec<i64>,
    nxt: Vec<i64>,
}

impl GridP {
    fn cell(&self, x: f64, y: f64, z: f64) -> (i64, i64, i64) {
        // Lattice fractional coordinates s = inv^T · p (columns of the inverse): position
        // p = s · b with rows as lattice vectors, so s_j = sum_i p_i inv[i][j]. The old
        // code used inv · p (rows), which agrees only for orthogonal boxes and mis-bins
        // triclinic ones so the ±1 stencil no longer matches spatial ±1.
        let mut sx = self.inv[0][0] * x + self.inv[1][0] * y + self.inv[2][0] * z;
        let mut sy = self.inv[0][1] * x + self.inv[1][1] * y + self.inv[2][1] * z;
        let mut sz = self.inv[0][2] * x + self.inv[1][2] * y + self.inv[2][2] * z;
        sx -= fast_floor(sx); sy -= fast_floor(sy); sz -= fast_floor(sz);
        (
            (sx * self.nx as f64) as i64 % self.nx,
            (sy * self.ny as f64) as i64 % self.ny,
            (sz * self.nz as f64) as i64 % self.nz,
        )
    }
}

fn build_grid_p(refc: &ArrayView3<f64>, boxes: &ArrayView3<f64>, s: usize, cutoff: f64) -> GridP {
    let nr = refc.shape()[1];
    let b: Mat3 = [
        [boxes[[s, 0, 0]], boxes[[s, 0, 1]], boxes[[s, 0, 2]]],
        [boxes[[s, 1, 0]], boxes[[s, 1, 1]], boxes[[s, 1, 2]]],
        [boxes[[s, 2, 0]], boxes[[s, 2, 1]], boxes[[s, 2, 2]]],
    ];
    let (nx, ny, nz) = grid_dims(&b, cutoff);
    let (ortho, wcell, winv) = crate::mic::prep_dist(&b);
    let mut g = GridP {
        nx, ny, nz, inv: inv3(&b), ortho, wcell, winv,
        head: vec![-1i64; (nx * ny * nz) as usize],
        nxt: vec![-1i64; nr],
    };
    for a in 0..nr {
        let (cx, cy, cz) = g.cell(refc[[s, a, 0]], refc[[s, a, 1]], refc[[s, a, 2]]);
        let c = (cx + g.nx * (cy + g.ny * cz)) as usize;
        g.nxt[a] = g.head[c];
        g.head[c] = a as i64;
    }
    g
}

#[allow(clippy::too_many_arguments)]
fn gather_p(g: &GridP, refc: &ArrayView3<f64>, s: usize, qx: f64, qy: f64, qz: f64,
            iq: usize, excl: bool, cutoff_sq: f64,
            cand: &mut Vec<i64>, csq: &mut Vec<f64>) {
    let (cx, cy, cz) = g.cell(qx, qy, qz);
    cand.clear();
    csq.clear();
    // Each periodic axis is visited over its *unique* neighbour cells: the ±1 wrap for
    // n >= 3, but all n cells (once each) for n < 3, where ±1 would revisit a cell and
    // double-count. mic_wrap still selects the correct image for whichever cell an atom
    // sits in, so visiting each cell once is complete.
    let (xs, nxs) = axis_cells(cx, g.nx);
    let (ys, nys) = axis_cells(cy, g.ny);
    let (zs, nzs) = axis_cells(cz, g.nz);
    for &wcx in &xs[..nxs] {
        for &wcy in &ys[..nys] {
            for &wcz in &zs[..nzs] {
                let c = (wcx + g.nx * (wcy + g.ny * wcz)) as usize;
                let mut j = g.head[c];
                while j != -1 {
                    let ju = j as usize;
                    if !(excl && j == iq as i64) {
                        let dx = refc[[s, ju, 0]] - qx;
                        let dy = refc[[s, ju, 1]] - qy;
                        let dz = refc[[s, ju, 2]] - qz;
                        let (wx, wy, wz) = mic_wrap(dx, dy, dz, &g.wcell, &g.winv, g.ortho);
                        let d2 = wx * wx + wy * wy + wz * wz;
                        if d2 <= cutoff_sq {
                            cand.push(j);
                            csq.push(d2);
                        }
                    }
                    j = g.nxt[ju];
                }
            }
        }
    }
}

fn core_vacuum(query: &ArrayView3<f64>, refc: &ArrayView3<f64>, cutoff: f64, excl: bool, sort: bool)
    -> (Vec<i64>, Vec<i64>, Vec<f64>) {
    let ns = query.shape()[0];
    let nq = query.shape()[1];
    let cutoff_sq = cutoff * cutoff;
    let grids: Vec<GridV> = (0..ns).into_par_iter().map(|s| build_grid_v(query, refc, s, cutoff)).collect();
    let per_work: Vec<(Vec<i64>, Vec<f64>)> = (0..ns * nq)
        .into_par_iter()
        .map_init(new_scratch, |(cand, csq, order), w| {
            let s = w / nq;
            let iq = w % nq;
            gather_v(&grids[s], refc, s,
                query[[s, iq, 0]], query[[s, iq, 1]], query[[s, iq, 2]], iq, excl, cutoff_sq,
                cand, csq);
            emit_from(cand, csq, sort, order)
        })
        .collect();
    flatten(per_work)
}

fn core_pbc(query: &ArrayView3<f64>, refc: &ArrayView3<f64>, boxes: &ArrayView3<f64>,
            cutoff: f64, excl: bool, sort: bool) -> (Vec<i64>, Vec<i64>, Vec<f64>) {
    let ns = query.shape()[0];
    let nq = query.shape()[1];
    let cutoff_sq = cutoff * cutoff;
    let grids: Vec<GridP> = (0..ns).into_par_iter().map(|s| build_grid_p(refc, boxes, s, cutoff)).collect();
    let per_work: Vec<(Vec<i64>, Vec<f64>)> = (0..ns * nq)
        .into_par_iter()
        .map_init(new_scratch, |(cand, csq, order), w| {
            let s = w / nq;
            let iq = w % nq;
            gather_p(&grids[s], refc, s,
                query[[s, iq, 0]], query[[s, iq, 1]], query[[s, iq, 2]], iq, excl, cutoff_sq,
                cand, csq);
            emit_from(cand, csq, sort, order)
        })
        .collect();
    flatten(per_work)
}

#[pyfunction]
#[pyo3(signature = (query, ref_coords, box_matrices, cutoff, exclude_self, sort_by_distance))]
pub fn neighbor_list_csr_multi<'py>(
    py: Python<'py>,
    query: PyReadonlyArray3<'py, f64>,
    ref_coords: PyReadonlyArray3<'py, f64>,
    box_matrices: Option<PyReadonlyArray3<'py, f64>>,
    cutoff: f64,
    exclude_self: bool,
    sort_by_distance: bool,
) -> (Bound<'py, PyArray1<i64>>, Bound<'py, PyArray1<i64>>, Bound<'py, PyArray1<f64>>) {
    let q = query.as_array();
    let r = ref_coords.as_array();
    let (offsets, indices, distances) = match &box_matrices {
        None => py.allow_threads(|| core_vacuum(&q, &r, cutoff, exclude_self, sort_by_distance)),
        Some(b) => {
            let bb = b.as_array();
            py.allow_threads(|| core_pbc(&q, &r, &bb, cutoff, exclude_self, sort_by_distance))
        }
    };
    (offsets.into_pyarray(py), indices.into_pyarray(py), distances.into_pyarray(py))
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(neighbor_list_csr_multi, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const ORTHO: Mat3 = [[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]];
    const TRIC: Mat3 = [[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]];

    #[test]
    fn orthogonality_detection() {
        assert!(is_orthogonal(&ORTHO));
        assert!(!is_orthogonal(&TRIC));
    }

    // ---- grid primitives -------------------------------------------------------------

    #[test]
    fn grid_cells_are_at_least_cutoff_thick_perpendicular() {
        // For every box the cell perpendicular thickness must be >= cutoff, which is what
        // makes the +-1 stencil complete. Thickness = perp_full / n.
        let boxes = [
            ORTHO, TRIC,
            [[6.0, 0.0, 0.0], [3.0, 6.0, 0.0], [3.0, 3.0, 6.0]],
            [[8.0, 0.0, 0.0], [-2.5, 7.0, 0.0], [2.0, -3.0, 5.0]],
        ];
        let cross = |u: &[f64; 3], v: &[f64; 3]| {
            [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
        };
        let norm = |v: [f64; 3]| (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]).sqrt();
        for b in boxes {
            let cutoff = 1.3;
            let (nx, ny, nz) = grid_dims(&b, cutoff);
            let vol = (b[0][0] * (b[1][1] * b[2][2] - b[1][2] * b[2][1])
                - b[0][1] * (b[1][0] * b[2][2] - b[1][2] * b[2][0])
                + b[0][2] * (b[1][0] * b[2][1] - b[1][1] * b[2][0]))
                .abs();
            let perp_a = vol / norm(cross(&b[1], &b[2]));
            let perp_b = vol / norm(cross(&b[0], &b[2]));
            let perp_c = vol / norm(cross(&b[0], &b[1]));
            assert!(perp_a / nx as f64 >= cutoff - 1e-9, "x cell too thin");
            assert!(perp_b / ny as f64 >= cutoff - 1e-9, "y cell too thin");
            assert!(perp_c / nz as f64 >= cutoff - 1e-9, "z cell too thin");
        }
    }

    #[test]
    fn axis_cells_are_unique_and_cover_the_neighbourhood() {
        for n in 1..8 {
            for c in 0..n {
                let (cells, k) = axis_cells(c, n);
                let used = &cells[..k];
                // no duplicates
                for i in 0..k {
                    for j in (i + 1)..k {
                        assert_ne!(used[i], used[j], "duplicate cell for n={n} c={c}");
                    }
                    assert!(used[i] >= 0 && used[i] < n, "cell out of range");
                }
                // the true ±1 wrapped neighbours are all present
                for off in [-1i64, 0, 1] {
                    let w = (c + off).rem_euclid(n);
                    assert!(used.contains(&w), "missing neighbour cell for n={n} c={c}");
                }
            }
        }
    }

    /// Brute-force minimum image over a wide ±3 shell — the ground truth for the grid.
    fn brute_pairs(coords: &[[f64; 3]], b: &Mat3, cutoff: f64) -> std::collections::BTreeSet<(usize, usize)> {
        let inv = crate::mathlib::inverse_matrix_3x3_full(b);
        let mut out = std::collections::BTreeSet::new();
        let n = coords.len();
        for i in 0..n {
            for j in 0..n {
                if i == j {
                    continue;
                }
                let d = [coords[j][0] - coords[i][0], coords[j][1] - coords[i][1], coords[j][2] - coords[i][2]];
                let s = [
                    inv[0][0] * d[0] + inv[1][0] * d[1] + inv[2][0] * d[2],
                    inv[0][1] * d[0] + inv[1][1] * d[1] + inv[2][1] * d[2],
                    inv[0][2] * d[0] + inv[1][2] * d[1] + inv[2][2] * d[2],
                ];
                let base = [s[0].round(), s[1].round(), s[2].round()];
                let mut dmin = f64::INFINITY;
                for a in -3..=3 {
                    for bb in -3..=3 {
                        for cc in -3..=3 {
                            let ds = [s[0] - base[0] - a as f64, s[1] - base[1] - bb as f64, s[2] - base[2] - cc as f64];
                            let w = [
                                b[0][0] * ds[0] + b[1][0] * ds[1] + b[2][0] * ds[2],
                                b[0][1] * ds[0] + b[1][1] * ds[1] + b[2][1] * ds[2],
                                b[0][2] * ds[0] + b[1][2] * ds[1] + b[2][2] * ds[2],
                            ];
                            dmin = dmin.min(w[0] * w[0] + w[1] * w[1] + w[2] * w[2]);
                        }
                    }
                }
                if dmin.sqrt() <= cutoff {
                    out.insert((i, j));
                }
            }
        }
        out
    }

    /// The full periodic neighbour list (`core_pbc`) must equal the brute-force ground
    /// truth on orthogonal, skewed and small boxes — the invariant every optimisation of
    /// the grid/wrap must preserve.
    #[test]
    fn neighbour_list_matches_brute_force_on_many_boxes() {
        use numpy::ndarray::Array3;
        let mut seed = 0xC0FFEEu64;
        let mut rng = || {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (seed >> 11) as f64 / (1u64 << 53) as f64
        };
        let cases: [(Mat3, f64); 4] = [
            (ORTHO, 1.2),
            ([[6.0, 0.0, 0.0], [3.0, 6.0, 0.0], [3.0, 3.0, 6.0]], 1.2), // heavily skewed
            ([[8.0, 0.0, 0.0], [-2.5, 7.0, 0.0], [2.0, -3.0, 5.0]], 1.5),
            ([[2.4, 0.0, 0.0], [0.6, 2.4, 0.0], [0.3, 0.4, 2.4]], 0.9), // small: n<3 cells
        ];
        for (b, cutoff) in cases {
            let n = 60usize;
            // atoms spilling past the faces (fractional in [-0.2, 1.2])
            let mut data = Vec::with_capacity(n * 3);
            let mut pts = Vec::with_capacity(n);
            for _ in 0..n {
                let f = [1.4 * rng() - 0.2, 1.4 * rng() - 0.2, 1.4 * rng() - 0.2];
                let p = [
                    f[0] * b[0][0] + f[1] * b[1][0] + f[2] * b[2][0],
                    f[0] * b[0][1] + f[1] * b[1][1] + f[2] * b[2][1],
                    f[0] * b[0][2] + f[1] * b[1][2] + f[2] * b[2][2],
                ];
                data.extend_from_slice(&p);
                pts.push(p);
            }
            let coords = Array3::from_shape_vec((1, n, 3), data).unwrap();
            let boxes = Array3::from_shape_vec((1, 3, 3),
                b.iter().flat_map(|r| r.iter().copied()).collect()).unwrap();
            let (off, idx, _) = core_pbc(&coords.view(), &coords.view(), &boxes.view(),
                                         cutoff, true, false);
            let mut got = std::collections::BTreeSet::new();
            for i in 0..n {
                for p in off[i] as usize..off[i + 1] as usize {
                    got.insert((i, idx[p] as usize));
                }
                // no duplicates in the row
                let row: Vec<i64> = (off[i] as usize..off[i + 1] as usize).map(|p| idx[p]).collect();
                let uniq: std::collections::BTreeSet<i64> = row.iter().copied().collect();
                assert_eq!(row.len(), uniq.len(), "duplicate neighbour, box {b:?}");
            }
            let truth = brute_pairs(&pts, &b, cutoff);
            assert_eq!(got, truth, "neighbour list != brute force for box {b:?} cutoff {cutoff}");
        }
    }

    #[test]
    fn full_inverse_round_trips() {
        let inv = inv3(&TRIC);
        for i in 0..3 {
            for j in 0..3 {
                let mut acc = 0.0;
                for k in 0..3 {
                    acc += inv[i][k] * TRIC[k][j];
                }
                let expect = if i == j { 1.0 } else { 0.0 };
                assert!((acc - expect).abs() < 1e-12, "({i},{j}) = {acc}");
            }
        }
    }

    #[test]
    fn mic_wrap_picks_the_nearest_image() {
        let inv = inv3(&ORTHO);
        let (x, _, _) = mic_wrap(5.0, 0.0, 0.0, &ORTHO, &inv, true);
        assert!((x - (-1.0)).abs() < 1e-12, "got {x}");
    }

    #[test]
    fn emit_sorts_by_distance_and_preserves_order_when_unsorted() {
        let cand = vec![7i64, 3, 9];
        let csq = vec![4.0, 1.0, 9.0];
        let mut order = Vec::new();

        let (idx, dist) = emit_from(&cand, &csq, true, &mut order);
        assert_eq!(idx, vec![3, 7, 9]);
        assert!((dist[0] - 1.0).abs() < 1e-15 && (dist[1] - 2.0).abs() < 1e-15
                && (dist[2] - 3.0).abs() < 1e-15, "distances are sqrt of csq, ascending");

        let (idx_u, _) = emit_from(&cand, &csq, false, &mut order);
        assert_eq!(idx_u, cand, "unsorted must keep the gather order");
    }

    #[test]
    fn emit_handles_an_empty_neighbour_set() {
        let mut order = Vec::new();
        let (idx, dist) = emit_from(&[], &[], true, &mut order);
        assert!(idx.is_empty() && dist.is_empty());
    }

    #[test]
    fn flatten_builds_cumulative_offsets() {
        let per_work = vec![
            (vec![1i64, 2], vec![0.5, 0.6]),
            (vec![], vec![]),
            (vec![7i64], vec![1.5]),
        ];
        let (offsets, indices, distances) = flatten(per_work);
        assert_eq!(offsets, vec![0, 2, 2, 3]);
        assert_eq!(indices, vec![1, 2, 7]);
        assert_eq!(distances.len(), 3);
    }
}
