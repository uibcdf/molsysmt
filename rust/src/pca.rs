//! Block 13 — `principal_component_analysis`, the last CPU kernel (97/97).
//!
//! Weighted PCA over a trajectory: flatten each structure to a `3·n_atoms` feature
//! vector, weight-centre it, form the covariance, and diagonalise. Feature `xx` is
//! `jj*n_atoms + ii` — all x-coordinates, then all y, then all z — matching upstream's
//! `aux_ind`. Eigenvalues come back ascending and the eigenvector matrix is transposed,
//! so row `i` of the result is the `i`-th principal component.
//!
//! # Two deliberate departures from a faithful port
//!
//! 1. **The covariance is a matrix product, not the triple loop.** Upstream builds `cov`
//!    with an `O(n_structures · n_features²)` scalar loop; this is exactly `Xc^T Xc`, a
//!    BLAS rank-k update. `faer` does it 48-132x faster (measured — see
//!    `devguide/pending_proposals/linear_algebra_backend_for_rust_kernels.md`). This is
//!    the one kernel where the faithful port would have preserved a mis-transcribed
//!    matrix multiply, so the redesign *is* the point of porting it.
//!
//! 2. **`faer`, not `nalgebra`.** The matrix is `3N × 3N` (2400×2400 for an 800-atom
//!    system), i.e. genuinely large and dense, which is `faer`'s domain; `nalgebra` is for
//!    small fixed-size matrices and is used elsewhere in this crate for the 3x3/4x4 cases.
//!    Still no BLAS system dependency — `faer` is pure Rust, so the self-contained wheel
//!    survives.
//!
//! # Parity is at tolerance, and the eigenvectors need care
//!
//! Different covariance summation order, a different eigensolver from LAPACK, and Numba's
//! `fastmath` all put the usual ~1e-12 floor under the eigenvalues. The eigen*vectors* are
//! worse than that: like the principal axes they carry a **sign** ambiguity (fixed here
//! deterministically, largest-magnitude component positive), and — unique to PCA — a
//! **degeneracy** problem. When `n_structures < n_features` the covariance is rank
//! deficient, so a large null space shares eigenvalue 0 and its eigenvectors are an
//! arbitrary orthonormal basis of that subspace; even up to sign they are not comparable.
//! The parity tests therefore compare eigenvectors only where the eigenvalue is nonzero
//! and well separated, and otherwise assert the defining property `cov v = λ v`.
//! See `devguide/pending_bugs/principal_axes_eigenvector_sign_unspecified.md`.

use faer::{Mat, Par, Side};
use numpy::ndarray::{Array1, Array2};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray1, PyReadonlyArray3};
use pyo3::prelude::*;
use std::sync::Mutex;

static FAER_PARALLELISM_LOCK: Mutex<()> = Mutex::new(());

/// Makes the largest-magnitude component positive, so an eigenvector is reproducible
/// across backends and platforms despite the intrinsic sign freedom.
#[inline]
fn fix_sign(v: &mut [f64]) {
    let mut lead = 0usize;
    for k in 1..v.len() {
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

#[pyfunction]
pub fn principal_component_analysis<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    weights: PyReadonlyArray1<'py, f64>,
    num_threads: usize,
) -> (Bound<'py, PyArray1<f64>>, Bound<'py, PyArray2<f64>>) {
    let c = coordinates.as_array();
    let w = weights.as_array();
    let (ns, na) = (c.shape()[0], c.shape()[1]);
    let nf = na * 3;

    // feature index xx = jj*na + ii  ->  (ii, jj) = (xx % na, xx / na)
    let atom_of = |xx: usize| (xx % na, xx / na);

    // per-feature mean and sqrt-weight
    let mut mean = vec![0.0f64; nf];
    for xx in 0..nf {
        let (ii, jj) = atom_of(xx);
        let mut acc = 0.0;
        for l in 0..ns {
            acc += c[[l, ii, jj]];
        }
        mean[xx] = acc / ns as f64;
    }
    let wpf: Vec<f64> = (0..nf).map(|xx| w[atom_of(xx).0].sqrt()).collect();

    // Xc[l, xx] = (coord - mean) * sqrt(weight); then cov = Xc^T Xc / ns (rank-k update)
    let xc = Mat::from_fn(ns, nf, |l, xx| {
        let (ii, jj) = atom_of(xx);
        (c[[l, ii, jj]] - mean[xx]) * wpf[xx]
    });
    let inv_ns = 1.0 / ns as f64;

    // The covariance (rank-k update) and its dense eigendecomposition are the whole cost,
    // and neither touches Python, so release the GIL and let faer use the cores. The
    // high-level `self_adjoint_eigen` reads faer's global parallelism, which defaults to
    // sequential — leaving it unset was a ~3x self-inflicted slowdown on large matrices.
    //
    let (values, vectors) = py.allow_threads(|| crate::threads::install(num_threads, || {
        let _parallelism_guard = FAER_PARALLELISM_LOCK
            .lock()
            .unwrap_or_else(|poisoned| poisoned.into_inner());
        faer::set_global_parallelism(Par::rayon(num_threads));
        let gram = xc.transpose() * xc.as_ref();
        let cov = Mat::from_fn(nf, nf, |i, j| gram[(i, j)] * inv_ns);
        let eig = cov
            .self_adjoint_eigen(Side::Lower)
            .expect("covariance eigendecomposition failed");
        let s = eig.S();
        let u = eig.U();
        let mut vals = vec![0.0f64; nf];
        let mut vecs = vec![0.0f64; nf * nf];
        for k in 0..nf {
            vals[k] = *s.column_vector().get(k);
            let mut v: Vec<f64> = (0..nf).map(|r| *u.get(r, k)).collect();
            fix_sign(&mut v);
            // row k is the k-th component (upstream transposes the eigenvector matrix)
            vecs[k * nf..(k + 1) * nf].copy_from_slice(&v);
        }
        (vals, vecs)
    }));

    let eigenvalues = Array1::from_vec(values);
    let eigenvectors = Array2::from_shape_vec((nf, nf), vectors).unwrap();
    (eigenvalues.into_pyarray(py), eigenvectors.into_pyarray(py))
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(principal_component_analysis, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use numpy::ndarray::Array3;

    /// Builds the covariance the way the kernel does and returns (eigenvalues ascending,
    /// eigenvectors as rows), so the tests can check the maths without the Python layer.
    fn pca(coords: &Array3<f64>, w: &[f64]) -> (Vec<f64>, Vec<Vec<f64>>, Mat<f64>) {
        let (ns, na) = (coords.shape()[0], coords.shape()[1]);
        let nf = na * 3;
        let atom_of = |xx: usize| (xx % na, xx / na);
        let mut mean = vec![0.0f64; nf];
        for xx in 0..nf {
            let (ii, jj) = atom_of(xx);
            mean[xx] = (0..ns).map(|l| coords[[l, ii, jj]]).sum::<f64>() / ns as f64;
        }
        let wpf: Vec<f64> = (0..nf).map(|xx| w[atom_of(xx).0].sqrt()).collect();
        let xc = Mat::from_fn(ns, nf, |l, xx| {
            let (ii, jj) = atom_of(xx);
            (coords[[l, ii, jj]] - mean[xx]) * wpf[xx]
        });
        let gram = xc.transpose() * xc.as_ref();
        let cov = Mat::from_fn(nf, nf, |i, j| gram[(i, j)] / ns as f64);
        let eig = cov.self_adjoint_eigen(Side::Lower).unwrap();
        let s = eig.S();
        let u = eig.U();
        let vals: Vec<f64> = (0..nf).map(|k| *s.column_vector().get(k)).collect();
        let vecs: Vec<Vec<f64>> = (0..nf)
            .map(|k| {
                let mut v: Vec<f64> = (0..nf).map(|r| *u.get(r, k)).collect();
                fix_sign(&mut v);
                v
            })
            .collect();
        (vals, vecs, cov)
    }

    /// A cloud spread mostly along one axis must put its largest variance there.
    fn elongated_cloud() -> (Array3<f64>, Vec<f64>) {
        let ns = 40;
        let na = 3;
        let mut c = Array3::<f64>::zeros((ns, na, 3));
        for l in 0..ns {
            let t = l as f64 / ns as f64 - 0.5;
            for a in 0..na {
                c[[l, a, 0]] = 10.0 * t + a as f64; // wide spread along x
                c[[l, a, 1]] = 0.1 * t;
                c[[l, a, 2]] = 0.02 * t;
            }
        }
        (c, vec![1.0; na])
    }

    #[test]
    fn eigenvalues_are_ascending_and_nonnegative() {
        let (c, w) = elongated_cloud();
        let (vals, _, _) = pca(&c, &w);
        for k in 1..vals.len() {
            assert!(vals[k] >= vals[k - 1] - 1e-12, "not ascending: {vals:?}");
        }
        assert!(vals[0] >= -1e-9, "covariance must be PSD: {}", vals[0]);
    }

    #[test]
    fn the_dominant_component_lies_along_the_spread() {
        let (c, w) = elongated_cloud();
        let (_, vecs, _) = pca(&c, &w);
        // the last (largest-eigenvalue) component should load on the x-features (0..na)
        let top = vecs.last().unwrap();
        let na = 3;
        let x_load: f64 = (0..na).map(|i| top[i] * top[i]).sum();
        assert!(x_load > 0.99, "dominant PC should be the x spread, got load {x_load}");
    }

    #[test]
    fn every_eigenpair_satisfies_the_defining_equation() {
        let (c, w) = elongated_cloud();
        let (vals, vecs, cov) = pca(&c, &w);
        let nf = vals.len();
        for k in 0..nf {
            for r in 0..nf {
                let cv: f64 = (0..nf).map(|j| cov[(r, j)] * vecs[k][j]).sum();
                assert!((cv - vals[k] * vecs[k][r]).abs() < 1e-8,
                        "component {k} row {r}: {cv} vs {}", vals[k] * vecs[k][r]);
            }
        }
    }

    #[test]
    fn eigenvectors_are_orthonormal() {
        let (c, w) = elongated_cloud();
        let (_, vecs, _) = pca(&c, &w);
        let nf = vecs.len();
        for i in 0..nf {
            let norm: f64 = vecs[i].iter().map(|x| x * x).sum();
            assert!((norm - 1.0).abs() < 1e-10, "component {i} not unit: {norm}");
        }
        // check a couple of off-diagonal dot products
        let d: f64 = (0..nf).map(|k| vecs[0][k] * vecs[nf - 1][k]).sum();
        assert!(d.abs() < 1e-10, "components not orthogonal: {d}");
    }

    #[test]
    fn the_sign_convention_is_deterministic() {
        let mut v = vec![0.2, -0.9, 0.3];
        fix_sign(&mut v);
        assert!(v[1] > 0.0, "leading-magnitude component must end positive: {v:?}");
    }
}
