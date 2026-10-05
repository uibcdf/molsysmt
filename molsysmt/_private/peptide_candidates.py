"""Discovering sparse backbone neighbors for the public peptide report."""

from collections import Counter
from numbers import Integral

import numpy as np

from molsysmt import pyunitwizard as puw


def discover_backbone_pairs(
    source, groups, names, chains, structure_index, ceiling, pbc
):
    """Search the full source backbone before applying the output selection."""
    from molsysmt._private.covalent_candidates import read_geometry
    from molsysmt.native import Structures
    from molsysmt.structure import get_neighbors

    roles = {"C": [], "N": []}
    atom_groups = {}
    for group in groups:
        index = group["group_index"]
        for atom, name in zip(group["atom_indices"], names[index]):
            if name in roles:
                atom = int(atom)
                roles[name].append(atom)
                atom_groups[atom] = index
    atoms = sorted(atom_groups)
    report = {
        "status": "unassessed",
        "reason_codes": [],
        "pbc_applied": False,
        "atom_indices": np.asarray(atoms, dtype=np.int64),
        "blocked_chain_indices": np.empty(0, dtype=np.int64),
        "unassessed_group_indices": np.asarray(
            sorted(
                {
                    group
                    for group in atom_groups.values()
                    if not isinstance(chains[group], Integral) or chains[group] < 0
                }
            ),
            dtype=np.int64,
        ),
        "scope": "all_source_named_backbone_endpoints",
    }
    if not atoms:
        report["reason_codes"].append("no_backbone_endpoints")
        report["status"] = "assessed"
        return [], set(), report, atoms, None
    if structure_index is None:
        report["reason_codes"].append("coordinates_unavailable")
        return [], set(), report, atoms, None
    geometry = read_geometry(source, atoms, structure_index)
    if geometry["coordinates"] is None:
        report["reason_codes"].append("coordinates_unavailable")
        return [], set(), report, atoms, geometry
    coordinates = puw.get_value(geometry["coordinates"], to_unit="nm")[0]
    box = geometry["box"] if pbc else None
    if box is not None:
        values = puw.get_value(box, to_unit="nm")
        if (
            values.shape != (1, 3, 3)
            or not np.isfinite(values).all()
            or np.linalg.det(values[0]) <= 0
        ):
            report["reason_codes"].append("invalid_periodic_box")
            return [], set(), report, atoms, geometry
    alternates = geometry["alternate_location"]
    if alternates is not None and not isinstance(alternates[0], dict):
        report["reason_codes"].append("unsupported_alternate_site_evidence")
        return [], set(), report, atoms, geometry
    alternate_atoms = set() if alternates is None else set(alternates[0])
    local = {atom: index for index, atom in enumerate(atoms)}
    finite = {atom for atom in atoms if np.isfinite(coordinates[local[atom]]).all()}
    blocked_chains = {
        int(chains[atom_groups[atom]])
        for atom in (set(atoms) - finite) | alternate_atoms
        if isinstance(chains[atom_groups[atom]], Integral)
        and chains[atom_groups[atom]] >= 0
    }
    report["blocked_chain_indices"] = np.asarray(sorted(blocked_chains), dtype=np.int64)
    if blocked_chains:
        report["reason_codes"].append("incomplete_backbone_geometry")
    valid = {
        role: [
            atom
            for atom in values
            if atom in finite
            and isinstance(chains[atom_groups[atom]], Integral)
            and chains[atom_groups[atom]] >= 0
        ]
        for role, values in roles.items()
    }
    if report["unassessed_group_indices"].size:
        report["reason_codes"].append("missing_or_ambiguous_chain")
    report["status"] = (
        "partial"
        if blocked_chains or report["unassessed_group_indices"].size
        else "assessed"
    )
    if not valid["C"] or not valid["N"]:
        return [], set(), report, atoms, geometry
    coordinate_source = Structures(coordinates=geometry["coordinates"], box=box)
    offsets, neighbors, _ = get_neighbors(
        coordinate_source,
        selection=[local[atom] for atom in valid["C"]],
        selection_2=[local[atom] for atom in valid["N"]],
        structure_indices=[0],
        threshold=puw.quantity(ceiling, "nm"),
        pbc=box is not None,
        output_type="csr",
        skip_digestion=True,
    )
    report["pbc_applied"] = box is not None
    pairs = set()
    for row, carbon in enumerate(valid["C"]):
        g = atom_groups[carbon]
        for neighbor in neighbors[offsets[row] : offsets[row + 1]]:
            h = atom_groups[valid["N"][int(neighbor)]]
            if g != h and chains[g] == chains[h]:
                pairs.add((g, h))
    outgoing = Counter(g for g, _ in pairs)
    incoming = Counter(h for _, h in pairs)
    ambiguous = {(g, h) for g, h in pairs if outgoing[g] > 1 or incoming[h] > 1}
    return sorted(pairs), ambiguous, report, atoms, geometry
