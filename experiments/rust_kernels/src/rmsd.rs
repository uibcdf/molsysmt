//! Block 11 — the RMSD family: `get_rmsd`, `get_least_rmsd` and
//! `get_least_rmsd_rotation_and_translation` (9 kernels).
//!
//! `get_rmsd` is a plain reduction — no superposition, no linear algebra. The other two
//! superpose first, using the **quaternion (Horn/Kearsley) method**: build the 3x3
//! correlation matrix `R` between the centred coordinate sets, assemble the 4x4 symmetric
//! `F` from it, and take the eigenvector of its largest eigenvalue as a rotation
//! quaternion. The least RMSD follows from the largest eigenvalue alone, which is why
//! `get_least_rmsd` calls `eigvalsh` while the rotation kernel needs full `eigh`.
//!
//! **Eigensolver**: `nalgebra`'s `symmetric_eigen`, in pure Rust. The matrix is 4x4, so a
//! LAPACK dependency would buy nothing and would cost the self-contained wheel — see
//! `devguide/pending_proposals/linear_algebra_backend_for_rust_kernels.md`. numpy returns
//! eigenvalues in ascending order and upstream indexes `[3]` for the largest, so the
//! decomposition is sorted here to match that convention explicitly rather than relying
//! on the solver's ordering.
//!
//! **Parity is at tolerance, and unavoidably so**, for three independent reasons: Numba's
//! `fastmath=True` (see block 9), a different eigensolver from LAPACK's `dsyevx`, and
//! upstream's use of `np.sum` for the centroid, which sums pairwise rather than
//! sequentially. All three are last-bit effects.
//!
//! One thing that is *not* ambiguous: the eigenvector's sign. `q` and `-q` map to the same
//! rotation matrix, so the kernel output is well defined even though the quaternion is
//! not — which is what makes an ordinary tolerance comparison valid here, unlike for the
//! principal axes.

use nalgebra::SMatrix;
use numpy::ndarray::{Array1, Array3, Array4, ArrayView2};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyArray3, PyArray4, PyReadonlyArray2,
            PyReadonlyArray3};
use pyo3::prelude::*;
use rayon::prelude::*;

use crate::mathlib::{quaternion_to_rotation_matrix, Mat3, Vec3};

// ------------------------------------------------------------------ plain RMSD

#[inline]
fn msd_rows(a: &ArrayView2<f64>, b: &ArrayView2<f64>) -> f64 {
    let mut acc = 0.0;
    for i in 0..a.shape()[0] {
        let dx = b[[i, 0]] - a[[i, 0]];
        let dy = b[[i, 1]] - a[[i, 1]];
        let dz = b[[i, 2]] - a[[i, 2]];
        acc += dx * dx + dy * dy + dz * dz;
    }
    acc
}

#[pyfunction]
pub fn get_rmsd_single_structure(
    coordinates: PyReadonlyArray2<'_, f64>,
    reference_coordinates: PyReadonlyArray2<'_, f64>,
) -> f64 {
    let c = coordinates.as_array();
    let n = c.shape()[0] as f64;
    (msd_rows(&c, &reference_coordinates.as_array()) / n).sqrt()
}

#[pyfunction]
pub fn get_rmsd<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    reference_coordinates: PyReadonlyArray3<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let r = reference_coordinates.as_array();
    let (ns, na) = (c.shape()[0], c.shape()[1] as f64);
    let out: Vec<f64> = py.allow_threads(|| {
        (0..ns)
            .into_par_iter()
            .map(|s| {
                let cs = c.index_axis(numpy::ndarray::Axis(0), s);
                let rs = r.index_axis(numpy::ndarray::Axis(0), s);
                (msd_rows(&cs, &rs) / na).sqrt()
            })
            .collect()
    });
    Array1::from_vec(out).into_pyarray(py)
}

#[pyfunction]
pub fn get_rmsd_with_single_reference_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    reference_coordinates: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let r = reference_coordinates.as_array();
    let (ns, na) = (c.shape()[0], c.shape()[1] as f64);
    let out: Vec<f64> = py.allow_threads(|| {
        (0..ns)
            .into_par_iter()
            .map(|s| (msd_rows(&c.index_axis(numpy::ndarray::Axis(0), s), &r) / na).sqrt())
            .collect()
    });
    Array1::from_vec(out).into_pyarray(py)
}

// ------------------------------------------------------------------ superposition

/// Copies a coordinate block, centres it, and returns the centroid and the sum of squares
/// of the centred coordinates.
#[inline]
fn centre(view: &ArrayView2<f64>) -> (Vec<[f64; 3]>, Vec3, f64) {
    let n = view.shape()[0];
    let mut pts: Vec<[f64; 3]> =
        (0..n).map(|i| [view[[i, 0]], view[[i, 1]], view[[i, 2]]]).collect();
    let nf = n as f64;
    let mut centroid = [0.0f64; 3];
    let mut norm = 0.0f64;
    for k in 0..3 {
        let mut sum = 0.0;
        for p in pts.iter() {
            sum += p[k];
        }
        centroid[k] = sum / nf;
        let mut acc = 0.0;
        for p in pts.iter_mut() {
            p[k] -= centroid[k];
            acc += p[k] * p[k];
        }
        norm += acc;
    }
    (pts, centroid, norm)
}

/// `R[i][j] = sum_atoms x[:,i] * y[:,j]` — the correlation between the two centred sets.
#[inline]
fn correlation(x: &[[f64; 3]], y: &[[f64; 3]]) -> Mat3 {
    let mut r = [[0.0f64; 3]; 3];
    for i in 0..3 {
        for j in 0..3 {
            let mut acc = 0.0;
            for (xa, ya) in x.iter().zip(y.iter()) {
                acc += xa[i] * ya[j];
            }
            r[i][j] = acc;
        }
    }
    r
}

/// The 4x4 symmetric Kearsley matrix built from the correlation matrix.
#[inline]
fn kearsley(r: &Mat3) -> [f64; 16] {
    let f00 = r[0][0] + r[1][1] + r[2][2];
    let f10 = r[1][2] - r[2][1];
    let f20 = r[2][0] - r[0][2];
    let f30 = r[0][1] - r[1][0];
    let f11 = r[0][0] - r[1][1] - r[2][2];
    let f21 = r[0][1] + r[1][0];
    let f31 = r[0][2] + r[2][0];
    let f22 = -r[0][0] + r[1][1] - r[2][2];
    let f32 = r[1][2] + r[2][1];
    let f33 = -r[0][0] - r[1][1] + r[2][2];
    // row-major, symmetric
    [f00, f10, f20, f30,
     f10, f11, f21, f31,
     f20, f21, f22, f32,
     f30, f31, f32, f33]
}

/// Symmetric 4x4 eigendecomposition, sorted **ascending** to match numpy's convention
/// (upstream indexes `[3]` for the largest eigenvalue).
#[inline]
fn eigen_ascending(f: &[f64; 16]) -> ([f64; 4], [[f64; 4]; 4]) {
    let m = SMatrix::<f64, 4, 4>::from_row_slice(f);
    let e = m.symmetric_eigen();
    let mut order = [0usize, 1, 2, 3];
    order.sort_by(|&a, &b| e.eigenvalues[a].partial_cmp(&e.eigenvalues[b]).unwrap());
    let mut values = [0.0f64; 4];
    let mut vectors = [[0.0f64; 4]; 4]; // vectors[c] is the c-th eigenvector
    for (c, &src) in order.iter().enumerate() {
        values[c] = e.eigenvalues[src];
        for row in 0..4 {
            vectors[c][row] = e.eigenvectors[(row, src)];
        }
    }
    (values, vectors)
}

/// Least RMSD after optimal superposition, from the largest eigenvalue alone.
#[inline]
fn least_rmsd_of(x: &ArrayView2<f64>, y: &ArrayView2<f64>) -> f64 {
    let n = x.shape()[0] as f64;
    let (xc, _, x_norm) = centre(x);
    let (yc, _, y_norm) = centre(y);
    let (values, _) = eigen_ascending(&kearsley(&correlation(&xc, &yc)));
    let msd = ((x_norm + y_norm) - 2.0 * values[3]).max(0.0) / n;
    msd.sqrt()
}

/// Optimal superposition: the centre to rotate about, the rotation, and the translation.
#[inline]
fn superposition_of(x: &ArrayView2<f64>, y: &ArrayView2<f64>) -> (Vec3, Mat3, Vec3) {
    let (xc, centre_ref, _) = centre(x);
    let (yc, centre_y, _) = centre(y);
    let (_, vectors) = eigen_ascending(&kearsley(&correlation(&xc, &yc)));
    let q = vectors[3]; // eigenvector of the largest eigenvalue, as a quaternion
    let rot = quaternion_to_rotation_matrix(q);
    let rotation = [
        [rot[0][0], rot[1][0], rot[2][0]],
        [rot[0][1], rot[1][1], rot[2][1]],
        [rot[0][2], rot[1][2], rot[2][2]],
    ];
    let translation = [
        centre_ref[0] - centre_y[0],
        centre_ref[1] - centre_y[1],
        centre_ref[2] - centre_y[2],
    ];
    (centre_y, rotation, translation)
}

#[pyfunction]
pub fn get_least_rmsd_single_structure(
    coordinates: PyReadonlyArray2<'_, f64>,
    reference_coordinates: PyReadonlyArray2<'_, f64>,
) -> f64 {
    least_rmsd_of(&reference_coordinates.as_array(), &coordinates.as_array())
}

#[pyfunction]
pub fn get_least_rmsd<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    reference_coordinates: PyReadonlyArray3<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let r = reference_coordinates.as_array();
    let ns = c.shape()[0];
    let out: Vec<f64> = py.allow_threads(|| {
        (0..ns)
            .into_par_iter()
            .map(|s| {
                least_rmsd_of(
                    &r.index_axis(numpy::ndarray::Axis(0), s),
                    &c.index_axis(numpy::ndarray::Axis(0), s),
                )
            })
            .collect()
    });
    Array1::from_vec(out).into_pyarray(py)
}

#[pyfunction]
pub fn get_least_rmsd_with_single_reference_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    reference_coordinates: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let r = reference_coordinates.as_array();
    let ns = c.shape()[0];
    let out: Vec<f64> = py.allow_threads(|| {
        (0..ns)
            .into_par_iter()
            .map(|s| least_rmsd_of(&r, &c.index_axis(numpy::ndarray::Axis(0), s)))
            .collect()
    });
    Array1::from_vec(out).into_pyarray(py)
}

type Superposition<'py> = (Bound<'py, PyArray3<f64>>, Bound<'py, PyArray4<f64>>,
                           Bound<'py, PyArray3<f64>>);

fn pack(ns: usize, parts: Vec<(Vec3, Mat3, Vec3)>, py: Python<'_>) -> Superposition<'_> {
    let mut centres = Array3::<f64>::zeros((ns, 1, 3));
    let mut rotations = Array4::<f64>::zeros((ns, 1, 3, 3));
    let mut translations = Array3::<f64>::zeros((ns, 1, 3));
    for (s, (c, rot, t)) in parts.into_iter().enumerate() {
        for k in 0..3 {
            centres[[s, 0, k]] = c[k];
            translations[[s, 0, k]] = t[k];
            for j in 0..3 {
                rotations[[s, 0, k, j]] = rot[k][j];
            }
        }
    }
    (centres.into_pyarray(py), rotations.into_pyarray(py), translations.into_pyarray(py))
}

#[pyfunction]
pub fn get_least_rmsd_rotation_and_translation_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    reference_coordinates: PyReadonlyArray2<'py, f64>,
) -> (Bound<'py, PyArray1<f64>>, Bound<'py, PyArray2<f64>>, Bound<'py, PyArray1<f64>>) {
    let (c, rot, t) =
        superposition_of(&reference_coordinates.as_array(), &coordinates.as_array());
    let mut rotation = numpy::ndarray::Array2::<f64>::zeros((3, 3));
    for i in 0..3 {
        for j in 0..3 {
            rotation[[i, j]] = rot[i][j];
        }
    }
    (
        Array1::from_vec(c.to_vec()).into_pyarray(py),
        rotation.into_pyarray(py),
        Array1::from_vec(t.to_vec()).into_pyarray(py),
    )
}

#[pyfunction]
pub fn get_least_rmsd_rotation_and_translation<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    reference_coordinates: PyReadonlyArray3<'py, f64>,
) -> Superposition<'py> {
    let c = coordinates.as_array();
    let r = reference_coordinates.as_array();
    let ns = c.shape()[0];
    let parts: Vec<(Vec3, Mat3, Vec3)> = py.allow_threads(|| {
        (0..ns)
            .into_par_iter()
            .map(|s| {
                superposition_of(
                    &r.index_axis(numpy::ndarray::Axis(0), s),
                    &c.index_axis(numpy::ndarray::Axis(0), s),
                )
            })
            .collect()
    });
    pack(ns, parts, py)
}

#[pyfunction]
pub fn get_least_rmsd_rotation_and_translation_with_single_reference_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    reference_coordinates: PyReadonlyArray2<'py, f64>,
) -> Superposition<'py> {
    let c = coordinates.as_array();
    let r = reference_coordinates.as_array();
    let ns = c.shape()[0];
    let parts: Vec<(Vec3, Mat3, Vec3)> = py.allow_threads(|| {
        (0..ns)
            .into_par_iter()
            .map(|s| superposition_of(&r, &c.index_axis(numpy::ndarray::Axis(0), s)))
            .collect()
    });
    pack(ns, parts, py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_rmsd_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_rmsd, m)?)?;
    m.add_function(wrap_pyfunction!(get_rmsd_with_single_reference_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_least_rmsd_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_least_rmsd, m)?)?;
    m.add_function(wrap_pyfunction!(get_least_rmsd_with_single_reference_structure, m)?)?;
    m.add_function(wrap_pyfunction!(
        get_least_rmsd_rotation_and_translation_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_least_rmsd_rotation_and_translation, m)?)?;
    m.add_function(wrap_pyfunction!(
        get_least_rmsd_rotation_and_translation_with_single_reference_structure, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use numpy::ndarray::array;

    fn shape() -> numpy::ndarray::Array2<f64> {
        array![[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0],
               [1.0, 1.0, 0.0], [-1.0, 0.5, 2.0]]
    }

    #[test]
    fn eigenvalues_come_back_ascending() {
        let r = correlation(&centre(&shape().view()).0, &centre(&shape().view()).0);
        let (values, _) = eigen_ascending(&kearsley(&r));
        for k in 1..4 {
            assert!(values[k] >= values[k - 1], "not ascending: {:?}", values);
        }
    }

    #[test]
    fn least_rmsd_of_a_structure_with_itself_is_zero() {
        let s = shape();
        assert!(least_rmsd_of(&s.view(), &s.view()).abs() < 1e-12);
    }

    /// A pure translation must be removed entirely by the superposition.
    #[test]
    fn least_rmsd_is_blind_to_translation() {
        let s = shape();
        let mut moved = s.clone();
        for i in 0..moved.shape()[0] {
            moved[[i, 0]] += 10.0;
            moved[[i, 1]] -= 4.0;
            moved[[i, 2]] += 0.5;
        }
        assert!(least_rmsd_of(&s.view(), &moved.view()).abs() < 1e-10);
    }

    /// And so must a pure rotation — this is the part that exercises the eigensolver.
    #[test]
    fn least_rmsd_is_blind_to_rotation() {
        let s = shape();
        let (c, si) = (0.6f64, 0.8f64); // exact 3-4-5 rotation about z
        let mut turned = s.clone();
        for i in 0..turned.shape()[0] {
            let (x, y) = (s[[i, 0]], s[[i, 1]]);
            turned[[i, 0]] = c * x - si * y;
            turned[[i, 1]] = si * x + c * y;
        }
        assert!(least_rmsd_of(&s.view(), &turned.view()).abs() < 1e-10,
                "got {}", least_rmsd_of(&s.view(), &turned.view()));
    }

    /// The recovered rotation must actually map the centred structure onto the reference.
    #[test]
    fn the_reported_rotation_superposes_the_structures() {
        let s = shape();
        let (c, si) = (0.6f64, 0.8f64);
        let mut turned = s.clone();
        for i in 0..turned.shape()[0] {
            let (x, y) = (s[[i, 0]], s[[i, 1]]);
            turned[[i, 0]] = c * x - si * y + 7.0;
            turned[[i, 1]] = si * x + c * y - 2.0;
            turned[[i, 2]] = s[[i, 2]] + 1.0;
        }
        let (centre_rot, rotation, translation) =
            superposition_of(&s.view(), &turned.view());
        for i in 0..s.shape()[0] {
            let v = [turned[[i, 0]] - centre_rot[0], turned[[i, 1]] - centre_rot[1],
                     turned[[i, 2]] - centre_rot[2]];
            for k in 0..3 {
                let got = rotation[k][0] * v[0] + rotation[k][1] * v[1] + rotation[k][2] * v[2]
                    + centre_rot[k] + translation[k];
                assert!((got - s[[i, k]]).abs() < 1e-9,
                        "atom {i} axis {k}: {got} vs {}", s[[i, k]]);
            }
        }
    }

    /// The quaternion's sign is arbitrary but the rotation it encodes is not.
    #[test]
    fn negating_the_quaternion_leaves_the_rotation_unchanged() {
        let q = [0.3, -0.5, 0.7, 0.4];
        let a = quaternion_to_rotation_matrix(q);
        let b = quaternion_to_rotation_matrix([-q[0], -q[1], -q[2], -q[3]]);
        for i in 0..3 {
            for j in 0..3 {
                assert!((a[i][j] - b[i][j]).abs() < 1e-15);
            }
        }
    }

    #[test]
    fn plain_rmsd_counts_every_atom() {
        let a = array![[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]];
        let b = array![[3.0, 4.0, 0.0], [0.0, 0.0, 0.0]];
        // one atom displaced by 5, two atoms total => sqrt(25/2)
        let got = (msd_rows(&a.view(), &b.view()) / 2.0).sqrt();
        assert!((got - (12.5f64).sqrt()).abs() < 1e-14);
    }
}
