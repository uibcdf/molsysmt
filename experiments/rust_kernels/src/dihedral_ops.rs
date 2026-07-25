//! Rusterized set/shift dihedral-angle operations (in-place coordinate edits).
//!
//! Faithful ports of `molsysmt.lib.structure.{set,shift}_dihedral_angles` and their
//! `_mic_` variants. Unlocked by block 7, which ported `rodrigues_rotation` and
//! `normalize_vector`.
//!
//! These are the first **mutating** kernels in the crate: they rotate every atom
//! flagged in `blocks` about the at1->at2 axis, writing back into `coordinates`.
//!
//! Faithfulness note: the Numba code binds `coordinates_at2 = coordinates[at2]` as a
//! live *view*, so a later write to `coordinates[at2]` would be visible. It cannot
//! actually change: if `at2` is flagged in the block then `vect_aux` is the zero vector,
//! Rodrigues leaves it at zero and the atom is rewritten to itself. A snapshot is
//! therefore equivalent, and that is what we take.

use numpy::{PyReadonlyArray1, PyReadonlyArray2, PyReadonlyArray3, PyReadwriteArray2,
            PyReadwriteArray3};
use pyo3::prelude::*;

use crate::mathlib::{dihedral_angle, normalize_vector,
                     rodrigues_rotation, Mat3, Vec3};
use crate::mic::{box_2d, box_at, mic_vector, prep_dist};

#[inline]
fn sub(a: Vec3, b: Vec3) -> Vec3 {
    [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
}

#[inline]
fn add(a: Vec3, b: Vec3) -> Vec3 {
    [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
}

/// Core rotation over one structure's coordinates (2D slice semantics).
/// `mic` carries `(box, inv, orthogonal)` for the periodic variants.
#[allow(clippy::too_many_arguments)]
fn apply_2d(
    coords: &mut numpy::ndarray::ArrayViewMut2<f64>,
    angle_at: &dyn Fn(usize) -> f64,
    quartets: &numpy::ndarray::ArrayView2<i64>,
    blocks: &numpy::ndarray::ArrayView2<bool>,
    mic: Option<(&Mat3, &Mat3, bool)>,
    set_mode: bool,
) {
    let n_angles = quartets.shape()[0];
    let n_atoms = coords.shape()[0];

    for ii in 0..n_angles {
        let at0 = quartets[[ii, 0]] as usize;
        let at1 = quartets[[ii, 1]] as usize;
        let at2 = quartets[[ii, 2]] as usize;
        let at3 = quartets[[ii, 3]] as usize;

        let c_at2: Vec3 = [coords[[at2, 0]], coords[[at2, 1]], coords[[at2, 2]]];
        let c_at1: Vec3 = [coords[[at1, 0]], coords[[at1, 1]], coords[[at1, 2]]];
        let mut vect1 = sub(c_at2, c_at1);
        if let Some((b, inv, ortho)) = mic {
            vect1 = mic_vector(vect1, b, inv, ortho);
        }

        let shift_ang = if set_mode {
            let c_at0: Vec3 = [coords[[at0, 0]], coords[[at0, 1]], coords[[at0, 2]]];
            let c_at3: Vec3 = [coords[[at3, 0]], coords[[at3, 1]], coords[[at3, 2]]];
            let mut vect0 = sub(c_at1, c_at0);
            let mut vect2 = sub(c_at3, c_at2);
            if let Some((b, inv, ortho)) = mic {
                vect0 = mic_vector(vect0, b, inv, ortho);
                vect2 = mic_vector(vect2, b, inv, ortho);
            }
            angle_at(ii) - dihedral_angle(vect0, vect1, vect2)
        } else {
            angle_at(ii)
        };

        let u_vect = normalize_vector(vect1);

        for jj in 0..n_atoms {
            if !blocks[[ii, jj]] {
                continue;
            }
            let cj: Vec3 = [coords[[jj, 0]], coords[[jj, 1]], coords[[jj, 2]]];
            let mut vect_aux = sub(cj, c_at2);
            if let Some((b, inv, ortho)) = mic {
                vect_aux = mic_vector(vect_aux, b, inv, ortho);
            }
            vect_aux = rodrigues_rotation(vect_aux, u_vect, shift_ang);
            if let Some((b, inv, ortho)) = mic {
                vect_aux = mic_vector(vect_aux, b, inv, ortho);
            }
            let out = add(c_at2, vect_aux);
            coords[[jj, 0]] = out[0];
            coords[[jj, 1]] = out[1];
            coords[[jj, 2]] = out[2];
        }
    }
}

// --------------------------------------------------------------------------- vacuum

#[pyfunction]
pub fn shift_dihedral_angles_single_structure(
    mut coordinates: PyReadwriteArray2<'_, f64>,
    angles: PyReadonlyArray1<'_, f64>,
    quartets: PyReadonlyArray2<'_, i64>,
    blocks: PyReadonlyArray2<'_, bool>,
) {
    let a = angles.as_array();
    apply_2d(&mut coordinates.as_array_mut(), &|i| a[i], &quartets.as_array(),
             &blocks.as_array(), None, false);
}

#[pyfunction]
pub fn set_dihedral_angles_single_structure(
    mut coordinates: PyReadwriteArray2<'_, f64>,
    angles: PyReadonlyArray1<'_, f64>,
    quartets: PyReadonlyArray2<'_, i64>,
    blocks: PyReadonlyArray2<'_, bool>,
) {
    let a = angles.as_array();
    apply_2d(&mut coordinates.as_array_mut(), &|i| a[i], &quartets.as_array(),
             &blocks.as_array(), None, true);
}

#[pyfunction]
pub fn shift_dihedral_angles(
    mut coordinates: PyReadwriteArray3<'_, f64>,
    angles: PyReadonlyArray2<'_, f64>,
    quartets: PyReadonlyArray2<'_, i64>,
    blocks: PyReadonlyArray2<'_, bool>,
    structure_indices: PyReadonlyArray1<'_, i64>,
) {
    let mut c = coordinates.as_array_mut();
    let a = angles.as_array();
    let q = quartets.as_array();
    let bl = blocks.as_array();
    for &s in structure_indices.as_array().iter() {
        let s = s as usize;
        apply_2d(&mut c.index_axis_mut(numpy::ndarray::Axis(0), s),
                 &|aa| a[[s, aa]], &q, &bl, None, false);
    }
}

/// NOTE: upstream `set_dihedral_angles` takes **no** `structure_indices` (it always
/// walks every structure) and is the only variant implementing broadcasting: a size-1
/// dimension of `angles` collapses to index 0. Replicated exactly — see
/// `devguide/pending_bugs/dihedral_angles_broadcast_mismatch_pbc.md`, which reports that
/// its periodic twin does *not* broadcast.
#[pyfunction]
pub fn set_dihedral_angles(
    mut coordinates: PyReadwriteArray3<'_, f64>,
    angles: PyReadonlyArray2<'_, f64>,
    quartets: PyReadonlyArray2<'_, i64>,
    blocks: PyReadonlyArray2<'_, bool>,
) {
    let mut c = coordinates.as_array_mut();
    let a = angles.as_array();
    let q = quartets.as_array();
    let bl = blocks.as_array();
    let n_structures = c.shape()[0];
    let inc_structures = a.shape()[0] != 1;
    let inc_angles = a.shape()[1] != 1;
    for s in 0..n_structures {
        let row = if inc_structures { s } else { 0 };
        apply_2d(&mut c.index_axis_mut(numpy::ndarray::Axis(0), s),
                 &|aa| a[[row, if inc_angles { aa } else { 0 }]], &q, &bl, None, true);
    }
}

// --------------------------------------------------------------------------- periodic

/// The MIC variants wrap `vect1` (and `vect0`/`vect2` in set mode) and then wrap
/// `vect_aux` before and after each rotation. We compute the inverse unconditionally;
/// `shift_mic` does the same upstream while `set_mic` computes it only for triclinic
/// boxes, but the wrap only reads it on the triclinic branch, so results
/// are identical either way.
fn mic_parts(b: &Mat3) -> (Mat3, Mat3, bool) {
    let (ortho, cell, inv) = prep_dist(b);
    (cell, inv, ortho)
}

#[pyfunction]
pub fn shift_mic_dihedral_angles_single_structure(
    mut coordinates: PyReadwriteArray2<'_, f64>,
    boxes: PyReadonlyArray2<'_, f64>,
    angles: PyReadonlyArray1<'_, f64>,
    quartets: PyReadonlyArray2<'_, i64>,
    blocks: PyReadonlyArray2<'_, bool>,
) {
    let b = box_2d(&boxes.as_array());
    let (cell, inv, ortho) = mic_parts(&b);
    let a = angles.as_array();
    apply_2d(&mut coordinates.as_array_mut(), &|i| a[i], &quartets.as_array(),
             &blocks.as_array(), Some((&cell, &inv, ortho)), false);
}

#[pyfunction]
pub fn set_mic_dihedral_angles_single_structure(
    mut coordinates: PyReadwriteArray2<'_, f64>,
    boxes: PyReadonlyArray2<'_, f64>,
    angles: PyReadonlyArray1<'_, f64>,
    quartets: PyReadonlyArray2<'_, i64>,
    blocks: PyReadonlyArray2<'_, bool>,
) {
    let b = box_2d(&boxes.as_array());
    let (cell, inv, ortho) = mic_parts(&b);
    let a = angles.as_array();
    apply_2d(&mut coordinates.as_array_mut(), &|i| a[i], &quartets.as_array(),
             &blocks.as_array(), Some((&cell, &inv, ortho)), true);
}

#[pyfunction]
pub fn shift_mic_dihedral_angles(
    mut coordinates: PyReadwriteArray3<'_, f64>,
    boxes: PyReadonlyArray3<'_, f64>,
    angles: PyReadonlyArray2<'_, f64>,
    quartets: PyReadonlyArray2<'_, i64>,
    blocks: PyReadonlyArray2<'_, bool>,
    structure_indices: PyReadonlyArray1<'_, i64>,
) {
    let mut c = coordinates.as_array_mut();
    let bx = boxes.as_array();
    let a = angles.as_array();
    let q = quartets.as_array();
    let bl = blocks.as_array();
    for &s in structure_indices.as_array().iter() {
        let s = s as usize;
        let b = box_at(&bx, s);
        let (cell, inv, ortho) = mic_parts(&b);
        apply_2d(&mut c.index_axis_mut(numpy::ndarray::Axis(0), s),
                 &|aa| a[[s, aa]], &q, &bl, Some((&cell, &inv, ortho)), false);
    }
}

/// DELIBERATE, TESTED DIVERGENCE from the Numba oracle.
///
/// Upstream this kernel indexes `angles[ii, aa]` directly while its vacuum twin
/// broadcasts a size-1 dimension — and the public `set_dihedral_angles` documents
/// `angles` as "compatible with shape (n_structures, n_quartets)" and feeds the same
/// array to either kernel depending only on whether a box exists. With a broadcast
/// shape the periodic path therefore reads out of bounds, and Numba does not
/// bounds-check: it silently returns garbage (measured: atoms displaced by ~7.8 nm).
///
/// Parity is the migration's gate only where the oracle is *defined*; there is nothing
/// to be faithful to in undefined behaviour. So this port broadcasts like the vacuum
/// twin, honouring the documented contract. On every well-defined input the two
/// backends remain bit-for-bit identical. See
/// `devguide/pending_bugs/dihedral_angles_broadcast_mismatch_pbc.md`.
#[pyfunction]
pub fn set_mic_dihedral_angles(
    mut coordinates: PyReadwriteArray3<'_, f64>,
    boxes: PyReadonlyArray3<'_, f64>,
    angles: PyReadonlyArray2<'_, f64>,
    quartets: PyReadonlyArray2<'_, i64>,
    blocks: PyReadonlyArray2<'_, bool>,
) {
    let mut c = coordinates.as_array_mut();
    let bx = boxes.as_array();
    let a = angles.as_array();
    let q = quartets.as_array();
    let bl = blocks.as_array();
    let inc_structures = a.shape()[0] != 1;
    let inc_angles = a.shape()[1] != 1;
    for s in 0..c.shape()[0] {
        let b = box_at(&bx, s);
        let (cell, inv, ortho) = mic_parts(&b);
        let row = if inc_structures { s } else { 0 };
        apply_2d(&mut c.index_axis_mut(numpy::ndarray::Axis(0), s),
                 &|aa| a[[row, if inc_angles { aa } else { 0 }]], &q, &bl,
                 Some((&cell, &inv, ortho)), true);
    }
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(shift_dihedral_angles_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(set_dihedral_angles_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(shift_dihedral_angles, m)?)?;
    m.add_function(wrap_pyfunction!(set_dihedral_angles, m)?)?;
    m.add_function(wrap_pyfunction!(shift_mic_dihedral_angles_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(set_mic_dihedral_angles_single_structure, m)?)?;
    m.add_function(wrap_pyfunction!(shift_mic_dihedral_angles, m)?)?;
    m.add_function(wrap_pyfunction!(set_mic_dihedral_angles, m)?)?;
    Ok(())
}
