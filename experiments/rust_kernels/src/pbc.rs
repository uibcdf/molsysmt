//! Block 9 — the `molsysmt.lib.pbc` package: box geometry and the wrap/unwrap family.
//!
//! Ports `box_is_orthogonal`, `get_lengths_from_box`, `get_angles_from_box`,
//! `get_lengths_and_angles_from_box`, `get_box_from_lengths_and_angles`, `wrap_to_pbc`,
//! `wrap_to_pbc_center`, `wrap_to_mic` and `unwrap`.
//!
//! Two details are load-bearing for parity:
//!
//! 1. **`round` is round-half-to-even.** `unwrap` uses Python's `round`, which Numba
//!    implements with Python semantics (verified: 0.5 -> 0, 1.5 -> 2, 2.5 -> 2). Rust's
//!    `f64::round` rounds half *away from zero*, so this module uses `round_ties_even`.
//!    Getting this wrong would displace an atom by a full box length on exact ties.
//! 2. **Accumulation order in the 27-image searches.** The triclinic MIC paths build each
//!    candidate as `((v + i*b0) + j*b1) + k*b2`; folding those differently changes the
//!    last bits, so the stepwise structure is preserved.
//!
//! Parity status for this block is *not* uniform, and the reasons are worth separating:
//!
//! - **Orthogonal boxes: bit-for-bit.** Every kernel matches the Numba oracle exactly.
//! - **Triclinic boxes: 1e-12 tolerance, and the oracle is the reason.** `lazy_njit` sets
//!   `fastmath=True`, which lets LLVM contract the three-term dot products of the
//!   fractional wrap into FMAs. Rust does not fuse by default, so the last bits differ on
//!   738/2000 sampled vectors (max 6.2e-15). This is *not* a port defect: compiling the
//!   same kernel with `fastmath=False` makes Rust and Numba agree on 2000/2000. It is a
//!   property of the oracle, so it cannot be fixed on this side — only matched by
//!   guessing LLVM's contraction choices, which would be brittle.
//! - **`wrap_to_mic` on triclinic boxes: deliberately corrected**, see `wrap_mic_vec`.
//!   Upstream does not return the minimum image there; parity would mean copying that.
//!
//! Note that this package's orthogonality test is a *fourth*, independent implementation
//! of the predicate discussed in `sasa.rs`: it compares dot products between box vectors
//! against 1e-4, which is basis-independent, rather than testing off-diagonal elements
//! against 1e-10. It is the most robust of the four and it is correct, so it is ported
//! as-is; the divergence between the four is reported in
//! `devguide/pending_bugs/sasa_is_orthogonal_typo.md`.

use numpy::ndarray::{Array1, Array2, Array3, ArrayView3};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyArray3, PyReadonlyArray1, PyReadonlyArray2,
            PyReadonlyArray3, PyReadwriteArray3};
use pyo3::prelude::*;

use crate::mathlib::{dot_product, inverse_matrix_3x3, norm_vector, Mat3, Vec3};

#[inline]
fn box_at(b: &ArrayView3<f64>, s: usize) -> Mat3 {
    [
        [b[[s, 0, 0]], b[[s, 0, 1]], b[[s, 0, 2]]],
        [b[[s, 1, 0]], b[[s, 1, 1]], b[[s, 1, 2]]],
        [b[[s, 2, 0]], b[[s, 2, 1]], b[[s, 2, 2]]],
    ]
}

#[inline]
fn mat_of(m: &numpy::ndarray::ArrayView2<f64>) -> Mat3 {
    [
        [m[[0, 0]], m[[0, 1]], m[[0, 2]]],
        [m[[1, 0]], m[[1, 1]], m[[1, 2]]],
        [m[[2, 0]], m[[2, 1]], m[[2, 2]]],
    ]
}

/// Mirrors `box_is_orthogonal.py`: pairwise dot products of the box vectors.
#[inline]
pub(crate) fn box_is_orthogonal_one(b: &Mat3) -> bool {
    dot_product(b[0], b[1]).abs() <= 0.0001
        && dot_product(b[0], b[2]).abs() <= 0.0001
        && dot_product(b[1], b[2]).abs() <= 0.0001
}

// ------------------------------------------------------------------ box geometry

#[inline]
fn lengths_of(b: &Mat3) -> Vec3 {
    [norm_vector(b[0]), norm_vector(b[1]), norm_vector(b[2])]
}

/// Mirrors `get_angles_from_box.py`. No clamping of the `acos` argument — a degenerate
/// box (parallel vectors) can push the ratio just past 1.0 and yield NaN, exactly as
/// upstream does.
#[inline]
fn angles_of(b: &Mat3) -> Vec3 {
    let (x, y, z) = (norm_vector(b[0]), norm_vector(b[1]), norm_vector(b[2]));
    [
        (dot_product(b[1], b[2]) / (y * z)).acos(),
        (dot_product(b[2], b[0]) / (x * z)).acos(),
        (dot_product(b[1], b[0]) / (x * y)).acos(),
    ]
}

#[inline]
fn box_of(lengths: Vec3, angles: Vec3) -> Mat3 {
    let (alpha, beta, gamm) = (angles[0], angles[1], angles[2]);
    let (x, y, z) = (lengths[0], lengths[1], lengths[2]);
    let mut b = [[0.0f64; 3]; 3];
    b[0][0] = x;
    b[1][0] = y * gamm.cos();
    b[1][1] = y * gamm.sin();
    b[2][0] = z * beta.cos();
    b[2][1] = z * (alpha.cos() - beta.cos() * gamm.cos()) / gamm.sin();
    b[2][2] = (z * z - b[2][0].powi(2) - b[2][1].powi(2)).sqrt();
    b
}

// ------------------------------------------------------------------ wrapping

/// Wrap into the primitive cell. `half` is 0.0 for the origin-based variant and 0.5 for
/// the centre-based one, which is the only difference between the two upstream kernels.
#[inline]
fn wrap_pbc_vec(v: Vec3, b: &Mat3, inv: &Mat3, orthogonal: bool, half: f64) -> Vec3 {
    if orthogonal {
        [
            v[0] - b[0][0] * (v[0] / b[0][0] + half).floor(),
            v[1] - b[1][1] * (v[1] / b[1][1] + half).floor(),
            v[2] - b[2][2] * (v[2] / b[2][2] + half).floor(),
        ]
    } else {
        let mut s = [
            inv[0][0] * v[0] + inv[1][0] * v[1] + inv[2][0] * v[2],
            inv[1][1] * v[1] + inv[2][1] * v[2],
            inv[2][2] * v[2],
        ];
        s[0] -= (s[0] + half).floor();
        s[1] -= (s[1] + half).floor();
        s[2] -= (s[2] + half).floor();
        [
            b[0][0] * s[0] + b[1][0] * s[1] + b[2][0] * s[2],
            b[1][1] * s[1] + b[2][1] * s[2],
            b[2][2] * s[2],
        ]
    }
}

/// Exhaustive search over the 27 neighbouring images, keeping the shortest. Shared by
/// `wrap_to_mic` and `unwrap`'s triclinic branch. `seed`/`dmin` carry the incumbent so
/// the caller's fractional wrap stays in the running, and the accumulation order matches
/// upstream (`((v + i*b0) + j*b1) + k*b2`).
#[inline]
fn shortest_image(v: Vec3, b: &Mat3, seed: Vec3, dmin_in: f64) -> Vec3 {
    let mut best = seed;
    let mut dmin = dmin_in;
    for i in [-1.0f64, 0.0, 1.0] {
        let a = [v[0] + i * b[0][0], v[1] + i * b[0][1], v[2] + i * b[0][2]];
        for j in [-1.0f64, 0.0, 1.0] {
            let c = [a[0] + j * b[1][0], a[1] + j * b[1][1], a[2] + j * b[1][2]];
            for k in [-1.0f64, 0.0, 1.0] {
                let d = [c[0] + k * b[2][0], c[1] + k * b[2][1], c[2] + k * b[2][2]];
                let dd = dot_product(d, d);
                if dmin > dd {
                    best = d;
                    dmin = dd;
                }
            }
        }
    }
    best
}

/// Mirrors `wrap_to_mic.py`, with one **deliberate correction** on the triclinic branch.
///
/// Upstream wraps to the [0,1) fractional cell and then searches the 27 images *of the
/// original vector*. When the input lies several box lengths outside the cell, none of
/// those 27 images is near the origin, so the corner-cell wrap wins by default — and the
/// primitive cell is not the minimum image. Measured on a triclinic box with inputs up to
/// 20 units out: upstream returns the minimum image in only 55/300 cases, while its own
/// orthogonal branch is always correct.
///
/// Searching around the *wrapped* candidate instead fixes it (300/300), and it is what
/// `unwrap.py` already does on its triclinic branch — which is what identifies this as a
/// defect rather than a design choice. Reported in
/// `devguide/pending_bugs/wrap_to_mic_triclinic_not_minimum_image.md`.
///
/// Note the ±1 shell is only exhaustive for reasonably conditioned cells; a strongly
/// skewed box needs a reduced (Niggli) cell for a general guarantee. That limitation is
/// upstream's too and is not addressed here.
#[inline]
fn wrap_mic_vec(v: Vec3, b: &Mat3, inv: &Mat3, orthogonal: bool) -> Vec3 {
    if orthogonal {
        return wrap_pbc_vec(v, b, inv, true, 0.5);
    }
    let wrapped = wrap_pbc_vec(v, b, inv, false, 0.0);
    shortest_image(wrapped, b, wrapped, dot_product(wrapped, wrapped))
}

/// Per-structure driver shared by the three whole-system wrap kernels.
fn wrap_all(
    coordinates: &mut numpy::ndarray::ArrayViewMut3<f64>,
    boxes: &ArrayView3<f64>,
    origin: Vec3,
    kind: WrapKind,
) {
    let (n_structures, n_atoms) = (coordinates.shape()[0], coordinates.shape()[1]);
    for s in 0..n_structures {
        let b = box_at(boxes, s);
        let orthogonal = box_is_orthogonal_one(&b);
        let inv = if orthogonal { [[0.0; 3]; 3] } else { inverse_matrix_3x3(&b) };
        for a in 0..n_atoms {
            let v = [
                coordinates[[s, a, 0]] - origin[0],
                coordinates[[s, a, 1]] - origin[1],
                coordinates[[s, a, 2]] - origin[2],
            ];
            let w = match kind {
                WrapKind::Pbc => wrap_pbc_vec(v, &b, &inv, orthogonal, 0.0),
                WrapKind::PbcCenter => wrap_pbc_vec(v, &b, &inv, orthogonal, 0.5),
                WrapKind::Mic => wrap_mic_vec(v, &b, &inv, orthogonal),
            };
            for k in 0..3 {
                coordinates[[s, a, k]] = w[k] + origin[k];
            }
        }
    }
}

#[derive(Clone, Copy)]
enum WrapKind {
    Pbc,
    PbcCenter,
    Mic,
}

// ------------------------------------------------------------------ python surface

#[pyfunction]
pub fn box_is_orthogonal_single_structure(b: PyReadonlyArray2<'_, f64>) -> bool {
    box_is_orthogonal_one(&mat_of(&b.as_array()))
}

#[pyfunction]
pub fn box_is_orthogonal<'py>(py: Python<'py>, boxes: PyReadonlyArray3<'py, f64>)
    -> Bound<'py, numpy::PyArray1<bool>> {
    let b = boxes.as_array();
    let out: Vec<bool> = (0..b.shape()[0]).map(|s| box_is_orthogonal_one(&box_at(&b, s))).collect();
    Array1::from_vec(out).into_pyarray(py)
}

#[pyfunction]
pub fn get_lengths_from_box_single_structure<'py>(py: Python<'py>, b: PyReadonlyArray2<'py, f64>)
    -> Bound<'py, PyArray1<f64>> {
    Array1::from_vec(lengths_of(&mat_of(&b.as_array())).to_vec()).into_pyarray(py)
}

#[pyfunction]
pub fn get_lengths_from_box<'py>(py: Python<'py>, boxes: PyReadonlyArray3<'py, f64>)
    -> Bound<'py, PyArray2<f64>> {
    let b = boxes.as_array();
    let n = b.shape()[0];
    let mut out = Array2::<f64>::zeros((n, 3));
    for s in 0..n {
        let l = lengths_of(&box_at(&b, s));
        for k in 0..3 { out[[s, k]] = l[k]; }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_angles_from_box_single_structure<'py>(py: Python<'py>, b: PyReadonlyArray2<'py, f64>)
    -> Bound<'py, PyArray1<f64>> {
    Array1::from_vec(angles_of(&mat_of(&b.as_array())).to_vec()).into_pyarray(py)
}

#[pyfunction]
pub fn get_angles_from_box<'py>(py: Python<'py>, boxes: PyReadonlyArray3<'py, f64>)
    -> Bound<'py, PyArray2<f64>> {
    let b = boxes.as_array();
    let n = b.shape()[0];
    let mut out = Array2::<f64>::zeros((n, 3));
    for s in 0..n {
        let a = angles_of(&box_at(&b, s));
        for k in 0..3 { out[[s, k]] = a[k]; }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_lengths_and_angles_from_box_single_structure<'py>(
    py: Python<'py>,
    b: PyReadonlyArray2<'py, f64>,
) -> (Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>) {
    let m = mat_of(&b.as_array());
    (
        Array1::from_vec(lengths_of(&m).to_vec()).into_pyarray(py),
        Array1::from_vec(angles_of(&m).to_vec()).into_pyarray(py),
    )
}

#[pyfunction]
pub fn get_lengths_and_angles_from_box<'py>(
    py: Python<'py>,
    boxes: PyReadonlyArray3<'py, f64>,
) -> (Bound<'py, PyArray2<f64>>, Bound<'py, PyArray2<f64>>) {
    let b = boxes.as_array();
    let n = b.shape()[0];
    let (mut lo, mut ao) = (Array2::<f64>::zeros((n, 3)), Array2::<f64>::zeros((n, 3)));
    for s in 0..n {
        let m = box_at(&b, s);
        let (l, a) = (lengths_of(&m), angles_of(&m));
        for k in 0..3 {
            lo[[s, k]] = l[k];
            ao[[s, k]] = a[k];
        }
    }
    (lo.into_pyarray(py), ao.into_pyarray(py))
}

#[pyfunction]
pub fn get_box_from_lengths_and_angles_single_structure<'py>(
    py: Python<'py>,
    lengths: PyReadonlyArray1<'py, f64>,
    angles: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let (l, a) = (lengths.as_array(), angles.as_array());
    let b = box_of([l[0], l[1], l[2]], [a[0], a[1], a[2]]);
    let mut out = Array2::<f64>::zeros((3, 3));
    for i in 0..3 { for j in 0..3 { out[[i, j]] = b[i][j]; } }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_box_from_lengths_and_angles<'py>(
    py: Python<'py>,
    lengths: PyReadonlyArray2<'py, f64>,
    angles: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray3<f64>> {
    let (l, a) = (lengths.as_array(), angles.as_array());
    let n = l.shape()[0];
    let mut out = Array3::<f64>::zeros((n, 3, 3));
    for s in 0..n {
        let b = box_of([l[[s, 0]], l[[s, 1]], l[[s, 2]]], [a[[s, 0]], a[[s, 1]], a[[s, 2]]]);
        for i in 0..3 { for j in 0..3 { out[[s, i, j]] = b[i][j]; } }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn wrap_to_pbc(
    mut coordinates: PyReadwriteArray3<'_, f64>,
    boxes: PyReadonlyArray3<'_, f64>,
    box_origin: PyReadonlyArray1<'_, f64>,
) {
    let o = box_origin.as_array();
    wrap_all(&mut coordinates.as_array_mut(), &boxes.as_array(), [o[0], o[1], o[2]], WrapKind::Pbc);
}

#[pyfunction]
pub fn wrap_to_pbc_center(
    mut coordinates: PyReadwriteArray3<'_, f64>,
    boxes: PyReadonlyArray3<'_, f64>,
    box_center: PyReadonlyArray1<'_, f64>,
) {
    let o = box_center.as_array();
    wrap_all(&mut coordinates.as_array_mut(), &boxes.as_array(), [o[0], o[1], o[2]],
             WrapKind::PbcCenter);
}

#[pyfunction]
pub fn wrap_to_mic(
    mut coordinates: PyReadwriteArray3<'_, f64>,
    boxes: PyReadonlyArray3<'_, f64>,
    mic_origin: PyReadonlyArray1<'_, f64>,
) {
    let o = mic_origin.as_array();
    wrap_all(&mut coordinates.as_array_mut(), &boxes.as_array(), [o[0], o[1], o[2]], WrapKind::Mic);
}

#[pyfunction]
pub fn wrap_to_pbc_vector_single_structure<'py>(
    py: Python<'py>,
    vector: PyReadonlyArray1<'py, f64>,
    b: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let v = vector.as_array();
    let m = mat_of(&b.as_array());
    let ortho = box_is_orthogonal_one(&m);
    let inv = if ortho { [[0.0; 3]; 3] } else { inverse_matrix_3x3(&m) };
    let w = wrap_pbc_vec([v[0], v[1], v[2]], &m, &inv, ortho, 0.0);
    Array1::from_vec(w.to_vec()).into_pyarray(py)
}

#[pyfunction]
pub fn wrap_to_pbc_center_vector_single_structure<'py>(
    py: Python<'py>,
    vector: PyReadonlyArray1<'py, f64>,
    b: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let v = vector.as_array();
    let m = mat_of(&b.as_array());
    let ortho = box_is_orthogonal_one(&m);
    let inv = if ortho { [[0.0; 3]; 3] } else { inverse_matrix_3x3(&m) };
    let w = wrap_pbc_vec([v[0], v[1], v[2]], &m, &inv, ortho, 0.5);
    Array1::from_vec(w.to_vec()).into_pyarray(py)
}

#[pyfunction]
pub fn wrap_to_mic_vector_single_structure<'py>(
    py: Python<'py>,
    vector: PyReadonlyArray1<'py, f64>,
    b: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let v = vector.as_array();
    let m = mat_of(&b.as_array());
    let ortho = box_is_orthogonal_one(&m);
    let inv = if ortho { [[0.0; 3]; 3] } else { inverse_matrix_3x3(&m) };
    let w = wrap_mic_vec([v[0], v[1], v[2]], &m, &inv, ortho);
    Array1::from_vec(w.to_vec()).into_pyarray(py)
}

/// Mirrors `unwrap.py`. Deliberately serial: structure `s+1` is written from the already
/// updated structure `s`, so the loop carries a dependency and cannot be parallelised.
/// Orthogonality is decided once from structure 0 and applied to all, as upstream does.
#[pyfunction]
pub fn unwrap(mut coordinates: PyReadwriteArray3<'_, f64>, boxes: PyReadonlyArray3<'_, f64>) {
    let b = boxes.as_array();
    let mut c = coordinates.as_array_mut();
    let (n_structures, n_atoms) = (c.shape()[0], c.shape()[1]);
    if n_structures == 0 {
        return;
    }
    let orthogonal = box_is_orthogonal_one(&box_at(&b, 0));

    for s in 0..n_structures.saturating_sub(1) {
        let bs = box_at(&b, s);
        let inv = if orthogonal { [[0.0; 3]; 3] } else { inverse_matrix_3x3(&bs) };
        for a in 0..n_atoms {
            let prev = [c[[s, a, 0]], c[[s, a, 1]], c[[s, a, 2]]];
            let mut delta = [
                c[[s + 1, a, 0]] - prev[0],
                c[[s + 1, a, 1]] - prev[1],
                c[[s + 1, a, 2]] - prev[2],
            ];
            let shift = if orthogonal {
                // `round`, not `f64::round`: Python/Numba round half to even.
                for k in 0..3 {
                    delta[k] -= bs[k][k] * (delta[k] / bs[k][k]).round_ties_even();
                }
                delta
            } else {
                let mut f = [
                    inv[0][0] * delta[0] + inv[1][0] * delta[1] + inv[2][0] * delta[2],
                    inv[1][1] * delta[1] + inv[2][1] * delta[2],
                    inv[2][2] * delta[2],
                ];
                for k in 0..3 {
                    f[k] -= f[k].round_ties_even();
                }
                let wrapped = [
                    bs[0][0] * f[0] + bs[1][0] * f[1] + bs[2][0] * f[2],
                    bs[1][1] * f[1] + bs[2][1] * f[2],
                    bs[2][2] * f[2],
                ];
                shortest_image(wrapped, &bs, wrapped, dot_product(wrapped, wrapped))
            };
            for k in 0..3 {
                c[[s + 1, a, k]] = prev[k] + shift[k];
            }
        }
    }
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(box_is_orthogonal_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(box_is_orthogonal, m)?)?;
    m.add_function(wrap_pyfunction!(get_lengths_from_box_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_lengths_from_box, m)?)?;
    m.add_function(wrap_pyfunction!(get_angles_from_box_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_angles_from_box, m)?)?;
    m.add_function(wrap_pyfunction!(get_lengths_and_angles_from_box_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_lengths_and_angles_from_box, m)?)?;
    m.add_function(wrap_pyfunction!(get_box_from_lengths_and_angles_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_box_from_lengths_and_angles, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_pbc, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_pbc_center, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_mic, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_pbc_vector_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_pbc_center_vector_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_mic_vector_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(unwrap, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const ORTHO: Mat3 = [[6.0, 0.0, 0.0], [0.0, 7.0, 0.0], [0.0, 0.0, 8.0]];
    const TRIC: Mat3 = [[6.0, 0.0, 0.0], [1.5, 6.5, 0.0], [0.8, 1.1, 7.0]];

    #[test]
    fn orthogonality_uses_dot_products_not_off_diagonals() {
        assert!(box_is_orthogonal_one(&ORTHO));
        assert!(!box_is_orthogonal_one(&TRIC));
        // Basis-independent: a rotated cube is still orthogonal, which the off-diagonal
        // test used elsewhere in the library would reject.
        let c = std::f64::consts::FRAC_PI_4.cos();
        let s = std::f64::consts::FRAC_PI_4.sin();
        let rotated: Mat3 = [[6.0 * c, 6.0 * s, 0.0], [-7.0 * s, 7.0 * c, 0.0], [0.0, 0.0, 8.0]];
        assert!(box_is_orthogonal_one(&rotated));
    }

    #[test]
    fn lengths_and_angles_round_trip_through_the_box() {
        for b in [ORTHO, TRIC] {
            let (l, a) = (lengths_of(&b), angles_of(&b));
            let back = box_of(l, a);
            for i in 0..3 {
                for j in 0..3 {
                    assert!((back[i][j] - b[i][j]).abs() < 1e-12,
                            "round trip failed at [{i}][{j}]: {} vs {}", back[i][j], b[i][j]);
                }
            }
        }
    }

    #[test]
    fn a_cubic_box_has_right_angles() {
        let a = angles_of(&ORTHO);
        for v in a {
            assert!((v - std::f64::consts::FRAC_PI_2).abs() < 1e-15);
        }
    }

    #[test]
    fn wrap_to_pbc_lands_inside_the_cell_and_mic_is_centred() {
        let inv = inverse_matrix_3x3(&ORTHO);
        for v in [[13.7, -9.2, 20.1], [-0.001, 6.999, 8.0], [0.0, 0.0, 0.0]] {
            let w = wrap_pbc_vec(v, &ORTHO, &inv, true, 0.0);
            for k in 0..3 {
                assert!(w[k] >= 0.0 && w[k] < ORTHO[k][k], "{:?} -> {:?}", v, w);
            }
            let m = wrap_mic_vec(v, &ORTHO, &inv, true);
            for k in 0..3 {
                assert!(m[k].abs() <= ORTHO[k][k] / 2.0 + 1e-12, "{:?} -> {:?}", v, m);
            }
        }
    }

    /// The corrected triclinic MIC wrap really is the minimum image, even for inputs many
    /// box lengths outside the cell — the regime where upstream fails (see `wrap_mic_vec`).
    #[test]
    fn triclinic_mic_wrap_returns_the_minimum_image() {
        let inv = inverse_matrix_3x3(&TRIC);
        // deterministic spread, deliberately far outside the cell
        let mut seed = 12345u64;
        let mut next = || {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            ((seed >> 11) as f64 / (1u64 << 53) as f64) * 40.0 - 20.0
        };
        for _ in 0..200 {
            let v = [next(), next(), next()];
            let out = wrap_mic_vec(v, &TRIC, &inv, false);
            let d2 = dot_product(out, out);
            for i in [-1.0f64, 0.0, 1.0] {
                for j in [-1.0f64, 0.0, 1.0] {
                    for k in [-1.0f64, 0.0, 1.0] {
                        let c = [
                            out[0] + i * TRIC[0][0] + j * TRIC[1][0] + k * TRIC[2][0],
                            out[1] + i * TRIC[0][1] + j * TRIC[1][1] + k * TRIC[2][1],
                            out[2] + i * TRIC[0][2] + j * TRIC[1][2] + k * TRIC[2][2],
                        ];
                        assert!(dot_product(c, c) >= d2 - 1e-12,
                                "not the minimum image: {:?} -> {:?}", v, out);
                    }
                }
            }
            // and it must still be an image of the original vector
            let d = [out[0] - v[0], out[1] - v[1], out[2] - v[2]];
            let f = [
                inv[0][0] * d[0] + inv[1][0] * d[1] + inv[2][0] * d[2],
                inv[1][1] * d[1] + inv[2][1] * d[2],
                inv[2][2] * d[2],
            ];
            for k in 0..3 {
                assert!((f[k] - f[k].round_ties_even()).abs() < 1e-9,
                        "not an integer image: {:?}", f);
            }
        }
    }

    /// Pins the rounding mode `unwrap` depends on. `f64::round` would give 1.0 and 3.0
    /// here, displacing an atom by a whole box length on an exact tie.
    #[test]
    fn unwrap_rounds_half_to_even_like_python() {
        assert_eq!(0.5f64.round_ties_even(), 0.0);
        assert_eq!(1.5f64.round_ties_even(), 2.0);
        assert_eq!(2.5f64.round_ties_even(), 2.0);
        assert_eq!((-2.5f64).round_ties_even(), -2.0);
        assert_eq!(0.5f64.round(), 1.0, "the trap this test exists to prevent");
    }
}
