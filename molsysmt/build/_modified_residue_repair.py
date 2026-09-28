"""Preflight exact chemical templates before native modified-residue repair."""

from __future__ import annotations

import numpy as np
import pandas as pd


def assess_modified_residue(topo, group_idx, missing_names, template, coordinates):
    """Return local anchors and a reason when repair cannot be assessed."""

    rows = topo.atoms[topo.atoms["group_index"] == group_idx]
    names = rows["atom_name"].tolist()
    heavy_rows = rows[~rows["atom_name"].str.match(r"^(?:H|[0-9]H)")]
    heavy_names = heavy_rows["atom_name"].tolist()
    atom_to_element = dict(zip(template["atoms"], template["elements"]))
    if len(names) != len(set(names)):
        return None, "duplicate atom names"
    if not set(heavy_names) <= set(atom_to_element):
        return None, "observed atom names do not match the exact template"
    for row in heavy_rows.itertuples():
        if str(row.atom_type).capitalize() != atom_to_element[row.atom_name]:
            return None, f"element mismatch for {row.atom_name}"

    # Multiple missing branch atoms admit rotamers or equivalent oxygen labels.
    sidechain = set(template["atoms"]) - {"N", "CA", "C", "O", "OXT"}
    if len(sidechain.intersection(missing_names)) > 1:
        return None, "multiple missing side-chain atoms have ambiguous placement"

    adjacency = {name: set() for name in template["atoms"]}
    for atom1, atom2 in template["bonds"]:
        adjacency[atom1].add(atom2)
        adjacency[atom2].add(atom1)

    current_bonds = topo._get_chemical_state_bonds()
    group_indices = set(rows.index)
    template_orders = {
        frozenset(pair): order
        for pair, order in zip(template["bonds"], template["bond_orders"])
    }
    for bond in current_bonds.itertuples():
        atom1, atom2 = int(bond.atom1_index), int(bond.atom2_index)
        if atom1 not in group_indices or atom2 not in group_indices:
            continue
        pair = frozenset(
            (topo.atoms.at[atom1, "atom_name"], topo.atoms.at[atom2, "atom_name"])
        )
        if any(name not in atom_to_element for name in pair):
            continue  # The curated template contains heavy-atom bonds only.
        if pair not in template_orders:
            return None, "observed connectivity conflicts with the exact template"
        if (
            not pd.isna(bond.bond_order)
            and int(bond.bond_order) != template_orders[pair]
        ):
            return None, "observed bond order conflicts with the exact template"

    anchors_by_atom = {}
    present = set(heavy_names)
    for missing in missing_names:
        distance = {missing: 0}
        frontier = [missing]
        while frontier:
            node = frontier.pop(0)
            for neighbor in adjacency[node]:
                if neighbor not in distance:
                    distance[neighbor] = distance[node] + 1
                    frontier.append(neighbor)
        anchors = []
        for radius in (2, 3):
            anchors = [
                name
                for name in template["atoms"]
                if name in present and distance.get(name, 99) <= radius
            ]
            if len(anchors) >= 3:
                break
        if len(anchors) < 3:
            return None, f"too few local anchors for {missing}"
        template_coords = np.asarray(template["coords_nm"])
        lookup = dict(zip(template["atoms"], template_coords))
        if (
            np.linalg.matrix_rank(
                np.array([lookup[name] for name in anchors]) - lookup[anchors[0]],
                tol=1e-4,
            )
            < 2
        ):
            return None, f"collinear template anchors for {missing}"
        actual_indices = [rows.index[names.index(name)] for name in anchors]
        for frame in coordinates:
            points = frame[actual_indices]
            if (
                not np.isfinite(points).all()
                or np.linalg.matrix_rank(points - points[0], tol=1e-4) < 2
            ):
                return None, f"invalid observed anchors for {missing}"
        anchors_by_atom[missing] = anchors
    return anchors_by_atom, None
