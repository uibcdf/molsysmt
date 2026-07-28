//! Shared vector/matrix helpers — faithful ports of `molsysmt.lib.math`.
//!
//! This module exists for two reasons: `math.py` is the single largest `njit` file in
//! the library (13 sites), and the earlier blocks had each re-implemented the same
//! helpers locally (`cross`, `dot`, `norm`, the 3x3 inverses, `angle`,
//! `dihedral_angle`). Consolidating them here removes that duplication and gives the
//! remaining blocks a common base — `rodrigues_rotation` unlocks the set/shift dihedral
//! kernels and `quaternion_to_rotation_matrix` unlocks the RMSD superposition family.
//!
//! [`fast_floor`] is here for a non-obvious reason: see its own documentation.
//!
//! Two distinct 3x3 inverses are deliberately kept apart:
//! - [`inverse_matrix_3x3`] is `math.py`'s, valid for the lower-triangular box
//!   convention (used by the MIC distance/angle/dihedral kernels);
//! - [`inverse_matrix_3x3_full`] is the general Cramer inverse that
//!   `neighbor_list`/`get_sasa` inline inside their own triclinic wrap.
//! They are not interchangeable; mixing them would silently change results.

use numpy::ndarray::{Array1, Array2};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray1, PyReadonlyArray2};
use pyo3::prelude::*;

pub type Vec3 = [f64; 3];
pub type Mat3 = [[f64; 3]; 3];

// --------------------------------------------------------------------------- floor

/// `x.floor()` without the libm call.
///
/// On the x86-64 **baseline** there is no floor instruction — `roundsd` is SSE4.1 — so
/// `f64::floor` lowers to an indirect call into libm. Every minimum-image wrap does three
/// of them per displacement vector, i.e. three calls in the innermost loop of the O(N^2)
/// distance kernels. Beyond their own cost, a call in the loop body makes the loop
/// **unvectorisable**: the shipped `get_mic_distances_single_system` emitted no packed
/// arithmetic at all, only `sqrtsd` between three `call *%rax`.
///
/// Truncate-and-correct is pure SSE2 (`cvttsd2si`/`cvtsi2sd`), inlines to a handful of
/// instructions, and is **exactly** `floor` on the domain these kernels use: fractional
/// coordinates and box ratios, i.e. small finite values.
///
/// Outside `|x| < 2^63` it is *not* a drop-in replacement (`as i64` saturates, and NaN maps
/// to 0), which is why it is a named helper with a documented domain rather than a blanket
/// replacement for `floor`. Never use it on unvalidated user input.
///
/// **This is an x86-64 fix, not a universal one.** The gap it closes is specific to the
/// x86-64 baseline ABI. AArch64's base ISA has `frintm`, so `f64::floor` is already a single
/// instruction there and the arithmetic version would only add work — hence the `cfg`. Any
/// future target should be checked the same way (does its baseline have a round-to-floor
/// instruction?) rather than assumed.
#[cfg(target_arch = "x86_64")]
#[inline(always)]
pub(crate) fn fast_floor(x: f64) -> f64 {
    let t = x as i64 as f64;
    // `as i64` truncates toward zero, so it overshoots by one on negative non-integers.
    // This compiles to a compare and a select, not a branch.
    let f = if t > x { t - 1.0 } else { t };
    // Truncation also loses the sign of zero, and `floor(-0.0)` is `-0.0`. Restoring x's
    // sign is unconditionally safe — `floor(x)` never has a sign opposite to `x` — and it
    // is two bitwise ops (`andpd`/`orpd`) rather than the third select that a `t == 0.0`
    // test would add, which measurably cost the vectorisation of the pair loops.
    f.copysign(x)
}

/// On targets whose baseline already has a floor instruction, use it.
#[cfg(not(target_arch = "x86_64"))]
#[inline(always)]
pub(crate) fn fast_floor(x: f64) -> f64 {
    x.floor() // libm-ok: this arm only exists for targets whose baseline has the instruction
}

/// `x.round_ties_even()` without the libm call, for the same reason as [`fast_floor`]:
/// `roundsd` is SSE4.1, so on the x86-64 baseline this is a call, and `unwrap` does three
/// per atom per structure.
///
/// The add-magic-number trick: adding and then subtracting `1.5 * 2^52` forces the mantissa
/// to drop every fractional bit under the *current* rounding mode, which is round-to-nearest,
/// ties-to-even — exactly the semantics Python and Numba use, and the reason this module
/// must not use `f64::round` (which rounds halves away from zero). Exact for
/// `|x| < 2^51`; the copysign restores the sign of zero as in [`fast_floor`].
#[cfg(target_arch = "x86_64")]
#[inline(always)]
pub(crate) fn fast_round_ties_even(x: f64) -> f64 {
    const MAGIC: f64 = 6755399441055744.0; // 1.5 * 2^52
    if x.abs() >= 2251799813685248.0 {
        // |x| >= 2^51: already integral, and the trick would overflow the mantissa.
        return x;
    }
    ((x + MAGIC) - MAGIC).copysign(x)
}

/// On targets whose baseline already has a round-to-nearest-even instruction, use it.
#[cfg(not(target_arch = "x86_64"))]
#[inline(always)]
pub(crate) fn fast_round_ties_even(x: f64) -> f64 {
    x.round_ties_even() // libm-ok: ditto — non-x86-64 baselines have the instruction
}

// --------------------------------------------------------------------------- vectors

#[inline]
pub(crate) fn dot_product(a: Vec3, b: Vec3) -> f64 {
    a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
}

#[inline]
pub(crate) fn cross_product(a: Vec3, b: Vec3) -> Vec3 {
    [
        a[1] * b[2] - a[2] * b[1],
        -a[0] * b[2] + a[2] * b[0],
        a[0] * b[1] - a[1] * b[0],
    ]
}

#[inline]
pub(crate) fn norm_vector(a: Vec3) -> f64 {
    (a[0] * a[0] + a[1] * a[1] + a[2] * a[2]).sqrt()
}

#[inline]
pub(crate) fn normalize_vector(a: Vec3) -> Vec3 {
    let n = norm_vector(a);
    [a[0] / n, a[1] / n, a[2] / n]
}

/// Mirrors math.py::angle — clamped acos of the normalised dot product.
#[inline]
pub(crate) fn angle(v0: Vec3, v1: Vec3) -> f64 {
    let mut cosa = dot_product(v0, v1) / (norm_vector(v0) * norm_vector(v1));
    if cosa >= 1.0 {
        cosa = 1.0;
    }
    if cosa <= -1.0 {
        cosa = -1.0;
    }
    cosa.acos()
}

/// Mirrors math.py::dihedral_angle, including the sign convention.
#[inline]
pub(crate) fn dihedral_angle(v0: Vec3, v1: Vec3, v2: Vec3) -> f64 {
    let aux0 = cross_product(v0, v1);
    let aux1 = cross_product(v1, v2);
    let mut cosa = dot_product(aux0, aux1) / (norm_vector(aux0) * norm_vector(aux1));
    if cosa >= 1.0 {
        cosa = 1.0;
    }
    if cosa <= -1.0 {
        cosa = -1.0;
    }
    let mut ang = cosa.acos();
    let aux2 = cross_product(aux0, aux1);
    if dot_product(aux2, v1) <= 0.0 {
        ang = -ang;
    }
    ang
}

/// Mirrors math.py::rodrigues_rotation. The Numba version rotates `vector` in place;
/// here we return the rotated vector (the caller writes it back).
#[inline]
pub(crate) fn rodrigues_rotation(vector: Vec3, unit_vector: Vec3, ang: f64) -> Vec3 {
    let cosa = ang.cos();
    let sina = ang.sin();
    let c = cross_product(unit_vector, vector);
    let d = dot_product(unit_vector, vector) * (1.0 - cosa);
    [
        vector[0] * cosa + c[0] * sina + d * unit_vector[0],
        vector[1] * cosa + c[1] * sina + d * unit_vector[1],
        vector[2] * cosa + c[2] * sina + d * unit_vector[2],
    ]
}

// --------------------------------------------------------------------------- matrices

/// Mirrors math.py::inverse_matrix_3x3 (lower-triangular box convention).
#[inline]
pub(crate) fn inverse_matrix_3x3(m: &Mat3) -> Mat3 {
    let mut inv = [[0.0; 3]; 3];
    inv[0][0] = 1.0 / m[0][0];
    inv[1][1] = 1.0 / m[1][1];
    inv[2][2] = 1.0 / m[2][2];
    inv[1][0] = -m[1][0] / (m[0][0] * m[1][1]);
    inv[2][0] = (m[1][0] * m[2][1] - m[2][0] * m[1][1]) / (m[0][0] * m[1][1] * m[2][2]);
    inv[2][1] = -m[2][1] / (m[1][1] * m[2][2]);
    inv
}

/// General 3x3 inverse (Cramer) — the one inlined in `neighbor_list` / `get_sasa`
/// triclinic wraps. NOT the same as [`inverse_matrix_3x3`].
#[inline]
pub(crate) fn inverse_matrix_3x3_full(b: &Mat3) -> Mat3 {
    let (b00, b01, b02) = (b[0][0], b[0][1], b[0][2]);
    let (b10, b11, b12) = (b[1][0], b[1][1], b[1][2]);
    let (b20, b21, b22) = (b[2][0], b[2][1], b[2][2]);
    let det = b00 * (b11 * b22 - b12 * b21) - b01 * (b10 * b22 - b12 * b20)
        + b02 * (b10 * b21 - b11 * b20);
    [
        [(b11 * b22 - b12 * b21) / det, (b02 * b21 - b01 * b22) / det, (b01 * b12 - b02 * b11) / det],
        [(b12 * b20 - b10 * b22) / det, (b00 * b22 - b02 * b20) / det, (b02 * b10 - b00 * b12) / det],
        [(b10 * b21 - b11 * b20) / det, (b01 * b20 - b00 * b21) / det, (b00 * b11 - b01 * b10) / det],
    ]
}

/// Mirrors math.py::quaternion_to_rotation_matrix.
#[inline]
pub(crate) fn quaternion_to_rotation_matrix(q: [f64; 4]) -> Mat3 {
    let (q0, q1, q2, q3) = (q[0], q[1], q[2], q[3]);
    let q00 = 2.0 * q0 * q0;
    let q11 = 2.0 * q1 * q1;
    let q22 = 2.0 * q2 * q2;
    let q33 = 2.0 * q3 * q3;
    let q01 = 2.0 * q0 * q1;
    let q02 = 2.0 * q0 * q2;
    let q03 = 2.0 * q0 * q3;
    let q12 = 2.0 * q1 * q2;
    let q13 = 2.0 * q1 * q3;
    let q23 = 2.0 * q2 * q3;
    [
        [q00 + q11 - 1.0, q12 - q03, q13 + q02],
        [q12 + q03, q00 + q22 - 1.0, q23 - q01],
        [q13 - q02, q23 + q01, q00 + q33 - 1.0],
    ]
}

// --------------------------------------------------------------------------- python API

#[pyfunction]
pub fn matmul<'py>(py: Python<'py>, m: PyReadonlyArray2<'py, f64>, v: PyReadonlyArray1<'py, f64>)
    -> Bound<'py, PyArray1<f64>> {
    let m = m.as_array();
    let v = v.as_array();
    let (rows, cols) = (m.shape()[0], m.shape()[1]);
    let mut out = Array1::<f64>::zeros(rows);
    for i in 0..rows {
        let mut acc = 0.0;
        for j in 0..cols {
            acc += m[[i, j]] * v[j];
        }
        out[i] = acc;
    }
    out.into_pyarray(py)
}

#[pyfunction]
pub fn transpmatmul<'py>(py: Python<'py>, m: PyReadonlyArray2<'py, f64>, v: PyReadonlyArray1<'py, f64>)
    -> Bound<'py, PyArray1<f64>> {
    let m = m.as_array();
    let v = v.as_array();
    let (rows, cols) = (m.shape()[0], m.shape()[1]);
    let mut out = Array1::<f64>::zeros(cols);
    for j in 0..rows {
        for i in 0..cols {
            out[i] += m[[j, i]] * v[j];
        }
    }
    out.into_pyarray(py)
}

fn v3(a: &numpy::ndarray::ArrayView1<f64>) -> Vec3 {
    [a[0], a[1], a[2]]
}

#[pyfunction]
#[pyo3(name = "dot_product")]
pub fn py_dot_product(a: PyReadonlyArray1<'_, f64>, b: PyReadonlyArray1<'_, f64>) -> f64 {
    dot_product(v3(&a.as_array()), v3(&b.as_array()))
}

#[pyfunction]
#[pyo3(name = "cross_product")]
pub fn py_cross_product<'py>(py: Python<'py>, a: PyReadonlyArray1<'py, f64>,
                             b: PyReadonlyArray1<'py, f64>) -> Bound<'py, PyArray1<f64>> {
    Array1::from_vec(cross_product(v3(&a.as_array()), v3(&b.as_array())).to_vec()).into_pyarray(py)
}

#[pyfunction]
#[pyo3(name = "norm_vector")]
pub fn py_norm_vector(a: PyReadonlyArray1<'_, f64>) -> f64 {
    norm_vector(v3(&a.as_array()))
}

#[pyfunction]
#[pyo3(name = "normalize_vector")]
pub fn py_normalize_vector<'py>(py: Python<'py>, a: PyReadonlyArray1<'py, f64>)
    -> Bound<'py, PyArray1<f64>> {
    Array1::from_vec(normalize_vector(v3(&a.as_array())).to_vec()).into_pyarray(py)
}

#[pyfunction]
#[pyo3(name = "angle")]
pub fn py_angle(a: PyReadonlyArray1<'_, f64>, b: PyReadonlyArray1<'_, f64>) -> f64 {
    angle(v3(&a.as_array()), v3(&b.as_array()))
}

#[pyfunction]
#[pyo3(name = "dihedral_angle")]
pub fn py_dihedral_angle(a: PyReadonlyArray1<'_, f64>, b: PyReadonlyArray1<'_, f64>,
                         c: PyReadonlyArray1<'_, f64>) -> f64 {
    dihedral_angle(v3(&a.as_array()), v3(&b.as_array()), v3(&c.as_array()))
}

#[pyfunction]
#[pyo3(name = "inverse_matrix_3x3")]
pub fn py_inverse_matrix_3x3<'py>(py: Python<'py>, m: PyReadonlyArray2<'py, f64>)
    -> Bound<'py, PyArray2<f64>> {
    let a = m.as_array();
    let mm: Mat3 = [
        [a[[0, 0]], a[[0, 1]], a[[0, 2]]],
        [a[[1, 0]], a[[1, 1]], a[[1, 2]]],
        [a[[2, 0]], a[[2, 1]], a[[2, 2]]],
    ];
    let inv = inverse_matrix_3x3(&mm);
    let mut out = Array2::<f64>::zeros((3, 3));
    for i in 0..3 {
        for j in 0..3 {
            out[[i, j]] = inv[i][j];
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
#[pyo3(name = "quaternion_to_rotation_matrix")]
pub fn py_quaternion_to_rotation_matrix<'py>(py: Python<'py>, q: PyReadonlyArray1<'py, f64>)
    -> Bound<'py, PyArray2<f64>> {
    let a = q.as_array();
    let u = quaternion_to_rotation_matrix([a[0], a[1], a[2], a[3]]);
    let mut out = Array2::<f64>::zeros((3, 3));
    for i in 0..3 {
        for j in 0..3 {
            out[[i, j]] = u[i][j];
        }
    }
    out.into_pyarray(py)
}

#[pyfunction]
#[pyo3(name = "rodrigues_rotation")]
pub fn py_rodrigues_rotation<'py>(py: Python<'py>, vector: PyReadonlyArray1<'py, f64>,
                                  unit_vector: PyReadonlyArray1<'py, f64>, ang: f64)
    -> Bound<'py, PyArray1<f64>> {
    let r = rodrigues_rotation(v3(&vector.as_array()), v3(&unit_vector.as_array()), ang);
    Array1::from_vec(r.to_vec()).into_pyarray(py)
}

// --------------------------------------------------------- minimum-distance kernels

/// Mirrors `math.py::minimum_distance_masked_not_bonded`: the shortest distance between
/// any two *included, non-bonded* atoms. Returns `+inf` when no such pair exists, matching
/// upstream's `np.inf`, so a caller probing for a clash can treat "nothing found" as
/// "infinitely far". The mask and bonded matrix are `u8` (0/non-zero), as upstream.
#[pyfunction]
pub fn minimum_distance_masked_not_bonded(
    coordinates: PyReadonlyArray2<'_, f64>,
    include_mask: PyReadonlyArray1<'_, u8>,
    bonded_matrix: PyReadonlyArray2<'_, u8>,
) -> f64 {
    let c = coordinates.as_array();
    let m = include_mask.as_array();
    let b = bonded_matrix.as_array();
    let n = c.shape()[0];
    let mut min_sq = f64::INFINITY;
    for i in 0..n.saturating_sub(1) {
        if m[i] == 0 {
            continue;
        }
        let (x1, y1, z1) = (c[[i, 0]], c[[i, 1]], c[[i, 2]]);
        for j in (i + 1)..n {
            if m[j] == 0 || b[[i, j]] != 0 {
                continue;
            }
            let dx = x1 - c[[j, 0]];
            let dy = y1 - c[[j, 1]];
            let dz = z1 - c[[j, 2]];
            let d = dx * dx + dy * dy + dz * dz;
            if d < min_sq {
                min_sq = d;
            }
        }
    }
    if min_sq.is_infinite() { f64::INFINITY } else { min_sq.sqrt() }
}

/// Mirrors `math.py::minimum_distance_between_coordinate_sets`: the shortest distance from
/// any included existing atom to any included candidate atom that is not bonded to it.
/// `candidate_start_index` offsets the candidate's local index into the (global) bonded
/// matrix. Returns `+inf` when no admissible pair exists.
#[pyfunction]
pub fn minimum_distance_between_coordinate_sets(
    existing_coordinates: PyReadonlyArray2<'_, f64>,
    existing_mask: PyReadonlyArray1<'_, u8>,
    candidate_coordinates: PyReadonlyArray2<'_, f64>,
    candidate_mask: PyReadonlyArray1<'_, u8>,
    candidate_start_index: i64,
    bonded_matrix: PyReadonlyArray2<'_, u8>,
) -> f64 {
    let e = existing_coordinates.as_array();
    let em = existing_mask.as_array();
    let cc = candidate_coordinates.as_array();
    let cm = candidate_mask.as_array();
    let b = bonded_matrix.as_array();
    let (n_existing, n_candidate) = (e.shape()[0], cc.shape()[0]);
    let mut min_sq = f64::INFINITY;
    for ei in 0..n_existing {
        if em[ei] == 0 {
            continue;
        }
        let (x1, y1, z1) = (e[[ei, 0]], e[[ei, 1]], e[[ei, 2]]);
        for cl in 0..n_candidate {
            if cm[cl] == 0 {
                continue;
            }
            let cg = (candidate_start_index + cl as i64) as usize;
            if b[[ei, cg]] != 0 {
                continue;
            }
            let dx = x1 - cc[[cl, 0]];
            let dy = y1 - cc[[cl, 1]];
            let dz = z1 - cc[[cl, 2]];
            let d = dx * dx + dy * dy + dz * dz;
            if d < min_sq {
                min_sq = d;
            }
        }
    }
    if min_sq.is_infinite() { f64::INFINITY } else { min_sq.sqrt() }
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(matmul, m)?)?;
    m.add_function(wrap_pyfunction!(minimum_distance_masked_not_bonded, m)?)?;
    m.add_function(wrap_pyfunction!(minimum_distance_between_coordinate_sets, m)?)?;
    m.add_function(wrap_pyfunction!(transpmatmul, m)?)?;
    m.add_function(wrap_pyfunction!(py_dot_product, m)?)?;
    m.add_function(wrap_pyfunction!(py_cross_product, m)?)?;
    m.add_function(wrap_pyfunction!(py_norm_vector, m)?)?;
    m.add_function(wrap_pyfunction!(py_normalize_vector, m)?)?;
    m.add_function(wrap_pyfunction!(py_angle, m)?)?;
    m.add_function(wrap_pyfunction!(py_dihedral_angle, m)?)?;
    m.add_function(wrap_pyfunction!(py_inverse_matrix_3x3, m)?)?;
    m.add_function(wrap_pyfunction!(py_quaternion_to_rotation_matrix, m)?)?;
    m.add_function(wrap_pyfunction!(py_rodrigues_rotation, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fast_floor_is_bit_identical_to_floor_on_the_kernel_domain() {
        // Exact integers, both signs of non-integers, ties, tiny and large magnitudes.
        let fixed = [
            0.0, -0.0, 1.0, -1.0, 2.0, -2.0, 0.5, -0.5, 1.5, -1.5, 2.5, -2.5, 0.9999999999,
            -0.9999999999, 1e-15, -1e-15, 3.7, -3.7, 1234.5678, -1234.5678, 1e6 + 0.5,
            -(1e6 + 0.5), 4503599627370495.5, -4503599627370495.5,
        ];
        for x in fixed {
            assert_eq!(
                fast_floor(x).to_bits(),
                x.floor().to_bits(),
                "fast_floor({x}) = {} but floor = {}",
                fast_floor(x),
                x.floor()
            );
        }
        // A deterministic sweep over the range the MIC wraps actually see: fractional
        // coordinates and box ratios, a few cells either side of the origin.
        let mut state = 0x9E3779B97F4A7C15u64;
        for _ in 0..200_000 {
            state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            let u = (state >> 11) as f64 / (1u64 << 53) as f64; // [0, 1)
            for scale in [1.0, 4.0, 100.0] {
                let x = (u - 0.5) * 2.0 * scale;
                assert_eq!(
                    fast_floor(x).to_bits(),
                    x.floor().to_bits(),
                    "fast_floor disagrees at x={x}"
                );
            }
        }
    }

    #[test]
    fn fast_round_ties_even_is_bit_identical_to_round_ties_even() {
        let fixed = [
            0.0, -0.0, 0.5, -0.5, 1.5, -1.5, 2.5, -2.5, 3.5, -3.5, 0.49999999999999994,
            -0.49999999999999994, 1.0, -1.0, 1e-15, -1e-15, 1234.5, -1234.5, 1234.4999999,
            2251799813685247.5, -2251799813685247.5, 4503599627370496.0, -4503599627370496.0,
            1e300, -1e300,
        ];
        for x in fixed {
            assert_eq!(
                fast_round_ties_even(x).to_bits(),
                x.round_ties_even().to_bits(),
                "fast_round_ties_even({x}) = {} but round_ties_even = {}",
                fast_round_ties_even(x),
                x.round_ties_even()
            );
        }
        let mut state = 0xD1B54A32D192ED03u64;
        for _ in 0..200_000 {
            state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            let u = (state >> 11) as f64 / (1u64 << 53) as f64;
            for scale in [1.0, 4.0, 100.0, 1e6] {
                let x = (u - 0.5) * 2.0 * scale;
                assert_eq!(
                    fast_round_ties_even(x).to_bits(),
                    x.round_ties_even().to_bits(),
                    "fast_round_ties_even disagrees at x={x}"
                );
            }
        }
    }

    #[test]
    fn the_two_inverses_agree_only_on_the_lower_triangular_convention() {
        // math.py's formula is derived for the lower-triangular box convention: there
        // it agrees with the general Cramer inverse and both are true inverses.
        let lower: Mat3 = [[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]];
        let a = inverse_matrix_3x3(&lower);
        let b = inverse_matrix_3x3_full(&lower);
        for i in 0..3 {
            for j in 0..3 {
                assert!((a[i][j] - b[i][j]).abs() < 1e-12, "lower ({i},{j})");
                let mut acc = 0.0;
                for k in 0..3 {
                    acc += b[i][k] * lower[k][j];
                }
                let expect = if i == j { 1.0 } else { 0.0 };
                assert!((acc - expect).abs() < 1e-12, "not an inverse at ({i},{j})");
            }
        }

        // On a general (non lower-triangular) matrix only the Cramer inverse is valid;
        // math.py's is not, which is exactly why the two must never be swapped.
        let general: Mat3 = [[2.0, 1.0, 0.5], [0.0, 3.0, 1.0], [1.0, 0.0, 4.0]];
        let ga = inverse_matrix_3x3(&general);
        let gb = inverse_matrix_3x3_full(&general);
        let mut ga_is_inverse = true;
        for i in 0..3 {
            for j in 0..3 {
                let mut acc = 0.0;
                for k in 0..3 {
                    acc += gb[i][k] * general[k][j];
                }
                let expect = if i == j { 1.0 } else { 0.0 };
                assert!((acc - expect).abs() < 1e-12, "Cramer must invert any matrix");

                let mut acc2 = 0.0;
                for k in 0..3 {
                    acc2 += ga[i][k] * general[k][j];
                }
                if (acc2 - expect).abs() > 1e-9 {
                    ga_is_inverse = false;
                }
            }
        }
        assert!(!ga_is_inverse,
                "math.py's inverse must NOT be a general inverse — the two are not interchangeable");
    }

    #[test]
    fn quaternion_identity_gives_the_identity_matrix() {
        let u = quaternion_to_rotation_matrix([1.0, 0.0, 0.0, 0.0]);
        for i in 0..3 {
            for j in 0..3 {
                let expect = if i == j { 1.0 } else { 0.0 };
                assert!((u[i][j] - expect).abs() < 1e-15, "({i},{j})={}", u[i][j]);
            }
        }
    }

    #[test]
    fn quaternion_half_turn_about_z() {
        // q = (cos(pi/2), 0, 0, sin(pi/2)) = (0,0,0,1) -> rotation by pi about z.
        let u = quaternion_to_rotation_matrix([0.0, 0.0, 0.0, 1.0]);
        assert!((u[0][0] + 1.0).abs() < 1e-15);
        assert!((u[1][1] + 1.0).abs() < 1e-15);
        assert!((u[2][2] - 1.0).abs() < 1e-15);
    }

    #[test]
    fn rodrigues_rotates_x_onto_y_about_z() {
        let r = rodrigues_rotation([1.0, 0.0, 0.0], [0.0, 0.0, 1.0], std::f64::consts::FRAC_PI_2);
        assert!(r[0].abs() < 1e-15 && (r[1] - 1.0).abs() < 1e-15 && r[2].abs() < 1e-15,
                "got {r:?}");
    }

    #[test]
    fn rodrigues_preserves_length_and_the_axis() {
        let v = [0.3, -1.2, 0.7];
        let axis = normalize_vector([1.0, 2.0, -0.5]);
        let r = rodrigues_rotation(v, axis, 0.9);
        assert!((norm_vector(r) - norm_vector(v)).abs() < 1e-12);
        // the component along the axis is invariant
        assert!((dot_product(r, axis) - dot_product(v, axis)).abs() < 1e-12);
    }

    #[test]
    fn normalize_gives_a_unit_vector() {
        let u = normalize_vector([3.0, 4.0, 0.0]);
        assert!((norm_vector(u) - 1.0).abs() < 1e-15);
        assert!((u[0] - 0.6).abs() < 1e-15 && (u[1] - 0.8).abs() < 1e-15);
    }
}
