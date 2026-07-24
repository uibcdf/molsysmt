//! Rusterized MIC (minimum-image) distance family.
//!
//! Faithful ports of `molsysmt.lib.structure.get_mic_distances.*`. Names match the
//! Numba functions 1:1 so the opt-in seam can dispatch by name. The Numba versions
//! remain the oracle; parity is checked bit-for-bit in the test suite.

use numpy::ndarray::{Array1, Array2, Array3};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyArray3, PyReadonlyArray2, PyReadonlyArray3};
use pyo3::prelude::*;

use crate::mathlib::inverse_matrix_3x3;

pub type Mat3 = [[f64; 3]; 3];

/// Mirrors molsysmt.lib.pbc.box_is_orthogonal_single_structure (row dot products).
pub(crate) fn box_is_orthogonal(b: &Mat3) -> bool {
    let dot = |u: &[f64; 3], v: &[f64; 3]| u[0] * v[0] + u[1] * v[1] + u[2] * v[2];
    dot(&b[0], &b[1]).abs() <= 1e-4 && dot(&b[0], &b[2]).abs() <= 1e-4 && dot(&b[1], &b[2]).abs() <= 1e-4
}

/// Mirrors molsysmt.lib.pbc.wrap_to_mic.wrap_to_mic_vector_single_structure.
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

#[inline]
fn mic_distance(p1: [f64; 3], p2: [f64; 3], b: &Mat3, inv: &Mat3, ortho: bool) -> f64 {
    let v = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]];
    let w = wrap_to_mic_vector(v, b, inv, ortho);
    (w[0] * w[0] + w[1] * w[1] + w[2] * w[2]).sqrt()
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
    let mut out = Array3::<f64>::zeros((ns, na, na));
    for s in 0..ns {
        let bs = box_at(&b, s);
        let (ortho, inv) = prep(&bs);
        for j in 0..na {
            let p1 = [c[[s, j, 0]], c[[s, j, 1]], c[[s, j, 2]]];
            for k in (j + 1)..na {
                let p2 = [c[[s, k, 0]], c[[s, k, 1]], c[[s, k, 2]]];
                let d = mic_distance(p1, p2, &bs, &inv, ortho);
                out[[s, j, k]] = d;
                out[[s, k, j]] = d;
            }
        }
    }
    out.into_pyarray(py)
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
        let (ortho, inv) = prep(&bs);
        for j in 0..na1 {
            let p1 = [c1[[s, j, 0]], c1[[s, j, 1]], c1[[s, j, 2]]];
            for k in 0..na2 {
                let p2 = [c2[[s, k, 0]], c2[[s, k, 1]], c2[[s, k, 2]]];
                out[[s, j, k]] = mic_distance(p1, p2, &bs, &inv, ortho);
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
        let (ortho, inv) = prep(&bs);
        for j in 0..na {
            let p1 = [c1[[s, j, 0]], c1[[s, j, 1]], c1[[s, j, 2]]];
            let p2 = [c2[[s, j, 0]], c2[[s, j, 1]], c2[[s, j, 2]]];
            out[[s, j]] = mic_distance(p1, p2, &bs, &inv, ortho);
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
    let (ortho, inv) = prep(&bs);
    let na = c.shape()[0];
    let mut out = Array2::<f64>::zeros((na, na));
    for j in 0..na {
        let p1 = [c[[j, 0]], c[[j, 1]], c[[j, 2]]];
        for k in (j + 1)..na {
            let p2 = [c[[k, 0]], c[[k, 1]], c[[k, 2]]];
            let d = mic_distance(p1, p2, &bs, &inv, ortho);
            out[[j, k]] = d;
            out[[k, j]] = d;
        }
    }
    out.into_pyarray(py)
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
    let (ortho, inv) = prep(&bs);
    let na1 = c1.shape()[0];
    let na2 = c2.shape()[0];
    let mut out = Array2::<f64>::zeros((na1, na2));
    for j in 0..na1 {
        let p1 = [c1[[j, 0]], c1[[j, 1]], c1[[j, 2]]];
        for k in 0..na2 {
            let p2 = [c2[[k, 0]], c2[[k, 1]], c2[[k, 2]]];
            out[[j, k]] = mic_distance(p1, p2, &bs, &inv, ortho);
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
    let (ortho, inv) = prep(&bs);
    let na = c1.shape()[0];
    let mut out = Array1::<f64>::zeros(na);
    for j in 0..na {
        let p1 = [c1[[j, 0]], c1[[j, 1]], c1[[j, 2]]];
        let p2 = [c2[[j, 0]], c2[[j, 1]], c2[[j, 2]]];
        out[j] = mic_distance(p1, p2, &bs, &inv, ortho);
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
