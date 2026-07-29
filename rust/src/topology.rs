//! Block 10c — `molsysmt.lib.topology.get_component_index_from_bonded_atom_pairs`:
//! union-find over the bond graph, assigning each atom a connected-component index.
//!
//! Component indices are numbered by **first atom of appearance**, not by root id, which
//! is what makes them contiguous and stable regardless of how the union tree happened to
//! be built. That relabelling pass is why this is a faithful port rather than "any correct
//! union-find": two implementations can agree on the partition and still disagree on the
//! labels.
//!
//! `_find_root` and `_union` mutate `parent` (path halving) and `rank` in place, exactly
//! as the replaced Numba implementation does, so they are exposed individually for parity testing.

use numpy::ndarray::Array1;
use numpy::{IntoPyArray, PyArray1, PyReadonlyArray2, PyReadwriteArray1};
use pyo3::prelude::*;

/// Path-halving find: every second node on the path is repointed to its grandparent.
#[inline]
fn find_root(parent: &mut [i64], node: i64) -> i64 {
    let mut node = node as usize;
    while parent[node] != node as i64 {
        parent[node] = parent[parent[node] as usize];
        node = parent[node] as usize;
    }
    node as i64
}

#[inline]
fn union(parent: &mut [i64], rank: &mut [i64], node_1: i64, node_2: i64) {
    let root_1 = find_root(parent, node_1);
    let root_2 = find_root(parent, node_2);
    if root_1 == root_2 {
        return;
    }
    let (r1, r2) = (root_1 as usize, root_2 as usize);
    if rank[r1] < rank[r2] {
        parent[r1] = root_2;
    } else if rank[r1] > rank[r2] {
        parent[r2] = root_1;
    } else {
        parent[r2] = root_1;
        rank[r1] += 1;
    }
}

#[pyfunction]
#[pyo3(name = "_find_root")]
pub fn py_find_root(mut parent: PyReadwriteArray1<'_, i64>, node: i64) -> i64 {
    let mut p = parent.as_array_mut();
    find_root(p.as_slice_mut().expect("parent must be contiguous"), node)
}

#[pyfunction]
#[pyo3(name = "_union")]
pub fn py_union(
    mut parent: PyReadwriteArray1<'_, i64>,
    mut rank: PyReadwriteArray1<'_, i64>,
    node_1: i64,
    node_2: i64,
) {
    let mut p = parent.as_array_mut();
    let mut r = rank.as_array_mut();
    union(
        p.as_slice_mut().expect("parent must be contiguous"),
        r.as_slice_mut().expect("rank must be contiguous"),
        node_1,
        node_2,
    );
}

#[pyfunction]
pub fn get_component_index_from_bonded_atom_pairs<'py>(
    py: Python<'py>,
    bonded_atom_pairs: PyReadonlyArray2<'py, i64>,
    n_atoms: i64,
) -> Bound<'py, PyArray1<i64>> {
    if n_atoms == 0 {
        return Array1::<i64>::zeros(0).into_pyarray(py);
    }
    let pairs = bonded_atom_pairs.as_array();
    let n = n_atoms as usize;

    let mut parent: Vec<i64> = (0..n_atoms).collect();
    let mut rank = vec![0i64; n];

    for b in 0..pairs.shape()[0] {
        union(&mut parent, &mut rank, pairs[[b, 0]], pairs[[b, 1]]);
    }

    let mut out = Vec::with_capacity(n);
    let mut root_to_component = vec![-1i64; n];
    let mut next_component = 0i64;
    for atom in 0..n_atoms {
        let root = find_root(&mut parent, atom) as usize;
        let mut component = root_to_component[root];
        if component == -1 {
            component = next_component;
            root_to_component[root] = component;
            next_component += 1;
        }
        out.push(component);
    }
    Array1::from_vec(out).into_pyarray(py)
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_find_root, m)?)?;
    m.add_function(wrap_pyfunction!(py_union, m)?)?;
    m.add_function(wrap_pyfunction!(
        get_component_index_from_bonded_atom_pairs,
        m
    )?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn components(pairs: &[(i64, i64)], n: i64) -> Vec<i64> {
        let mut parent: Vec<i64> = (0..n).collect();
        let mut rank = vec![0i64; n as usize];
        for &(a, b) in pairs {
            union(&mut parent, &mut rank, a, b);
        }
        let mut out = Vec::new();
        let mut map = vec![-1i64; n as usize];
        let mut next = 0i64;
        for atom in 0..n {
            let root = find_root(&mut parent, atom) as usize;
            if map[root] == -1 {
                map[root] = next;
                next += 1;
            }
            out.push(map[root]);
        }
        out
    }

    #[test]
    fn isolated_atoms_each_form_their_own_component() {
        assert_eq!(components(&[], 4), vec![0, 1, 2, 3]);
    }

    #[test]
    fn a_chain_collapses_to_one_component() {
        assert_eq!(components(&[(0, 1), (1, 2), (2, 3)], 4), vec![0, 0, 0, 0]);
    }

    /// Labels follow first appearance, so they stay contiguous and independent of the
    /// order in which the bonds were given.
    #[test]
    fn labels_are_contiguous_and_bond_order_independent() {
        let a = components(&[(3, 4), (0, 2)], 5);
        assert_eq!(a, vec![0, 1, 0, 2, 2]);
        let b = components(&[(0, 2), (3, 4)], 5);
        assert_eq!(
            a, b,
            "relabelling must not depend on the order of the bonds"
        );
    }

    #[test]
    fn redundant_and_self_bonds_are_harmless() {
        assert_eq!(
            components(&[(0, 1), (1, 0), (0, 0), (0, 1)], 3),
            vec![0, 0, 1]
        );
    }

    /// Path halving must leave the forest describing the same partition.
    #[test]
    fn find_root_is_idempotent_after_compression() {
        let mut parent: Vec<i64> = (0..6).collect();
        let mut rank = vec![0i64; 6];
        for &(a, b) in &[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)] {
            union(&mut parent, &mut rank, a, b);
        }
        let first: Vec<i64> = (0..6).map(|i| find_root(&mut parent, i)).collect();
        let second: Vec<i64> = (0..6).map(|i| find_root(&mut parent, i)).collect();
        assert_eq!(first, second);
        assert!(first.iter().all(|&r| r == first[0]));
    }
}
