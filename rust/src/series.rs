//! Block 10b — `molsysmt.lib.series`: run-length encoding of integer series and the
//! serialisation behind `serialized_lists`.
//!
//! Two kernels in the replaced Numba implementation indexed `serie[0]` before checking
//! the length, so an empty input was
//! an unchecked out-of-bounds read under `njit` (`serie_to_chunks` also returns a
//! one-element result built from whatever that read produced). The oracle is undefined
//! there, so these ports return empty output instead, and a parity test pins that the
//! divergence exists only for the empty case.
//!
//! `_jit_serialize` took a Numba typed list of typed lists in the replaced implementation;
//! the Rust port takes
//! an ordinary Python sequence of sequences, which the seam feeds from the same source.
//! Note that it **sorts each segment** — that behavior is inherited from the replaced
//! Numba implementation, not added here.

use numpy::ndarray::Array1;
use numpy::{IntoPyArray, PyArray1, PyReadonlyArray1};
use pyo3::prelude::*;
use std::collections::HashMap;

/// Splits a series into maximal runs of consecutive integers (steps of exactly 1).
/// Mirrors `serie_to_chunks`, returning `(starts, chunk_size)`.
#[pyfunction]
pub fn serie_to_chunks<'py>(
    py: Python<'py>,
    serie: PyReadonlyArray1<'py, i64>,
) -> (Bound<'py, PyArray1<i64>>, Bound<'py, PyArray1<i64>>) {
    let s = serie.as_array();
    let n = s.len();
    if n == 0 {
        return (
            Array1::<i64>::zeros(0).into_pyarray(py),
            Array1::<i64>::zeros(0).into_pyarray(py),
        );
    }
    let mut starts: Vec<i64> = Vec::new();
    let mut sizes: Vec<i64> = Vec::new();
    let mut start_idx = 0usize;
    for i in 1..n {
        if s[i] - s[i - 1] > 1 {
            starts.push(s[start_idx]);
            sizes.push((i - start_idx) as i64);
            start_idx = i;
        }
    }
    starts.push(s[start_idx]);
    sizes.push((n - start_idx) as i64);
    (
        Array1::from_vec(starts).into_pyarray(py),
        Array1::from_vec(sizes).into_pyarray(py),
    )
}

/// Inverse of [`serie_to_chunks`].
#[pyfunction]
pub fn chunks_to_serie<'py>(
    py: Python<'py>,
    starts: PyReadonlyArray1<'py, i64>,
    chunk_size: PyReadonlyArray1<'py, i64>,
) -> Bound<'py, PyArray1<i64>> {
    let (st, cs) = (starts.as_array(), chunk_size.as_array());
    let total: i64 = cs.iter().sum();
    let mut out = Vec::with_capacity(total.max(0) as usize);
    for (&start, &size) in st.iter().zip(cs.iter()) {
        for k in 0..size {
            out.push(start + k);
        }
    }
    Array1::from_vec(out).into_pyarray(py)
}

/// Flattens a sequence of sequences into `(starts, values)`, sorting each segment.
/// `starts` has one extra trailing entry holding the total length.
#[pyfunction]
pub fn jit_serialize<'py>(
    py: Python<'py>,
    item: Vec<Vec<i64>>,
) -> (Bound<'py, PyArray1<i64>>, Bound<'py, PyArray1<i64>>) {
    let n_values: usize = item.iter().map(|s| s.len()).sum();
    let mut values = Vec::with_capacity(n_values);
    let mut starts = Vec::with_capacity(item.len() + 1);
    for segment in item.iter() {
        starts.push(values.len() as i64);
        let mut sorted = segment.clone();
        sorted.sort_unstable();
        values.extend_from_slice(&sorted);
    }
    starts.push(values.len() as i64);
    (
        Array1::from_vec(starts).into_pyarray(py),
        Array1::from_vec(values).into_pyarray(py),
    )
}

/// Ranks each value by the order in which it first appears.
#[pyfunction]
pub fn occurrence_order<'py>(
    py: Python<'py>,
    serie: PyReadonlyArray1<'py, i64>,
) -> Bound<'py, PyArray1<i64>> {
    let s = serie.as_array();
    let mut seen: HashMap<i64, i64> = HashMap::with_capacity(s.len());
    let mut next = 0i64;
    let mut out = Vec::with_capacity(s.len());
    for &v in s.iter() {
        let rank = *seen.entry(v).or_insert_with(|| {
            let r = next;
            next += 1;
            r
        });
        out.push(rank);
    }
    Array1::from_vec(out).into_pyarray(py)
}

/// Same ranking, but exploiting a sorted input: a new rank starts at every value change.
/// Note this does *not* agree with [`occurrence_order`] on unsorted input — the replaced Numba implementation
/// offers both and the caller picks; the parity tests cover each on its own terms.
#[pyfunction]
pub fn occurrence_order_sorted_serie<'py>(
    py: Python<'py>,
    serie: PyReadonlyArray1<'py, i64>,
) -> Bound<'py, PyArray1<i64>> {
    let s = serie.as_array();
    if s.is_empty() {
        return Array1::<i64>::zeros(0).into_pyarray(py);
    }
    let mut out = Vec::with_capacity(s.len());
    let mut rank = 0i64;
    let mut previous = s[0];
    for &v in s.iter() {
        if v != previous {
            previous = v;
            rank += 1;
        }
        out.push(rank);
    }
    Array1::from_vec(out).into_pyarray(py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(serie_to_chunks, m)?)?;
    m.add_function(wrap_pyfunction!(chunks_to_serie, m)?)?;
    m.add_function(wrap_pyfunction!(jit_serialize, m)?)?;
    m.add_function(wrap_pyfunction!(occurrence_order, m)?)?;
    m.add_function(wrap_pyfunction!(occurrence_order_sorted_serie, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    /// The chunking logic, exercised without the Python layer.
    fn chunks(s: &[i64]) -> (Vec<i64>, Vec<i64>) {
        let n = s.len();
        if n == 0 {
            return (vec![], vec![]);
        }
        let (mut starts, mut sizes, mut start_idx) = (vec![], vec![], 0usize);
        for i in 1..n {
            if s[i] - s[i - 1] > 1 {
                starts.push(s[start_idx]);
                sizes.push((i - start_idx) as i64);
                start_idx = i;
            }
        }
        starts.push(s[start_idx]);
        sizes.push((n - start_idx) as i64);
        (starts, sizes)
    }

    #[test]
    fn a_fully_consecutive_series_is_one_chunk() {
        let (starts, sizes) = chunks(&[5, 6, 7, 8]);
        assert_eq!(starts, vec![5]);
        assert_eq!(sizes, vec![4]);
    }

    #[test]
    fn gaps_split_chunks_but_repeats_do_not() {
        // a step of 0 or a negative step is *not* a gap: only steps > 1 split.
        let (starts, sizes) = chunks(&[1, 2, 4, 4, 5, 9]);
        assert_eq!(starts, vec![1, 4, 9]);
        assert_eq!(sizes, vec![2, 3, 1]);
        assert_eq!(
            sizes.iter().sum::<i64>(),
            6,
            "every element lands in exactly one chunk"
        );
    }

    #[test]
    fn chunking_round_trips_through_expansion() {
        let serie: Vec<i64> = vec![0, 1, 2, 7, 8, 20];
        let (starts, sizes) = chunks(&serie);
        let mut back = Vec::new();
        for (s, n) in starts.iter().zip(sizes.iter()) {
            for k in 0..*n {
                back.push(s + k);
            }
        }
        assert_eq!(back, serie);
    }

    #[test]
    fn empty_input_yields_no_chunks() {
        let (starts, sizes) = chunks(&[]);
        assert!(
            starts.is_empty() && sizes.is_empty(),
            "the replaced Numba implementation read serie[0] out of bounds here; this port returns nothing"
        );
    }
}
