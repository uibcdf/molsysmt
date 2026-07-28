//! Rusterized (non-periodic) distance family.
//!
//! Faithful ports of `molsysmt.lib.structure.get_distances.*` — the vacuum
//! counterpart of `mic.rs`, and the most-used fallback path (the full distance matrix
//! behind `get_neighbors`/`get_contacts` when the cell list does not apply).
//!
//! The Numba versions call `get_distance_two_points_single_structure`, which does
//! `tmp_vect = point2 - point1` — one numpy allocation **per pair**, i.e. O(N^2)
//! allocations. The Rust ports use stack arithmetic. Same maths, bit-for-bit results.

use numpy::ndarray::{Array1, Array2, Array3, ArrayView2};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyArray3, PyReadonlyArray2, PyReadonlyArray3};
use pyo3::prelude::*;
use rayon::prelude::*;

use crate::symmetric::mirror_upper_to_lower;

#[inline(always)]
fn dist3(ax: f64, ay: f64, az: f64, bx: f64, by: f64, bz: f64) -> f64 {
    let dx = bx - ax;
    let dy = by - ay;
    let dz = bz - az;
    (dx * dx + dy * dy + dz * dz).sqrt()
}

// --------------------------------------------------------------------------- multi

#[pyfunction]
pub fn get_distances_single_system<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    num_threads: usize,
) -> Bound<'py, PyArray3<f64>> {
    let c = coordinates.as_array();
    let ns = c.shape()[0];
    let na = c.shape()[1];
    // Parallel over structures, mirroring the Numba kernel's prange; each structure
    // writes a disjoint slab so the result is unchanged.
    // Flat coordinate reads: `c[[s, k, 0]]` recomputes strides and bounds-checks on every
    // access, which by itself stops the pair loop vectorising. `as_standard_layout`
    // borrows when the input is already C-contiguous (the norm).
    let cc = c.as_standard_layout();
    let cs = cc.as_slice().expect("standard layout is contiguous");
    let flat: Vec<f64> = py.detach(|| {
        crate::threads::install(num_threads, || {
            (0..ns)
                .into_par_iter()
                .flat_map_iter(|s| {
                    let cst = &cs[s * na * 3..(s + 1) * na * 3];
                    let mut slab = vec![0.0f64; na * na];
                    // Upper triangle with unit-stride stores, then one blocked mirror pass:
                    // the interleaved `slab[k * na + j] = d` form cannot vectorise.
                    for j in 0..na {
                        let (ax, ay, az) = (cst[3 * j], cst[3 * j + 1], cst[3 * j + 2]);
                        let row = &mut slab[j * na..(j + 1) * na];
                        for k in (j + 1)..na {
                            row[k] = dist3(ax, ay, az, cst[3 * k], cst[3 * k + 1], cst[3 * k + 2]);
                        }
                    }
                    mirror_upper_to_lower(&mut slab, na);
                    slab.into_iter()
                })
                .collect()
        })
    });
    Array3::from_shape_vec((ns, na, na), flat)
        .unwrap()
        .into_pyarray(py)
}

#[pyfunction]
pub fn get_distances<'py>(
    py: Python<'py>,
    coordinates1: PyReadonlyArray3<'py, f64>,
    coordinates2: PyReadonlyArray3<'py, f64>,
    num_threads: usize,
) -> Bound<'py, PyArray3<f64>> {
    let c1 = coordinates1.as_array();
    let c2 = coordinates2.as_array();
    let ns = c1.shape()[0];
    let na1 = c1.shape()[1];
    let na2 = c2.shape()[1];
    let flat: Vec<f64> = py.detach(|| {
        crate::threads::install(num_threads, || {
            (0..ns)
                .into_par_iter()
                .flat_map_iter(|s| {
                    let mut slab = vec![0.0f64; na1 * na2];
                    for j in 0..na1 {
                        let (ax, ay, az) = (c1[[s, j, 0]], c1[[s, j, 1]], c1[[s, j, 2]]);
                        for k in 0..na2 {
                            slab[j * na2 + k] =
                                dist3(ax, ay, az, c2[[s, k, 0]], c2[[s, k, 1]], c2[[s, k, 2]]);
                        }
                    }
                    slab.into_iter()
                })
                .collect()
        })
    });
    Array3::from_shape_vec((ns, na1, na2), flat)
        .unwrap()
        .into_pyarray(py)
}

#[pyfunction]
pub fn get_distances_pairs<'py>(
    py: Python<'py>,
    coordinates1: PyReadonlyArray3<'py, f64>,
    coordinates2: PyReadonlyArray3<'py, f64>,
    num_threads: usize,
) -> Bound<'py, PyArray2<f64>> {
    let c1 = coordinates1.as_array();
    let c2 = coordinates2.as_array();
    let ns = c1.shape()[0];
    let na = c1.shape()[1];
    let mut flat = vec![0.0; ns * na];
    py.detach(|| {
        crate::threads::install(num_threads, || {
            flat.par_chunks_mut(na).enumerate().for_each(|(s, row)| {
                for j in 0..na {
                    row[j] = dist3(
                        c1[[s, j, 0]],
                        c1[[s, j, 1]],
                        c1[[s, j, 2]],
                        c2[[s, j, 0]],
                        c2[[s, j, 1]],
                        c2[[s, j, 2]],
                    );
                }
            })
        })
    });
    Array2::from_shape_vec((ns, na), flat)
        .unwrap()
        .into_pyarray(py)
}

// --------------------------------------------------------------------------- single structure

fn pairs_matrix_self(c: &ArrayView2<f64>) -> Array2<f64> {
    let na = c.shape()[0];
    let cc = c.as_standard_layout();
    let cs = cc.as_slice().expect("standard layout is contiguous");
    let mut flat = vec![0.0f64; na * na];
    // Flat coordinate reads, upper triangle with unit-stride stores, then one blocked
    // mirror pass; see `symmetric::mirror_upper_to_lower` for why the interleaved form
    // is slower and cannot vectorise.
    for j in 0..na {
        let (ax, ay, az) = (cs[3 * j], cs[3 * j + 1], cs[3 * j + 2]);
        let row = &mut flat[j * na..(j + 1) * na];
        for k in (j + 1)..na {
            row[k] = dist3(ax, ay, az, cs[3 * k], cs[3 * k + 1], cs[3 * k + 2]);
        }
    }
    mirror_upper_to_lower(&mut flat, na);
    Array2::from_shape_vec((na, na), flat).unwrap()
}

#[pyfunction]
pub fn get_distances_single_system_single_structure<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    pairs_matrix_self(&coordinates.as_array()).into_pyarray(py)
}

#[pyfunction]
pub fn get_distances_single_structure<'py>(
    py: Python<'py>,
    coordinates1: PyReadonlyArray2<'py, f64>,
    coordinates2: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let c1 = coordinates1.as_array();
    let c2 = coordinates2.as_array();
    let na1 = c1.shape()[0];
    let na2 = c2.shape()[0];
    let mut out = Array2::<f64>::zeros((na1, na2));
    for j in 0..na1 {
        let (ax, ay, az) = (c1[[j, 0]], c1[[j, 1]], c1[[j, 2]]);
        for k in 0..na2 {
            out[[j, k]] = dist3(ax, ay, az, c2[[k, 0]], c2[[k, 1]], c2[[k, 2]]);
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn get_distances_pairs_single_structure<'py>(
    py: Python<'py>,
    coordinates1: PyReadonlyArray2<'py, f64>,
    coordinates2: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let c1 = coordinates1.as_array();
    let c2 = coordinates2.as_array();
    let na = c1.shape()[0];
    let mut out = Array1::<f64>::zeros(na);
    for j in 0..na {
        out[j] = dist3(
            c1[[j, 0]],
            c1[[j, 1]],
            c1[[j, 2]],
            c2[[j, 0]],
            c2[[j, 1]],
            c2[[j, 2]],
        );
    }
    out.into_pyarray(py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_distances_single_system, m)?)?;
    m.add_function(wrap_pyfunction!(get_distances, m)?)?;
    m.add_function(wrap_pyfunction!(get_distances_pairs, m)?)?;
    m.add_function(wrap_pyfunction!(
        get_distances_single_system_single_structure,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(get_distances_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(get_distances_pairs_single_structure, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use numpy::ndarray::arr2;

    #[test]
    fn distance_is_symmetric_and_zero_on_the_diagonal() {
        let c = arr2(&[[0.0, 0.0, 0.0], [3.0, 4.0, 0.0], [1.0, 0.0, 0.0]]);
        let m = pairs_matrix_self(&c.view());
        assert_eq!(m[[0, 0]], 0.0);
        assert!((m[[0, 1]] - 5.0).abs() < 1e-15, "3-4-5 triangle");
        assert_eq!(m[[0, 1]], m[[1, 0]]);
        assert!((m[[0, 2]] - 1.0).abs() < 1e-15);
    }

    #[test]
    fn dist3_matches_euclidean() {
        assert!((dist3(0.0, 0.0, 0.0, 1.0, 2.0, 2.0) - 3.0).abs() < 1e-15);
        assert_eq!(dist3(1.5, -2.0, 7.0, 1.5, -2.0, 7.0), 0.0);
    }

    #[test]
    fn single_atom_matrix_is_one_by_one_zero() {
        let c = arr2(&[[1.0, 2.0, 3.0]]);
        let m = pairs_matrix_self(&c.view());
        assert_eq!(m.shape(), &[1, 1]);
        assert_eq!(m[[0, 0]], 0.0);
    }
}
