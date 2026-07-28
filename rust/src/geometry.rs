//! Block 10a — weighted-geometry kernels: `get_center`, `flip`,
//! `get_radius_of_gyration` and `get_rmsf`.
//!
//! Accumulation order is the parity-critical part here: every one of these kernels is a
//! reduction, so summing in a different order changes the last bits. Each loop keeps
//! upstream's nesting exactly.
//!
//! Rayon distributes independent structure slabs. RMSF uses per-worker contiguous
//! accumulators and merges them after each pass, avoiding strided atom-major scans while
//! retaining vectorizable inner loops.

use numpy::ndarray::{Array1, Array2, Array3, ArrayView2, ArrayView3};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyArray3, PyReadonlyArray1, PyReadonlyArray2,
            PyReadonlyArray3};
use pyo3::prelude::*;
use rayon::prelude::*;

/// Weighted centre of one structure. Mirrors `get_center_single_structure`.
#[inline]
fn center_of(c: &ArrayView2<f64>, w: &numpy::ndarray::ArrayView1<f64>) -> [f64; 3] {
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

/// Weighted centre of structure `s` of a 3-D array.
#[inline]
fn center_at(c: &ArrayView3<f64>, s: usize, w: &numpy::ndarray::ArrayView1<f64>) -> [f64; 3] {
    let mut acc = [0.0f64; 3];
    let mut total = 0.0f64;
    for i in 0..c.shape()[1] {
        acc[0] += w[i] * c[[s, i, 0]];
        acc[1] += w[i] * c[[s, i, 1]];
        acc[2] += w[i] * c[[s, i, 2]];
        total += w[i];
    }
    [acc[0] / total, acc[1] / total, acc[2] / total]
}

/// Per-group weighted centres for one structure. The atom cursor runs straight through
/// `coordinates`, so groups are consecutive blocks of `atoms_per_group[k]` atoms.
#[inline]
fn centers_of_groups(
    c: &ArrayView2<f64>,
    atoms_per_group: &numpy::ndarray::ArrayView1<i64>,
    w: &numpy::ndarray::ArrayView1<f64>,
    out: &mut [f64],
) {
    let mut atom = 0usize;
    for (k, &n_in_group) in atoms_per_group.iter().enumerate() {
        let mut acc = [0.0f64; 3];
        let mut total = 0.0f64;
        for _ in 0..n_in_group {
            acc[0] += w[atom] * c[[atom, 0]];
            acc[1] += w[atom] * c[[atom, 1]];
            acc[2] += w[atom] * c[[atom, 2]];
            total += w[atom];
            atom += 1;
        }
        out[k * 3] = acc[0] / total;
        out[k * 3 + 1] = acc[1] / total;
        out[k * 3 + 2] = acc[2] / total;
    }
}

#[pyfunction]
pub fn get_center_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    weights: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = center_of(&coordinates.as_array(), &weights.as_array());
    Array1::from_vec(c.to_vec()).into_pyarray(py)
}

/// Shape is `(n_structures, 1, 3)` upstream — the middle axis is a singleton kept so the
/// result broadcasts against `(n_structures, n_atoms, 3)` coordinates.
#[pyfunction]
pub fn get_center<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    weights: PyReadonlyArray1<'py, f64>,
    num_threads: usize,
) -> Bound<'py, PyArray3<f64>> {
    let c = coordinates.as_array();
    let w = weights.as_array();
    let ns = c.shape()[0];
    let flat: Vec<f64> = py.allow_threads(|| crate::threads::install(num_threads, || {
        (0..ns).into_par_iter().flat_map(|s| center_at(&c, s, &w)).collect()
    }));
    Array3::from_shape_vec((ns, 1, 3), flat).unwrap().into_pyarray(py)
}

#[pyfunction]
pub fn get_center_groups_of_atoms_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    atoms_per_group: PyReadonlyArray1<'py, i64>,
    weights: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let g = atoms_per_group.as_array();
    let n_groups = g.len();
    let mut out = vec![0.0f64; n_groups * 3];
    centers_of_groups(&coordinates.as_array(), &g, &weights.as_array(), &mut out);
    Array2::from_shape_vec((n_groups, 3), out).unwrap().into_pyarray(py)
}

#[pyfunction]
pub fn get_center_groups_of_atoms<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    atoms_per_group: PyReadonlyArray1<'py, i64>,
    weights: PyReadonlyArray1<'py, f64>,
    num_threads: usize,
) -> Bound<'py, PyArray3<f64>> {
    let c = coordinates.as_array();
    let g = atoms_per_group.as_array();
    let w = weights.as_array();
    let (ns, n_groups) = (c.shape()[0], g.len());
    let flat: Vec<f64> = py.allow_threads(|| crate::threads::install(num_threads, || {
        (0..ns)
            .into_par_iter()
            .flat_map(|s| {
                let mut out = vec![0.0f64; n_groups * 3];
                centers_of_groups(&c.index_axis(numpy::ndarray::Axis(0), s), &g, &w, &mut out);
                out
            })
            .collect()
    }));
    Array3::from_shape_vec((ns, n_groups, 3), flat).unwrap().into_pyarray(py)
}

/// Reflection through the plane with normal `vector` passing through `point`.
///
/// Upstream computes `position - 2*dist*vector`, i.e. numpy scales the vector by the
/// scalar `2*dist`; the grouping is preserved here because `(2.0*dist)*v` and
/// `2.0*(dist*v)` need not agree in the last bit.
#[inline]
fn flip_point(p: [f64; 3], v: &[f64; 3], point: &[f64; 3]) -> [f64; 3] {
    let dist = (p[0] - point[0]) * v[0] + (p[1] - point[1]) * v[1] + (p[2] - point[2]) * v[2];
    let two_dist = 2.0 * dist;
    [p[0] - two_dist * v[0], p[1] - two_dist * v[1], p[2] - two_dist * v[2]]
}

#[pyfunction]
pub fn flip_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
    vector: PyReadonlyArray1<'py, f64>,
    point: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let c = coordinates.as_array();
    let (v, p) = (vector.as_array(), point.as_array());
    let (vv, pp) = ([v[0], v[1], v[2]], [p[0], p[1], p[2]]);
    let n = c.shape()[0];
    let mut out = Vec::with_capacity(n * 3);
    for i in 0..n {
        out.extend_from_slice(&flip_point([c[[i, 0]], c[[i, 1]], c[[i, 2]]], &vv, &pp));
    }
    Array2::from_shape_vec((n, 3), out).unwrap().into_pyarray(py)
}

#[pyfunction]
pub fn flip<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    vector: PyReadonlyArray1<'py, f64>,
    point: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray3<f64>> {
    let c = coordinates.as_array();
    let (v, p) = (vector.as_array(), point.as_array());
    let (vv, pp) = ([v[0], v[1], v[2]], [p[0], p[1], p[2]]);
    let (ns, na) = (c.shape()[0], c.shape()[1]);
    let mut out = Vec::with_capacity(ns * na * 3);
    for s in 0..ns {
        for i in 0..na {
            out.extend_from_slice(&flip_point([c[[s, i, 0]], c[[s, i, 1]], c[[s, i, 2]]], &vv, &pp));
        }
    }
    Array3::from_shape_vec((ns, na, 3), out).unwrap().into_pyarray(py)
}

#[inline]
fn radius_of_gyration_of(c: &ArrayView2<f64>, w: &numpy::ndarray::ArrayView1<f64>) -> f64 {
    let n = c.shape()[0];
    let (mut cx, mut cy, mut cz, mut total) = (0.0f64, 0.0f64, 0.0f64, 0.0f64);
    for i in 0..n {
        cx += w[i] * c[[i, 0]];
        cy += w[i] * c[[i, 1]];
        cz += w[i] * c[[i, 2]];
        total += w[i];
    }
    cx /= total;
    cy /= total;
    cz /= total;
    let mut sum_sq = 0.0f64;
    for i in 0..n {
        let (dx, dy, dz) = (c[[i, 0]] - cx, c[[i, 1]] - cy, c[[i, 2]] - cz);
        sum_sq += w[i] * (dx * dx + dy * dy + dz * dz);
    }
    (sum_sq / total).sqrt()
}

#[pyfunction]
pub fn get_radius_of_gyration_single_structure(
    coordinates: PyReadonlyArray2<'_, f64>,
    weights: PyReadonlyArray1<'_, f64>,
) -> f64 {
    radius_of_gyration_of(&coordinates.as_array(), &weights.as_array())
}

#[pyfunction]
pub fn get_radius_of_gyration<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    weights: PyReadonlyArray1<'py, f64>,
    num_threads: usize,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let w = weights.as_array();
    let ns = c.shape()[0];
    let out: Vec<f64> = py.allow_threads(|| crate::threads::install(num_threads, || {
        (0..ns)
            .into_par_iter()
            .map(|s| radius_of_gyration_of(&c.index_axis(numpy::ndarray::Axis(0), s), &w))
            .collect()
    }));
    Array1::from_vec(out).into_pyarray(py)
}

/// Root-mean-square fluctuation per atom. Parallel folds keep each structure slab
/// contiguous so the inner coordinate loops remain suitable for auto-vectorization.
#[pyfunction]
pub fn get_rmsf<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    num_threads: usize,
) -> Bound<'py, PyArray1<f64>> {
    let c = coordinates.as_array();
    let (ns, na) = (c.shape()[0], c.shape()[1]);
    let frame_size = na * 3;
    let nsf = ns as f64;
    let cc = c.as_standard_layout();
    let coordinates_flat = cc.as_slice().expect("standard layout is contiguous");
    let rmsf = py.allow_threads(|| crate::threads::install(num_threads, || {
        let sums = (0..ns)
            .into_par_iter()
            .fold(
                || vec![0.0; frame_size],
                |mut local, s| {
                    let frame = &coordinates_flat[s * frame_size..(s + 1) * frame_size];
                    for index in 0..frame_size {
                        local[index] += frame[index];
                    }
                    local
                },
            )
            .reduce(
                || vec![0.0; frame_size],
                |mut left, right| {
                    for index in 0..frame_size {
                        left[index] += right[index];
                    }
                    left
                },
            );
        let mean: Vec<f64> = sums.into_iter().map(|value| value / nsf).collect();
        let square_displacements = (0..ns)
            .into_par_iter()
            .fold(
                || vec![0.0; na],
                |mut local, s| {
                    let frame = &coordinates_flat[s * frame_size..(s + 1) * frame_size];
                    for atom in 0..na {
                        let offset = atom * 3;
                        let dx = frame[offset] - mean[offset];
                        let dy = frame[offset + 1] - mean[offset + 1];
                        let dz = frame[offset + 2] - mean[offset + 2];
                        local[atom] += dx * dx + dy * dy + dz * dz;
                    }
                    local
                },
            )
            .reduce(
                || vec![0.0; na],
                |mut left, right| {
                    for atom in 0..na {
                        left[atom] += right[atom];
                    }
                    left
                },
            );
        square_displacements
            .into_iter()
            .map(|value| (value / nsf).sqrt())
            .collect::<Vec<_>>()
    }));
    Array1::from_vec(rmsf).into_pyarray(py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_center_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_center, m)?)?;
    m.add_function(wrap_pyfunction!(get_center_groups_of_atoms_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_center_groups_of_atoms, m)?)?;
    m.add_function(wrap_pyfunction!(flip_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(flip, m)?)?;
    m.add_function(wrap_pyfunction!(get_radius_of_gyration_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_radius_of_gyration, m)?)?;
    m.add_function(wrap_pyfunction!(get_rmsf, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use numpy::ndarray::array;

    #[test]
    fn unweighted_centre_is_the_arithmetic_mean() {
        let c = array![[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [1.0, 3.0, 0.0]];
        let w = array![1.0, 1.0, 1.0];
        let got = center_of(&c.view(), &w.view());
        assert!((got[0] - 1.0).abs() < 1e-15);
        assert!((got[1] - 1.0).abs() < 1e-15);
        assert_eq!(got[2], 0.0);
    }

    #[test]
    fn a_dominant_weight_pulls_the_centre_onto_its_atom() {
        let c = array![[0.0, 0.0, 0.0], [10.0, 10.0, 10.0]];
        let w = array![1.0, 1.0e9];
        let got = center_of(&c.view(), &w.view());
        for k in 0..3 {
            assert!((got[k] - 10.0).abs() < 1e-6, "{:?}", got);
        }
    }

    /// Reflecting twice must return the original point, and a point on the plane must not
    /// move. Both hold only if the normal is a unit vector, which is the kernel's contract.
    #[test]
    fn flipping_twice_is_the_identity() {
        let v = [0.0, 0.0, 1.0];
        let point = [0.0, 0.0, 5.0];
        for p in [[1.0, 2.0, 3.0], [0.0, 0.0, 5.0], [-4.0, 7.0, 11.5]] {
            let once = flip_point(p, &v, &point);
            let twice = flip_point(once, &v, &point);
            for k in 0..3 {
                assert!((twice[k] - p[k]).abs() < 1e-12, "{:?} -> {:?} -> {:?}", p, once, twice);
            }
        }
        // a point on the mirror plane is fixed
        let on_plane = flip_point([3.0, 4.0, 5.0], &v, &point);
        assert!((on_plane[2] - 5.0).abs() < 1e-15);
    }

    #[test]
    fn radius_of_gyration_of_a_symmetric_pair_is_half_their_separation() {
        let c = array![[-3.0, 0.0, 0.0], [3.0, 0.0, 0.0]];
        let w = array![1.0, 1.0];
        assert!((radius_of_gyration_of(&c.view(), &w.view()) - 3.0).abs() < 1e-14);
    }

    #[test]
    fn group_centres_split_the_atom_run_by_group_size() {
        // two groups: atoms 0-1 and atoms 2-4
        let c = array![[0.0, 0.0, 0.0], [2.0, 0.0, 0.0],
                       [0.0, 3.0, 0.0], [0.0, 3.0, 0.0], [0.0, 6.0, 0.0]];
        let g = array![2i64, 3];
        let w = array![1.0, 1.0, 1.0, 1.0, 1.0];
        let mut out = vec![0.0; 6];
        centers_of_groups(&c.view(), &g.view(), &w.view(), &mut out);
        assert!((out[0] - 1.0).abs() < 1e-15, "{:?}", out);
        assert!((out[4] - 4.0).abs() < 1e-15, "{:?}", out);
    }
}
