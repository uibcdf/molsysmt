//! Unweighted orthogonal plane fits on packed atom groups.
//!
//! Each group uses centered, scaled coordinates and a rectangular SVD, without
//! forming a covariance matrix. Only right singular vectors are computed.
//! Independent frames can use the configured Rayon pool; each worker keeps only
//! one group's workspace. Python owns physical units and periodic validation.

use faer::diag::Diag;
use faer::dyn_stack::{MemBuffer, MemStack};
use faer::linalg::svd::{svd, svd_scratch, ComputeSvdVectors};
use faer::{Mat, Par};
use numpy::ndarray::{Array2, Array3, ArrayView1, ArrayView3};
use numpy::{IntoPyArray, PyArray2, PyArray3, PyReadonlyArray1, PyReadonlyArray3};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use rayon::prelude::*;

struct Plane {
    center: [f64; 3],
    normal: [f64; 3],
    rms: f64,
    maximum: f64,
}

fn fit(
    c: &ArrayView3<f64>,
    frame: usize,
    atoms: ArrayView1<'_, i64>,
) -> Result<Plane, &'static str> {
    let anchor = [
        c[[frame, atoms[0] as usize, 0]],
        c[[frame, atoms[0] as usize, 1]],
        c[[frame, atoms[0] as usize, 2]],
    ];
    let mut mean = [0.0; 3];
    for &position in atoms {
        let atom = position as usize;
        for k in 0..3 {
            mean[k] += c[[frame, atom, k]] - anchor[k];
        }
    }
    for value in &mut mean {
        *value /= atoms.len() as f64;
    }
    let mut matrix = Mat::from_fn(atoms.len(), 3, |row, k| {
        (c[[frame, atoms[row] as usize, k]] - anchor[k]) - mean[k]
    });
    let mut scale = 0.0_f64;
    for &value in matrix.as_ref().col_iter().flat_map(|col| col.iter()) {
        if !value.is_finite() {
            return Err("unrepresentable centered coordinates");
        }
        scale = scale.max(value.abs());
    }
    if scale == 0.0 {
        return Err("coincident coordinates");
    }
    for col in matrix.as_mut().col_iter_mut() {
        for value in col.iter_mut() {
            *value /= scale;
        }
    }
    let mut s = Diag::zeros(3);
    let mut axes = Mat::zeros(3, 3);
    // Keep inner factorization sequential: the outer frame loop owns parallelism.
    // Explicit scratch avoids computing unused left vectors or a full n-by-n U.
    let mut scratch = MemBuffer::new(svd_scratch::<f64>(
        atoms.len(),
        3,
        ComputeSvdVectors::No,
        ComputeSvdVectors::Full,
        Par::Seq,
        Default::default(),
    ));
    svd(
        matrix.as_ref(),
        s.as_mut(),
        None,
        Some(axes.as_mut()),
        Par::Seq,
        MemStack::new(&mut scratch),
        Default::default(),
    )
    .map_err(|_| "plane SVD did not converge")?;
    let singular = [s[0], s[1], s[2]];
    if singular.iter().any(|value| !value.is_finite()) || s[1] - s[2] <= 1e-12 * s[0] {
        return Err("no unique normal (collinear or degenerate geometry)");
    }
    let mut normal = [axes[(0, 2)], axes[(1, 2)], axes[(2, 2)]];
    let mut pivot = 0;
    for k in 1..3 {
        if normal[k].abs() > normal[pivot].abs() {
            pivot = k;
        }
    }
    if normal[pivot] < 0.0 {
        for value in &mut normal {
            *value = -*value;
        }
    }
    let mut squared = 0.0;
    let mut maximum = 0.0_f64;
    for &position in atoms {
        let atom = position as usize;
        let mut residual = 0.0;
        for k in 0..3 {
            residual += ((c[[frame, atom, k]] - anchor[k]) - mean[k]) / scale * normal[k];
        }
        squared += residual * residual;
        maximum = maximum.max(residual.abs());
    }
    Ok(Plane {
        center: std::array::from_fn(|k| anchor[k] + mean[k]),
        normal,
        rms: (squared / atoms.len() as f64).sqrt() * scale,
        maximum: maximum * scale,
    })
}

type PlaneArrays<'py> = (
    Bound<'py, PyArray3<f64>>,
    Bound<'py, PyArray3<f64>>,
    Bound<'py, PyArray2<f64>>,
    Bound<'py, PyArray2<f64>>,
);

#[pyfunction]
pub fn get_least_squares_planes<'py>(
    py: Python<'py>,
    coordinates: PyReadonlyArray3<'py, f64>,
    atom_offsets: PyReadonlyArray1<'py, i64>,
    atom_positions: PyReadonlyArray1<'py, i64>,
    num_threads: usize,
) -> PyResult<PlaneArrays<'py>> {
    let c = coordinates.as_array();
    let offsets = atom_offsets.as_array();
    let positions = atom_positions.as_array();
    if num_threads == 0 || c.shape()[2] != 3 || c.iter().any(|value| !value.is_finite()) {
        return Err(PyValueError::new_err(
            "Finite (..., ..., 3) coordinates and positive thread count required.",
        ));
    }
    if offsets.is_empty() || offsets[0] != 0 || offsets[offsets.len() - 1] != positions.len() as i64
    {
        return Err(PyValueError::new_err(
            "Packed group offsets must span all positions from zero.",
        ));
    }
    for group in 0..offsets.len() - 1 {
        let (start, stop) = (offsets[group], offsets[group + 1]);
        if start < 0 || stop < start || stop as usize > positions.len() || stop - start < 3 {
            return Err(PyValueError::new_err(
                "Every packed group requires at least three valid positions.",
            ));
        }
        for &position in positions.slice(numpy::ndarray::s![start as usize..stop as usize]) {
            if position < 0 || position as usize >= c.shape()[1] {
                return Err(PyValueError::new_err(
                    "Packed atom position is outside the coordinate axis.",
                ));
            }
        }
    }
    let (ns, ng) = (c.shape()[0], offsets.len() - 1);
    ns.checked_mul(ng)
        .and_then(|rows| rows.checked_mul(3))
        .ok_or_else(|| PyValueError::new_err("Plane output shape overflows address space."))?;
    // Frames are collected in source traversal order, so failures and outputs
    // are deterministic across thread counts. There is no per-group Python call.
    let frames: Vec<Result<Vec<Plane>, (usize, &'static str)>> = py.detach(|| {
        crate::threads::install(num_threads, || {
            (0..ns)
                .into_par_iter()
                .map(|frame| {
                    (0..ng)
                        .map(|group| {
                            let atoms = positions.slice(numpy::ndarray::s![
                                offsets[group] as usize..offsets[group + 1] as usize
                            ]);
                            fit(&c, frame, atoms).map_err(|reason| (group, reason))
                        })
                        .collect()
                })
                .collect()
        })
    });
    let mut centers = Array3::zeros((ns, ng, 3));
    let mut normals = Array3::zeros((ns, ng, 3));
    let mut rms = Array2::zeros((ns, ng));
    let mut maximum = Array2::zeros((ns, ng));
    for (frame, values) in frames.into_iter().enumerate() {
        let planes = values.map_err(|(group, reason)| {
            PyValueError::new_err(format!(
                "Plane group {group}, local structure {frame}: {reason}."
            ))
        })?;
        for (group, plane) in planes.into_iter().enumerate() {
            for k in 0..3 {
                centers[[frame, group, k]] = plane.center[k];
                normals[[frame, group, k]] = plane.normal[k];
            }
            rms[[frame, group]] = plane.rms;
            maximum[[frame, group]] = plane.maximum;
        }
    }
    Ok((
        centers.into_pyarray(py),
        normals.into_pyarray(py),
        rms.into_pyarray(py),
        maximum.into_pyarray(py),
    ))
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_least_squares_planes, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn factorization_buffers_fit_the_public_per_frame_workspace_estimate() {
        for n in [3, 4, 6, 12, 128, 10_000] {
            let matrix = Mat::<f64>::zeros(n, 3);
            let axes = Mat::<f64>::zeros(3, 3);
            let scratch = svd_scratch::<f64>(
                n,
                3,
                ComputeSvdVectors::No,
                ComputeSvdVectors::Full,
                Par::Seq,
                Default::default(),
            );
            let numeric_bytes = (matrix.col_stride() + axes.col_stride()) as usize * 3 * 8
                + 64
                + scratch.size_bytes();
            assert!(
                numeric_bytes <= 192 * n + 2048,
                "{n} atoms require {numeric_bytes} factorization bytes"
            );
        }
    }
}
