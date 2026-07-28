//! Rusterized dihedral-angle family.
//!
//! Faithful ports of `molsysmt.lib.structure.get_dihedral_angles.*` and
//! `get_mic_dihedral_angles.*`, reusing the MIC helpers from `mic.rs`.
//!
//! Heaviest per-element allocation of the geometry kernels: the Numba versions build
//! three numpy vectors per quartet and `dihedral_angle` calls `cross_product` three
//! times, each allocating `np.empty((3))` — six allocations per quartet (nine in the
//! MIC variants, which also wrap each vector). The Rust port is fully stack-based.

use numpy::ndarray::{Array1, Array2, ArrayView2, ArrayView3};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray2, PyReadonlyArray3};
use pyo3::prelude::*;

use crate::mathlib::dihedral_angle;
use crate::mic::{box_2d, box_at, mic_vector, prep_dist, Mat3};

#[inline]
fn quartet(q: &ArrayView2<i64>, j: usize) -> (usize, usize, usize, usize) {
    (q[[j, 0]] as usize, q[[j, 1]] as usize, q[[j, 2]] as usize, q[[j, 3]] as usize)
}

/// vect0 = c[a1]-c[a0], vect1 = c[a2]-c[a1], vect2 = c[a3]-c[a2]  (Numba convention).
#[inline]
fn quartet_vectors_3d(c: &ArrayView3<f64>, s: usize, a0: usize, a1: usize, a2: usize, a3: usize)
    -> ([f64; 3], [f64; 3], [f64; 3]) {
    (
        [c[[s, a1, 0]] - c[[s, a0, 0]], c[[s, a1, 1]] - c[[s, a0, 1]], c[[s, a1, 2]] - c[[s, a0, 2]]],
        [c[[s, a2, 0]] - c[[s, a1, 0]], c[[s, a2, 1]] - c[[s, a1, 1]], c[[s, a2, 2]] - c[[s, a1, 2]]],
        [c[[s, a3, 0]] - c[[s, a2, 0]], c[[s, a3, 1]] - c[[s, a2, 1]], c[[s, a3, 2]] - c[[s, a2, 2]]],
    )
}

#[inline]
fn quartet_vectors_2d(c: &ArrayView2<f64>, a0: usize, a1: usize, a2: usize, a3: usize)
    -> ([f64; 3], [f64; 3], [f64; 3]) {
    (
        [c[[a1, 0]] - c[[a0, 0]], c[[a1, 1]] - c[[a0, 1]], c[[a1, 2]] - c[[a0, 2]]],
        [c[[a2, 0]] - c[[a1, 0]], c[[a2, 1]] - c[[a1, 1]], c[[a2, 2]] - c[[a1, 2]]],
        [c[[a3, 0]] - c[[a2, 0]], c[[a3, 1]] - c[[a2, 1]], c[[a3, 2]] - c[[a2, 2]]],
    )
}

// --------------------------------------------------------------------------- vacuum

#[pyfunction]
pub fn get_dihedral_angles<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    quartets: PyReadonlyArray2<'py, i64>,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let q = quartets.as_array();
    let ns = c.shape()[0];
    let nq = q.shape()[0];
    let mut out = Array2::<f64>::zeros((ns, nq));
    for s in 0..ns {
        for j in 0..nq {
            let (a0, a1, a2, a3) = quartet(&q, j);
            let (v0, v1, v2) = quartet_vectors_3d(&c, s, a0, a1, a2, a3);
            out[[s, j]] = dihedral_angle(v0, v1, v2);
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_dihedral_angles_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    quartets: PyReadonlyArray2<'py, i64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let q = quartets.as_array();
    let nq = q.shape()[0];
    let mut out = Array1::<f64>::zeros(nq);
    for j in 0..nq {
        let (a0, a1, a2, a3) = quartet(&q, j);
        let (v0, v1, v2) = quartet_vectors_2d(&c, a0, a1, a2, a3);
        out[j] = dihedral_angle(v0, v1, v2);
    }
    out.into_pyarray(py)
}

// --------------------------------------------------------------------------- periodic

#[inline]
fn mic_dihedral(v0: [f64; 3], v1: [f64; 3], v2: [f64; 3], cell: &Mat3, inv: &Mat3, ortho: bool) -> f64 {
    dihedral_angle(
        mic_vector(v0, cell, inv, ortho),
        mic_vector(v1, cell, inv, ortho),
        mic_vector(v2, cell, inv, ortho),
    )
}

#[pyfunction]
pub fn get_mic_dihedral_angles<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    boxes: PyReadonlyArray3<'py, f64>,
    quartets: PyReadonlyArray2<'py, i64>,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let b = boxes.as_array();
    let q = quartets.as_array();
    let ns = c.shape()[0];
    let nq = q.shape()[0];
    let mut out = Array2::<f64>::zeros((ns, nq));
    for s in 0..ns {
        let bs = box_at(&b, s);
        let (ortho, cell, inv) = prep_dist(&bs);
        for j in 0..nq {
            let (a0, a1, a2, a3) = quartet(&q, j);
            let (v0, v1, v2) = quartet_vectors_3d(&c, s, a0, a1, a2, a3);
            out[[s, j]] = mic_dihedral(v0, v1, v2, &cell, &inv, ortho);
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_mic_dihedral_angles_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    boxes: PyReadonlyArray2<'py, f64>,
    quartets: PyReadonlyArray2<'py, i64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let bs = box_2d(&boxes.as_array());
    let (ortho, cell, inv) = prep_dist(&bs);
    let q = quartets.as_array();
    let nq = q.shape()[0];
    let mut out = Array1::<f64>::zeros(nq);
    for j in 0..nq {
        let (a0, a1, a2, a3) = quartet(&q, j);
        let (v0, v1, v2) = quartet_vectors_2d(&c, a0, a1, a2, a3);
        out[j] = mic_dihedral(v0, v1, v2, &cell, &inv, ortho);
    }
    out.into_pyarray(py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_dihedral_angles, m)?)?;
    m.add_function(wrap_pyfunction!(get_dihedral_angles_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_dihedral_angles, m)?)?;
    m.add_function(wrap_pyfunction!(get_mic_dihedral_angles_single_structure, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::mathlib::cross_product as cross;

    #[test]
    fn cross_product_follows_the_right_hand_rule() {
        let x = [1.0, 0.0, 0.0];
        let y = [0.0, 1.0, 0.0];
        assert_eq!(cross(x, y), [0.0, 0.0, 1.0]);
        assert_eq!(cross(y, x), [0.0, 0.0, -1.0]);
    }

    /// Planar reference values, cross-checked against the Numba oracle for the chain
    /// a0=(0,0,0) a1=(1,1,0) a2=(2,1,0) a3=a2+v2, i.e. v0=[1,1,0], v1=[1,0,0].
    #[test]
    fn planar_cis_and_trans_conformations() {
        let v0 = [1.0, 1.0, 0.0];
        let v1 = [1.0, 0.0, 0.0];

        // Cis/syn: a0 and a3 fall on the same side of the a1-a2 axis -> 0.
        assert!(dihedral_angle(v0, v1, [1.0, -1.0, 0.0]).abs() < 1e-12);

        // Trans/anti: opposite sides -> |pi| (the oracle returns -pi here).
        let trans = dihedral_angle(v0, v1, [1.0, 1.0, 0.0]);
        assert!((trans.abs() - std::f64::consts::PI).abs() < 1e-12, "got {trans}");
    }

    /// Perpendicular quartets are +/- pi/2, with the sign set by the chirality.
    #[test]
    fn perpendicular_quartets_are_half_pi_with_sign() {
        let v0 = [1.0, 1.0, 0.0];
        let v1 = [1.0, 0.0, 0.0];
        let up = dihedral_angle(v0, v1, [1.0, 0.0, 1.0]);
        let down = dihedral_angle(v0, v1, [1.0, 0.0, -1.0]);
        assert!((up + std::f64::consts::FRAC_PI_2).abs() < 1e-12, "got {up}");
        assert!((down - std::f64::consts::FRAC_PI_2).abs() < 1e-12, "got {down}");
    }

    #[test]
    fn sign_flips_with_chirality() {
        let v0 = [1.0, 1.0, 0.0];
        let v1 = [1.0, 0.0, 0.0];
        let plus = dihedral_angle(v0, v1, [1.0, 0.0, 1.0]);
        let minus = dihedral_angle(v0, v1, [1.0, 0.0, -1.0]);
        assert!(plus * minus < 0.0, "mirror quartets must have opposite signs");
        assert!((plus.abs() - minus.abs()).abs() < 1e-12);
    }

    #[test]
    fn cosine_is_clamped_so_acos_never_nans() {
        let v0 = [1.0, 1e-18, 0.0];
        let v1 = [1.0, 0.0, 0.0];
        let v2 = [1.0, 1e-18, 0.0];
        let ang = dihedral_angle(v0, v1, v2);
        assert!(ang.is_finite(), "got {ang}");
    }
}
