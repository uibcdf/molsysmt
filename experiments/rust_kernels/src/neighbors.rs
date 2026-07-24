//! Rusterized multi-structure CSR neighbour list.
//!
//! Faithful port of `molsysmt.lib.structure.neighbor_list.neighbor_list_csr_multi`
//! (the hot kernel behind get_contacts and get_neighbors). Same algorithm and MIC
//! convention as the Numba oracle (full inverse + nearest-image fractional round; no
//! 27-image search), so results are bit-for-bit identical. The parallelism (rayon
//! over the flattened work, GIL released) is a structure-level change that does not
//! affect the result: each query atom is gathered independently and the flat CSR is
//! assembled in work order.

use numpy::ndarray::ArrayView3;
use numpy::{IntoPyArray, PyArray1, PyReadonlyArray3};
use pyo3::prelude::*;

use crate::mathlib::inverse_matrix_3x3_full as inv3;
use rayon::prelude::*;

type Mat3 = [[f64; 3]; 3];

fn is_orthogonal(b: &Mat3) -> bool {
    let tol = 1e-10;
    b[0][1].abs() < tol && b[0][2].abs() < tol && b[1][0].abs() < tol
        && b[1][2].abs() < tol && b[2][0].abs() < tol && b[2][1].abs() < tol
}

/// Matches neighbor_list._mic_wrap_vector.
fn mic_wrap(dx: f64, dy: f64, dz: f64, b: &Mat3, inv: &Mat3, ortho: bool) -> (f64, f64, f64) {
    if ortho {
        (
            dx - b[0][0] * (dx / b[0][0] + 0.5).floor(),
            dy - b[1][1] * (dy / b[1][1] + 0.5).floor(),
            dz - b[2][2] * (dz / b[2][2] + 0.5).floor(),
        )
    } else {
        let mut sx = inv[0][0] * dx + inv[0][1] * dy + inv[0][2] * dz;
        let mut sy = inv[1][0] * dx + inv[1][1] * dy + inv[1][2] * dz;
        let mut sz = inv[2][0] * dx + inv[2][1] * dy + inv[2][2] * dz;
        sx -= (sx + 0.5).floor();
        sy -= (sy + 0.5).floor();
        sz -= (sz + 0.5).floor();
        (
            b[0][0] * sx + b[0][1] * sy + b[0][2] * sz,
            b[1][0] * sx + b[1][1] * sy + b[1][2] * sz,
            b[2][0] * sx + b[2][1] * sy + b[2][2] * sz,
        )
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
            (((x - self.xmin) / self.cdx).floor() as i64).clamp(0, self.nx - 1),
            (((y - self.ymin) / self.cdy).floor() as i64).clamp(0, self.ny - 1),
            (((z - self.zmin) / self.cdz).floor() as i64).clamp(0, self.nz - 1),
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
    let nx = ((lx / cutoff).floor() as i64).max(1);
    let ny = ((ly / cutoff).floor() as i64).max(1);
    let nz = ((lz / cutoff).floor() as i64).max(1);
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
    b: Mat3, inv: Mat3, ortho: bool,
    head: Vec<i64>,
    nxt: Vec<i64>,
}

impl GridP {
    fn cell(&self, x: f64, y: f64, z: f64) -> (i64, i64, i64) {
        let mut sx = self.inv[0][0] * x + self.inv[0][1] * y + self.inv[0][2] * z;
        let mut sy = self.inv[1][0] * x + self.inv[1][1] * y + self.inv[1][2] * z;
        let mut sz = self.inv[2][0] * x + self.inv[2][1] * y + self.inv[2][2] * z;
        sx -= sx.floor(); sy -= sy.floor(); sz -= sz.floor();
        (
            (sx * self.nx as f64).floor() as i64 % self.nx,
            (sy * self.ny as f64).floor() as i64 % self.ny,
            (sz * self.nz as f64).floor() as i64 % self.nz,
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
    let nx = ((b[0][0] / cutoff).floor() as i64).max(1);
    let ny = ((b[1][1] / cutoff).floor() as i64).max(1);
    let nz = ((b[2][2] / cutoff).floor() as i64).max(1);
    let mut g = GridP {
        nx, ny, nz, b, inv: inv3(&b), ortho: is_orthogonal(&b),
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
    for ox in (cx - 1)..(cx + 2) {
        let wcx = (ox + g.nx) % g.nx;
        for oy in (cy - 1)..(cy + 2) {
            let wcy = (oy + g.ny) % g.ny;
            for oz in (cz - 1)..(cz + 2) {
                let wcz = (oz + g.nz) % g.nz;
                let c = (wcx + g.nx * (wcy + g.ny * wcz)) as usize;
                let mut j = g.head[c];
                while j != -1 {
                    let ju = j as usize;
                    if !(excl && j == iq as i64) {
                        let dx = refc[[s, ju, 0]] - qx;
                        let dy = refc[[s, ju, 1]] - qy;
                        let dz = refc[[s, ju, 2]] - qz;
                        let (wx, wy, wz) = mic_wrap(dx, dy, dz, &g.b, &g.inv, g.ortho);
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
