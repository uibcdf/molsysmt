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
use numpy::{IntoPyArray, PyArray1, PyReadonlyArray3, PyUntypedArrayMethods};
use pyo3::exceptions::{PyMemoryError, PyValueError};
use pyo3::prelude::*;
use std::sync::atomic::{AtomicUsize, Ordering};

use crate::mathlib::fast_floor;
use crate::mathlib::inverse_matrix_3x3_full as inv3;
use rayon::prelude::*;

type Mat3 = [[f64; 3]; 3];
const MAX_HEADS_PER_REFERENCE: usize = 4;

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

/// Unique periodic neighbour cells along one axis: the ±1 wrap for `n >= 3`, or all `n`
/// cells (each once) for `n < 3`, avoiding the double-count a ±1 wrap causes on a small box.
#[inline]
pub(crate) fn axis_cells(c: i64, n: i64) -> ([i64; 3], usize) {
    if n >= 3 {
        (
            [
                (c - 1).rem_euclid(n),
                c.rem_euclid(n),
                (c + 1).rem_euclid(n),
            ],
            3,
        )
    } else if n == 2 {
        ([0, 1, 0], 2)
    } else {
        ([0, 0, 0], 1)
    }
}

type Buffers = (Vec<i64>, Vec<i64>, Vec<f64>);
type KernelResult<T> = Result<T, String>;
type Scratch = (Vec<i64>, Vec<f64>, Vec<usize>);

fn checked_mul(a: usize, b: usize) -> KernelResult<usize> {
    a.checked_mul(b)
        .ok_or_else(|| "Neighbor working-size multiplication overflow".into())
}

fn checked_add(a: usize, b: usize) -> KernelResult<usize> {
    a.checked_add(b)
        .ok_or_else(|| "Neighbor working-size addition overflow".into())
}

fn reserved<T>(count: usize) -> KernelResult<Vec<T>> {
    let mut out = Vec::new();
    out.try_reserve_exact(count)
        .map_err(|e| format!("Cannot reserve neighbor storage: {e}"))?;
    Ok(out)
}

fn filled(count: usize, value: i64) -> KernelResult<Vec<i64>> {
    let mut out = reserved(count)?;
    out.resize(count, value);
    Ok(out)
}

/// Coarsening increases cell widths, preserving the complete ±1 candidate stencil.
/// Every head table is bounded by reference population, never empty spatial volume.
fn bounded_dims(dims: (i64, i64, i64), limit: usize) -> (i64, i64, i64) {
    let limit = limit.max(1).min(i64::MAX as usize) as i64;
    let mut n = [
        dims.0.clamp(1, limit),
        dims.1.clamp(1, limit),
        dims.2.clamp(1, limit),
    ];
    while n[0]
        .checked_mul(n[1])
        .and_then(|v| v.checked_mul(n[2]))
        .is_none_or(|v| v > limit)
    {
        let axis = (0..3).max_by_key(|&i| n[i]).unwrap();
        n[axis] = (n[axis] / 2).max(1);
    }
    (n[0], n[1], n[2])
}

struct WorkingBudget {
    used: AtomicUsize,
    limit: usize,
}

impl WorkingBudget {
    fn new(baseline: usize, limit: usize) -> KernelResult<Self> {
        if baseline > limit {
            return Err(format!("Neighbor working estimate {baseline} bytes exceeds the {limit}-byte numerical budget"));
        }
        Ok(Self {
            used: AtomicUsize::new(baseline),
            limit,
        })
    }

    fn charge_output(&self, entries: usize) -> KernelResult<()> {
        // Both per-query vectors and the final packed CSR can coexist during flattening.
        let bytes = checked_mul(entries, 32)?;
        self.used.fetch_update(Ordering::Relaxed, Ordering::Relaxed, |used| {
            used.checked_add(bytes).filter(|&total| total <= self.limit)
        }).map_err(|used| format!("Neighbor CSR output needs {bytes} additional working bytes after {used}; numerical budget is {}", self.limit))?;
        Ok(())
    }
}

fn working_budget(
    q: &ArrayView3<f64>,
    r: &ArrayView3<f64>,
    grid_size: usize,
    periodic: bool,
    limit: usize,
) -> KernelResult<WorkingBudget> {
    let ns = q.shape()[0];
    let nr = r.shape()[1];
    let rows = checked_mul(ns, q.shape()[1])?;
    let heads = checked_mul(nr, MAX_HEADS_PER_REFERENCE)?.max(1);
    let threads = rayon::current_num_threads();
    let terms = [
        checked_mul(q.len(), 8)?,
        if q.as_ptr() == r.as_ptr() && q.shape() == r.shape() {
            0
        } else {
            checked_mul(r.len(), 8)?
        },
        checked_mul(
            ns,
            checked_add(checked_mul(checked_add(heads, nr)?, 8)?, grid_size)?,
        )?,
        if periodic { checked_mul(ns, 72)? } else { 0 },
        // Row descriptors, allocation bookkeeping, and packed offsets.
        checked_mul(rows, 96)?,
        checked_mul(checked_add(rows, 1)?, 8)?,
        // Scratch lengths never exceed nr. Include bounded reallocation overlap
        // and task bookkeeping; this is a numerical estimate, not process RSS.
        checked_mul(threads, checked_add(checked_mul(nr, 64)?, 65536)?)?,
    ];
    let baseline = terms.into_iter().try_fold(0usize, checked_add)?;
    WorkingBudget::new(baseline, limit)
}

fn empty_rows(rows: usize, limit: usize) -> KernelResult<Buffers> {
    WorkingBudget::new(checked_mul(checked_add(rows, 1)?, 8)?, limit)?;
    Ok((filled(checked_add(rows, 1)?, 0)?, Vec::new(), Vec::new()))
}

fn new_scratch(nr: usize) -> KernelResult<Scratch> {
    let initial = nr.min(256);
    Ok((reserved(initial)?, reserved(initial)?, reserved(initial)?))
}

fn push_candidate(
    cand: &mut Vec<i64>,
    csq: &mut Vec<f64>,
    j: i64,
    d2: f64,
    nr: usize,
) -> KernelResult<()> {
    if cand.len() >= nr {
        return Err("Neighbor gather exceeded the reference population".into());
    }
    if cand.len() == cand.capacity() {
        let next = checked_mul(cand.capacity(), 2)?.max(1).min(nr);
        cand.try_reserve_exact(next - cand.len())
            .map_err(|e| format!("Cannot grow neighbor scratch: {e}"))?;
    }
    if csq.len() == csq.capacity() {
        let next = checked_mul(csq.capacity(), 2)?.max(1).min(nr);
        csq.try_reserve_exact(next - csq.len())
            .map_err(|e| format!("Cannot grow neighbor scratch: {e}"))?;
    }
    cand.push(j);
    csq.push(d2);
    Ok(())
}

fn emit_from(
    cand: &[i64],
    csq: &[f64],
    sort: bool,
    order: &mut Vec<usize>,
) -> KernelResult<(Vec<i64>, Vec<f64>)> {
    let m = cand.len();
    let mut idx = reserved(m)?;
    let mut dist = reserved(m)?;
    if sort {
        order.clear();
        order
            .try_reserve_exact(m)
            .map_err(|e| format!("Cannot reserve neighbor sorting workspace: {e}"))?;
        order.extend(0..m);
        // The target-index tiebreak makes this a total order without stable-sort scratch.
        order.sort_unstable_by(|&a, &b| {
            csq[a]
                .partial_cmp(&csq[b])
                .unwrap()
                .then_with(|| cand[a].cmp(&cand[b]))
        });
        for &i in order.iter() {
            idx.push(cand[i]);
            dist.push(csq[i].sqrt());
        }
    } else {
        for i in 0..m {
            idx.push(cand[i]);
            dist.push(csq[i].sqrt());
        }
    }
    Ok((idx, dist))
}

fn flatten(per_work: Vec<(Vec<i64>, Vec<f64>)>) -> KernelResult<Buffers> {
    let mut offsets = reserved(checked_add(per_work.len(), 1)?)?;
    offsets.push(0);
    let mut total = 0usize;
    for (idx, _) in &per_work {
        total = checked_add(total, idx.len())?;
        offsets.push(
            i64::try_from(total).map_err(|_| "Neighbor CSR offset exceeds int64".to_string())?,
        );
    }
    let mut indices = reserved(total)?;
    let mut distances = reserved(total)?;
    for (mut idx, mut dist) in per_work {
        indices.append(&mut idx);
        distances.append(&mut dist);
    }
    Ok((offsets, indices, distances))
}

struct GridV {
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

impl GridV {
    fn cell(&self, x: f64, y: f64, z: f64) -> (i64, i64, i64) {
        (
            (((x - self.xmin) / self.cdx) as i64).clamp(0, self.nx - 1),
            (((y - self.ymin) / self.cdy) as i64).clamp(0, self.ny - 1),
            (((z - self.zmin) / self.cdz) as i64).clamp(0, self.nz - 1),
        )
    }
}

fn build_grid_v(
    query: &ArrayView3<f64>,
    refc: &ArrayView3<f64>,
    s: usize,
    cutoff: f64,
) -> KernelResult<GridV> {
    let nq = query.shape()[1];
    let nr = refc.shape()[1];
    let (mut xmn, mut ymn, mut zmn) = (query[[s, 0, 0]], query[[s, 0, 1]], query[[s, 0, 2]]);
    let (mut xmx, mut ymx, mut zmx) = (xmn, ymn, zmn);
    for a in 0..nq {
        let (x, y, z) = (query[[s, a, 0]], query[[s, a, 1]], query[[s, a, 2]]);
        xmn = xmn.min(x);
        xmx = xmx.max(x);
        ymn = ymn.min(y);
        ymx = ymx.max(y);
        zmn = zmn.min(z);
        zmx = zmx.max(z);
    }
    for a in 0..nr {
        let (x, y, z) = (refc[[s, a, 0]], refc[[s, a, 1]], refc[[s, a, 2]]);
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
    let (nx, ny, nz) = bounded_dims(
        (
            ((lx / cutoff) as i64).max(1),
            ((ly / cutoff) as i64).max(1),
            ((lz / cutoff) as i64).max(1),
        ),
        checked_mul(nr, MAX_HEADS_PER_REFERENCE)?.max(1),
    );
    let mut g = GridV {
        nx,
        ny,
        nz,
        xmin: xmn,
        ymin: ymn,
        zmin: zmn,
        cdx: lx / nx as f64,
        cdy: ly / ny as f64,
        cdz: lz / nz as f64,
        head: filled((nx * ny * nz) as usize, -1)?,
        nxt: filled(nr, -1)?,
    };
    for a in 0..nr {
        let (cx, cy, cz) = g.cell(refc[[s, a, 0]], refc[[s, a, 1]], refc[[s, a, 2]]);
        let c = (cx + g.nx * (cy + g.ny * cz)) as usize;
        g.nxt[a] = g.head[c];
        g.head[c] = a as i64;
    }
    Ok(g)
}

#[allow(clippy::too_many_arguments)]
fn gather_v(
    g: &GridV,
    refc: &ArrayView3<f64>,
    s: usize,
    qx: f64,
    qy: f64,
    qz: f64,
    iq: usize,
    excl: bool,
    cutoff_sq: f64,
    cand: &mut Vec<i64>,
    csq: &mut Vec<f64>,
) -> KernelResult<()> {
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
                            push_candidate(cand, csq, j, d2, refc.shape()[1])?;
                        }
                    }
                    j = g.nxt[ju];
                }
            }
        }
    }
    Ok(())
}

struct GridP {
    nx: i64,
    ny: i64,
    nz: i64,
    inv: Mat3,
    ortho: bool, // inv: original-box inverse, for cell binning only
    wcell: Mat3,
    winv: Mat3, // reduced wrap cell + inverse, for the MIC distance
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
    refc: &ArrayView3<f64>,
    boxes: &ArrayView3<f64>,
    s: usize,
    cutoff: f64,
) -> KernelResult<GridP> {
    let nr = refc.shape()[1];
    let b: Mat3 = [
        [boxes[[s, 0, 0]], boxes[[s, 0, 1]], boxes[[s, 0, 2]]],
        [boxes[[s, 1, 0]], boxes[[s, 1, 1]], boxes[[s, 1, 2]]],
        [boxes[[s, 2, 0]], boxes[[s, 2, 1]], boxes[[s, 2, 2]]],
    ];
    let (nx, ny, nz) = bounded_dims(
        grid_dims(&b, cutoff),
        checked_mul(nr, MAX_HEADS_PER_REFERENCE)?.max(1),
    );
    let (ortho, wcell, winv) = crate::mic::prep_dist(&b);
    let mut g = GridP {
        nx,
        ny,
        nz,
        inv: inv3(&b),
        ortho,
        wcell,
        winv,
        head: filled((nx * ny * nz) as usize, -1)?,
        nxt: filled(nr, -1)?,
    };
    for a in 0..nr {
        let (cx, cy, cz) = g.cell(refc[[s, a, 0]], refc[[s, a, 1]], refc[[s, a, 2]]);
        let c = (cx + g.nx * (cy + g.ny * cz)) as usize;
        g.nxt[a] = g.head[c];
        g.head[c] = a as i64;
    }
    Ok(g)
}

#[allow(clippy::too_many_arguments)]
fn gather_p(
    g: &GridP,
    refc: &ArrayView3<f64>,
    s: usize,
    qx: f64,
    qy: f64,
    qz: f64,
    iq: usize,
    excl: bool,
    cutoff_sq: f64,
    cand: &mut Vec<i64>,
    csq: &mut Vec<f64>,
) -> KernelResult<()> {
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
                            push_candidate(cand, csq, j, d2, refc.shape()[1])?;
                        }
                    }
                    j = g.nxt[ju];
                }
            }
        }
    }
    Ok(())
}

fn core_vacuum(
    query: &ArrayView3<f64>,
    refc: &ArrayView3<f64>,
    cutoff: f64,
    excl: bool,
    sort: bool,
    memory_budget: usize,
) -> KernelResult<Buffers> {
    let ns = query.shape()[0];
    let nq = query.shape()[1];
    let nr = refc.shape()[1];
    let rows = checked_mul(ns, nq)?;
    if rows == 0 || nr == 0 {
        return empty_rows(rows, memory_budget);
    }
    let budget = working_budget(
        query,
        refc,
        std::mem::size_of::<GridV>(),
        false,
        memory_budget,
    )?;
    let cutoff_sq = cutoff * cutoff;
    let mut grids = reserved(ns)?;
    for s in 0..ns {
        grids.push(build_grid_v(query, refc, s, cutoff)?);
    }
    let mut per_work = reserved(rows)?;
    per_work.resize_with(rows, || (Vec::new(), Vec::new()));
    per_work
        .par_iter_mut()
        .enumerate()
        .map_init(
            || new_scratch(nr),
            |scratch, (w, output)| {
                let (cand, csq, order) = scratch.as_mut().map_err(|error| error.clone())?;
                let s = w / nq;
                let iq = w % nq;
                gather_v(
                    &grids[s],
                    refc,
                    s,
                    query[[s, iq, 0]],
                    query[[s, iq, 1]],
                    query[[s, iq, 2]],
                    iq,
                    excl,
                    cutoff_sq,
                    cand,
                    csq,
                )?;
                budget.charge_output(cand.len())?;
                *output = emit_from(cand, csq, sort, order)?;
                Ok(())
            },
        )
        .try_for_each(|out: KernelResult<()>| out)?;
    flatten(per_work)
}

fn core_pbc(
    query: &ArrayView3<f64>,
    refc: &ArrayView3<f64>,
    boxes: &ArrayView3<f64>,
    cutoff: f64,
    excl: bool,
    sort: bool,
    memory_budget: usize,
) -> KernelResult<Buffers> {
    let ns = query.shape()[0];
    let nq = query.shape()[1];
    let nr = refc.shape()[1];
    let rows = checked_mul(ns, nq)?;
    if rows == 0 || nr == 0 {
        return empty_rows(rows, memory_budget);
    }
    let budget = working_budget(
        query,
        refc,
        std::mem::size_of::<GridP>(),
        true,
        memory_budget,
    )?;
    let cutoff_sq = cutoff * cutoff;
    let mut grids = reserved(ns)?;
    for s in 0..ns {
        grids.push(build_grid_p(refc, boxes, s, cutoff)?);
    }
    let mut per_work = reserved(rows)?;
    per_work.resize_with(rows, || (Vec::new(), Vec::new()));
    per_work
        .par_iter_mut()
        .enumerate()
        .map_init(
            || new_scratch(nr),
            |scratch, (w, output)| {
                let (cand, csq, order) = scratch.as_mut().map_err(|error| error.clone())?;
                let s = w / nq;
                let iq = w % nq;
                gather_p(
                    &grids[s],
                    refc,
                    s,
                    query[[s, iq, 0]],
                    query[[s, iq, 1]],
                    query[[s, iq, 2]],
                    iq,
                    excl,
                    cutoff_sq,
                    cand,
                    csq,
                )?;
                budget.charge_output(cand.len())?;
                *output = emit_from(cand, csq, sort, order)?;
                Ok(())
            },
        )
        .try_for_each(|out: KernelResult<()>| out)?;
    flatten(per_work)
}

#[pyfunction]
#[pyo3(signature = (query, ref_coords, box_matrices, cutoff, exclude_self, sort_by_distance, num_threads, *, memory_budget=1_073_741_824))]
#[allow(clippy::too_many_arguments, clippy::type_complexity)]
pub fn neighbor_list_csr_multi<'py>(
    py: Python<'py>,
    query: PyReadonlyArray3<'py, f64>,
    ref_coords: PyReadonlyArray3<'py, f64>,
    box_matrices: Option<PyReadonlyArray3<'py, f64>>,
    cutoff: f64,
    exclude_self: bool,
    sort_by_distance: bool,
    num_threads: usize,
    memory_budget: usize,
) -> PyResult<(
    Bound<'py, PyArray1<i64>>,
    Bound<'py, PyArray1<i64>>,
    Bound<'py, PyArray1<f64>>,
)> {
    let q = query.as_array();
    let r = ref_coords.as_array();
    if q.shape()[2] != 3 || r.shape()[2] != 3 || q.shape()[0] != r.shape()[0] {
        return Err(PyValueError::new_err(
            "Neighbor coordinates require matching structure axes and xyz columns",
        ));
    }
    if !cutoff.is_finite() || cutoff <= 0.0 {
        return Err(PyValueError::new_err(
            "Native cell-search cutoff must be finite and positive",
        ));
    }
    if q.iter().chain(r.iter()).any(|x| !x.is_finite()) {
        return Err(PyValueError::new_err("Neighbor coordinates must be finite"));
    }
    if let Some(ref b) = box_matrices {
        if b.shape() != [q.shape()[0], 3, 3] || b.as_array().iter().any(|x| !x.is_finite()) {
            return Err(PyValueError::new_err(
                "Neighbor boxes require finite structure-by-3-by-3 matrices",
            ));
        }
    }
    let result = match &box_matrices {
        None => py.detach(|| {
            crate::threads::install(num_threads, || {
                core_vacuum(
                    &q,
                    &r,
                    cutoff,
                    exclude_self,
                    sort_by_distance,
                    memory_budget,
                )
            })
        }),
        Some(b) => {
            let bb = b.as_array();
            py.detach(|| {
                crate::threads::install(num_threads, || {
                    core_pbc(
                        &q,
                        &r,
                        &bb,
                        cutoff,
                        exclude_self,
                        sort_by_distance,
                        memory_budget,
                    )
                })
            })
        }
    };
    let (offsets, indices, distances) = result.map_err(PyMemoryError::new_err)?;
    Ok((
        offsets.into_pyarray(py),
        indices.into_pyarray(py),
        distances.into_pyarray(py),
    ))
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
    fn bounded_dimensions_handle_empty_volume_and_integer_overflow() {
        for (dims, limit) in [
            ((1000, 1000, 1000), 4),
            ((i64::MAX, i64::MAX, i64::MAX), 1024),
            ((1, 1, 1), 1),
        ] {
            let (x, y, z) = bounded_dims(dims, limit);
            assert!(x >= 1 && y >= 1 && z >= 1);
            assert!(x <= dims.0 && y <= dims.1 && z <= dims.2);
            assert!((x * y * z) as usize <= limit);
        }
        assert!(checked_mul(usize::MAX, 2).is_err());
        assert!(checked_add(usize::MAX, 1).is_err());
    }

    #[test]
    fn sparse_vacuum_grid_heads_follow_population_not_empty_volume() {
        use numpy::ndarray::Array3;
        let q = Array3::zeros((1, 1, 3));
        let r = Array3::from_shape_vec((1, 1, 3), vec![1.0, 1.0, 1.0]).unwrap();
        // The regression remains safe even for an old dense implementation: 8 MiB.
        let grid = build_grid_v(&q.view(), &r.view(), 0, 0.01).unwrap();
        assert!(grid.head.len() <= 4);
        assert!(grid.cdx >= 0.01 && grid.cdy >= 0.01 && grid.cdz >= 0.01);
        let (off, idx, _) = crate::threads::install(1, || {
            core_vacuum(&q.view(), &r.view(), 0.01, false, true, 1 << 20)
        })
        .unwrap();
        assert_eq!(off, vec![0, 0]);
        assert!(idx.is_empty());
    }

    #[test]
    fn working_budget_charges_observed_output_not_quadratic_candidates() {
        use numpy::ndarray::Array3;
        let q = Array3::from_shape_fn(
            (1, 300, 3),
            |(_, a, k)| if k == 0 { a as f64 * 10.0 } else { 0.0 },
        );
        let r = q.mapv(|x| x + 1.0);
        let sparse = crate::threads::install(1, || {
            core_vacuum(&q.view(), &r.view(), 0.1, false, true, 1 << 18)
        })
        .unwrap();
        assert_eq!(sparse.0.len(), 301);
        assert!(sparse.1.is_empty());
        let dense = Array3::zeros((1, 300, 3));
        let failure = crate::threads::install(1, || {
            core_vacuum(&dense.view(), &dense.view(), 0.1, true, true, 1 << 18)
        })
        .unwrap_err();
        assert!(failure.contains("CSR output"), "{failure}");
    }

    #[test]
    fn empty_reference_only_needs_typed_offsets() {
        use numpy::ndarray::Array3;
        let q = Array3::zeros((3, 2, 3));
        let r = Array3::zeros((3, 0, 3));
        let result = core_vacuum(&q.view(), &r.view(), 0.1, false, false, 56).unwrap();
        assert_eq!(result.0, vec![0; 7]);
        assert!(result.1.is_empty() && result.2.is_empty());
        assert!(core_vacuum(&q.view(), &r.view(), 0.1, false, false, 55).is_err());
    }

    #[test]
    fn shared_output_charge_is_atomic_under_parallel_admission() {
        let budget = WorkingBudget::new(0, 1024).unwrap();
        let accepted: usize = crate::threads::install(2, || {
            (0..64usize)
                .into_par_iter()
                .map(|_| usize::from(budget.charge_output(1).is_ok()))
                .sum()
        });
        assert_eq!(accepted, 32);
        assert_eq!(budget.used.load(Ordering::Relaxed), 1024);
    }

    #[test]
    fn equal_distances_sort_by_local_target_index() {
        let mut order = Vec::new();
        let (indices, distances) =
            emit_from(&[3, 1, 2], &[1.0, 1.0, 1.0], true, &mut order).unwrap();
        assert_eq!(indices, vec![1, 2, 3]);
        assert_eq!(distances, vec![1.0, 1.0, 1.0]);
    }

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
            ORTHO,
            TRIC,
            [[6.0, 0.0, 0.0], [3.0, 6.0, 0.0], [3.0, 3.0, 6.0]],
            [[8.0, 0.0, 0.0], [-2.5, 7.0, 0.0], [2.0, -3.0, 5.0]],
        ];
        let cross = |u: &[f64; 3], v: &[f64; 3]| {
            [
                u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0],
            ]
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
    fn brute_pairs(
        coords: &[[f64; 3]],
        b: &Mat3,
        cutoff: f64,
    ) -> std::collections::BTreeSet<(usize, usize)> {
        let inv = crate::mathlib::inverse_matrix_3x3_full(b);
        let mut out = std::collections::BTreeSet::new();
        let n = coords.len();
        for i in 0..n {
            for j in 0..n {
                if i == j {
                    continue;
                }
                let d = [
                    coords[j][0] - coords[i][0],
                    coords[j][1] - coords[i][1],
                    coords[j][2] - coords[i][2],
                ];
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
                            let ds = [
                                s[0] - base[0] - a as f64,
                                s[1] - base[1] - bb as f64,
                                s[2] - base[2] - cc as f64,
                            ];
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
            seed = seed
                .wrapping_mul(6364136223846793005)
                .wrapping_add(1442695040888963407);
            (seed >> 11) as f64 / (1u64 << 53) as f64
        };
        let cases: [(Mat3, f64); 6] = [
            (ORTHO, 0.1),
            (TRIC, 0.1),
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
            let boxes = Array3::from_shape_vec(
                (1, 3, 3),
                b.iter().flat_map(|r| r.iter().copied()).collect(),
            )
            .unwrap();
            let (off, idx, _) = core_pbc(
                &coords.view(),
                &coords.view(),
                &boxes.view(),
                cutoff,
                true,
                false,
                usize::MAX,
            )
            .unwrap();
            let mut got = std::collections::BTreeSet::new();
            for i in 0..n {
                for p in off[i] as usize..off[i + 1] as usize {
                    got.insert((i, idx[p] as usize));
                }
                // no duplicates in the row
                let row: Vec<i64> = (off[i] as usize..off[i + 1] as usize)
                    .map(|p| idx[p])
                    .collect();
                let uniq: std::collections::BTreeSet<i64> = row.iter().copied().collect();
                assert_eq!(row.len(), uniq.len(), "duplicate neighbour, box {b:?}");
            }
            let truth = brute_pairs(&pts, &b, cutoff);
            assert_eq!(
                got, truth,
                "neighbour list != brute force for box {b:?} cutoff {cutoff}"
            );
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

        let (idx, dist) = emit_from(&cand, &csq, true, &mut order).unwrap();
        assert_eq!(idx, vec![3, 7, 9]);
        assert!(
            (dist[0] - 1.0).abs() < 1e-15
                && (dist[1] - 2.0).abs() < 1e-15
                && (dist[2] - 3.0).abs() < 1e-15,
            "distances are sqrt of csq, ascending"
        );

        let (idx_u, _) = emit_from(&cand, &csq, false, &mut order).unwrap();
        assert_eq!(idx_u, cand, "unsorted must keep the gather order");
    }

    #[test]
    fn emit_handles_an_empty_neighbour_set() {
        let mut order = Vec::new();
        let (idx, dist) = emit_from(&[], &[], true, &mut order).unwrap();
        assert!(idx.is_empty() && dist.is_empty());
    }

    #[test]
    fn flatten_builds_cumulative_offsets() {
        let per_work = vec![
            (vec![1i64, 2], vec![0.5, 0.6]),
            (vec![], vec![]),
            (vec![7i64], vec![1.5]),
        ];
        let (offsets, indices, distances) = flatten(per_work).unwrap();
        assert_eq!(offsets, vec![0, 2, 2, 3]);
        assert_eq!(indices, vec![1, 2, 7]);
        assert_eq!(distances.len(), 3);
    }
}
