//! Native MolSysMT kernels distributed in the private `molsysmt._rust` extension.
//!
//! Production numerical kernels use Rayon where parallel execution is beneficial.
//! The `threads` module caches pools by size so session defaults and per-call
//! overrides can coexist without resizing Rayon's global pool.

use numpy::ndarray::{Array1, Array2};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray1, PyReadonlyArray2};
use pyo3::prelude::*;
use rayon::prelude::*;

mod angles;
mod axes;
mod dihedral_ops;
mod dihedrals;
mod distances;
mod geometry;
mod mathlib;
mod mic;
mod neighbors;
mod pbc;
mod pca;
mod rmsd;
mod sasa;
mod series;
mod symmetric;
mod threads;
mod topology;

// --------------------------------------------------------------- synthetic bench probes

/// Evenly distributed points on the unit sphere (Fibonacci spiral).
#[pyfunction]
fn fibonacci_sphere_points(py: Python<'_>, n_points: usize) -> Bound<'_, PyArray2<f64>> {
    let golden_ratio = (1.0 + 5.0_f64.sqrt()) / 2.0;
    let n = n_points as f64;
    let mut data: Vec<f64> = Vec::with_capacity(n_points * 3);
    for i in 0..n_points {
        let fi = i as f64;
        let theta = (1.0 - 2.0 * (fi + 0.5) / n).acos();
        let phi = 2.0 * std::f64::consts::PI * fi / golden_ratio;
        data.push(theta.sin() * phi.cos());
        data.push(theta.sin() * phi.sin());
        data.push(theta.cos());
    }
    Array2::from_shape_vec((n_points, 3), data)
        .unwrap()
        .into_pyarray(py)
}

/// Regular arithmetic O(N^2): all-pairs squared distances.
#[pyfunction]
fn pairwise_sqdistances<'py>(
    py: Python<'py>,
    coords: PyReadonlyArray2<'py, f64>,
) -> Bound<'py, PyArray2<f64>> {
    let c = coords.as_array();
    let n = c.shape()[0];
    let mut out = Array2::<f64>::zeros((n, n));
    for i in 0..n {
        let (xi, yi, zi) = (c[[i, 0]], c[[i, 1]], c[[i, 2]]);
        for j in 0..n {
            let dx = xi - c[[j, 0]];
            let dy = yi - c[[j, 1]];
            let dz = zi - c[[j, 2]];
            out[[i, j]] = dx * dx + dy * dy + dz * dz;
        }
    }
    out.into_pyarray(py)
}

fn coords_to_vec(c: &numpy::ndarray::ArrayView2<f64>) -> Vec<[f64; 3]> {
    let n = c.shape()[0];
    (0..n).map(|i| [c[[i, 0]], c[[i, 1]], c[[i, 2]]]).collect()
}

/// Transcendental O(N^2): Coulomb-like potential (sqrt + division).
#[pyfunction]
fn coulomb_potential<'py>(
    py: Python<'py>,
    coords: PyReadonlyArray2<'py, f64>,
    charges: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let c = coords.as_array();
    let q = charges.as_array();
    let n = c.shape()[0];
    let mut out = Array1::<f64>::zeros(n);
    for i in 0..n {
        let (xi, yi, zi) = (c[[i, 0]], c[[i, 1]], c[[i, 2]]);
        let mut s = 0.0;
        for j in 0..n {
            if i == j {
                continue;
            }
            let dx = xi - c[[j, 0]];
            let dy = yi - c[[j, 1]];
            let dz = zi - c[[j, 2]];
            s += q[j] / (dx * dx + dy * dy + dz * dz).sqrt();
        }
        out[i] = s;
    }
    out.into_pyarray(py)
}

/// Transcendental + rayon (GIL released).
#[pyfunction]
fn coulomb_potential_parallel<'py>(
    py: Python<'py>,
    coords: PyReadonlyArray2<'py, f64>,
    charges: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let cv = coords_to_vec(&coords.as_array());
    let qv: Vec<f64> = charges.as_array().to_vec();
    let n = cv.len();
    let out: Vec<f64> = py.allow_threads(|| {
        (0..n)
            .into_par_iter()
            .map(|i| {
                let (xi, yi, zi) = (cv[i][0], cv[i][1], cv[i][2]);
                let mut s = 0.0;
                for j in 0..n {
                    if i == j {
                        continue;
                    }
                    let dx = xi - cv[j][0];
                    let dy = yi - cv[j][1];
                    let dz = zi - cv[j][2];
                    s += qv[j] / (dx * dx + dy * dy + dz * dz).sqrt();
                }
                s
            })
            .collect()
    });
    Array1::from_vec(out).into_pyarray(py)
}

/// Branchy / irregular ~O(N): per-atom neighbour count via a linked-cell grid.
#[pyfunction]
fn neighbor_counts<'py>(
    py: Python<'py>,
    coords: PyReadonlyArray2<'py, f64>,
    cutoff: f64,
) -> Bound<'py, PyArray1<i64>> {
    let c = coords.as_array();
    let n = c.shape()[0];
    let cv = coords_to_vec(&c);
    let cutoff_sq = cutoff * cutoff;

    let (mut xmin, mut ymin, mut zmin) = (cv[0][0], cv[0][1], cv[0][2]);
    let (mut xmax, mut ymax, mut zmax) = (cv[0][0], cv[0][1], cv[0][2]);
    for p in &cv {
        xmin = xmin.min(p[0]);
        xmax = xmax.max(p[0]);
        ymin = ymin.min(p[1]);
        ymax = ymax.max(p[1]);
        zmin = zmin.min(p[2]);
        zmax = zmax.max(p[2]);
    }
    let lx = (xmax - xmin + 1e-5).max(cutoff);
    let ly = (ymax - ymin + 1e-5).max(cutoff);
    let lz = (zmax - zmin + 1e-5).max(cutoff);
    let nx = ((lx / cutoff).floor() as i64).max(1); // libm-ok: synthetic bench probe, kept a faithful transcription
    let ny = ((ly / cutoff).floor() as i64).max(1); // libm-ok: synthetic bench probe, kept a faithful transcription
    let nz = ((lz / cutoff).floor() as i64).max(1); // libm-ok: synthetic bench probe, kept a faithful transcription
    let (dx, dy, dz) = (lx / nx as f64, ly / ny as f64, lz / nz as f64);

    let n_cells = (nx * ny * nz) as usize;
    let mut head = vec![-1i64; n_cells];
    let mut next = vec![-1i64; n];
    let cell_of = |p: &[f64; 3]| -> usize {
        let cx = (((p[0] - xmin) / dx).floor() as i64).clamp(0, nx - 1); // libm-ok: synthetic bench probe, kept a faithful transcription
        let cy = (((p[1] - ymin) / dy).floor() as i64).clamp(0, ny - 1); // libm-ok: synthetic bench probe, kept a faithful transcription
        let cz = (((p[2] - zmin) / dz).floor() as i64).clamp(0, nz - 1); // libm-ok: synthetic bench probe, kept a faithful transcription
        (cx + nx * (cy + ny * cz)) as usize
    };
    for (a, p) in cv.iter().enumerate() {
        let cell = cell_of(p);
        next[a] = head[cell];
        head[cell] = a as i64;
    }

    let mut out = Array1::<i64>::zeros(n);
    for i in 0..n {
        let p = &cv[i];
        let cx = (((p[0] - xmin) / dx).floor() as i64).clamp(0, nx - 1); // libm-ok: synthetic bench probe, kept a faithful transcription
        let cy = (((p[1] - ymin) / dy).floor() as i64).clamp(0, ny - 1); // libm-ok: synthetic bench probe, kept a faithful transcription
        let cz = (((p[2] - zmin) / dz).floor() as i64).clamp(0, nz - 1); // libm-ok: synthetic bench probe, kept a faithful transcription
        let mut cnt = 0i64;
        for ox in (cx - 1).max(0)..(cx + 2).min(nx) {
            for oy in (cy - 1).max(0)..(cy + 2).min(ny) {
                for oz in (cz - 1).max(0)..(cz + 2).min(nz) {
                    let cell = (ox + nx * (oy + ny * oz)) as usize;
                    let mut j = head[cell];
                    while j != -1 {
                        let ju = j as usize;
                        if ju != i {
                            let ddx = p[0] - cv[ju][0];
                            let ddy = p[1] - cv[ju][1];
                            let ddz = p[2] - cv[ju][2];
                            if ddx * ddx + ddy * ddy + ddz * ddz <= cutoff_sq {
                                cnt += 1;
                            }
                        }
                        j = next[ju];
                    }
                }
            }
        }
        out[i] = cnt;
    }
    out.into_pyarray(py)
}

#[pymodule]
fn _rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    threads::register(m)?;
    // Private production kernels.
    mathlib::register(m)?;
    mic::register(m)?;
    neighbors::register(m)?;
    sasa::register(m)?;
    angles::register(m)?;
    distances::register(m)?;
    dihedrals::register(m)?;
    dihedral_ops::register(m)?;
    pbc::register(m)?;
    geometry::register(m)?;
    series::register(m)?;
    topology::register(m)?;
    rmsd::register(m)?;
    axes::register(m)?;
    pca::register(m)?;
    // Synthetic bench probes.
    m.add_function(wrap_pyfunction!(fibonacci_sphere_points, m)?)?;
    m.add_function(wrap_pyfunction!(pairwise_sqdistances, m)?)?;
    m.add_function(wrap_pyfunction!(coulomb_potential, m)?)?;
    m.add_function(wrap_pyfunction!(coulomb_potential_parallel, m)?)?;
    m.add_function(wrap_pyfunction!(neighbor_counts, m)?)?;
    Ok(())
}
