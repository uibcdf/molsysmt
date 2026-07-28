//! Block 12 — principal axes: `get_principal_inertia_axes` and
//! `get_principal_geometric_axes` (4 kernels).
//!
//! Both build a 3x3 symmetric matrix about the weighted centroid and diagonalise it. The
//! inertia tensor uses `+w(y²+z²)` on the diagonal and `-w·xy` off it; the geometric one
//! is the plain weighted second-moment matrix, `+w·x²` and `+w·xy`, divided by the total
//! weight. Eigenvalues come back **ascending** and the eigenvector matrix is transposed,
//! so row `i` of the result is the `i`-th axis.
//!
//! Solved with `nalgebra` in pure Rust — the matrix is 3x3, so LAPACK would buy nothing
//! (see `devguide/pending_proposals/linear_algebra_backend_for_rust_kernels.md`).
//!
//! # The sign convention, and why this port adds one
//!
//! An eigenvector is only defined up to sign: `v` and `-v` are equally valid principal
//! axes. Upstream returns whatever LAPACK happens to produce, which is not specified by
//! the API, is not guaranteed stable across LAPACK implementations or versions, and would
//! make `backend='rust'` and `backend='numba'` disagree *visibly* on the same input —
//! axes flipping when the accelerator is switched on.
//!
//! This port therefore fixes signs deterministically: **the component of largest absolute
//! value is made positive** (ties broken by lowest index). The axes are mathematically
//! identical either way; the difference is that this answer is reproducible.
//!
//! Consequence for the parity tests: eigenvalues are compared directly, eigenvectors only
//! up to sign (`|v_rust · v_numba| ≈ 1`), plus the defining property `M v = λ v`. The
//! underspecified contract is reported in
//! `devguide/pending_bugs/principal_axes_eigenvector_sign_unspecified.md`.

use nalgebra::SMatrix;
use numpy::ndarray::{Array1, Array2, Array3, ArrayView2};
use numpy::{
    IntoPyArray, PyArray1, PyArray2, PyArray3, PyReadonlyArray1, PyReadonlyArray2, PyReadonlyArray3,
};
use pyo3::prelude::*;

use crate::mathlib::{Mat3, Vec3};

#[inline]
fn weighted_centroid(c: &ArrayView2<f64>, w: &numpy::ndarray::ArrayView1<f64>) -> Vec3 {
    let mut acc = [0.0f64; 3];
    let mut total = 0.0f64;
    for i in 0..c.shape()[0] {
        acc[0] += w[i] * c[[i, 0]];
        acc[1] += w[i] * c[[i, 1]];
        acc[2] += w[i] * c[[i, 2]];
        total += w[i];
    }
    [acc[0] / total, acc[1] / total, acc[2] / total]
}

#[inline]
fn total_weight(w: &numpy::ndarray::ArrayView1<f64>) -> f64 {
    let mut t = 0.0;
    for &v in w.iter() {
        t += v;
    }
    t
}

/// The inertia tensor about the weighted centroid.
#[inline]
fn inertia_matrix(c: &ArrayView2<f64>, w: &numpy::ndarray::ArrayView1<f64>) -> Mat3 {
    let centre = weighted_centroid(c, w);
    let mut m = [[0.0f64; 3]; 3];
    for i in 0..c.shape()[0] {
        let (x, y, z) = (
            c[[i, 0]] - centre[0],
            c[[i, 1]] - centre[1],
            c[[i, 2]] - centre[2],
        );
        m[0][0] += w[i] * (y * y + z * z);
        m[1][1] += w[i] * (x * x + z * z);
        m[2][2] += w[i] * (x * x + y * y);
        m[0][1] -= w[i] * (x * y);
        m[0][2] -= w[i] * (x * z);
        m[1][2] -= w[i] * (y * z);
    }
    m[1][0] = m[0][1];
    m[2][0] = m[0][2];
    m[2][1] = m[1][2];
    m
}

/// The weighted second-moment matrix about the centroid, normalised by the total weight.
#[inline]
fn geometric_matrix(c: &ArrayView2<f64>, w: &numpy::ndarray::ArrayView1<f64>) -> Mat3 {
    let centre = weighted_centroid(c, w);
    let mut m = [[0.0f64; 3]; 3];
    for i in 0..c.shape()[0] {
        let (x, y, z) = (
            c[[i, 0]] - centre[0],
            c[[i, 1]] - centre[1],
            c[[i, 2]] - centre[2],
        );
        m[0][0] += w[i] * x * x;
        m[1][1] += w[i] * y * y;
        m[2][2] += w[i] * z * z;
        m[0][1] += w[i] * x * y;
        m[0][2] += w[i] * x * z;
        m[1][2] += w[i] * y * z;
    }
    m[1][0] = m[0][1];
    m[2][0] = m[0][2];
    m[2][1] = m[1][2];
    let total = total_weight(w);
    for row in m.iter_mut() {
        for v in row.iter_mut() {
            *v /= total;
        }
    }
    m
}

/// Makes the largest-magnitude component positive, so the axis is reproducible.
#[inline]
fn fix_sign(v: &mut [f64; 3]) {
    let mut lead = 0usize;
    for k in 1..3 {
        if v[k].abs() > v[lead].abs() {
            lead = k;
        }
    }
    if v[lead] < 0.0 {
        for x in v.iter_mut() {
            *x = -*x;
        }
    }
}

/// Ascending eigenvalues and the matching axes as **rows**, signs fixed.
#[inline]
fn principal_axes(m: &Mat3) -> (Vec3, Mat3) {
    let flat = [
        m[0][0], m[0][1], m[0][2], m[1][0], m[1][1], m[1][2], m[2][0], m[2][1], m[2][2],
    ];
    let e = SMatrix::<f64, 3, 3>::from_row_slice(&flat).symmetric_eigen();
    let mut order = [0usize, 1, 2];
    order.sort_by(|&a, &b| e.eigenvalues[a].partial_cmp(&e.eigenvalues[b]).unwrap());
    let mut values = [0.0f64; 3];
    let mut axes = [[0.0f64; 3]; 3];
    for (i, &src) in order.iter().enumerate() {
        values[i] = e.eigenvalues[src];
        let mut v = [
            e.eigenvectors[(0, src)],
            e.eigenvectors[(1, src)],
            e.eigenvectors[(2, src)],
        ];
        fix_sign(&mut v);
        axes[i] = v; // row i is the i-th axis, matching upstream's transpose
    }
    (values, axes)
}

fn pack_single<'py>(
    py: Python<'py>,
    values: Vec3,
    axes: Mat3,
) -> (Bound<'py, PyArray1<f64>>, Bound<'py, PyArray2<f64>>) {
    let mut m = Array2::<f64>::zeros((3, 3));
    for i in 0..3 {
        for j in 0..3 {
            m[[i, j]] = axes[i][j];
        }
    }
    (
        Array1::from_vec(values.to_vec()).into_pyarray(py),
        m.into_pyarray(py),
    )
}

fn pack_many<'py>(
    py: Python<'py>,
    parts: Vec<(Vec3, Mat3)>,
) -> (Bound<'py, PyArray2<f64>>, Bound<'py, PyArray3<f64>>) {
    let ns = parts.len();
    let mut values = Array2::<f64>::zeros((ns, 3));
    let mut axes = Array3::<f64>::zeros((ns, 3, 3));
    for (s, (v, a)) in parts.into_iter().enumerate() {
        for i in 0..3 {
            values[[s, i]] = v[i];
            for j in 0..3 {
                axes[[s, i, j]] = a[i][j];
            }
        }
    }
    (values.into_pyarray(py), axes.into_pyarray(py))
}

#[pyfunction]
pub fn get_principal_inertia_axes_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    weights: PyReadonlyArray1<'py, f64>,
) -> (Bound<'py, PyArray1<f64>>, Bound<'py, PyArray2<f64>>) {
    let (v, a) = principal_axes(&inertia_matrix(
        &coordinates.as_array(),
        &weights.as_array(),
    ));
    pack_single(py, v, a)
}

#[pyfunction]
pub fn get_principal_inertia_axes<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    weights: PyReadonlyArray1<'py, f64>,
) -> (Bound<'py, PyArray2<f64>>, Bound<'py, PyArray3<f64>>) {
    let c = coordinates.as_array();
    let w = weights.as_array();
    let parts: Vec<(Vec3, Mat3)> = (0..c.shape()[0])
        .map(|s| {
            principal_axes(&inertia_matrix(
                &c.index_axis(numpy::ndarray::Axis(0), s),
                &w,
            ))
        })
        .collect();
    pack_many(py, parts)
}

#[pyfunction]
pub fn get_principal_geometric_axes_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    weights: PyReadonlyArray1<'py, f64>,
) -> (Bound<'py, PyArray1<f64>>, Bound<'py, PyArray2<f64>>) {
    let (v, a) = principal_axes(&geometric_matrix(
        &coordinates.as_array(),
        &weights.as_array(),
    ));
    pack_single(py, v, a)
}

#[pyfunction]
pub fn get_principal_geometric_axes<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    weights: PyReadonlyArray1<'py, f64>,
) -> (Bound<'py, PyArray2<f64>>, Bound<'py, PyArray3<f64>>) {
    let c = coordinates.as_array();
    let w = weights.as_array();
    let parts: Vec<(Vec3, Mat3)> = (0..c.shape()[0])
        .map(|s| {
            principal_axes(&geometric_matrix(
                &c.index_axis(numpy::ndarray::Axis(0), s),
                &w,
            ))
        })
        .collect();
    pack_many(py, parts)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(
        get_principal_inertia_axes_single_structure,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(get_principal_inertia_axes, m)?)?;
    m.add_function(wrap_pyfunction!(
        get_principal_geometric_axes_single_structure,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(get_principal_geometric_axes, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use numpy::ndarray::array;

    /// A rod along x: the smallest inertia is about x, and that axis must be x itself.
    #[test]
    fn a_rod_has_its_light_inertia_axis_along_the_rod() {
        let c = array![
            [-2.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0]
        ];
        let w = array![1.0, 1.0, 1.0, 1.0, 1.0];
        let (values, axes) = principal_axes(&inertia_matrix(&c.view(), &w.view()));
        assert!(
            values[0].abs() < 1e-12,
            "inertia about the rod axis must vanish: {values:?}"
        );
        assert!(
            (axes[0][0].abs() - 1.0).abs() < 1e-12,
            "expected x, got {:?}",
            axes[0]
        );
    }

    /// The geometric axes of the same rod put the *largest* variance along x — the two
    /// kernels order their axes oppositely, which is easy to get wrong.
    #[test]
    fn geometric_axes_order_opposite_to_inertia_axes() {
        let c = array![
            [-2.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0]
        ];
        let w = array![1.0, 1.0, 1.0, 1.0, 1.0];
        let (values, axes) = principal_axes(&geometric_matrix(&c.view(), &w.view()));
        assert!(values[0].abs() < 1e-12);
        assert!(
            (axes[2][0].abs() - 1.0).abs() < 1e-12,
            "largest variance should be along x, got {:?}",
            axes[2]
        );
    }

    #[test]
    fn eigenvalues_are_ascending_and_axes_orthonormal() {
        let c = array![
            [1.0, 0.0, 0.5],
            [0.0, 2.0, -1.0],
            [-1.5, 0.3, 2.0],
            [0.7, -1.1, 0.2],
            [2.0, 1.0, -0.4]
        ];
        let w = array![1.0, 12.0, 14.0, 16.0, 32.0];
        for m in [
            inertia_matrix(&c.view(), &w.view()),
            geometric_matrix(&c.view(), &w.view()),
        ] {
            let (values, axes) = principal_axes(&m);
            assert!(
                values[0] <= values[1] && values[1] <= values[2],
                "{values:?}"
            );
            for i in 0..3 {
                let n: f64 = axes[i].iter().map(|x| x * x).sum();
                assert!((n - 1.0).abs() < 1e-12, "axis {i} not unit: {n}");
                for j in (i + 1)..3 {
                    let d: f64 = (0..3).map(|k| axes[i][k] * axes[j][k]).sum();
                    assert!(d.abs() < 1e-12, "axes {i},{j} not orthogonal: {d}");
                }
            }
        }
    }

    /// The defining property, which no sign convention can affect.
    #[test]
    fn each_axis_satisfies_the_eigenvalue_equation() {
        let c = array![
            [1.0, 0.0, 0.5],
            [0.0, 2.0, -1.0],
            [-1.5, 0.3, 2.0],
            [0.7, -1.1, 0.2]
        ];
        let w = array![1.0, 12.0, 14.0, 16.0];
        let m = inertia_matrix(&c.view(), &w.view());
        let (values, axes) = principal_axes(&m);
        for i in 0..3 {
            for k in 0..3 {
                let mv: f64 = (0..3).map(|j| m[k][j] * axes[i][j]).sum();
                assert!(
                    (mv - values[i] * axes[i][k]).abs() < 1e-9,
                    "axis {i} component {k}: {mv} vs {}",
                    values[i] * axes[i][k]
                );
            }
        }
    }

    #[test]
    fn the_sign_convention_is_deterministic() {
        let mut v = [-0.9, 0.1, 0.2];
        fix_sign(&mut v);
        assert!(v[0] > 0.0, "largest component must end positive: {v:?}");
        let mut u = [0.1, -0.95, 0.2];
        fix_sign(&mut u);
        assert!(
            u[1] > 0.0 && u[0] < 0.0,
            "only the leading component sets the sign: {u:?}"
        );
    }
}
