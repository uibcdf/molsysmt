//! Rusterized angle family.
//!
//! Faithful ports of `molsysmt.lib.structure.get_angles.*` and
//! `get_mic_angles.*`. The Numba versions allocate per triplet (two numpy
//! subtractions, plus two `np.empty((3))` inside `wrap_to_mic_vector` in the MIC
//! variants); the Rust ports use stack arrays. Same maths and same MIC convention
//! as the distance family, so results are bit-for-bit identical.
//!
//! `get_angles` is on the `hbonds.get_luzard_chandler_hbonds` path, so this block
//! completes the h-bond chain started by the neighbour-list block.

use numpy::ndarray::{Array1, Array2, ArrayView2, ArrayView3};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray2, PyReadonlyArray3};
use pyo3::prelude::*;

use crate::mathlib::angle;
use crate::mic::{box_2d, box_at, mic_vector, prep_dist, Mat3};

#[inline]
fn triplet_vectors_3d(c: &ArrayView3<f64>, s: usize, a0: usize, a1: usize, a2: usize)
    -> ([f64; 3], [f64; 3]) {
    (
        [c[[s, a0, 0]] - c[[s, a1, 0]], c[[s, a0, 1]] - c[[s, a1, 1]], c[[s, a0, 2]] - c[[s, a1, 2]]],
        [c[[s, a2, 0]] - c[[s, a1, 0]], c[[s, a2, 1]] - c[[s, a1, 1]], c[[s, a2, 2]] - c[[s, a1, 2]]],
    )
}

#[inline]
fn triplet_vectors_2d(c: &ArrayView2<f64>, a0: usize, a1: usize, a2: usize)
    -> ([f64; 3], [f64; 3]) {
    (
        [c[[a0, 0]] - c[[a1, 0]], c[[a0, 1]] - c[[a1, 1]], c[[a0, 2]] - c[[a1, 2]]],
        [c[[a2, 0]] - c[[a1, 0]], c[[a2, 1]] - c[[a1, 1]], c[[a2, 2]] - c[[a1, 2]]],
    )
}

#[inline]
fn tri(t: &ArrayView2<i64>, j: usize) -> (usize, usize, usize) {
    (t[[j, 0]] as usize, t[[j, 1]] as usize, t[[j, 2]] as usize)
}

// --------------------------------------------------------------------------- vacuum

#[pyfunction]
pub fn get_angles<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    triplets: PyReadonlyArray2<'py, i64>,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let t = triplets.as_array();
    let ns = c.shape()[0];
    let nt = t.shape()[0];
    let mut out = Array2::<f64>::zeros((ns, nt));
    for s in 0..ns {
        for j in 0..nt {
            let (a0, a1, a2) = tri(&t, j);
            let (v0, v1) = triplet_vectors_3d(&c, s, a0, a1, a2);
            out[[s, j]] = angle(v0, v1);
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_angles_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    triplets: PyReadonlyArray2<'py, i64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let t = triplets.as_array();
    let nt = t.shape()[0];
    let mut out = Array1::<f64>::zeros(nt);
    for j in 0..nt {
        let (a0, a1, a2) = tri(&t, j);
        let (v0, v1) = triplet_vectors_2d(&c, a0, a1, a2);
        out[j] = angle(v0, v1);
    }
    out.into_pyarray(py)
}

// --------------------------------------------------------------------------- periodic

#[inline]
fn mic_angle(v0: [f64; 3], v1: [f64; 3], cell: &Mat3, inv: &Mat3, ortho: bool) -> f64 {
    angle(
        mic_vector(v0, cell, inv, ortho),
        mic_vector(v1, cell, inv, ortho),
    )
}

#[pyfunction]
pub fn get_mic_angles<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    boxes: PyReadonlyArray3<'py, f64>,
    triplets: PyReadonlyArray2<'py, i64>,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let b = boxes.as_array();
    let t = triplets.as_array();
    let ns = c.shape()[0];
    let nt = t.shape()[0];
    let mut out = Array2::<f64>::zeros((ns, nt));
    for s in 0..ns {
        let bs = box_at(&b, s);
        let (ortho, cell, inv) = prep_dist(&bs);
        for j in 0..nt {
            let (a0, a1, a2) = tri(&t, j);
            let (v0, v1) = triplet_vectors_3d(&c, s, a0, a1, a2);
            out[[s, j]] = mic_angle(v0, v1, &cell, &inv, ortho);
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_mic_angles_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    boxes: PyReadonlyArray2<'py, f64>,
    triplets: PyReadonlyArray2<'py, i64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let bs = box_2d(&boxes.as_array());
    let (ortho, cell, inv) = prep_dist(&bs);
    let t = triplets.as_array();
    let nt = t.shape()[0];
    let mut out = Array1::<f64>::zeros(nt);
    for j in 0..nt {
        let (a0, a1, a2) = tri(&t, j);
        let (v0, v1) = triplet_vectors_2d(&c, a0, a1, a2);
        out[j] = mic_angle(v0, v1, &cell, &inv, ortho);
    }
    out.into_pyarray(py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_angles, m)?)?;
    m.add_function(wrap_pyfunction!(get_angles_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_angles, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_angles_single_structure, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn known_angles() {
        let x = [1.0, 0.0, 0.0];
        let y = [0.0, 1.0, 0.0];
        assert!((angle(x, y) - std::f64::consts::FRAC_PI_2).abs() < 1e-12);
        assert!(angle(x, [2.0, 0.0, 0.0]).abs() < 1e-12);
        assert!((angle(x, [-1.0, 0.0, 0.0]) - std::f64::consts::PI).abs() < 1e-12);
    }

    #[test]
    fn cosine_is_clamped_so_acos_never_nans() {
        // Near-parallel vectors can push the normalised dot product just past 1.0.
        let a = [1.0, 1e-17, 0.0];
        let b = [1.0, 0.0, 0.0];
        let ang = angle(a, b);
        assert!(ang.is_finite(), "angle must not be NaN, got {ang}");
        assert!(ang >= 0.0 && ang <= std::f64::consts::PI);
    }

    #[test]
    fn angle_is_symmetric() {
        let a = [0.3, -1.2, 0.7];
        let b = [-0.5, 0.4, 2.0];
        assert!((angle(a, b) - angle(b, a)).abs() < 1e-15);
    }
}
