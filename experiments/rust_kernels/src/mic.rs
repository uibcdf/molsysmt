//! Rusterized MIC (minimum-image) distance family.
//!
//! Names match `molsysmt.lib.structure.get_mic_distances.*` 1:1 so the opt-in seam can
//! dispatch by name. **This is the definitive implementation; the Numba kernels are
//! provisional and will be removed.** The distance path uses the reduced-cell minimum
//! image (`prep_dist` + `mic_distance_auto`), which is *correct on skewed boxes* — unlike
//! the exhaustive ±1 (27-image) search, whose shell can miss a second-neighbour minimum
//! image (see the module tests and `wrap_to_mic_triclinic_not_minimum_image.md`). It is
//! therefore no longer bit-for-bit with Numba on skewed boxes (Rust is the correct one);
//! on orthogonal and mildly-tilted boxes the two still agree to tolerance.
//!
//! Every wrap-based MIC kernel — distances, angles, dihedrals, the set/shift dihedral
//! ops — now goes through the reduced-cell `mic_vector`. The exhaustive ±1
//! `wrap_to_mic_vector` and `mic_distance` are retained **only as mild-box test
//! references** (they are `#[cfg(test)]`). The grid-based cell list and cell-list SASA
//! keep their own centred-wrap for now: their grid gathering has a separate triclinic
//! completeness limitation that the wrap change alone does not resolve — see
//! `devguide/pending_proposals/triclinic_cell_list_completeness.md`.

use numpy::ndarray::{Array1, Array2, Array3};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyArray3, PyReadonlyArray2, PyReadonlyArray3};
use pyo3::prelude::*;

#[cfg(test)]
use crate::mathlib::inverse_matrix_3x3;
use crate::mathlib::fast_floor;
use crate::symmetric::mirror_upper_to_lower;

pub type Mat3 = [[f64; 3]; 3];

/// Mirrors molsysmt.lib.pbc.box_is_orthogonal_single_structure (row dot products).
pub(crate) fn box_is_orthogonal(b: &Mat3) -> bool {
    let dot = |u: &[f64; 3], v: &[f64; 3]| u[0] * v[0] + u[1] * v[1] + u[2] * v[2];
    dot(&b[0], &b[1]).abs() <= 1e-4 && dot(&b[0], &b[2]).abs() <= 1e-4 && dot(&b[1], &b[2]).abs() <= 1e-4
}

/// The exhaustive ±1 (27-image) wrap — the mild-box reference kept only for tests
/// (production uses the reduced-cell `mic_vector`).
#[cfg(test)]
pub(crate) fn wrap_to_mic_vector(v: [f64; 3], b: &Mat3, inv: &Mat3, orthogonal: bool) -> [f64; 3] {
    if orthogonal {
        [
            v[0] - b[0][0] * (v[0] / b[0][0] + 0.5).floor(),
            v[1] - b[1][1] * (v[1] / b[1][1] + 0.5).floor(),
            v[2] - b[2][2] * (v[2] / b[2][2] + 0.5).floor(),
        ]
    } else {
        let mut vaux = [
            inv[0][0] * v[0] + inv[1][0] * v[1] + inv[2][0] * v[2],
            inv[1][1] * v[1] + inv[2][1] * v[2],
            inv[2][2] * v[2],
        ];
        vaux[0] -= vaux[0].floor();
        vaux[1] -= vaux[1].floor();
        vaux[2] -= vaux[2].floor();
        let mut out = [
            b[0][0] * vaux[0] + b[1][0] * vaux[1] + b[2][0] * vaux[2],
            b[1][1] * vaux[1] + b[2][1] * vaux[2],
            b[2][2] * vaux[2],
        ];
        let mut dmin = out[0] * out[0] + out[1] * out[1] + out[2] * out[2];
        for ii in -1..=1 {
            for jj in -1..=1 {
                for kk in -1..=1 {
                    let f = |c: usize| {
                        v[c] + (ii as f64) * b[0][c] + (jj as f64) * b[1][c] + (kk as f64) * b[2][c]
                    };
                    let cand = [f(0), f(1), f(2)];
                    let dd = cand[0] * cand[0] + cand[1] * cand[1] + cand[2] * cand[2];
                    if dmin > dd {
                        out = cand;
                        dmin = dd;
                    }
                }
            }
        }
        out
    }
}

/// The ±1 exhaustive distance, kept only as a mild-box reference for the tests (the
/// production distance path is `mic_distance_auto`, which is correct on skewed boxes too).
#[cfg(test)]
#[inline]
fn mic_distance(p1: [f64; 3], p2: [f64; 3], b: &Mat3, inv: &Mat3, ortho: bool) -> f64 {
    let v = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]];
    let w = wrap_to_mic_vector(v, b, inv, ortho);
    (w[0] * w[0] + w[1] * w[1] + w[2] * w[2]).sqrt()
}

// ---------------------------------------------------------- reduced-cell fast MIC path
//
// Reduce the cell once per box (MD-style lattice reduction, as OpenMM/LAMMPS require of
// their input boxes) so the minimum image is found among the 8 corners of the fractional
// cell instead of 27 images. Unlike the unreduced ±1 search, this is correct for skewed
// cells — the ±1 shell can miss a second-neighbour minimum image. Validated in the unit
// tests below against a wide (±2) ground-truth search (not against the ±1 wrap, which is
// itself wrong on skewed boxes); the two agree on mild boxes and the reduced path is never
// worse on skewed ones. Fixes `wrap_to_mic_triclinic_not_minimum_image.md` on these paths.

/// MD-style lattice reduction: greedily shorten each basis vector by the nearest-integer
/// multiple of the others until stable. Returns an equivalent basis (same lattice) whose
/// vectors are short enough that per-coordinate rounding locates the closest lattice point.
pub(crate) fn reduce_cell(b: &Mat3) -> Mat3 {
    let dot = |u: &[f64; 3], v: &[f64; 3]| u[0] * v[0] + u[1] * v[1] + u[2] * v[2];
    let mut m = *b;
    for _ in 0..100 {
        let mut changed = false;
        for i in 0..3 {
            for j in 0..3 {
                if i == j {
                    continue;
                }
                let vjj = dot(&m[j], &m[j]);
                if vjj == 0.0 {
                    continue;
                }
                let q = (dot(&m[i], &m[j]) / vjj).round();
                if q != 0.0 {
                    for k in 0..3 {
                        m[i][k] -= q * m[j][k];
                    }
                    changed = true;
                }
            }
        }
        if !changed {
            break;
        }
    }
    m
}

/// Precompute the reduced basis and its (general) inverse for a box.
#[inline]
pub(crate) fn prep_reduced(b: &Mat3) -> (Mat3, Mat3) {
    let red = reduce_cell(b);
    let inv = crate::mathlib::inverse_matrix_3x3_full(&red);
    (red, inv)
}

/// Minimum-image displacement **vector** via the reduced cell: fractional coordinates,
/// then the 8 corners of the containing cell (floor/ceil per axis) — sufficient on a
/// reduced basis — instead of the exhaustive 27-image search. `red`/`inv` are the reduced
/// cell and its general inverse from [`prep_reduced`].
#[inline(always)]
pub(crate) fn wrap_to_mic_vector_reduced(v: [f64; 3], red: &Mat3, inv: &Mat3) -> [f64; 3] {
    // fractional coordinates s (v = s . red with rows as lattice vectors => s = inv^T v).
    let s = [
        inv[0][0] * v[0] + inv[1][0] * v[1] + inv[2][0] * v[2],
        inv[0][1] * v[0] + inv[1][1] * v[1] + inv[2][1] * v[2],
        inv[0][2] * v[0] + inv[1][2] * v[1] + inv[2][2] * v[2],
    ];
    // The 8 candidates are the corners floor(s) + δ, δ ∈ {0,1}³, and the residual is
    // r(δ) = red^T·(frac − δ) with frac = s − floor(s). Factor out the shared base
    // `rf = red^T·frac`: each corner is then `rf` minus a subset of the lattice-vector
    // rows, so the eight matrix–vector products collapse to one plus vector subtractions.
    let frac = [s[0] - fast_floor(s[0]), s[1] - fast_floor(s[1]), s[2] - fast_floor(s[2])];
    let rf = [
        red[0][0] * frac[0] + red[1][0] * frac[1] + red[2][0] * frac[2],
        red[0][1] * frac[0] + red[1][1] * frac[1] + red[2][1] * frac[2],
        red[0][2] * frac[0] + red[1][2] * frac[1] + red[2][2] * frac[2],
    ];
    // Build the eight candidates and their squared norms independently, then pick the
    // winner with a three-level tournament. The sequential `if dd < dmin { dmin = dd; .. }`
    // scan this replaces is *latency* bound: eight `minsd`-plus-select steps chained
    // through `dmin`/`best`, which at ~60 ns per pair was the dominant cost of the
    // triclinic distance kernels. The tree has depth 3 instead of 8 and lets the eight
    // norms be computed in parallel.
    //
    // Bit-for-bit identical to the scan: each `d` is the same expression, and every
    // comparison keeps the lower δ on a tie exactly as `<` did while scanning upward.
    let cand = [
        rf,
        sub3(rf, red[0]),
        sub3(rf, red[1]),
        sub3(sub3(rf, red[0]), red[1]),
        sub3(rf, red[2]),
        sub3(sub3(rf, red[0]), red[2]),
        sub3(sub3(rf, red[1]), red[2]),
        sub3(sub3(sub3(rf, red[0]), red[1]), red[2]),
    ];
    let d = [
        norm2(cand[0]),
        norm2(cand[1]),
        norm2(cand[2]),
        norm2(cand[3]),
        norm2(cand[4]),
        norm2(cand[5]),
        norm2(cand[6]),
        norm2(cand[7]),
    ];
    // `pick` keeps the *lower* index on a tie, so the whole tree reproduces the scan's
    // tie-breaking (first minimum wins) as long as each pairing puts the lower index left.
    let pick = |i: usize, j: usize| if d[j] < d[i] { j } else { i };
    let a = pick(0, 1);
    let b = pick(2, 3);
    let c = pick(4, 5);
    let e = pick(6, 7);
    let ab = pick(a, b);
    let ce = pick(c, e);
    cand[pick(ab, ce)]
}

#[inline(always)]
fn sub3(a: [f64; 3], b: [f64; 3]) -> [f64; 3] {
    [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
}

#[inline(always)]
fn norm2(a: [f64; 3]) -> f64 {
    a[0] * a[0] + a[1] * a[1] + a[2] * a[2]
}

/// The single production minimum-image **vector** mechanism, used by every MIC kernel
/// (distances, angles, dihedrals, cell list, SASA). Orthogonal boxes use the centred wrap;
/// triclinic boxes use the reduced cell — correct on skewed boxes, unlike the ±1 search,
/// whose shell can miss a second-neighbour minimum image (see the module tests). `cell`/`inv`
/// come from [`prep_dist`]: for orthogonal boxes `cell` is the box and `inv` is unused; for
/// triclinic they are the reduced cell and its inverse.
#[inline(always)]
pub(crate) fn mic_vector(v: [f64; 3], cell: &Mat3, inv: &Mat3, ortho: bool) -> [f64; 3] {
    if ortho {
        mic_vector_ortho(v, cell)
    } else {
        wrap_to_mic_vector_reduced(v, cell, inv)
    }
}

/// The orthogonal branch of [`mic_vector`]: one centred floor per axis. Split out so the
/// hot pair loops can select the branch *outside* the loop (see [`mic_vector_const`]).
#[inline(always)]
pub(crate) fn mic_vector_ortho(v: [f64; 3], cell: &Mat3) -> [f64; 3] {
    [
        v[0] - cell[0][0] * fast_floor(v[0] / cell[0][0] + 0.5),
        v[1] - cell[1][1] * fast_floor(v[1] / cell[1][1] + 0.5),
        v[2] - cell[2][2] * fast_floor(v[2] / cell[2][2] + 0.5),
    ]
}

/// [`mic_vector`] with the orthogonal/triclinic choice as a **const** parameter instead of
/// a runtime flag.
///
/// The flag is loop-invariant — it comes from the box — but as a runtime `bool` it keeps a
/// branch inside the innermost pair loop, and that alone stops auto-vectorisation: the
/// emitted code for the O(N^2) kernels contained no packed `sqrtpd` at all. Monomorphising
/// on it hoists the branch out of the loop and lets the body be vectorised. Callers select
/// once per box with `if ortho { f::<true>(..) } else { f::<false>(..) }`.
///
/// Bit-for-bit identical to [`mic_vector`]; only the branch placement changes.
#[inline(always)]
pub(crate) fn mic_vector_const<const ORTHO: bool>(v: [f64; 3], cell: &Mat3, inv: &Mat3) -> [f64; 3] {
    if ORTHO {
        mic_vector_ortho(v, cell)
    } else {
        wrap_to_mic_vector_reduced(v, cell, inv)
    }
}

/// Minimum-image distance via the reduced cell (norm of [`wrap_to_mic_vector_reduced`]).
#[cfg(test)]
#[inline]
pub(crate) fn mic_distance_reduced(p1: [f64; 3], p2: [f64; 3], red: &Mat3, inv: &Mat3) -> f64 {
    let v = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]];
    let w = wrap_to_mic_vector_reduced(v, red, inv);
    (w[0] * w[0] + w[1] * w[1] + w[2] * w[2]).sqrt()
}

/// Per-box precompute: orthogonal flag, the cell to wrap in (the box itself when
/// orthogonal, its reduced form when triclinic), and the reduced cell's general inverse.
#[inline]
pub(crate) fn prep_dist(b: &Mat3) -> (bool, Mat3, Mat3) {
    if box_is_orthogonal(b) {
        (true, *b, [[0.0; 3]; 3])
    } else {
        let (red, inv) = prep_reduced(b);
        (false, red, inv)
    }
}

/// MIC distance through the unified [`mic_vector`] mechanism.
#[inline(always)]
fn mic_distance_auto(p1: [f64; 3], p2: [f64; 3], cell: &Mat3, inv: &Mat3, ortho: bool) -> f64 {
    let v = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]];
    let w = mic_vector(v, cell, inv, ortho);
    (w[0] * w[0] + w[1] * w[1] + w[2] * w[2]).sqrt()
}

/// Fill the strict **upper** triangle of the `na x na` row-major `slab` with the
/// minimum-image distances of the `na` atoms in the flat `cst` (`[x, y, z]` per atom).
/// The lower triangle is left to [`crate::symmetric::mirror_upper_to_lower`].
///
/// `ORTHO` is a const parameter, not a runtime flag: see [`mic_vector_const`].
#[inline(always)]
fn fill_mic_upper<const ORTHO: bool>(cst: &[f64], na: usize, slab: &mut [f64], cell: &Mat3, inv: &Mat3) {
    for j in 0..na {
        let p1 = [cst[3 * j], cst[3 * j + 1], cst[3 * j + 2]];
        let row = &mut slab[j * na..(j + 1) * na];
        for k in (j + 1)..na {
            let v = [cst[3 * k] - p1[0], cst[3 * k + 1] - p1[1], cst[3 * k + 2] - p1[2]];
            let w = mic_vector_const::<ORTHO>(v, cell, inv);
            row[k] = (w[0] * w[0] + w[1] * w[1] + w[2] * w[2]).sqrt();
        }
    }
}

/// Fill **both** triangles as each pair is computed, storing the mirror element directly.
/// Same results as [`fill_mic_upper`] plus the mirror pass; only the store pattern differs.
#[inline(always)]
fn fill_mic_both<const ORTHO: bool>(cst: &[f64], na: usize, slab: &mut [f64], cell: &Mat3, inv: &Mat3) {
    for j in 0..na {
        let p1 = [cst[3 * j], cst[3 * j + 1], cst[3 * j + 2]];
        for k in (j + 1)..na {
            let v = [cst[3 * k] - p1[0], cst[3 * k + 1] - p1[1], cst[3 * k + 2] - p1[2]];
            let w = mic_vector_const::<ORTHO>(v, cell, inv);
            let d = (w[0] * w[0] + w[1] * w[1] + w[2] * w[2]).sqrt();
            slab[j * na + k] = d;
            slab[k * na + j] = d;
        }
    }
}

/// The whole symmetric MIC distance matrix for one structure.
///
/// The two store strategies are kept because **which one wins depends on the box**, and the
/// two effects have opposite signs (measured, n = 4000, x86-64 baseline):
///
/// | | mirror store per pair | upper triangle + mirror pass |
/// |---|---|---|
/// | orthogonal | 230 ms | **201 ms** |
/// | triclinic | **388 ms** | 409 ms |
///
/// Deferring the mirror to [`crate::symmetric::mirror_upper_to_lower`] makes the pair loop's
/// stores unit-stride, which is worth ~15% when the per-pair arithmetic is cheap (the
/// orthogonal wrap is three centred floors; for the non-periodic matrix in `distances.rs`
/// it is worth 1.31x). But the mirror pass is a second sweep over the whole `na x na`
/// matrix, a fixed cost the triclinic path's much heavier 8-corner arithmetic does not
/// amortise. So: split the stores when the arithmetic is cheap, keep them interleaved when
/// it is not.
#[inline]
fn fill_mic_self(cst: &[f64], na: usize, slab: &mut [f64], cell: &Mat3, inv: &Mat3, ortho: bool) {
    if ortho {
        fill_mic_upper::<true>(cst, na, slab, cell, inv);
        mirror_upper_to_lower(slab, na);
    } else {
        fill_mic_both::<false>(cst, na, slab, cell, inv);
    }
}

pub(crate) fn box_at(b: &numpy::ndarray::ArrayView3<f64>, s: usize) -> Mat3 {
    [
        [b[[s, 0, 0]], b[[s, 0, 1]], b[[s, 0, 2]]],
        [b[[s, 1, 0]], b[[s, 1, 1]], b[[s, 1, 2]]],
        [b[[s, 2, 0]], b[[s, 2, 1]], b[[s, 2, 2]]],
    ]
}

pub(crate) fn box_2d(b: &numpy::ndarray::ArrayView2<f64>) -> Mat3 {
    [
        [b[[0, 0]], b[[0, 1]], b[[0, 2]]],
        [b[[1, 0]], b[[1, 1]], b[[1, 2]]],
        [b[[2, 0]], b[[2, 1]], b[[2, 2]]],
    ]
}

#[inline]
#[cfg(test)]
pub(crate) fn prep(b: &Mat3) -> (bool, Mat3) {
    let ortho = box_is_orthogonal(b);
    let inv = if ortho { [[0.0; 3]; 3] } else { inverse_matrix_3x3(b) };
    (ortho, inv)
}

// --------------------------------------------------------------------------- multi

#[pyfunction]
pub fn get_mic_distances_single_system<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    boxes: PyReadonlyArray3<'py, f64>,
) -> Bound<'py, PyArray3<f64>> {
    let c = coordinates.as_array();
    let b = boxes.as_array();
    let ns = c.shape()[0];
    let na = c.shape()[1];
    // Read the coordinates through a flat slice: `c[[s, k, 0]]` recomputes strides and
    // bounds-checks on every access, which by itself stops the pair loop vectorising.
    // `as_standard_layout` borrows when the input is already C-contiguous (the norm).
    let cc = c.as_standard_layout();
    let cs = cc.as_slice().expect("standard layout is contiguous");
    let mut flat = vec![0.0f64; ns * na * na];
    for s in 0..ns {
        let bs = box_at(&b, s);
        let (ortho, bs_red, inv) = prep_dist(&bs);
        let cst = &cs[s * na * 3..(s + 1) * na * 3];
        let slab = &mut flat[s * na * na..(s + 1) * na * na];
        fill_mic_self(cst, na, slab, &bs_red, &inv, ortho);
    }
    Array3::from_shape_vec((ns, na, na), flat).unwrap().into_pyarray(py)
}

#[pyfunction]
pub fn get_mic_distances<'py>(
    py: Python<'py>,
    coordinates1: PyReadonlyArray3<'py, f64>,
    coordinates2: PyReadonlyArray3<'py, f64>,
    boxes: PyReadonlyArray3<'py, f64>,
) -> Bound<'py, PyArray3<f64>> {
    let c1 = coordinates1.as_array();
    let c2 = coordinates2.as_array();
    let b = boxes.as_array();
    let ns = c1.shape()[0];
    let na1 = c1.shape()[1];
    let na2 = c2.shape()[1];
    let mut out = Array3::<f64>::zeros((ns, na1, na2));
    for s in 0..ns {
        let bs = box_at(&b, s);
        let (ortho, bs_red, inv) = prep_dist(&bs);
        for j in 0..na1 {
            let p1 = [c1[[s, j, 0]], c1[[s, j, 1]], c1[[s, j, 2]]];
            for k in 0..na2 {
                let p2 = [c2[[s, k, 0]], c2[[s, k, 1]], c2[[s, k, 2]]];
                out[[s, j, k]] = mic_distance_auto(p1, p2, &bs_red, &inv, ortho);
            }
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_mic_distances_pairs<'py>(
    py: Python<'py>,
    coordinates1: PyReadonlyArray3<'py, f64>,
    coordinates2: PyReadonlyArray3<'py, f64>,
    boxes: PyReadonlyArray3<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let c1 = coordinates1.as_array();
    let c2 = coordinates2.as_array();
    let b = boxes.as_array();
    let ns = c1.shape()[0];
    let na = c1.shape()[1];
    let mut out = Array2::<f64>::zeros((ns, na));
    for s in 0..ns {
        let bs = box_at(&b, s);
        let (ortho, bs_red, inv) = prep_dist(&bs);
        for j in 0..na {
            let p1 = [c1[[s, j, 0]], c1[[s, j, 1]], c1[[s, j, 2]]];
            let p2 = [c2[[s, j, 0]], c2[[s, j, 1]], c2[[s, j, 2]]];
            out[[s, j]] = mic_distance_auto(p1, p2, &bs_red, &inv, ortho);
        }
    }
    out.into_pyarray(py)
}

// --------------------------------------------------------------------------- single structure

#[pyfunction]
pub fn get_mic_distances_single_system_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    boxes: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let bs = box_2d(&boxes.as_array());
    let (ortho, bs_red, inv) = prep_dist(&bs);
    let na = c.shape()[0];
    let cc = c.as_standard_layout();
    let cs = cc.as_slice().expect("standard layout is contiguous");
    let mut flat = vec![0.0f64; na * na];
    fill_mic_self(cs, na, &mut flat, &bs_red, &inv, ortho);
    Array2::from_shape_vec((na, na), flat).unwrap().into_pyarray(py)
}

#[pyfunction]
pub fn get_mic_distances_single_structure<'py>(
    py: Python<'py>,
    coordinates1: PyReadonlyArray2<'py, f64>,
    coordinates2: PyReadonlyArray2<'py, f64>,
    boxes: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let c1 = coordinates1.as_array();
    let c2 = coordinates2.as_array();
    let bs = box_2d(&boxes.as_array());
    let (ortho, bs_red, inv) = prep_dist(&bs);
    let na1 = c1.shape()[0];
    let na2 = c2.shape()[0];
    let mut out = Array2::<f64>::zeros((na1, na2));
    for j in 0..na1 {
        let p1 = [c1[[j, 0]], c1[[j, 1]], c1[[j, 2]]];
        for k in 0..na2 {
            let p2 = [c2[[k, 0]], c2[[k, 1]], c2[[k, 2]]];
            out[[j, k]] = mic_distance_auto(p1, p2, &bs_red, &inv, ortho);
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_mic_distances_pairs_single_structure<'py>(
    py: Python<'py>,
    coordinates1: PyReadonlyArray2<'py, f64>,
    coordinates2: PyReadonlyArray2<'py, f64>,
    boxes: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let c1 = coordinates1.as_array();
    let c2 = coordinates2.as_array();
    let bs = box_2d(&boxes.as_array());
    let (ortho, bs_red, inv) = prep_dist(&bs);
    let na = c1.shape()[0];
    let mut out = Array1::<f64>::zeros(na);
    for j in 0..na {
        let p1 = [c1[[j, 0]], c1[[j, 1]], c1[[j, 2]]];
        let p2 = [c2[[j, 0]], c2[[j, 1]], c2[[j, 2]]];
        out[j] = mic_distance_auto(p1, p2, &bs_red, &inv, ortho);
    }
    out.into_pyarray(py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_mic_distances_single_system, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_distances, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_distances_pairs, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_distances_single_system_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_distances_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_distances_pairs_single_structure, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const ORTHO: Mat3 = [[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]];
    const TRIC: Mat3 = [[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]];

    #[test]
    fn orthogonality_detection() {
        assert!(box_is_orthogonal(&ORTHO));
        assert!(!box_is_orthogonal(&TRIC));
    }

    /// Reference minimum image by a wide exhaustive search (±2 shell around the fractional
    /// wrap), stronger than the production ±1 oracle — a ground truth for the reduced path.
    fn brute_min_image_distance(v: [f64; 3], b: &Mat3) -> f64 {
        let inv = crate::mathlib::inverse_matrix_3x3_full(b);
        let s = [
            inv[0][0] * v[0] + inv[1][0] * v[1] + inv[2][0] * v[2],
            inv[0][1] * v[0] + inv[1][1] * v[1] + inv[2][1] * v[2],
            inv[0][2] * v[0] + inv[1][2] * v[1] + inv[2][2] * v[2],
        ];
        let base = [s[0].round(), s[1].round(), s[2].round()];
        let mut dmin = f64::INFINITY;
        for i in -2..=2 {
            for j in -2..=2 {
                for k in -2..=2 {
                    let n = [base[0] + i as f64, base[1] + j as f64, base[2] + k as f64];
                    let ds = [s[0] - n[0], s[1] - n[1], s[2] - n[2]];
                    let r = [
                        b[0][0] * ds[0] + b[1][0] * ds[1] + b[2][0] * ds[2],
                        b[0][1] * ds[0] + b[1][1] * ds[1] + b[2][1] * ds[2],
                        b[0][2] * ds[0] + b[1][2] * ds[1] + b[2][2] * ds[2],
                    ];
                    let dd = r[0] * r[0] + r[1] * r[1] + r[2] * r[2];
                    if dd < dmin {
                        dmin = dd;
                    }
                }
            }
        }
        dmin.sqrt()
    }

    #[test]
    fn reduce_cell_preserves_the_lattice_volume() {
        let det = |m: &Mat3| {
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        };
        for b in [TRIC, [[6.0, 0.0, 0.0], [4.0, 6.0, 0.0], [3.5, 3.0, 6.0]]] {
            let red = reduce_cell(&b);
            // a lattice-preserving basis change has determinant of the same magnitude
            assert!((det(&red).abs() - det(&b).abs()).abs() < 1e-9, "volume changed");
        }
    }

    /// The reduced-cell 8-corner distance must equal the ground-truth minimum image, over
    /// random skewed boxes and vectors many box lengths out — the case the unreduced ±1
    /// search gets wrong.
    #[test]
    fn reduced_mic_matches_the_ground_truth_minimum_image() {
        let mut seed = 88172645463325252u64;
        let mut rng = || {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            (seed >> 11) as f64 / (1u64 << 53) as f64
        };
        let mut worst = 0.0f64;
        for _ in 0..5000 {
            // random lower-triangular-ish box with strong tilt
            let b: Mat3 = [
                [4.0 + 4.0 * rng(), 0.0, 0.0],
                [8.0 * rng() - 4.0, 4.0 + 4.0 * rng(), 0.0],
                [8.0 * rng() - 4.0, 8.0 * rng() - 4.0, 4.0 + 4.0 * rng()],
            ];
            let (red, inv) = prep_reduced(&b);
            let v = [40.0 * rng() - 20.0, 40.0 * rng() - 20.0, 40.0 * rng() - 20.0];
            let got = mic_distance_reduced([0.0, 0.0, 0.0], v, &red, &inv);
            let truth = brute_min_image_distance(v, &b);
            worst = worst.max((got - truth).abs());
        }
        assert!(worst < 1e-9, "reduced MIC deviates from ground truth by {worst:.2e}");
    }

    /// Against the production exhaustive oracle, two things must hold: on mildly tilted
    /// boxes (where the ±1 oracle is itself correct) they agree; and on *any* box the
    /// reduced path is never longer than the oracle — it can only find an image the ±1
    /// search missed, never a worse one. The second half is the correctness fix in action.
    #[test]
    fn reduced_mic_agrees_on_mild_boxes_and_is_never_worse_on_skewed_ones() {
        let mut seed = 12345u64;
        let mut rng = || {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
            (seed >> 11) as f64 / (1u64 << 53) as f64
        };
        let mut fixed_the_oracle = 0;
        for _ in 0..3000 {
            let mild = rng() < 0.5;
            // mild: tilt <= 1.0 (ratio 1/6, ±1 oracle valid); skewed: tilt up to 3.0
            let tmax = if mild { 1.0 } else { 3.0 };
            let t = |r: f64| tmax * (2.0 * r - 1.0);
            let b: Mat3 = [
                [6.0, 0.0, 0.0],
                [t(rng()), 6.0, 0.0],
                [t(rng()), t(rng()), 6.0],
            ];
            let (ortho, inv) = prep(&b);
            let (red, invr) = prep_reduced(&b);
            let p1 = [6.0 * rng(), 6.0 * rng(), 6.0 * rng()];
            let p2 = [6.0 * rng(), 6.0 * rng(), 6.0 * rng()];
            let oracle = mic_distance(p1, p2, &b, &inv, ortho);
            let fast = mic_distance_reduced(p1, p2, &red, &invr);
            if mild {
                assert!((oracle - fast).abs() < 1e-9,
                        "mild box: oracle {oracle} vs reduced {fast}");
            } else {
                assert!(fast <= oracle + 1e-9, "reduced longer than oracle: {fast} > {oracle}");
                if fast < oracle - 1e-9 {
                    fixed_the_oracle += 1;
                }
            }
        }
        assert!(fixed_the_oracle > 0,
                "expected the reduced path to beat the ±1 oracle on some skewed boxes");
    }

    #[test]
    fn lower_triangular_inverse_is_a_left_inverse() {
        let inv = inverse_matrix_3x3(&TRIC);
        // The molsysmt convention stores the box lower-triangular; inv * m must be I
        // for the lower-triangular part it is defined on.
        for i in 0..3 {
            let mut acc = 0.0;
            for k in 0..3 {
                acc += inv[i][k] * TRIC[k][i];
            }
            assert!((acc - 1.0).abs() < 1e-12, "diagonal {i} = {acc}");
        }
    }

    #[test]
    fn orthogonal_wrap_returns_the_short_image() {
        let (_, inv) = prep(&ORTHO);
        // A displacement longer than half the box must wrap to the short image.
        let w = wrap_to_mic_vector([5.0, 0.0, 0.0], &ORTHO, &inv, true);
        assert!((w[0] - (-1.0)).abs() < 1e-12, "got {:?}", w);
        // Anything already shorter than L/2 is unchanged.
        let w2 = wrap_to_mic_vector([1.0, -2.0, 0.5], &ORTHO, &inv, true);
        assert!((w2[0] - 1.0).abs() < 1e-12 && (w2[1] + 2.0).abs() < 1e-12);
    }

    #[test]
    fn triclinic_wrap_never_lengthens_the_vector() {
        let (ortho, inv) = prep(&TRIC);
        assert!(!ortho);
        for v in [[5.5, 0.2, 0.1], [0.3, 5.9, -0.4], [-4.8, 2.0, 5.5]] {
            let w = wrap_to_mic_vector(v, &TRIC, &inv, false);
            let n_in = v[0] * v[0] + v[1] * v[1] + v[2] * v[2];
            let n_out = w[0] * w[0] + w[1] * w[1] + w[2] * w[2];
            assert!(n_out <= n_in + 1e-12, "v={v:?} -> w={w:?}");
        }
    }

    #[test]
    fn distance_of_a_point_to_itself_is_zero() {
        let (ortho, inv) = prep(&ORTHO);
        let p = [1.0, 2.0, 3.0];
        assert_eq!(mic_distance(p, p, &ORTHO, &inv, ortho), 0.0);
    }
}
