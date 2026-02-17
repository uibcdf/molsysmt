from molsysmt._private.arg_digestion import arg_digest
import numpy as np
import gzip
import json
import warnings
from functools import lru_cache
from importlib.resources import files


def _guess_atom_type(atom_name):
    """Infer atom type from a PDB-like atom name."""

    for character in atom_name:
        if character.isalpha():
            return character.upper()
    return "X"


def _pick_topology_variant(topologies, prefer_oxt=None):
    """Select a topology variant according to terminal preference."""

    if not topologies:
        raise ValueError("No topology variants were found in the group database.")

    if prefer_oxt is None:
        return topologies[0]

    for topology in topologies:
        has_oxt = "OXT" in topology["atoms"]
        if has_oxt == prefer_oxt:
            return topology

    return topologies[0]


def _place_group_coordinates(group_anchor_x, atom_names):
    """Generate deterministic initial coordinates for a group."""

    coordinates = np.zeros((len(atom_names), 3), dtype=float)

    backbone_map = {
        "N": np.array([0.00, 0.00, 0.00], dtype=float),
        "CA": np.array([0.14, 0.06, 0.00], dtype=float),
        "C": np.array([0.28, 0.00, 0.00], dtype=float),
        "O": np.array([0.34, -0.06, 0.00], dtype=float),
        "OXT": np.array([0.34, -0.14, 0.00], dtype=float),
    }

    for atom_index, atom_name in enumerate(atom_names):
        if atom_name in backbone_map:
            atom_coordinates = backbone_map[atom_name].copy()
        else:
            angle = atom_index * 2.399963229728653  # irrational multiple to reduce overlaps
            atom_coordinates = np.array(
                [
                    0.14 + 0.12 * np.cos(angle),
                    0.00 + 0.12 * np.sin(angle),
                    0.08 * np.sin(0.5 * angle),
                ],
                dtype=float,
            )

        atom_coordinates[0] += group_anchor_x
        coordinates[atom_index, :] = atom_coordinates

    return coordinates


def _normalize(vector):
    norm = np.linalg.norm(vector)
    if norm < 1.0e-12:
        return None
    return vector / norm


def _rotation_matrix_from_axis_angle(axis, angle):
    """Return rotation matrix from axis-angle parameters."""

    axis = _normalize(axis)
    if axis is None:
        return np.eye(3, dtype=float)

    x, y, z = axis
    c = np.cos(angle)
    s = np.sin(angle)
    one_minus_c = 1.0 - c

    return np.array(
        [
            [c + x * x * one_minus_c, x * y * one_minus_c - z * s, x * z * one_minus_c + y * s],
            [y * x * one_minus_c + z * s, c + y * y * one_minus_c, y * z * one_minus_c - x * s],
            [z * x * one_minus_c - y * s, z * y * one_minus_c + x * s, c + z * z * one_minus_c],
        ],
        dtype=float,
    )


def _apply_rotation(coordinates, rotation_matrix, pivot):
    """Rotate coordinates around a pivot point."""

    return (coordinates - pivot) @ rotation_matrix.T + pivot


def _orthogonal_unit(vector):
    """Return a deterministic unit vector orthogonal to the input."""

    unit = _normalize(vector)
    if unit is None:
        return np.array([1.0, 0.0, 0.0], dtype=float)

    trial = np.array([1.0, 0.0, 0.0], dtype=float)
    if abs(np.dot(unit, trial)) > 0.9:
        trial = np.array([0.0, 1.0, 0.0], dtype=float)

    orthogonal = trial - np.dot(trial, unit) * unit
    orthogonal = _normalize(orthogonal)
    if orthogonal is None:
        return np.array([0.0, 0.0, 1.0], dtype=float)
    return orthogonal


def _angle_degrees(atom_1, atom_2, atom_3):
    """Return angle atom_1-atom_2-atom_3 in degrees."""

    vector_1 = atom_1 - atom_2
    vector_2 = atom_3 - atom_2
    norm_1 = np.linalg.norm(vector_1)
    norm_2 = np.linalg.norm(vector_2)
    if norm_1 < 1.0e-12 or norm_2 < 1.0e-12:
        return None
    cosine = np.dot(vector_1, vector_2) / (norm_1 * norm_2)
    cosine = float(np.clip(cosine, -1.0, 1.0))
    return float(np.degrees(np.arccos(cosine)))


def _dihedral_degrees(atom_1, atom_2, atom_3, atom_4):
    """Return dihedral atom_1-atom_2-atom_3-atom_4 in degrees."""

    bond_0 = atom_1 - atom_2
    bond_1 = atom_3 - atom_2
    bond_2 = atom_4 - atom_3

    norm_1 = np.linalg.norm(bond_1)
    if norm_1 < 1.0e-12:
        return None
    unit_1 = bond_1 / norm_1

    vector = bond_0 - np.dot(bond_0, unit_1) * unit_1
    wector = bond_2 - np.dot(bond_2, unit_1) * unit_1

    norm_v = np.linalg.norm(vector)
    norm_w = np.linalg.norm(wector)
    if norm_v < 1.0e-12 or norm_w < 1.0e-12:
        return None

    x_value = float(np.dot(vector, wector))
    y_value = float(np.dot(np.cross(unit_1, vector), wector))
    return float(np.degrees(np.arctan2(y_value, x_value)))


def _wrap_degrees(angle):
    """Wrap angle to [-180, 180)."""

    return ((angle + 180.0) % 360.0) - 180.0


def _fibonacci_unit_vectors(n_points):
    """Generate approximately uniform unit vectors on a sphere."""

    if n_points <= 0:
        return []
    if n_points == 1:
        return [np.array([0.0, 0.0, 1.0], dtype=float)]

    directions = []
    golden_angle = np.pi * (3.0 - np.sqrt(5.0))
    for index in range(n_points):
        y_value = 1.0 - 2.0 * index / (n_points - 1)
        radius = np.sqrt(max(0.0, 1.0 - y_value * y_value))
        theta = golden_angle * index
        x_value = np.cos(theta) * radius
        z_value = np.sin(theta) * radius
        directions.append(np.array([x_value, y_value, z_value], dtype=float))
    return directions


def _atomic_number_to_symbol(atomic_number):
    """Map common atomic numbers to element symbols."""

    mapping = {
        1: "H",
        6: "C",
        7: "N",
        8: "O",
        15: "P",
        16: "S",
    }
    return mapping.get(atomic_number)


@lru_cache(maxsize=1)
def _get_peptide_builder_templates():
    """Load bundled peptide-builder templates."""

    try:
        path = files("molsysmt.data.databases.peptide_builder").joinpath("amber14sb.json.gz")
        with gzip.open(path, "rt", encoding="utf-8") as file_handle:
            database = json.load(file_handle)
        return database.get("templates", {})
    except Exception:
        return {}


def _resolve_template_alias(template_name, available_templates):
    """Resolve aliases for template names."""

    if template_name in available_templates:
        return template_name

    alias = {
        "HIS": "HIE",
        "NHIS": "NHIE",
        "CHIS": "CHIE",
    }
    mapped = alias.get(template_name, template_name)
    if mapped in available_templates:
        return mapped
    return None


def _minimum_nonbonded_heavy_distance(existing_coordinates, existing_atom_types, existing_bonds_set,
                                      candidate_coordinates, candidate_atom_types, candidate_start_index,
                                      existing_bonded_matrix=None):
    """Compute minimum heavy-heavy distance between existing and candidate atoms."""

    if existing_coordinates.shape[0] == 0:
        return np.inf

    existing_mask = np.zeros(len(existing_atom_types), dtype=np.uint8)
    candidate_mask = np.zeros(len(candidate_atom_types), dtype=np.uint8)

    for atom_index, atom_type in enumerate(existing_atom_types):
        if atom_type != "H":
            existing_mask[atom_index] = 1
    for atom_index, atom_type in enumerate(candidate_atom_types):
        if atom_type != "H":
            candidate_mask[atom_index] = 1

    if np.count_nonzero(existing_mask) == 0 or np.count_nonzero(candidate_mask) == 0:
        return np.inf

    if existing_bonded_matrix is not None:
        from molsysmt.lib.math import minimum_distance_between_coordinate_sets

        return minimum_distance_between_coordinate_sets(
            np.asarray(existing_coordinates, dtype=np.float64),
            existing_mask,
            np.asarray(candidate_coordinates, dtype=np.float64),
            candidate_mask,
            int(candidate_start_index),
            existing_bonded_matrix,
        )

    min_distance = np.inf
    existing_heavy = np.where(existing_mask == 1)[0]
    candidate_heavy = np.where(candidate_mask == 1)[0]
    for existing_index in existing_heavy:
        for candidate_local_index in candidate_heavy:
            candidate_global_index = candidate_start_index + int(candidate_local_index)
            if tuple(sorted((int(existing_index), int(candidate_global_index)))) in existing_bonds_set:
                continue
            distance = np.linalg.norm(
                existing_coordinates[existing_index, :] - candidate_coordinates[candidate_local_index, :]
            )
            if distance < min_distance:
                min_distance = distance

    return min_distance


def _minimum_nonbonded_heavy_distance_between_groups(left_coordinates, left_atom_names, left_atom_types,
                                                     right_coordinates, right_atom_names, right_atom_types,
                                                     skip_pair_names=None):
    """Compute minimum non-bonded heavy-heavy distance between two groups."""

    min_distance = np.inf
    for left_index, left_atom_type in enumerate(left_atom_types):
        if left_atom_type == "H" or left_atom_names[left_index].startswith("H"):
            continue
        for right_index, right_atom_type in enumerate(right_atom_types):
            if right_atom_type == "H" or right_atom_names[right_index].startswith("H"):
                continue
            if skip_pair_names is not None:
                if (left_atom_names[left_index], right_atom_names[right_index]) == skip_pair_names:
                    continue
            distance = np.linalg.norm(left_coordinates[left_index, :] - right_coordinates[right_index, :])
            if distance < min_distance:
                min_distance = distance
    return min_distance


def _prepare_nonbonded_heavy_distance_full(atom_types, bonds):
    """Build reusable heavy-mask and bonded-matrix for global non-bonded scans."""

    n_atoms = len(atom_types)
    heavy_mask = np.zeros(n_atoms, dtype=np.uint8)
    for atom_index, atom_type in enumerate(atom_types):
        if atom_type != "H":
            heavy_mask[atom_index] = 1

    bonded_matrix = np.zeros((n_atoms, n_atoms), dtype=np.uint8)
    for atom_index_1, atom_index_2 in bonds:
        atom_index_1 = int(atom_index_1)
        atom_index_2 = int(atom_index_2)
        if atom_index_1 == atom_index_2:
            continue
        bonded_matrix[atom_index_1, atom_index_2] = 1
        bonded_matrix[atom_index_2, atom_index_1] = 1

    return heavy_mask, bonded_matrix


def _minimum_nonbonded_heavy_distance_full(coordinates, atom_types=None, bonds=None,
                                           heavy_mask=None, bonded_matrix=None):
    """Compute global minimum heavy-heavy distance for non-bonded pairs."""

    if heavy_mask is None or bonded_matrix is None:
        if atom_types is None or bonds is None:
            raise ValueError("atom_types and bonds are required when no prepared masks are provided.")
        heavy_mask, bonded_matrix = _prepare_nonbonded_heavy_distance_full(atom_types, bonds)

    if np.count_nonzero(heavy_mask) < 2:
        return np.inf

    from molsysmt.lib.math import minimum_distance_masked_not_bonded

    return minimum_distance_masked_not_bonded(
        np.asarray(coordinates, dtype=np.float64),
        heavy_mask,
        bonded_matrix,
    )


def _optimize_peptide_torsions(coordinates, atom_types, bonds, groups_data, group_start_indices,
                               n_rounds=2, n_angles=24):
    """Improve initial peptide geometry by rotating downstream fragments around C-N links."""

    if len(group_start_indices) < 2:
        return coordinates

    heavy_mask, bonded_matrix = _prepare_nonbonded_heavy_distance_full(atom_types, bonds)
    optimized_coordinates = coordinates.copy()
    best_score = _minimum_nonbonded_heavy_distance_full(
        optimized_coordinates, heavy_mask=heavy_mask, bonded_matrix=bonded_matrix
    )
    if not np.isfinite(best_score):
        return optimized_coordinates

    angle_grid = np.linspace(0.0, 2.0 * np.pi, num=n_angles, endpoint=False)[1:]

    for _ in range(n_rounds):
        improved = False

        for group_index in range(len(group_start_indices) - 1):
            if groups_data[group_index + 1].get("group_name", "") == "PRO":
                # Preserve dedicated proline-link placement to avoid ring clashes.
                continue
            left_connect = groups_data[group_index]["connect"]
            right_connect = groups_data[group_index + 1]["connect"]
            left_tail = left_connect[1]
            right_head = right_connect[0]

            if left_tail is None or right_head is None:
                continue

            left_tail_index = group_start_indices[group_index] + left_tail
            right_head_index = group_start_indices[group_index + 1] + right_head
            downstream_start = group_start_indices[group_index + 1]

            axis = _normalize(optimized_coordinates[right_head_index, :] - optimized_coordinates[left_tail_index, :])
            if axis is None:
                continue

            pivot = optimized_coordinates[right_head_index, :].copy()
            candidate_best_score = best_score
            candidate_best_coordinates = optimized_coordinates

            for angle in angle_grid:
                rotation_matrix = _rotation_matrix_from_axis_angle(axis, angle)
                trial_coordinates = optimized_coordinates.copy()
                trial_coordinates[downstream_start:, :] = _apply_rotation(
                    optimized_coordinates[downstream_start:, :], rotation_matrix, pivot
                )
                score = _minimum_nonbonded_heavy_distance_full(
                    trial_coordinates, heavy_mask=heavy_mask, bonded_matrix=bonded_matrix
                )
                if score > candidate_best_score + 1.0e-10:
                    candidate_best_score = score
                    candidate_best_coordinates = trial_coordinates

            if candidate_best_score > best_score + 1.0e-10:
                best_score = candidate_best_score
                optimized_coordinates = candidate_best_coordinates
                improved = True

        if not improved:
            break

    return optimized_coordinates


def _get_connected_component(adjacency, start_index, blocked_bond):
    """Return connected component from start_index when blocked_bond is removed."""

    stack = [start_index]
    visited = set()
    i_block, j_block = blocked_bond
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        for neighbor in adjacency.get(current, []):
            if (current == i_block and neighbor == j_block) or (current == j_block and neighbor == i_block):
                continue
            if neighbor not in visited:
                stack.append(neighbor)
    return visited


def _optimize_sidechain_torsions(coordinates, atom_types, atom_names, bonds, groups_data, group_start_indices,
                                 n_rounds=1, n_angles=12):
    """Relieve local clashes by rotating sidechain fragments around internal rotatable bonds."""

    if len(group_start_indices) == 0:
        return coordinates

    adjacency = {}
    for atom1_index, atom2_index in bonds:
        adjacency.setdefault(atom1_index, set()).add(atom2_index)
        adjacency.setdefault(atom2_index, set()).add(atom1_index)

    backbone_names = {"N", "CA", "C", "O", "OXT", "H", "H1", "H2", "H3", "HA", "HA2", "HA3"}
    heavy_mask, bonded_matrix = _prepare_nonbonded_heavy_distance_full(atom_types, bonds)
    optimized_coordinates = coordinates.copy()
    best_score = _minimum_nonbonded_heavy_distance_full(
        optimized_coordinates, heavy_mask=heavy_mask, bonded_matrix=bonded_matrix
    )
    if not np.isfinite(best_score):
        return optimized_coordinates

    angle_grid = np.linspace(0.0, 2.0 * np.pi, num=n_angles, endpoint=False)[1:]

    for _ in range(n_rounds):
        improved = False

        for group_index, group_data in enumerate(groups_data):
            group_start = group_start_indices[group_index]
            group_size = len(group_data["atom_names"])
            group_indices = list(range(group_start, group_start + group_size))
            group_set = set(group_indices)

            for atom1_index, atom2_index in bonds:
                if atom1_index not in group_set or atom2_index not in group_set:
                    continue

                atom_name_1 = atom_names[atom1_index]
                atom_name_2 = atom_names[atom2_index]

                # Skip hydrogen-involving bonds.
                if atom_name_1.startswith("H") or atom_name_2.startswith("H"):
                    continue

                component_1 = _get_connected_component(adjacency, atom1_index, (atom1_index, atom2_index))
                if atom2_index in component_1:
                    # Ring bond or alternate path exists; avoid rotating constrained cycles.
                    continue
                component_2 = _get_connected_component(adjacency, atom2_index, (atom1_index, atom2_index))

                component_1 = component_1 & group_set
                component_2 = component_2 & group_set

                if not component_1 or not component_2:
                    continue

                backbone_count_1 = sum(atom_names[ii] in backbone_names for ii in component_1)
                backbone_count_2 = sum(atom_names[ii] in backbone_names for ii in component_2)

                if backbone_count_1 < backbone_count_2:
                    rotating_indices = sorted(component_1)
                elif backbone_count_2 < backbone_count_1:
                    rotating_indices = sorted(component_2)
                else:
                    # If tied, rotate the smaller component.
                    rotating_indices = sorted(component_1 if len(component_1) <= len(component_2) else component_2)

                # Avoid rotating the full residue or backbone-dominated fragments.
                if len(rotating_indices) <= 1 or len(rotating_indices) >= len(group_indices):
                    continue
                if all(atom_names[ii] in backbone_names for ii in rotating_indices):
                    continue

                axis = _normalize(optimized_coordinates[atom2_index, :] - optimized_coordinates[atom1_index, :])
                if axis is None:
                    continue

                pivot = optimized_coordinates[atom1_index, :].copy()
                candidate_best_score = best_score
                candidate_best_coordinates = optimized_coordinates

                rotating_coordinates = optimized_coordinates[rotating_indices, :]
                for angle in angle_grid:
                    rotation_matrix = _rotation_matrix_from_axis_angle(axis, angle)
                    trial_coordinates = optimized_coordinates.copy()
                    trial_coordinates[rotating_indices, :] = _apply_rotation(
                        rotating_coordinates, rotation_matrix, pivot
                    )
                    score = _minimum_nonbonded_heavy_distance_full(
                        trial_coordinates, heavy_mask=heavy_mask, bonded_matrix=bonded_matrix
                    )
                    if score > candidate_best_score + 1.0e-10:
                        candidate_best_score = score
                        candidate_best_coordinates = trial_coordinates

                if candidate_best_score > best_score + 1.0e-10:
                    best_score = candidate_best_score
                    optimized_coordinates = candidate_best_coordinates
                    improved = True

        if not improved:
            break

    return optimized_coordinates


def _align_capping_junction_geometry(coordinates, atom_types, groups_data, group_start_indices):
    """Enforce trigonal carbonyl geometry for capping-to-residue peptide links."""

    if len(group_start_indices) < 2:
        return coordinates

    aligned_coordinates = coordinates.copy()

    for group_index in range(len(group_start_indices) - 1):
        previous_group_data = groups_data[group_index]
        next_group_data = groups_data[group_index + 1]

        if previous_group_data.get("group_type", "") != "terminal capping":
            continue
        if next_group_data.get("group_name", "") == "PRO":
            # Proline requires dedicated ring-aware placement handled earlier.
            continue

        previous_tail_local_index = previous_group_data["connect"][1]
        next_head_local_index = next_group_data["connect"][0]
        if previous_tail_local_index is None or next_head_local_index is None:
            continue

        previous_group_start = group_start_indices[group_index]
        next_group_start = group_start_indices[group_index + 1]
        carbonyl_carbon_index = previous_group_start + previous_tail_local_index
        next_nitrogen_index = next_group_start + next_head_local_index

        previous_name_to_index = previous_group_data["atom_name_to_local_index"]
        oxygen_local_index = previous_name_to_index.get("O", None)
        if oxygen_local_index is None:
            oxygen_local_index = previous_name_to_index.get("OXT", None)
        if oxygen_local_index is None:
            continue

        oxygen_index = previous_group_start + oxygen_local_index

        substituent_local_index = None
        oxygen_local_candidates = {oxygen_local_index}
        for local_i, local_j in previous_group_data["bonded_atom_indices"]:
            neighbor_local_index = None
            if local_i == previous_tail_local_index:
                neighbor_local_index = local_j
            elif local_j == previous_tail_local_index:
                neighbor_local_index = local_i
            if neighbor_local_index is None or neighbor_local_index in oxygen_local_candidates:
                continue
            atom_name_neighbor = previous_group_data["atom_names"][neighbor_local_index]
            atom_type_neighbor = previous_group_data["atom_types"][neighbor_local_index]
            if atom_name_neighbor.startswith("H") or atom_type_neighbor == "H":
                continue
            substituent_local_index = neighbor_local_index
            break

        if substituent_local_index is None:
            continue

        substituent_index = previous_group_start + substituent_local_index
        carbonyl_carbon_coordinates = aligned_coordinates[carbonyl_carbon_index, :]
        oxygen_coordinates = aligned_coordinates[oxygen_index, :]
        substituent_coordinates = aligned_coordinates[substituent_index, :]
        next_nitrogen_coordinates = aligned_coordinates[next_nitrogen_index, :]

        direction_from_oxygen = _normalize(oxygen_coordinates - carbonyl_carbon_coordinates)
        direction_from_substituent = _normalize(substituent_coordinates - carbonyl_carbon_coordinates)
        current_direction = _normalize(next_nitrogen_coordinates - carbonyl_carbon_coordinates)
        if direction_from_oxygen is None or direction_from_substituent is None or current_direction is None:
            continue

        desired_direction = _normalize(-(direction_from_oxygen + direction_from_substituent))
        if desired_direction is None:
            continue

        dot_value = float(np.clip(np.dot(current_direction, desired_direction), -1.0, 1.0))
        rotation_angle = float(np.arccos(dot_value))
        if rotation_angle < 1.0e-6:
            continue

        rotation_axis = np.cross(current_direction, desired_direction)
        rotation_axis = _normalize(rotation_axis)
        if rotation_axis is None:
            continue

        downstream_start = next_group_start
        rotation_matrix = _rotation_matrix_from_axis_angle(rotation_axis, rotation_angle)
        aligned_coordinates[downstream_start:, :] = _apply_rotation(
            aligned_coordinates[downstream_start:, :],
            rotation_matrix,
            carbonyl_carbon_coordinates,
        )

    return aligned_coordinates


def _optimize_backbone_torsions(coordinates, atom_types, atom_names, bonds, groups_data, group_start_indices,
                                n_rounds=1, n_angles=18):
    """Relieve backbone clashes by rotating downstream fragments around N-CA and CA-C."""

    if len(group_start_indices) == 0:
        return coordinates

    adjacency = {}
    for atom1_index, atom2_index in bonds:
        adjacency.setdefault(atom1_index, set()).add(atom2_index)
        adjacency.setdefault(atom2_index, set()).add(atom1_index)

    heavy_mask, bonded_matrix = _prepare_nonbonded_heavy_distance_full(atom_types, bonds)
    optimized_coordinates = coordinates.copy()
    best_score = _minimum_nonbonded_heavy_distance_full(
        optimized_coordinates, heavy_mask=heavy_mask, bonded_matrix=bonded_matrix
    )
    if not np.isfinite(best_score):
        return optimized_coordinates

    angle_grid = np.linspace(0.0, 2.0 * np.pi, num=n_angles, endpoint=False)[1:]

    for _ in range(n_rounds):
        improved = False

        for group_index, group_data in enumerate(groups_data):
            name_to_local = group_data["atom_name_to_local_index"]
            group_start = group_start_indices[group_index]

            for atom_name_1, atom_name_2 in (("N", "CA"), ("CA", "C")):
                local_index_1 = name_to_local.get(atom_name_1, None)
                local_index_2 = name_to_local.get(atom_name_2, None)
                if local_index_1 is None or local_index_2 is None:
                    continue

                atom1_index = group_start + local_index_1
                atom2_index = group_start + local_index_2

                component_1 = _get_connected_component(adjacency, atom1_index, (atom1_index, atom2_index))
                if atom2_index in component_1:
                    continue
                component_2 = _get_connected_component(adjacency, atom2_index, (atom1_index, atom2_index))

                # Rotate downstream side only to keep already-built upstream residues stable.
                if np.mean(list(component_1)) > np.mean(list(component_2)):
                    rotating_indices = sorted(component_1)
                    pivot_index = atom1_index
                else:
                    rotating_indices = sorted(component_2)
                    pivot_index = atom2_index

                if len(rotating_indices) <= 1:
                    continue

                axis = _normalize(optimized_coordinates[atom2_index, :] - optimized_coordinates[atom1_index, :])
                if axis is None:
                    continue

                pivot = optimized_coordinates[pivot_index, :].copy()
                rotating_coordinates = optimized_coordinates[rotating_indices, :]
                candidate_best_score = best_score
                candidate_best_coordinates = optimized_coordinates

                for angle in angle_grid:
                    rotation_matrix = _rotation_matrix_from_axis_angle(axis, angle)
                    trial_coordinates = optimized_coordinates.copy()
                    trial_coordinates[rotating_indices, :] = _apply_rotation(
                        rotating_coordinates, rotation_matrix, pivot
                    )
                    score = _minimum_nonbonded_heavy_distance_full(
                        trial_coordinates, heavy_mask=heavy_mask, bonded_matrix=bonded_matrix
                    )
                    if score > candidate_best_score + 1.0e-10:
                        candidate_best_score = score
                        candidate_best_coordinates = trial_coordinates

                if candidate_best_score > best_score + 1.0e-10:
                    best_score = candidate_best_score
                    optimized_coordinates = candidate_best_coordinates
                    improved = True

        if not improved:
            break

    return optimized_coordinates


@arg_digest()
def build_peptide(molecular_system, to_form='molsysmt.MolSys', engine='LEaP'):
    """
    Building a peptide from a sequence.

    This function constructs a capped or uncapped peptide from a sequence of amino acids.
    It generates the complete atomic topology, including bonds, angles, and coordinates
    for the resulting system. Optionally, terminal capping groups can be included in the input
    sequence.

    Parameters
    ----------
    molecular_system : str or list of str
        The peptide sequence provided using either three-letter or one-letter amino acid codes.
        The sequence can also include optional terminal caps such as 'ACE' or 'NME'.

    to_form : str, default='molsysmt.MolSys'
        Output form of the resulting molecular system. Must be one of the :ref:`supported forms <Introduction_Forms>`.

    engine : {'LEaP', 'MolSysMT'}, default 'LEaP'
        Engine used to build the peptide.
        ``'LEaP'`` uses AmberTools and requires ``tleap`` in the environment.
        ``'MolSysMT'`` builds the peptide using bundled residue templates.

    Returns
    -------
    molecular system
        A new molecular system representing the fully constructed peptide, including coordinates
        and all relevant topological information.

    Raises
    ------
    NotImplementedError
        Raised if the selected engine is not supported.

    ArgumentError
        Raised if the input sequence is invalid or contains unsupported codes.

    NotSupportedFormError
        Raised if the output form is not recognized or supported.

    Notes
    -----
    - The sequence must contain amino acid and/or capping group codes recognized by the selected engine.
    - Terminal caps can be specified explicitly by using residue names such as 'ACE' (N-terminus) and 'NME' (C-terminus).
    - The resulting structure is built in vacuum and can be subsequently solvated using :func:`molsysmt.build.solvate`.

    See Also
    --------
    :func:`molsysmt.build.add_missing_terminal_cappings`
        Add terminal groups to complete or neutralize peptide ends.

    :func:`molsysmt.build.solvate`
        Surround a molecular system with solvent molecules.

    :func:`molsysmt.structure.center`
        Center a molecular system in a simulation box.

    :func:`molsysmt.basic.view`
        Visualize the resulting molecular system in a Jupyter notebook.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.build.build_peptide('AceGlyGlyNme')
    >>> msm.basic.get(molsys, n_groups=True)
    4

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:  
       :ref:`User Guide > Tools > Build > Build peptide <Tutorial_Build_peptide>`

    .. versionadded:: 1.0.0
    """

    if engine=="LEaP":

        from molsysmt.basic import convert
        from os import getcwd, chdir
        from molsysmt.thirds.tleap import TLeap
        from molsysmt._private.files_and_directories import temp_directory, temp_filename
        from shutil import rmtree, copyfile

        sequence = convert(molecular_system, to_form='string:amino_acids_3')
        sequence = sequence.upper()
        sequence = ' '.join([sequence[ii:ii+3] for ii in range(0, len(sequence), 3)])

        current_directory = getcwd()
        working_directory = temp_directory()
        temp_prmtop = temp_filename(dir=working_directory, extension='prmtop')
        temp_inpcrd = temp_prmtop.replace('prmtop','inpcrd')
        temp_logfile = temp_prmtop.replace('prmtop','leap.log')

        if False:
            print('Working directory:', working_directory)

        tleap = TLeap()

        # 'AMBER14'
        tleap.load_parameters("leaprc.protein.ff14SB")

        # implicit_solvent 'OBC1'
        tleap.set_global_parameter(PBRadii='mbondi2')

        tleap.make_sequence('peptide', sequence)
        tleap.check_unit('peptide')
        tleap.get_total_charge('peptide')

        tleap.save_unit('peptide', temp_prmtop)

        errors=tleap.run(working_directory=working_directory, verbose=False)

        del(tleap)

        temp_item = convert([temp_prmtop, temp_inpcrd], to_form=to_form)

        if to_form in ['molsysmt.MolSys', 'molsysmt.Topology']:
            temp_item.topology.chains['chain_name'] = 'A'

        rmtree(working_directory)

    elif engine=="MolSysMT":

        from molsysmt.basic import convert
        from molsysmt.native import MolSys
        from molsysmt import pyunitwizard as puw
        from molsysmt.element.group.amino_acid import group_names as amino_acid_group_names
        from molsysmt.element.group.amino_acid import get_group_db as get_amino_acid_group_db
        from molsysmt.element.group.terminal_capping import group_names as terminal_capping_group_names
        from molsysmt.element.group.terminal_capping import get_group_db as get_terminal_capping_group_db

        peptide_builder_templates = _get_peptide_builder_templates()
        if not peptide_builder_templates:
            warnings.warn(
                "Peptide-builder template database could not be loaded; using fallback topology templates.",
                UserWarning,
                stacklevel=2,
            )

        sequence = convert(molecular_system, to_form='string:amino_acids_3')
        sequence = sequence.upper()
        if sequence == '':
            raise ValueError("Input peptide sequence is empty.")
        group_names = [sequence[ii:ii+3] for ii in range(0, len(sequence), 3)]

        amino_acid_group_names = set(amino_acid_group_names)
        terminal_capping_group_names = set(terminal_capping_group_names)

        for group_name in group_names:
            if group_name not in amino_acid_group_names and group_name not in terminal_capping_group_names:
                raise ValueError(f"Unsupported residue or capping group: {group_name}")

        amino_group_indices = [ii for ii, group_name in enumerate(group_names) if group_name in amino_acid_group_names]
        first_amino_group_index = amino_group_indices[0] if amino_group_indices else None
        last_amino_group_index = amino_group_indices[-1] if amino_group_indices else None

        groups_data = []

        for group_index, group_name in enumerate(group_names):
            if group_name in terminal_capping_group_names:
                template_name = group_name
                group_type = "terminal capping"
            else:
                # Match current LEaP behavior used by MolSysMT: uncapped peptides are
                # built from standard residue templates (no forced N*/C* termini forms).
                template_name = group_name
                group_type = "amino acid"

            resolved_template_name = _resolve_template_alias(template_name, peptide_builder_templates)
            if resolved_template_name is not None:
                template_data = peptide_builder_templates[resolved_template_name]

                atom_names = list(template_data["atom_names"])
                atom_types = []
                for atom_name, atomic_number in zip(atom_names, template_data["atom_elements"]):
                    atom_type = _atomic_number_to_symbol(atomic_number)
                    if atom_type is None:
                        atom_type = _guess_atom_type(atom_name)
                    atom_types.append(atom_type)

                coordinates_nm = np.array(template_data["coordinates_nm"], dtype=float)

                groups_data.append(
                    {
                        "group_name": group_name,
                        "group_type": group_type,
                        "template_name": resolved_template_name,
                        "atom_names": atom_names,
                        "atom_types": atom_types,
                        "atom_ff_types": list(template_data.get("atom_types", atom_types)),
                        "bonded_atom_indices": [tuple(pair) for pair in template_data["bonds"]],
                        "coordinates_nm": coordinates_nm,
                        "connect": template_data.get("connect", [None, None]),
                        "atom_name_to_local_index": {name: idx for idx, name in enumerate(atom_names)},
                    }
                )
            else:
                if group_name in terminal_capping_group_names:
                    group_db = get_terminal_capping_group_db(group_name)
                    topology = _pick_topology_variant(group_db['topology'])
                else:
                    group_db = get_amino_acid_group_db(template_name)

                    if template_name == group_name:
                        if group_index == last_amino_group_index:
                            topology = _pick_topology_variant(group_db['topology'], prefer_oxt=True)
                        else:
                            topology = _pick_topology_variant(group_db['topology'], prefer_oxt=False)
                    else:
                        topology = _pick_topology_variant(group_db['topology'])

                atom_names = list(topology["atoms"])
                atom_types = [_guess_atom_type(atom_name) for atom_name in atom_names]
                local_atom_indices = {atom_name: ii for ii, atom_name in enumerate(atom_names)}
                bonded_atom_indices = []
                for atom_name_1, atom_name_2 in list(topology["bonds"]):
                    if atom_name_1 in local_atom_indices and atom_name_2 in local_atom_indices:
                        ii = local_atom_indices[atom_name_1]
                        jj = local_atom_indices[atom_name_2]
                        if ii < jj:
                            bonded_atom_indices.append((ii, jj))
                        else:
                            bonded_atom_indices.append((jj, ii))
                bonded_atom_indices = sorted(set(bonded_atom_indices))

                head_index = local_atom_indices.get("N", None)
                tail_index = local_atom_indices.get("C", None)

                groups_data.append(
                    {
                        "group_name": group_name,
                        "group_type": group_type,
                        "template_name": template_name,
                        "atom_names": atom_names,
                        "atom_types": atom_types,
                        "atom_ff_types": list(atom_types),
                        "bonded_atom_indices": bonded_atom_indices,
                        "coordinates_nm": _place_group_coordinates(0.0, atom_names),
                        "connect": [head_index, tail_index],
                        "atom_name_to_local_index": local_atom_indices,
                    }
                )

        n_groups = len(groups_data)
        n_atoms = sum(len(group_data["atom_names"]) for group_data in groups_data)

        atom_names = []
        atom_types = []
        atom_group_indices = []
        atom_component_indices = []
        atom_chain_indices = []
        atom_ff_types = []
        all_bonds = []
        coordinates = np.zeros((n_atoms, 3), dtype=float)
        group_start_indices = []
        registered_bonds = set()
        registered_bonded_matrix = np.zeros((n_atoms, n_atoms), dtype=np.uint8)

        peptide_bond_length = 0.133
        previous_tail_coordinates = None
        fallback_anchor_x = 0.0

        atom_index = 0
        for group_index, group_data in enumerate(groups_data):
            atom_names_in_group = group_data["atom_names"]
            atom_types_in_group = group_data["atom_types"]
            atom_ff_types_in_group = group_data["atom_ff_types"]
            local_coordinates = group_data["coordinates_nm"]
            local_bonded_atom_indices = group_data["bonded_atom_indices"]
            head_index, tail_index = group_data["connect"]

            if group_index == 0:
                if head_index is not None:
                    anchor_index = head_index
                elif tail_index is not None:
                    anchor_index = tail_index
                else:
                    anchor_index = 0
                group_coordinates = local_coordinates - local_coordinates[anchor_index]
            else:
                if previous_tail_coordinates is not None and head_index is not None:
                    skip_local_cn_scan = False
                    bond_direction = np.array([1.0, 0.0, 0.0], dtype=float)
                    previous_group_data = groups_data[group_index - 1]
                    previous_group_start = group_start_indices[group_index - 1]
                    previous_name_to_index = previous_group_data["atom_name_to_local_index"]
                    previous_tail_local_index = previous_group_data["connect"][1]

                    ca_local_index = previous_name_to_index.get("CA", None)
                    oxygen_local_index = previous_name_to_index.get("O", None)
                    if oxygen_local_index is None:
                        oxygen_local_index = previous_name_to_index.get("OXT", None)

                    # Prefer a trigonal-planar estimate around the previous carbonyl C:
                    # place the new N opposite to the CA/O directions.
                    if ca_local_index is not None and oxygen_local_index is not None:
                        ca_coordinates = coordinates[previous_group_start + ca_local_index, :]
                        oxygen_coordinates = coordinates[previous_group_start + oxygen_local_index, :]
                        direction_from_ca = _normalize(ca_coordinates - previous_tail_coordinates)
                        direction_from_oxygen = _normalize(oxygen_coordinates - previous_tail_coordinates)
                        if direction_from_ca is not None and direction_from_oxygen is not None:
                            trigonal_sum = direction_from_ca + direction_from_oxygen
                            if np.linalg.norm(trigonal_sum) > 1.0e-3:
                                trigonal_direction = _normalize(-trigonal_sum)
                                if trigonal_direction is not None:
                                    bond_direction = trigonal_direction
                    elif oxygen_local_index is not None and previous_tail_local_index is not None:
                        oxygen_coordinates = coordinates[previous_group_start + oxygen_local_index, :]
                        direction_from_oxygen = _normalize(previous_tail_coordinates - oxygen_coordinates)

                        candidate_directions = []
                        if direction_from_oxygen is not None:
                            candidate_directions.append(direction_from_oxygen)

                        # For capping/non-amino groups, mimic LEaP-like planar choice by using
                        # an additional heavy substituent at the carbonyl center when available.
                        substituent_local_index = None
                        oxygen_local_candidates = {oxygen_local_index}
                        for local_i, local_j in previous_group_data["bonded_atom_indices"]:
                            neighbor_local_index = None
                            if local_i == previous_tail_local_index:
                                neighbor_local_index = local_j
                            elif local_j == previous_tail_local_index:
                                neighbor_local_index = local_i
                            if neighbor_local_index is None or neighbor_local_index in oxygen_local_candidates:
                                continue
                            atom_name_neighbor = previous_group_data["atom_names"][neighbor_local_index]
                            atom_type_neighbor = previous_group_data["atom_types"][neighbor_local_index]
                            if atom_name_neighbor.startswith("H") or atom_type_neighbor == "H":
                                continue
                            substituent_local_index = neighbor_local_index
                            break

                        if substituent_local_index is not None:
                            substituent_coordinates = coordinates[previous_group_start + substituent_local_index, :]
                            direction_from_substituent = _normalize(
                                substituent_coordinates - previous_tail_coordinates
                            )
                            if direction_from_substituent is not None and direction_from_oxygen is not None:
                                trigonal_sum = direction_from_substituent + direction_from_oxygen
                                if np.linalg.norm(trigonal_sum) > 1.0e-3:
                                    trigonal_direction = _normalize(-trigonal_sum)
                                    if trigonal_direction is not None:
                                        candidate_directions.append(trigonal_direction)

                        if candidate_directions:
                            best_direction = candidate_directions[0]
                            best_local_junction_score = -np.inf
                            best_global_score = -np.inf
                            substituent_coordinates = None
                            if substituent_local_index is not None:
                                substituent_coordinates = coordinates[previous_group_start + substituent_local_index, :]
                            for candidate_direction in candidate_directions:
                                target_coordinates = previous_tail_coordinates + peptide_bond_length * candidate_direction
                                translation = target_coordinates - local_coordinates[head_index]
                                candidate_coordinates = local_coordinates + translation
                                candidate_n_coordinates = candidate_coordinates[head_index, :]

                                # Reject geometrically implausible placements for capping links.
                                if np.linalg.norm(candidate_n_coordinates - oxygen_coordinates) < 0.12:
                                    continue
                                if substituent_coordinates is not None:
                                    if np.linalg.norm(candidate_n_coordinates - substituent_coordinates) < 0.12:
                                        continue

                                local_junction_score = np.linalg.norm(candidate_n_coordinates - oxygen_coordinates)
                                if substituent_coordinates is not None:
                                    local_junction_score = min(
                                        local_junction_score,
                                        np.linalg.norm(candidate_n_coordinates - substituent_coordinates),
                                    )

                                global_score = _minimum_nonbonded_heavy_distance(
                                    existing_coordinates=coordinates[:atom_index, :],
                                    existing_atom_types=atom_types,
                                    existing_bonds_set=registered_bonds,
                                    candidate_coordinates=candidate_coordinates,
                                    candidate_atom_types=atom_types_in_group,
                                    candidate_start_index=atom_index,
                                    existing_bonded_matrix=registered_bonded_matrix,
                                )
                                if local_junction_score > best_local_junction_score + 1.0e-10:
                                    best_local_junction_score = local_junction_score
                                    best_global_score = global_score
                                    best_direction = candidate_direction
                                elif abs(local_junction_score - best_local_junction_score) <= 1.0e-10:
                                    if global_score > best_global_score + 1.0e-10:
                                        best_global_score = global_score
                                        best_direction = candidate_direction
                                elif global_score > best_global_score + 1.0e-10 and (
                                    local_junction_score >= best_local_junction_score - 0.01
                                ):
                                    # Allow better global placement when local junction quality is comparable.
                                    best_global_score = global_score
                                    best_direction = candidate_direction
                            bond_direction = best_direction
                    elif oxygen_local_index is not None:
                        oxygen_coordinates = coordinates[previous_group_start + oxygen_local_index, :]
                        direction_from_oxygen = _normalize(previous_tail_coordinates - oxygen_coordinates)
                        if direction_from_oxygen is not None:
                            bond_direction = direction_from_oxygen

                    target_coordinates = previous_tail_coordinates + peptide_bond_length * bond_direction
                    translation = target_coordinates - local_coordinates[head_index]
                    group_coordinates = local_coordinates + translation

                    # Focused search for X->PRO links, where local ring closure geometry
                    # can otherwise lead to short C(carbonyl)-CD contacts.
                    current_group_is_proline = group_data["group_name"] == "PRO"
                    if current_group_is_proline:
                        previous_group_start = group_start_indices[group_index - 1]
                        previous_group_size = len(groups_data[group_index - 1]["atom_names"])
                        previous_group_coordinates = coordinates[
                            previous_group_start: previous_group_start + previous_group_size, :
                        ]
                        previous_group_names = groups_data[group_index - 1]["atom_names"]
                        previous_group_types = groups_data[group_index - 1]["atom_types"]

                        previous_name_to_index = groups_data[group_index - 1]["atom_name_to_local_index"]
                        oxygen_local_index = previous_name_to_index.get("O", None)
                        if oxygen_local_index is None:
                            oxygen_local_index = previous_name_to_index.get("OXT", None)
                        oxygen_coordinates = None
                        if oxygen_local_index is not None:
                            oxygen_coordinates = coordinates[previous_group_start + oxygen_local_index, :]

                        best_objective_score = -np.inf
                        best_local_score = -np.inf
                        best_geometry_penalty = np.inf
                        best_candidate_coordinates = group_coordinates

                        capping_substituent_local_index = None
                        for local_i, local_j in groups_data[group_index - 1]["bonded_atom_indices"]:
                            neighbor_local_index = None
                            if local_i == previous_group_data["connect"][1]:
                                neighbor_local_index = local_j
                            elif local_j == previous_group_data["connect"][1]:
                                neighbor_local_index = local_i
                            if neighbor_local_index is None or neighbor_local_index == oxygen_local_index:
                                continue
                            atom_name_neighbor = groups_data[group_index - 1]["atom_names"][neighbor_local_index]
                            atom_type_neighbor = groups_data[group_index - 1]["atom_types"][neighbor_local_index]
                            if atom_name_neighbor.startswith("H") or atom_type_neighbor == "H":
                                continue
                            capping_substituent_local_index = neighbor_local_index
                            break

                        capping_substituent_coordinates = None
                        if capping_substituent_local_index is not None:
                            capping_substituent_coordinates = coordinates[
                                previous_group_start + capping_substituent_local_index, :
                            ]

                        # Imitate LEaP-like peptide-junction geometry:
                        # 1) Search N placement around carbonyl C in a near-sp2 angular window.
                        # 2) Optimize rigid orientation of PRO around C-N and N-CA.
                        direction_candidates = _fibonacci_unit_vectors(320)
                        direction_trigonal = None
                        if oxygen_coordinates is not None and capping_substituent_coordinates is not None:
                            direction_from_oxygen = _normalize(oxygen_coordinates - previous_tail_coordinates)
                            direction_from_substituent = _normalize(
                                capping_substituent_coordinates - previous_tail_coordinates
                            )
                            if direction_from_oxygen is not None and direction_from_substituent is not None:
                                direction_trigonal = _normalize(
                                    -(direction_from_oxygen + direction_from_substituent)
                                )
                        if direction_trigonal is not None:
                            direction_candidates.insert(0, direction_trigonal)

                        proline_ca_local_index = group_data["atom_name_to_local_index"].get("CA", None)
                        proline_cd_local_index = group_data["atom_name_to_local_index"].get("CD", None)
                        previous_alpha_local_index = previous_name_to_index.get("CA", None)
                        if previous_alpha_local_index is None:
                            previous_alpha_local_index = previous_name_to_index.get("CH3", None)
                        previous_alpha_coordinates = None
                        if previous_alpha_local_index is not None:
                            previous_alpha_coordinates = coordinates[
                                previous_group_start + previous_alpha_local_index, :
                            ]
                        orientation_matrices = [np.eye(3, dtype=float)]
                        rng_orient = np.random.default_rng(1729 + group_index)
                        for _ in range(47):
                            random_values = rng_orient.random(3)
                            u_1, u_2, u_3 = random_values[0], random_values[1], random_values[2]
                            quaternion = np.array(
                                [
                                    np.sqrt(1.0 - u_1) * np.sin(2.0 * np.pi * u_2),
                                    np.sqrt(1.0 - u_1) * np.cos(2.0 * np.pi * u_2),
                                    np.sqrt(u_1) * np.sin(2.0 * np.pi * u_3),
                                    np.sqrt(u_1) * np.cos(2.0 * np.pi * u_3),
                                ],
                                dtype=float,
                            )
                            qx, qy, qz, qw = quaternion
                            rotation_matrix = np.array(
                                [
                                    [1.0 - 2.0 * (qy * qy + qz * qz), 2.0 * (qx * qy - qz * qw), 2.0 * (qx * qz + qy * qw)],
                                    [2.0 * (qx * qy + qz * qw), 1.0 - 2.0 * (qx * qx + qz * qz), 2.0 * (qy * qz - qx * qw)],
                                    [2.0 * (qx * qz - qy * qw), 2.0 * (qy * qz + qx * qw), 1.0 - 2.0 * (qx * qx + qy * qy)],
                                ],
                                dtype=float,
                            )
                            orientation_matrices.append(rotation_matrix)

                        for direction in direction_candidates:
                            candidate_target = previous_tail_coordinates + peptide_bond_length * direction

                            angle_oxygen = None
                            if oxygen_coordinates is not None:
                                angle_oxygen = _angle_degrees(
                                    oxygen_coordinates, previous_tail_coordinates, candidate_target
                                )
                            angle_substituent = None
                            if capping_substituent_coordinates is not None:
                                angle_substituent = _angle_degrees(
                                    capping_substituent_coordinates, previous_tail_coordinates, candidate_target
                                )

                            # Keep peptide carbonyl center in a realistic near-sp2 angular region.
                            if angle_oxygen is not None and (angle_oxygen < 105.0 or angle_oxygen > 135.0):
                                continue
                            if angle_substituent is not None and (angle_substituent < 105.0 or angle_substituent > 135.0):
                                continue

                            candidate_translation = candidate_target - local_coordinates[head_index]
                            candidate_coordinates = local_coordinates + candidate_translation
                            for rotation_matrix in orientation_matrices:
                                rotated_coordinates = _apply_rotation(
                                    candidate_coordinates,
                                    rotation_matrix,
                                    candidate_target,
                                )
                                local_score = _minimum_nonbonded_heavy_distance_between_groups(
                                    left_coordinates=previous_group_coordinates,
                                    left_atom_names=previous_group_names,
                                    left_atom_types=previous_group_types,
                                    right_coordinates=rotated_coordinates,
                                    right_atom_names=atom_names_in_group,
                                    right_atom_types=atom_types_in_group,
                                    skip_pair_names=("C", "N"),
                                )

                                geometry_penalty = 0.0
                                if angle_oxygen is not None:
                                    geometry_penalty += 1.0 * abs(angle_oxygen - 123.0)
                                if angle_substituent is not None:
                                    geometry_penalty += 0.5 * abs(angle_substituent - 117.0)

                                if proline_ca_local_index is not None:
                                    angle_c_n_ca = _angle_degrees(
                                        previous_tail_coordinates,
                                        rotated_coordinates[head_index, :],
                                        rotated_coordinates[proline_ca_local_index, :],
                                    )
                                    if angle_c_n_ca is not None:
                                        geometry_penalty += 0.6 * abs(angle_c_n_ca - 122.0)
                                if proline_cd_local_index is not None:
                                    angle_c_n_cd = _angle_degrees(
                                        previous_tail_coordinates,
                                        rotated_coordinates[head_index, :],
                                        rotated_coordinates[proline_cd_local_index, :],
                                    )
                                    if angle_c_n_cd is not None:
                                        geometry_penalty += 0.2 * abs(angle_c_n_cd - 122.0)

                                if oxygen_coordinates is not None and proline_ca_local_index is not None:
                                    dihedral_ocnca = _dihedral_degrees(
                                        oxygen_coordinates,
                                        previous_tail_coordinates,
                                        rotated_coordinates[head_index, :],
                                        rotated_coordinates[proline_ca_local_index, :],
                                    )
                                    if dihedral_ocnca is not None:
                                        geometry_penalty += 0.3 * abs(_wrap_degrees(dihedral_ocnca))

                                if previous_alpha_coordinates is not None and proline_ca_local_index is not None:
                                    omega = _dihedral_degrees(
                                        previous_alpha_coordinates,
                                        previous_tail_coordinates,
                                        rotated_coordinates[head_index, :],
                                        rotated_coordinates[proline_ca_local_index, :],
                                    )
                                    if omega is not None:
                                        omega_abs = abs(_wrap_degrees(omega))
                                        geometry_penalty += 0.5 * abs(180.0 - omega_abs)

                                objective_score = local_score - 0.0006 * geometry_penalty
                                if objective_score > best_objective_score + 1.0e-10:
                                    best_objective_score = objective_score
                                    best_local_score = local_score
                                    best_geometry_penalty = geometry_penalty
                                    best_candidate_coordinates = rotated_coordinates
                                elif abs(objective_score - best_objective_score) <= 1.0e-10:
                                    if local_score > best_local_score + 1.0e-10:
                                        best_local_score = local_score
                                        best_geometry_penalty = geometry_penalty
                                        best_candidate_coordinates = rotated_coordinates
                                    elif abs(local_score - best_local_score) <= 1.0e-10:
                                        if geometry_penalty < best_geometry_penalty - 1.0e-10:
                                            best_geometry_penalty = geometry_penalty
                                            best_candidate_coordinates = rotated_coordinates
                                elif abs(local_score - best_local_score) <= 1.0e-10:
                                    if geometry_penalty < best_geometry_penalty - 1.0e-10:
                                        best_geometry_penalty = geometry_penalty
                                        best_candidate_coordinates = rotated_coordinates

                        group_coordinates = best_candidate_coordinates
                        target_coordinates = group_coordinates[head_index, :].copy()
                        skip_local_cn_scan = True

                    # Optimize torsion around the peptide C-N axis to reduce local clashes.
                    if atom_index > 0 and (not skip_local_cn_scan):
                        axis = _normalize(target_coordinates - previous_tail_coordinates)
                        if axis is not None:
                            best_coordinates = group_coordinates
                            best_score = _minimum_nonbonded_heavy_distance(
                                existing_coordinates=coordinates[:atom_index, :],
                                existing_atom_types=atom_types,
                                existing_bonds_set=registered_bonds,
                                candidate_coordinates=group_coordinates,
                                candidate_atom_types=atom_types_in_group,
                                candidate_start_index=atom_index,
                                existing_bonded_matrix=registered_bonded_matrix,
                            )
                            for angle in np.linspace(0.0, 2.0 * np.pi, num=24, endpoint=False):
                                rotation = _rotation_matrix_from_axis_angle(axis, angle)
                                trial_coordinates = _apply_rotation(group_coordinates, rotation, target_coordinates)
                                score = _minimum_nonbonded_heavy_distance(
                                    existing_coordinates=coordinates[:atom_index, :],
                                    existing_atom_types=atom_types,
                                    existing_bonds_set=registered_bonds,
                                    candidate_coordinates=trial_coordinates,
                                    candidate_atom_types=atom_types_in_group,
                                    candidate_start_index=atom_index,
                                    existing_bonded_matrix=registered_bonded_matrix,
                                )
                                if score > best_score:
                                    best_score = score
                                    best_coordinates = trial_coordinates
                            group_coordinates = best_coordinates

                            # Refine by rigid tilts around two perpendicular axes through N when
                            # local heavy-atom proximity indicates compressed backbone geometry.
                            if best_score < 0.22:
                                axis_u = _orthogonal_unit(axis)
                                axis_v = _normalize(np.cross(axis, axis_u))
                                if axis_v is None:
                                    axis_v = np.array([0.0, 0.0, 1.0], dtype=float)

                                tilt_angles = np.deg2rad(
                                    np.array([-50.0, -35.0, -20.0, 0.0, 20.0, 35.0, 50.0], dtype=float)
                                )
                                for angle_u in tilt_angles:
                                    rotation_u = _rotation_matrix_from_axis_angle(axis_u, angle_u)
                                    tilted_u = _apply_rotation(best_coordinates, rotation_u, target_coordinates)
                                    for angle_v in tilt_angles:
                                        rotation_v = _rotation_matrix_from_axis_angle(axis_v, angle_v)
                                        tilted_uv = _apply_rotation(tilted_u, rotation_v, target_coordinates)
                                        score = _minimum_nonbonded_heavy_distance(
                                            existing_coordinates=coordinates[:atom_index, :],
                                            existing_atom_types=atom_types,
                                            existing_bonds_set=registered_bonds,
                                            candidate_coordinates=tilted_uv,
                                            candidate_atom_types=atom_types_in_group,
                                            candidate_start_index=atom_index,
                                            existing_bonded_matrix=registered_bonded_matrix,
                                        )
                                        if score > best_score:
                                            best_score = score
                                            group_coordinates = tilted_uv
                else:
                    group_coordinates = local_coordinates + np.array([fallback_anchor_x, 0.0, 0.0], dtype=float)

            # Keep peptide-bond geometry intact; clashes are handled by torsion scan + warning.

            fallback_anchor_x = max(fallback_anchor_x, float(np.max(group_coordinates[:, 0])) + 0.25)
            previous_tail_coordinates = None

            for local_atom_index, atom_name in enumerate(atom_names_in_group):
                atom_names.append(atom_name)
                atom_types.append(atom_types_in_group[local_atom_index])
                atom_ff_types.append(atom_ff_types_in_group[local_atom_index])
                atom_group_indices.append(group_index)
                atom_component_indices.append(group_index)
                atom_chain_indices.append(0)
                coordinates[atom_index, :] = group_coordinates[local_atom_index, :]
                atom_index += 1

            group_start = atom_index - len(atom_names_in_group)
            group_start_indices.append(group_start)
            for atom_index_1_local, atom_index_2_local in group_data["bonded_atom_indices"]:
                atom_index_1 = group_start + atom_index_1_local
                atom_index_2 = group_start + atom_index_2_local
                if atom_index_1 < atom_index_2:
                    bond = (atom_index_1, atom_index_2)
                else:
                    bond = (atom_index_2, atom_index_1)
                all_bonds.append(bond)
                registered_bonds.add(bond)
                registered_bonded_matrix[bond[0], bond[1]] = 1
                registered_bonded_matrix[bond[1], bond[0]] = 1

            if tail_index is not None:
                previous_tail_coordinates = coordinates[group_start + tail_index, :]

        for group_index in range(n_groups - 1):
            left_connect = groups_data[group_index]["connect"]
            right_connect = groups_data[group_index + 1]["connect"]
            left_tail = left_connect[1]
            right_head = right_connect[0]
            if left_tail is None or right_head is None:
                continue
            left_group_start = group_start_indices[group_index]
            right_group_start = group_start_indices[group_index + 1]
            atom_index_1 = left_group_start + left_tail
            atom_index_2 = right_group_start + right_head
            if atom_index_1 < atom_index_2:
                bond = (atom_index_1, atom_index_2)
            else:
                bond = (atom_index_2, atom_index_1)
            all_bonds.append(bond)
            registered_bonds.add(bond)
            registered_bonded_matrix[bond[0], bond[1]] = 1
            registered_bonded_matrix[bond[1], bond[0]] = 1

        all_bonds = sorted(set(all_bonds))
        n_bonds = len(all_bonds)

        coordinates = _align_capping_junction_geometry(
            coordinates=coordinates,
            atom_types=atom_types,
            groups_data=groups_data,
            group_start_indices=group_start_indices,
        )

        coordinates = _optimize_peptide_torsions(
            coordinates=coordinates,
            atom_types=atom_types,
            bonds=all_bonds,
            groups_data=groups_data,
            group_start_indices=group_start_indices,
            n_rounds=2,
            n_angles=24,
        )

        # Keep backbone torsions as generated by the LEaP-inspired linker construction.
        # Global backbone scans can over-optimize special cases (e.g., constrained PRO links).
        # coordinates = _optimize_backbone_torsions(
        #     coordinates=coordinates,
        #     atom_types=atom_types,
        #     atom_names=atom_names,
        #     bonds=all_bonds,
        #     groups_data=groups_data,
        #     group_start_indices=group_start_indices,
        #     n_rounds=1,
        #     n_angles=18,
        # )

        coordinates = _optimize_sidechain_torsions(
            coordinates=coordinates,
            atom_types=atom_types,
            atom_names=atom_names,
            bonds=all_bonds,
            groups_data=groups_data,
            group_start_indices=group_start_indices,
            n_rounds=1,
            n_angles=12,
        )

        temp_item = MolSys(
            n_atoms=n_atoms,
            n_groups=n_groups,
            n_components=n_groups,
            n_molecules=1,
            n_entities=1,
            n_chains=1,
            n_bonds=n_bonds,
            skip_digestion=True,
        )

        temp_item.topology.atoms['atom_id'] = np.arange(n_atoms)
        temp_item.topology.atoms['atom_name'] = atom_names
        temp_item.topology.atoms['atom_type'] = atom_types
        temp_item.topology.atoms['atom_ff_type'] = atom_ff_types
        temp_item.topology.atoms['group_index'] = atom_group_indices
        temp_item.topology.atoms['component_index'] = atom_component_indices
        temp_item.topology.atoms['chain_index'] = atom_chain_indices

        temp_item.topology.groups['group_id'] = np.arange(n_groups)
        temp_item.topology.groups['group_name'] = [group_data["group_name"] for group_data in groups_data]
        temp_item.topology.groups['group_type'] = [group_data["group_type"] for group_data in groups_data]
        temp_item.topology.groups['molecule_index'] = 0

        temp_item.topology.components['component_id'] = np.arange(n_groups)
        temp_item.topology.components['component_name'] = [group_data["group_name"] for group_data in groups_data]
        temp_item.topology.components['component_type'] = [group_data["group_type"] for group_data in groups_data]

        temp_item.topology.molecules['molecule_id'] = [0]
        temp_item.topology.molecules['molecule_name'] = ['peptide']
        temp_item.topology.molecules['molecule_type'] = ['peptide']
        temp_item.topology.molecules['entity_index'] = [0]

        temp_item.topology.entities['entity_id'] = [0]
        temp_item.topology.entities['entity_name'] = ['peptide']
        temp_item.topology.entities['entity_type'] = ['protein']

        temp_item.topology.chains['chain_id'] = [0]
        temp_item.topology.chains['chain_name'] = ['A']
        temp_item.topology.chains['chain_type'] = ['protein']

        if n_bonds > 0:
            temp_item.topology.bonds['atom1_index'] = np.array([bond[0] for bond in all_bonds], dtype=int)
            temp_item.topology.bonds['atom2_index'] = np.array([bond[1] for bond in all_bonds], dtype=int)
        temp_item.topology.bonds._remove_empty_columns()

        heavy_mask_final, bonded_matrix_final = _prepare_nonbonded_heavy_distance_full(atom_types, all_bonds)
        min_nonbonded_heavy_distance = _minimum_nonbonded_heavy_distance_full(
            coordinates=coordinates,
            heavy_mask=heavy_mask_final,
            bonded_matrix=bonded_matrix_final,
        )
        if min_nonbonded_heavy_distance < 0.12:
            warnings.warn(
                (
                    "The initial peptide geometry contains close heavy-atom contacts "
                    f"(minimum non-bonded heavy-heavy distance: {min_nonbonded_heavy_distance:.3f} nm). "
                    "Running a geometry minimization is recommended."
                ),
                UserWarning,
                stacklevel=2,
            )

        temp_item.structures.coordinates = puw.standardize(puw.quantity(coordinates[np.newaxis, :, :], 'nm'))
        temp_item.structures.n_atoms = n_atoms
        temp_item.structures.n_structures = 1

        if to_form != 'molsysmt.MolSys':
            temp_item = convert(temp_item, to_form=to_form)

    else:

        raise NotImplementedError

    return temp_item
