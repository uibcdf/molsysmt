//! Directed pair or Cartesian-product geometry using the shared MIC primitive.

use numpy::ndarray::{Array2, Array3};
use numpy::{IntoPyArray, PyArray2, PyArray3, PyReadonlyArray3};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use rayon::prelude::*;

use crate::mathlib::{fast_round_ties_even, inverse_matrix_3x3_full};
use crate::mic::{mic_vector, prep_dist};

type VectorArrays<'py> = (
    Bound<'py, PyArray3<f64>>,
    Bound<'py, PyArray2<f64>>,
    Bound<'py, PyArray3<f64>>,
    Bound<'py, PyArray3<i32>>,
);

#[pyfunction]
pub fn get_vectors<'py>(
    py: Python<'py>,
    coordinates1: PyReadonlyArray3<'py, f64>,
    coordinates2: PyReadonlyArray3<'py, f64>,
    boxes: Option<PyReadonlyArray3<'py, f64>>,
    pairs: bool,
    details: bool,
    num_threads: usize,
) -> PyResult<VectorArrays<'py>> {
    let c1 = coordinates1.as_array();
    let c2 = coordinates2.as_array();
    let ns = c1.shape()[0];
    let n1 = c1.shape()[1];
    let n2 = c2.shape()[1];
    if c1.shape()[2] != 3 || c2.shape()[2] != 3 || c2.shape()[0] != ns || (pairs && n1 != n2) {
        return Err(PyValueError::new_err(
            "Incompatible endpoint coordinate axes.",
        ));
    }
    // Borrow C-contiguous input, copying only unusual strided native callers.
    // Flat access avoids repeated ndarray stride/bounds work in the pair loop.
    let cc1 = c1.as_standard_layout();
    let cc2 = c2.as_standard_layout();
    let cs1 = cc1.as_slice().unwrap();
    let cs2 = cc2.as_slice().unwrap();
    if cs1.iter().chain(cs2.iter()).any(|v| !v.is_finite()) {
        return Err(PyValueError::new_err(
            "Endpoint coordinates must be finite.",
        ));
    }
    let nv = if pairs {
        n1
    } else {
        n1.checked_mul(n2)
            .ok_or_else(|| PyValueError::new_err("Vector count overflow."))?
    };
    let mut prepared = Vec::new();
    if let Some(ref boxes) = boxes {
        let b = boxes.as_array();
        if b.shape() != [ns, 3, 3] {
            return Err(PyValueError::new_err(
                "Boxes must match the first structure axis.",
            ));
        }
        for s in 0..ns {
            let cell = std::array::from_fn(|i| std::array::from_fn(|j| b[[s, i, j]]));
            let inverse = inverse_matrix_3x3_full(&cell);
            if cell
                .iter()
                .chain(inverse.iter())
                .flatten()
                .any(|v| !v.is_finite())
            {
                return Err(PyValueError::new_err(
                    "Periodic box must be finite and nonsingular.",
                ));
            }
            let (orthogonal, reduced, reduced_inverse) = prep_dist(&cell);
            prepared.push((cell, inverse, orthogonal, reduced, reduced_inverse));
        }
    }
    let mut vectors = Array3::<f64>::zeros((ns, nv, 3));
    let nd = if details { nv } else { 0 };
    let mut distances = Array2::<f64>::zeros((ns, nd));
    let mut directions = Array3::<f64>::zeros((ns, nd, 3));
    let mut images = Array3::<i32>::zeros((ns, nd, 3));
    if ns == 0 || nv == 0 {
        return Ok((
            vectors.into_pyarray(py),
            distances.into_pyarray(py),
            directions.into_pyarray(py),
            images.into_pyarray(py),
        ));
    }
    let v = vectors.as_slice_mut().unwrap();
    let mut d = distances.as_slice_mut().unwrap();
    let mut u = directions.as_slice_mut().unwrap();
    let mut im = images.as_slice_mut().unwrap();
    // Empty detail slices are split into one empty view per structure. Each
    // worker owns disjoint output; no per-pair arrays or dense index lists exist.
    let mut outputs = Vec::with_capacity(ns);
    for (s, vs) in v.chunks_mut(nv * 3).enumerate() {
        let (ds, dr) = d.split_at_mut(nd);
        let (us, ur) = u.split_at_mut(nd * 3);
        let (ims, ir) = im.split_at_mut(nd * 3);
        d = dr;
        u = ur;
        im = ir;
        outputs.push((s, vs, ds, us, ims));
    }
    py.detach(|| {
        crate::threads::install(num_threads, || {
            outputs.into_par_iter().try_for_each(
                |(s, vs, ds, us, ims)| -> Result<(), &'static str> {
                    for p in 0..nv {
                        let (a, b) = if pairs { (p, p) } else { (p / n2, p % n2) };
                        let i = (s * n1 + a) * 3;
                        let j = (s * n2 + b) * 3;
                        let raw = [
                            cs2[j] - cs1[i],
                            cs2[j + 1] - cs1[i + 1],
                            cs2[j + 2] - cs1[i + 2],
                        ];
                        if raw.iter().any(|x| !x.is_finite()) {
                            return Err("Unrepresentable endpoint displacement.");
                        }
                        let observed = if prepared.is_empty() {
                            raw
                        } else {
                            let (_, _, ortho, cell, inv) = &prepared[s];
                            mic_vector(raw, cell, inv, *ortho)
                        };
                        vs[3 * p..3 * p + 3].copy_from_slice(&observed);
                        if details {
                            let length = observed[0].hypot(observed[1]).hypot(observed[2]);
                            if !length.is_finite() {
                                return Err("Unrepresentable vector length.");
                            }
                            ds[p] = length;
                            for k in 0..3 {
                                us[3 * p + k] = if length > 0.0 {
                                    observed[k] / length
                                } else {
                                    f64::NAN
                                };
                            }
                            if !prepared.is_empty() {
                                let (cell, inv, _, _, _) = &prepared[s];
                                for k in 0..3 {
                                    let shift = (0..3)
                                        .map(|j| (observed[j] - raw[j]) * inv[j][k])
                                        .sum::<f64>();
                                    let rounded = fast_round_ties_even(shift);
                                    if !rounded.is_finite()
                                        || rounded < i32::MIN as f64
                                        || rounded > i32::MAX as f64
                                    {
                                        return Err("Periodic image exceeds int32 storage.");
                                    }
                                    ims[3 * p + k] = rounded as i32;
                                }
                                for k in 0..3 {
                                    let shift = (0..3)
                                        .map(|j| f64::from(ims[3 * p + j]) * cell[j][k])
                                        .sum::<f64>();
                                    if ((observed[k] - raw[k]) - shift).abs()
                                        > 1e-9 * (1.0 + shift.abs())
                                    {
                                        return Err(
                                            "Periodic image cannot be expressed in the box basis.",
                                        );
                                    }
                                }
                            }
                        }
                    }
                    Ok(())
                },
            )
        })
    })
    .map_err(PyValueError::new_err)?;
    Ok((
        vectors.into_pyarray(py),
        distances.into_pyarray(py),
        directions.into_pyarray(py),
        images.into_pyarray(py),
    ))
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_vectors, m)?)?;
    Ok(())
}
