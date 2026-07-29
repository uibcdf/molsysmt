"""Private adapters for the bundled Rust compute kernels.

The extension is part of every supported MolSysMT installation. These adapters
preserve the Python-facing kernel contracts while keeping native implementation
details out of the public API.
"""

import molsysmt._rust as _rust


def _num_threads(*payloads):
    from molsysmt.configure import _resolve_num_threads

    return _resolve_num_threads(*payloads)


def _num_threads_for_size(payload_size):
    from molsysmt.configure import _get_effective_num_threads

    return _get_effective_num_threads(payload_size)


# --------------------------------------------------------------------------- MIC distances
# Adapters for the minimum-image distance family.


def get_mic_distances_single_system(coordinates, box, backend=None):
    return _rust.get_mic_distances_single_system(coordinates, box)


def get_mic_distances(coordinates1, coordinates2, box, backend=None):
    return _rust.get_mic_distances(coordinates1, coordinates2, box)


def get_mic_distances_pairs(coordinates1, coordinates2, box, backend=None):
    return _rust.get_mic_distances_pairs(coordinates1, coordinates2, box)


def get_mic_distances_single_system_single_structure(coordinates, box, backend=None):
    return _rust.get_mic_distances_single_system_single_structure(coordinates, box)


def get_mic_distances_single_structure(coordinates1, coordinates2, box, backend=None):
    return _rust.get_mic_distances_single_structure(coordinates1, coordinates2, box)


def get_mic_distances_pairs_single_structure(
    coordinates1, coordinates2, box, backend=None
):
    return _rust.get_mic_distances_pairs_single_structure(
        coordinates1, coordinates2, box
    )


# --------------------------------------------------------------------------- neighbour list
# Dispatch of molsysmt.lib.structure.neighbor_list.neighbor_list_csr_multi (the hot
# kernel behind get_contacts and get_neighbors). Bit-for-bit identical results.


def neighbor_list_csr_multi(
    query_coords,
    ref_coords=None,
    box=None,
    cutoff=None,
    exclude_self=True,
    sort_by_distance=False,
    backend=None,
):
    import numpy as np

    q = np.ascontiguousarray(query_coords, dtype=np.float64)
    r = q if ref_coords is None else np.ascontiguousarray(ref_coords, dtype=np.float64)
    b = None if box is None else np.ascontiguousarray(box, dtype=np.float64)
    return _rust.neighbor_list_csr_multi(
        q,
        r,
        b,
        float(cutoff),
        bool(exclude_self),
        bool(sort_by_distance),
        _num_threads(q, r),
    )


# --------------------------------------------------------------------------- SASA
# Dispatch of the cell-list Shrake-Rupley kernels
# (molsysmt.lib.structure.get_sasa.{get_sasa_cell_list, get_mic_sasa_cell_list}).


def get_sasa_cell_list(
    coordinates, radii, sphere_points, probe_radius, cutoff, backend=None
):
    return _rust.get_sasa_cell_list(
        coordinates,
        radii,
        sphere_points,
        float(probe_radius),
        float(cutoff),
        _num_threads(coordinates, sphere_points),
    )


def get_mic_sasa_cell_list(
    coordinates, box, radii, sphere_points, probe_radius, cutoff, backend=None
):
    return _rust.get_mic_sasa_cell_list(
        coordinates,
        box,
        radii,
        sphere_points,
        float(probe_radius),
        float(cutoff),
        _num_threads(coordinates, sphere_points),
    )


# --------------------------------------------------------------------------- angles
# Dispatch of molsysmt.lib.structure.{get_angles, get_mic_angles}.* — on the
# hbonds.get_luzard_chandler_hbonds path.


def get_angles(coordinates, triplets, backend=None):
    return _rust.get_angles(coordinates, triplets)


def get_angles_single_structure(coordinates, triplets, backend=None):
    return _rust.get_angles_single_structure(coordinates, triplets)


def get_mic_angles(coordinates, box, triplets, backend=None):
    return _rust.get_mic_angles(coordinates, box, triplets)


def get_mic_angles_single_structure(coordinates, box, triplets, backend=None):
    return _rust.get_mic_angles_single_structure(coordinates, box, triplets)


# --------------------------------------------------------------------------- distances
# Dispatch of molsysmt.lib.structure.get_distances.* (the vacuum counterpart of the MIC
# family; the full-matrix fallback used by get_neighbors / get_contacts).


def get_distances_single_system(coordinates, backend=None):
    return _rust.get_distances_single_system(coordinates, _num_threads(coordinates))


def get_distances(coordinates1, coordinates2, backend=None):
    return _rust.get_distances(
        coordinates1,
        coordinates2,
        _num_threads(coordinates1, coordinates2),
    )


def get_distances_pairs(coordinates1, coordinates2, backend=None):
    return _rust.get_distances_pairs(
        coordinates1,
        coordinates2,
        _num_threads(coordinates1, coordinates2),
    )


def get_distances_single_system_single_structure(coordinates, backend=None):
    return _rust.get_distances_single_system_single_structure(coordinates)


def get_distances_single_structure(coordinates1, coordinates2, backend=None):
    return _rust.get_distances_single_structure(coordinates1, coordinates2)


def get_distances_pairs_single_structure(coordinates1, coordinates2, backend=None):
    return _rust.get_distances_pairs_single_structure(coordinates1, coordinates2)


# --------------------------------------------------------------------------- dihedrals
# Dispatch of molsysmt.lib.structure.{get_dihedral_angles, get_mic_dihedral_angles}.*


def get_dihedral_angles(coordinates, quartets, backend=None):
    return _rust.get_dihedral_angles(coordinates, quartets)


def get_dihedral_angles_single_structure(coordinates, quartets, backend=None):
    return _rust.get_dihedral_angles_single_structure(coordinates, quartets)


def get_mic_dihedral_angles(coordinates, box, quartets, backend=None):
    return _rust.get_mic_dihedral_angles(coordinates, box, quartets)


def get_mic_dihedral_angles_single_structure(coordinates, box, quartets, backend=None):
    return _rust.get_mic_dihedral_angles_single_structure(coordinates, box, quartets)


# --------------------------------------------------------------------------- math helpers
# Adapters for shared mathematical helpers. ``rodrigues_rotation`` returns a
# new rotated vector rather than mutating the caller's array.


def matmul(m, v, backend=None):
    return _rust.matmul(m, v)


def transpmatmul(m, v, backend=None):
    return _rust.transpmatmul(m, v)


def normalize_vector(a, backend=None):
    return _rust.normalize_vector(a)


def inverse_matrix_3x3(m, backend=None):
    return _rust.inverse_matrix_3x3(m)


def quaternion_to_rotation_matrix(q, backend=None):
    return _rust.quaternion_to_rotation_matrix(q)


def rodrigues_rotation(vector, unit_vector, angle, backend=None):
    """Returns the rotated vector (never mutates the caller's array)."""
    import numpy as np

    return _rust.rodrigues_rotation(vector, unit_vector, angle)


# --------------------------------------------------------------------------- dihedral edits
# Dispatch of molsysmt.lib.structure.{set,shift}[_mic]_dihedral_angles.*
# These kernels MUTATE `coordinates` in place; the seam preserves that contract.


def _dihedral_edit(name, rust_fn, args, backend):
    return rust_fn(*args)


def shift_dihedral_angles_single_structure(
    coordinates, angles, quartets, blocks, backend=None
):
    return _rust.shift_dihedral_angles_single_structure(
        coordinates, angles, quartets, blocks
    )


def set_dihedral_angles_single_structure(
    coordinates, angles, quartets, blocks, backend=None
):
    return _rust.set_dihedral_angles_single_structure(
        coordinates, angles, quartets, blocks
    )


def shift_dihedral_angles(
    coordinates, angles, quartets, blocks, structure_indices, backend=None
):
    return _rust.shift_dihedral_angles(
        coordinates, angles, quartets, blocks, structure_indices
    )


def set_dihedral_angles(coordinates, angles, quartets, blocks, backend=None):
    """Apply targets to every structure, broadcasting size-one target dimensions."""
    return _rust.set_dihedral_angles(coordinates, angles, quartets, blocks)


def shift_mic_dihedral_angles_single_structure(
    coordinates, box, angles, quartets, blocks, backend=None
):
    return _rust.shift_mic_dihedral_angles_single_structure(
        coordinates, box, angles, quartets, blocks
    )


def set_mic_dihedral_angles_single_structure(
    coordinates, box, angles, quartets, blocks, backend=None
):
    return _rust.set_mic_dihedral_angles_single_structure(
        coordinates, box, angles, quartets, blocks
    )


# Multi-structure variants preserve the established asymmetric signatures: set_* apply
# to every structure, while shift_* accept structure_indices. Both set paths broadcast
# size-one target dimensions. See the archived migration record under
# devguide/archive/resolved_bugs/dihedral_angles_broadcast_mismatch_pbc.md.


def set_mic_dihedral_angles(coordinates, box, angles, quartets, blocks, backend=None):
    return _rust.set_mic_dihedral_angles(coordinates, box, angles, quartets, blocks)


def shift_mic_dihedral_angles(
    coordinates, box, angles, quartets, blocks, structure_indices, backend=None
):
    return _rust.shift_mic_dihedral_angles(
        coordinates, box, angles, quartets, blocks, structure_indices
    )


# --------------------------------------------------------------------------------- pbc
# Block 9: molsysmt.lib.pbc — box geometry plus the wrap/unwrap family.
#
# The `*_vector_single_structure` helpers take `inv_box`/`orthogonal` as optional
# precomputed values in the replaced Numba implementation; the Rust ports always
# recompute them from `box` (the same
# way the whole-system kernels do), so the seam simply drops them on the Rust path.
#
# `wrap_to_pbc`, `wrap_to_pbc_center`, `wrap_to_mic` and `unwrap` mutate `coordinates`
# in place and return None, on both backends.


def box_is_orthogonal_single_structure(box, backend=None):
    return _rust.box_is_orthogonal_single_structure(box)


def box_is_orthogonal(box, backend=None):
    return _rust.box_is_orthogonal(box)


def get_lengths_from_box_single_structure(box, backend=None):
    return _rust.get_lengths_from_box_single_structure(box)


def get_lengths_from_box(box, backend=None):
    return _rust.get_lengths_from_box(box)


def get_angles_from_box_single_structure(box, backend=None):
    return _rust.get_angles_from_box_single_structure(box)


def get_angles_from_box(box, backend=None):
    return _rust.get_angles_from_box(box)


def get_lengths_and_angles_from_box_single_structure(box, backend=None):
    return _rust.get_lengths_and_angles_from_box_single_structure(box)


def get_lengths_and_angles_from_box(box, backend=None):
    return _rust.get_lengths_and_angles_from_box(box)


def get_box_from_lengths_and_angles_single_structure(lengths, angles, backend=None):
    return _rust.get_box_from_lengths_and_angles_single_structure(lengths, angles)


def get_box_from_lengths_and_angles(lengths, angles, backend=None):
    return _rust.get_box_from_lengths_and_angles(lengths, angles)


def wrap_to_pbc_vector_single_structure(
    vector, box, inv_box=None, orthogonal=None, backend=None
):
    return _rust.wrap_to_pbc_vector_single_structure(vector, box)


def wrap_to_pbc_center_vector_single_structure(
    vector, box, inv_box=None, orthogonal=None, backend=None
):
    return _rust.wrap_to_pbc_center_vector_single_structure(vector, box)


def wrap_to_mic_vector_single_structure(
    vector, box, inv_box=None, orthogonal=None, backend=None
):
    return _rust.wrap_to_mic_vector_single_structure(vector, box)


def wrap_to_pbc(coordinates, box, box_origin, backend=None):
    return _rust.wrap_to_pbc(coordinates, box, box_origin)


def wrap_to_pbc_center(coordinates, box, box_center, backend=None):
    return _rust.wrap_to_pbc_center(coordinates, box, box_center)


def wrap_to_mic(coordinates, box, mic_origin, backend=None):
    return _rust.wrap_to_mic(coordinates, box, mic_origin)


def unwrap(coordinates, box, backend=None):
    return _rust.unwrap(coordinates, box)


# ---------------------------------------------------------------------------- geometry
# Block 10: the mechanical long tail — weighted geometry, series encoding and the
# connected-component kernel.


def get_center_single_structure(coordinates, weights, backend=None):
    return _rust.get_center_single_structure(coordinates, weights)


def get_center(coordinates, weights, backend=None):
    return _rust.get_center(coordinates, weights, _num_threads(coordinates))


def get_center_groups_of_atoms_single_structure(
    coordinates, atoms_per_group, weights, backend=None
):
    return _rust.get_center_groups_of_atoms_single_structure(
        coordinates, atoms_per_group, weights
    )


def get_center_groups_of_atoms(coordinates, atoms_per_group, weights, backend=None):
    return _rust.get_center_groups_of_atoms(
        coordinates,
        atoms_per_group,
        weights,
        _num_threads(coordinates),
    )


def flip_single_structure(coordinates, vector, point, backend=None):
    return _rust.flip_single_structure(coordinates, vector, point)


def flip(coordinates, vector, point, backend=None):
    return _rust.flip(coordinates, vector, point)


def get_radius_of_gyration_single_structure(coordinates, weights, backend=None):
    return _rust.get_radius_of_gyration_single_structure(coordinates, weights)


def get_radius_of_gyration(coordinates, weights, backend=None):
    return _rust.get_radius_of_gyration(
        coordinates,
        weights,
        _num_threads(coordinates),
    )


def get_rmsf(coordinates, backend=None):
    return _rust.get_rmsf(coordinates, _num_threads(coordinates))


# ------------------------------------------------------------------------------ series


def serie_to_chunks(serie, backend=None):
    return _rust.serie_to_chunks(serie)


def chunks_to_serie(starts, chunk_size, backend=None):
    return _rust.chunks_to_serie(starts, chunk_size)


def jit_serialize(item, backend=None):
    """`item` is a sequence of integer sequences.

    The native function accepts ordinary Python integer sequences.
    """
    return _rust.jit_serialize([list(segment) for segment in item])


def occurrence_order(serie, backend=None):
    return _rust.occurrence_order(serie)


def occurrence_order_sorted_serie(serie, backend=None):
    return _rust.occurrence_order_sorted_serie(serie)


# ---------------------------------------------------------------------------- topology


def get_component_index_from_bonded_atom_pairs(
    bonded_atom_pairs, n_atoms, backend=None
):
    return _rust.get_component_index_from_bonded_atom_pairs(bonded_atom_pairs, n_atoms)


def _find_root(parent, node, backend=None):
    """Path-halving find. Mutates `parent` in place on both backends."""
    return _rust._find_root(parent, node)


def _union(parent, rank, node_1, node_2, backend=None):
    """Union by rank. Mutates `parent` and `rank` in place on both backends."""
    return _rust._union(parent, rank, node_1, node_2)


# -------------------------------------------------------------------------------- rmsd
# Block 11. `get_rmsd` is a plain reduction; the `least_rmsd` family superposes first via
# the quaternion (Horn/Kearsley) method, whose 4x4 eigenproblem Rust solves with
# `nalgebra` rather than LAPACK. Parity is at tolerance there -- different eigensolver,
# `fastmath`, and the replaced Numba implementation's pairwise `np.sum` for the centroid.


def get_rmsd_single_structure(coordinates, reference_coordinates, backend=None):
    return _rust.get_rmsd_single_structure(coordinates, reference_coordinates)


def get_rmsd(coordinates, reference_coordinates, backend=None):
    return _rust.get_rmsd(
        coordinates,
        reference_coordinates,
        _num_threads(coordinates, reference_coordinates),
    )


def get_rmsd_with_single_reference_structure(
    coordinates, reference_coordinates, backend=None
):
    return _rust.get_rmsd_with_single_reference_structure(
        coordinates,
        reference_coordinates,
        _num_threads(coordinates, reference_coordinates),
    )


def get_least_rmsd_single_structure(coordinates, reference_coordinates, backend=None):
    return _rust.get_least_rmsd_single_structure(coordinates, reference_coordinates)


def get_least_rmsd(coordinates, reference_coordinates, backend=None):
    return _rust.get_least_rmsd(
        coordinates,
        reference_coordinates,
        _num_threads(coordinates, reference_coordinates),
    )


def get_least_rmsd_with_single_reference_structure(
    coordinates, reference_coordinates, backend=None
):
    return _rust.get_least_rmsd_with_single_reference_structure(
        coordinates,
        reference_coordinates,
        _num_threads(coordinates, reference_coordinates),
    )


def get_least_rmsd_rotation_and_translation_single_structure(
    coordinates, reference_coordinates, backend=None
):
    return _rust.get_least_rmsd_rotation_and_translation_single_structure(
        coordinates, reference_coordinates
    )


def get_least_rmsd_rotation_and_translation(
    coordinates, reference_coordinates, backend=None
):
    return _rust.get_least_rmsd_rotation_and_translation(
        coordinates,
        reference_coordinates,
        _num_threads(coordinates, reference_coordinates),
    )


def get_least_rmsd_rotation_and_translation_with_single_reference_structure(
    coordinates, reference_coordinates, backend=None
):
    return (
        _rust.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
            coordinates,
            reference_coordinates,
            _num_threads(coordinates, reference_coordinates),
        )
    )


# -------------------------------------------------------------------------------- axes
# Block 12. 3x3 symmetric eigenproblems, solved with `nalgebra`.
#
# Eigenvectors are defined only up to sign. The replaced Numba implementation returned whatever LAPACK produces;
# the Rust port fixes the sign deterministically (largest-magnitude component positive),
# so switching backend cannot flip an axis. Compare eigenvectors up to sign.


def get_principal_inertia_axes_single_structure(coordinates, weights, backend=None):
    return _rust.get_principal_inertia_axes_single_structure(coordinates, weights)


def get_principal_inertia_axes(coordinates, weights, backend=None):
    return _rust.get_principal_inertia_axes(coordinates, weights)


def get_principal_geometric_axes_single_structure(coordinates, weights, backend=None):
    return _rust.get_principal_geometric_axes_single_structure(coordinates, weights)


def get_principal_geometric_axes(coordinates, weights, backend=None):
    return _rust.get_principal_geometric_axes(coordinates, weights)


# --------------------------------------------------------------------------------- pca
# Block 13, the last CPU kernel. The covariance is built as a matrix product (faer
# rank-k) rather than the replaced Numba implementation's triple loop, and diagonalised with faer's dense
# self-adjoint eigensolver. Eigenvalues are at tolerance; eigenvectors carry a sign
# ambiguity (fixed deterministically here) and, when n_structures < n_features, a
# degenerate null space that no element-wise comparison can match.


def principal_component_analysis(coordinates, weights, backend=None):
    n_features = coordinates.shape[1] * 3
    payload_size = coordinates.shape[0] * n_features * n_features
    return _rust.principal_component_analysis(
        coordinates,
        weights,
        _num_threads_for_size(payload_size),
    )


# ------------------------------------------------------------------- minimum distance
# molsysmt.lib.math brute-force minimum-distance kernels (used by build_peptide).


def minimum_distance_masked_not_bonded(
    coordinates, include_mask, bonded_matrix, backend=None
):
    return _rust.minimum_distance_masked_not_bonded(
        coordinates, include_mask, bonded_matrix
    )


def minimum_distance_between_coordinate_sets(
    existing_coordinates,
    existing_mask,
    candidate_coordinates,
    candidate_mask,
    candidate_start_index,
    bonded_matrix,
    backend=None,
):
    return _rust.minimum_distance_between_coordinate_sets(
        existing_coordinates,
        existing_mask,
        candidate_coordinates,
        candidate_mask,
        candidate_start_index,
        bonded_matrix,
    )


# ------------------------------------------------------------------- brute-force SASA
# The small-system Shrake-Rupley path (below configure CELL_LIST_MIN_ATOMS).


def get_sasa(coordinates, radii, sphere_points, probe_radius, backend=None):
    return _rust.get_sasa(
        coordinates,
        radii,
        sphere_points,
        probe_radius,
        _num_threads(coordinates, sphere_points),
    )


def get_mic_sasa(coordinates, box, radii, sphere_points, probe_radius, backend=None):
    return _rust.get_mic_sasa(
        coordinates,
        box,
        radii,
        sphere_points,
        probe_radius,
        _num_threads(coordinates, sphere_points),
    )
