//! Box geometry and periodic wrapping over row-vector cell bases.
//!
//! Public geometric orthogonality remains basis-independent. Computational diagonal
//! fast paths require actual Cartesian axis alignment; other orientations use the
//! full inverse. Primary/centered-primary wrapping keeps the original primitive
//! basis, while MIC wrapping reuses the distance family's reduced-cell mechanism.
//!
//! Temporal unwrap uses the previous selected structure's actual cell at every
//! transition. Original-basis ties-to-even seeds survive unless a strictly shorter
//! MIC image exists. This retains the historical exact half-cell convention.
//!
//! Earlier Numba-port measurements and the former local 27-image search are
//! historical evidence in source history and the archived wrap-to-MIC report.
//! Current orientation and changing-cell corrections are tracked by #607/#606.

use numpy::ndarray::{Array1, Array2, Array3, ArrayView3};
use numpy::{
    IntoPyArray, PyArray1, PyArray2, PyArray3, PyReadonlyArray1, PyReadonlyArray2,
    PyReadonlyArray3, PyReadwriteArray3,
};
use pyo3::prelude::*;

use crate::mathlib::{
    dot_product, fast_floor, fast_round_ties_even, inverse_matrix_3x3_full, norm_vector, Mat3, Vec3,
};
use crate::mic::{box_is_axis_aligned, mic_vector, prep_dist};

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
/// the replaced Numba implementation did.
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
/// the centre-based one, which was the only difference between the two replaced Numba
/// kernels.
#[inline]
fn wrap_pbc_vec(v: Vec3, b: &Mat3, inv: &Mat3, axis_aligned: bool, half: f64) -> Vec3 {
    if axis_aligned {
        [
            v[0] - b[0][0] * fast_floor(v[0] / b[0][0] + half),
            v[1] - b[1][1] * fast_floor(v[1] / b[1][1] + half),
            v[2] - b[2][2] * fast_floor(v[2] / b[2][2] + half),
        ]
    } else {
        let mut s = fractional(v, inv);
        s[0] -= fast_floor(s[0] + half);
        s[1] -= fast_floor(s[1] + half);
        s[2] -= fast_floor(s[2] + half);
        cartesian(s, b)
    }
}

#[inline]
fn fractional(v: Vec3, inv: &Mat3) -> Vec3 {
    [
        inv[0][0] * v[0] + inv[1][0] * v[1] + inv[2][0] * v[2],
        inv[0][1] * v[0] + inv[1][1] * v[1] + inv[2][1] * v[2],
        inv[0][2] * v[0] + inv[1][2] * v[1] + inv[2][2] * v[2],
    ]
}

#[inline]
fn cartesian(s: Vec3, b: &Mat3) -> Vec3 {
    [
        b[0][0] * s[0] + b[1][0] * s[1] + b[2][0] * s[2],
        b[0][1] * s[0] + b[1][1] * s[1] + b[2][1] * s[2],
        b[0][2] * s[0] + b[1][2] * s[1] + b[2][2] * s[2],
    ]
}

/// Prepare the original primitive basis; reduction would change its cell boundaries.
fn prep_primary(b: &Mat3) -> (bool, Mat3, Mat3) {
    let aligned = box_is_axis_aligned(b);
    let inv = if aligned {
        [[0.0; 3]; 3]
    } else {
        inverse_matrix_3x3_full(b)
    };
    (aligned, *b, inv)
}

/// Reuse the production distance-family MIC primitive and its per-cell preparation.
/// This replaces the historical PBC-local 27-image search; original port evidence
/// remains in the archived wrap-to-MIC report and the source history.
#[inline]
fn wrap_mic_vec(v: Vec3, b: &Mat3, inv: &Mat3, axis_aligned: bool) -> Vec3 {
    mic_vector(v, b, inv, axis_aligned)
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
        let (axis_aligned, cell, inv) = match kind {
            WrapKind::Mic => prep_dist(&b),
            _ => prep_primary(&b),
        };
        for a in 0..n_atoms {
            let v = [
                coordinates[[s, a, 0]] - origin[0],
                coordinates[[s, a, 1]] - origin[1],
                coordinates[[s, a, 2]] - origin[2],
            ];
            let w = match kind {
                WrapKind::Pbc => wrap_pbc_vec(v, &cell, &inv, axis_aligned, 0.0),
                WrapKind::PbcCenter => wrap_pbc_vec(v, &cell, &inv, axis_aligned, 0.5),
                WrapKind::Mic => wrap_mic_vec(v, &cell, &inv, axis_aligned),
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
pub fn box_is_orthogonal<'py>(
    py: Python<'py>,
    boxes: PyReadonlyArray3<'py, f64>,
) -> Bound<'py, numpy::PyArray1<bool>> {
    let b = boxes.as_array();
    let out: Vec<bool> = (0..b.shape()[0])
        .map(|s| box_is_orthogonal_one(&box_at(&b, s)))
        .collect();
    Array1::from_vec(out).into_pyarray(py)
}

#[pyfunction]
pub fn get_lengths_from_box_single_structure<'py>(
    py: Python<'py>,
    b: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    Array1::from_vec(lengths_of(&mat_of(&b.as_array())).to_vec()).into_pyarray(py)
}

#[pyfunction]
pub fn get_lengths_from_box<'py>(
    py: Python<'py>,
    boxes: PyReadonlyArray3<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let b = boxes.as_array();
    let n = b.shape()[0];
    let mut out = Array2::<f64>::zeros((n, 3));
    for s in 0..n {
        let l = lengths_of(&box_at(&b, s));
        for k in 0..3 {
            out[[s, k]] = l[k];
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_angles_from_box_single_structure<'py>(
    py: Python<'py>,
    b: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    Array1::from_vec(angles_of(&mat_of(&b.as_array())).to_vec()).into_pyarray(py)
}

#[pyfunction]
pub fn get_angles_from_box<'py>(
    py: Python<'py>,
    boxes: PyReadonlyArray3<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let b = boxes.as_array();
    let n = b.shape()[0];
    let mut out = Array2::<f64>::zeros((n, 3));
    for s in 0..n {
        let a = angles_of(&box_at(&b, s));
        for k in 0..3 {
            out[[s, k]] = a[k];
        }
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
    for i in 0..3 {
        for j in 0..3 {
            out[[i, j]] = b[i][j];
        }
    }
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
        let b = box_of(
            [l[[s, 0]], l[[s, 1]], l[[s, 2]]],
            [a[[s, 0]], a[[s, 1]], a[[s, 2]]],
        );
        for i in 0..3 {
            for j in 0..3 {
                out[[s, i, j]] = b[i][j];
            }
        }
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
    wrap_all(
        &mut coordinates.as_array_mut(),
        &boxes.as_array(),
        [o[0], o[1], o[2]],
        WrapKind::Pbc,
    );
}

#[pyfunction]
pub fn wrap_to_pbc_center(
    mut coordinates: PyReadwriteArray3<'_, f64>,
    boxes: PyReadonlyArray3<'_, f64>,
    box_center: PyReadonlyArray1<'_, f64>,
) {
    let o = box_center.as_array();
    wrap_all(
        &mut coordinates.as_array_mut(),
        &boxes.as_array(),
        [o[0], o[1], o[2]],
        WrapKind::PbcCenter,
    );
}

#[pyfunction]
pub fn wrap_to_mic(
    mut coordinates: PyReadwriteArray3<'_, f64>,
    boxes: PyReadonlyArray3<'_, f64>,
    mic_origin: PyReadonlyArray1<'_, f64>,
) {
    let o = mic_origin.as_array();
    wrap_all(
        &mut coordinates.as_array_mut(),
        &boxes.as_array(),
        [o[0], o[1], o[2]],
        WrapKind::Mic,
    );
}

#[pyfunction]
pub fn wrap_to_pbc_vector_single_structure<'py>(
    py: Python<'py>,
    vector: PyReadonlyArray1<'py, f64>,
    b: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let v = vector.as_array();
    let m = mat_of(&b.as_array());
    let (ortho, _, inv) = prep_primary(&m);
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
    let (ortho, _, inv) = prep_primary(&m);
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
    let (ortho, cell, inv) = prep_dist(&m);
    let w = wrap_mic_vec([v[0], v[1], v[2]], &cell, &inv, ortho);
    Array1::from_vec(w.to_vec()).into_pyarray(py)
}

/// Mirrors `unwrap.py`. Deliberately serial: structure `s+1` is written from the already
/// updated structure `s`, so the loop carries a dependency and cannot be parallelised.
/// Each transition uses the previous selected structure's actual cell. Axis-aligned
/// half-cell jumps retain ties-to-even; general cells retain the original-basis
/// ties-to-even seed unless the shared MIC mechanism finds a strictly shorter image.
#[pyfunction]
#[allow(clippy::needless_range_loop)] // Fixed Cartesian indexing is intentional in this hot loop.
pub fn unwrap(mut coordinates: PyReadwriteArray3<'_, f64>, boxes: PyReadonlyArray3<'_, f64>) {
    let b = boxes.as_array();
    let mut c = coordinates.as_array_mut();
    let (n_structures, n_atoms) = (c.shape()[0], c.shape()[1]);
    if n_structures == 0 {
        return;
    }
    for s in 0..n_structures.saturating_sub(1) {
        let bs = box_at(&b, s);
        let (axis_aligned, cell, reduced_inv) = prep_dist(&bs);
        let inv = if axis_aligned {
            [[0.0; 3]; 3]
        } else {
            inverse_matrix_3x3_full(&bs)
        };
        for a in 0..n_atoms {
            let prev = [c[[s, a, 0]], c[[s, a, 1]], c[[s, a, 2]]];
            let mut delta = [
                c[[s + 1, a, 0]] - prev[0],
                c[[s + 1, a, 1]] - prev[1],
                c[[s + 1, a, 2]] - prev[2],
            ];
            let shift = if axis_aligned {
                // `round`, not `f64::round`: Python/Numba round half to even.
                for k in 0..3 {
                    delta[k] -= bs[k][k] * fast_round_ties_even(delta[k] / bs[k][k]);
                }
                delta
            } else {
                let mut f = fractional(delta, &inv);
                for k in 0..3 {
                    f[k] -= fast_round_ties_even(f[k]);
                }
                let seed = cartesian(f, &bs);
                let shortest = mic_vector(delta, &cell, &reduced_inv, false);
                if dot_product(shortest, shortest) < dot_product(seed, seed) {
                    shortest
                } else {
                    seed
                }
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
    m.add_function(wrap_pyfunction!(
        get_lengths_and_angles_from_box_single_structure,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(get_lengths_and_angles_from_box, m)?)?;
    m.add_function(wrap_pyfunction!(
        get_box_from_lengths_and_angles_single_structure,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(get_box_from_lengths_and_angles, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_pbc, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_pbc_center, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_mic, m)?)?;
    m.add_function(wrap_pyfunction!(wrap_to_pbc_vector_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(
        wrap_to_pbc_center_vector_single_structure,
        m
    )?)?;
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
        let rotated: Mat3 = [
            [6.0 * c, 6.0 * s, 0.0],
            [-7.0 * s, 7.0 * c, 0.0],
            [0.0, 0.0, 8.0],
        ];
        assert!(box_is_orthogonal_one(&rotated));
    }

    #[test]
    fn lengths_and_angles_round_trip_through_the_box() {
        for b in [ORTHO, TRIC] {
            let (l, a) = (lengths_of(&b), angles_of(&b));
            let back = box_of(l, a);
            for i in 0..3 {
                for j in 0..3 {
                    assert!(
                        (back[i][j] - b[i][j]).abs() < 1e-12,
                        "round trip failed at [{i}][{j}]: {} vs {}",
                        back[i][j],
                        b[i][j]
                    );
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
        let inv = inverse_matrix_3x3_full(&ORTHO);
        for v in [[13.7, -9.2, 20.1], [-0.001, 6.999, 8.0], [0.0, 0.0, 0.0]] {
            let w = wrap_pbc_vec(v, &ORTHO, &inv, true, 0.0);
            for k in 0..3 {
                assert!(w[k] >= 0.0 && w[k] < ORTHO[k][k], "{:?} -> {:?}", v, w);
            }
            let m = wrap_mic_vec(v, &ORTHO, &inv, true);
            for k in 0..3 {
                assert!(
                    m[k].abs() <= ORTHO[k][k] / 2.0 + 1e-12,
                    "{:?} -> {:?}",
                    v,
                    m
                );
            }
        }
    }

    /// The corrected triclinic MIC wrap really is the minimum image, even for inputs many
    /// box lengths outside the cell — the regime where the replaced Numba implementation failed (see `wrap_mic_vec`).
    #[test]
    fn triclinic_mic_wrap_returns_the_minimum_image() {
        let original_inverse = inverse_matrix_3x3_full(&TRIC);
        let (ortho, cell, inv) = prep_dist(&TRIC);
        // deterministic spread, deliberately far outside the cell
        let mut seed = 12345u64;
        let mut next = || {
            seed = seed
                .wrapping_mul(6364136223846793005)
                .wrapping_add(1442695040888963407);
            ((seed >> 11) as f64 / (1u64 << 53) as f64) * 40.0 - 20.0
        };
        for _ in 0..200 {
            let v = [next(), next(), next()];
            let out = wrap_mic_vec(v, &cell, &inv, ortho);
            let d2 = dot_product(out, out);
            for i in [-1.0f64, 0.0, 1.0] {
                for j in [-1.0f64, 0.0, 1.0] {
                    for k in [-1.0f64, 0.0, 1.0] {
                        let c = [
                            out[0] + i * TRIC[0][0] + j * TRIC[1][0] + k * TRIC[2][0],
                            out[1] + i * TRIC[0][1] + j * TRIC[1][1] + k * TRIC[2][1],
                            out[2] + i * TRIC[0][2] + j * TRIC[1][2] + k * TRIC[2][2],
                        ];
                        assert!(
                            dot_product(c, c) >= d2 - 1e-12,
                            "not the minimum image: {:?} -> {:?}",
                            v,
                            out
                        );
                    }
                }
            }
            // and it must still be an image of the original vector
            let d = [out[0] - v[0], out[1] - v[1], out[2] - v[2]];
            let f = [
                original_inverse[0][0] * d[0]
                    + original_inverse[1][0] * d[1]
                    + original_inverse[2][0] * d[2],
                original_inverse[0][1] * d[0]
                    + original_inverse[1][1] * d[1]
                    + original_inverse[2][1] * d[2],
                original_inverse[0][2] * d[0]
                    + original_inverse[1][2] * d[1]
                    + original_inverse[2][2] * d[2],
            ];
            for k in 0..3 {
                assert!(
                    (f[k] - f[k].round_ties_even()).abs() < 1e-9,
                    "not an integer image: {:?}",
                    f
                );
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
