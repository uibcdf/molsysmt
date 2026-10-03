"""Comparing exact residue inventories without assigning or repairing chemistry."""

from collections import defaultdict
from copy import deepcopy
from hashlib import sha256
from importlib.resources import files

import numpy as np
import pandas as pd

from molsysmt._private.chemical_readiness import _assess_from_domains as audit_fields
from molsysmt._private.chemical_readiness import _domains
from molsysmt._private.residue_templates import (
    CURATED_MODIFIED_RESIDUES,
    load_residue_template,
)
from molsysmt._private.smonitor import (
    ArgumentError,
    NotWithThisFormError,
    StructuralInconsistencyError,
)
from molsysmt._private.variables import is_all


def _pairs(values):
    return np.asarray(sorted(values), dtype=np.int64).reshape(-1, 2)


def _template(name, names, cache):
    """Reuse exact owning reference tools; never resolve a sequence parent."""
    from molsysmt.element.atom import get_atom_type_from_atom_name
    from molsysmt.element.atom.names import atom as named_elements
    from molsysmt.element.group.amino_acid import (
        get_expected_heavy_atoms,
        get_group_db,
        group_names,
    )
    from molsysmt.element.group.amino_acid.get_expected_heavy_atoms import _is_hydrogen

    if name not in CURATED_MODIFIED_RESIDUES and name not in group_names:
        return None
    if name not in cache:
        modified = name in CURATED_MODIFIED_RESIDUES
        if modified:
            raw = load_residue_template(name)
            variants = [{"atoms": raw["atoms"], "bonds": raw["bonds"]}]
            elements = dict(zip(raw["atoms"], raw["elements"]))
            elements_origin = "declared_template"
            orders = {
                tuple(sorted(pair)): order
                for pair, order in zip(raw["bonds"], raw["bond_orders"])
            }
            resource = f"molsysmt.data.databases.residue_templates/{name}.json"
            provenance = deepcopy(raw["source"])
        else:
            variants = get_group_db(name)["topology"]
            all_names = set().union(*(set(v["atoms"]) for v in variants))
            elements = {
                atom: get_atom_type_from_atom_name(atom)
                for atom in sorted(all_names)
                if atom in named_elements
            }
            elements_origin = "standard_atom_name_mapping"
            orders = None
            resource = f"molsysmt.data.databases.amino_acids/{name[0]}.pkl.gz"
            provenance = {"original_sources": "unassessed"}
        package, basename = resource.rsplit("/", 1)
        provenance["packaged_sha256"] = sha256(
            files(package).joinpath(basename).read_bytes()
        ).hexdigest()
        cache[name] = (
            variants,
            elements,
            orders,
            resource,
            provenance,
            elements_origin,
            modified,
        )
    variants, elements, orders, resource, provenance, elements_origin, modified = cache[
        name
    ]
    key = (name, tuple(sorted(names)))
    if key not in cache:
        expected = get_expected_heavy_atoms(name, present_atom_names=sorted(names))
        if expected is None:
            expected = get_expected_heavy_atoms(name)
        cache[key] = set(expected) - ({"OXT"} if "OXT" not in names else set())
    expected = cache[key]
    candidates = [
        (index, variant)
        for index, variant in enumerate(variants)
        if {a for a in variant["atoms"] if not _is_hydrogen(a)} - {"OXT"}
        == expected - {"OXT"}
        and ("OXT" not in names or "OXT" in variant["atoms"])
    ]
    return {
        "expected": expected,
        "elements": elements,
        "orders": orders,
        "candidates": candidates,
        "modified": modified,
        "identity": {
            "group_name": name,
            "resource": resource,
            "variant_indices": [index for index, _ in candidates],
            "provenance": deepcopy(provenance),
            "element_reference": elements_origin,
        },
    }


def _hydrogens(template, names, indices, mapping_valid):
    from molsysmt.element.group.amino_acid.get_expected_heavy_atoms import _is_hydrogen

    candidates = []
    for index, variant in template["candidates"]:
        expected = {name for name in variant["atoms"] if _is_hydrogen(name)}
        candidates.append(
            {
                "variant_index": index,
                "expected_atom_names": sorted(expected),
                "missing_atom_names": sorted(expected - names),
                "unexpected_atom_names": sorted(names - expected),
            }
        )
    signatures = {tuple(c["expected_atom_names"]) for c in candidates}
    reason = (
        "heavy_only_template"
        if template["modified"]
        else "incomplete_or_conflicting_atom_mapping"
        if not mapping_valid
        else "ambiguous_hydrogen_template_variants"
        if len(signatures) != 1
        else None
    )
    # Heavy-only curated templates supply no hydrogen expectation, including
    # when the observed residue happens to contain zero hydrogen atoms.
    if template["modified"]:
        candidates = []
    return {
        "status": "unassessed"
        if reason
        else "incomplete"
        if candidates[0]["missing_atom_names"] or candidates[0]["unexpected_atom_names"]
        else "assessed",
        "reason_code": reason,
        "observed_atom_indices": indices.copy(),
        "candidates": candidates,
    }


def _connectivity(
    template,
    name_to_index,
    mapping_valid,
    records,
    readiness,
    hydrogen_indices,
    bond_fields,
):
    hydrogen_indices = set(hydrogen_indices)
    records = [
        record for record in records if not hydrogen_indices.intersection(record[1])
    ]
    empty = {
        "status": "unassessed",
        "reason_code": "ambiguous_atom_mapping",
        "expected_bonded_atom_pairs": _pairs([]),
        "missing_bonded_atom_pairs": _pairs([]),
        "blocked_by_missing_atom_name_pairs": [],
        "unexpected_bond_indices": np.empty(0, dtype=np.int64),
        "untyped_bond_indices": np.empty(0, dtype=np.int64),
        "examined_bond_indices": np.asarray([r[0] for r in records], dtype=np.int64),
        "bond_order": {
            "status": "unassessed",
            "reason_code": "no_reference_bond_orders",
            "missing_bond_indices": np.empty(0, dtype=np.int64),
            "conflict_bond_indices": np.empty(0, dtype=np.int64),
        },
    }
    if not mapping_valid:
        return empty
    if readiness["chemical_state_status"] != "resolved":
        empty["reason_code"] = "chemical_state_" + readiness["chemical_state_status"]
        return empty
    edge_sets = [
        {
            tuple(sorted(pair))
            for pair in variant["bonds"]
            if set(pair) <= template["expected"]
        }
        for _, variant in template["candidates"]
    ]
    if not edge_sets:
        empty["reason_code"] = "no_compatible_template_variant"
        return empty
    expected_names = set.intersection(*edge_sets)
    allowed_names = set.union(*edge_sets)
    expected_pairs = {
        tuple(sorted((name_to_index[a], name_to_index[b])))
        for a, b in expected_names
        if a in name_to_index and b in name_to_index
    }
    allowed_pairs = {
        tuple(sorted((name_to_index[a], name_to_index[b])))
        for a, b in allowed_names
        if a in name_to_index and b in name_to_index
    }
    types, orders = bond_fields
    covalent = [r for r in records if types.get(r[0]) == "covalent"]
    untyped = [r[0] for r in records if types.get(r[0]) is None]
    wrong_types = [
        r[0]
        for r in records
        if types.get(r[0]) not in (None, "covalent") and r[1] in expected_pairs
    ]
    observed = {r[1] for r in records}
    unexpected = [index for index, pair in covalent if pair not in allowed_pairs]
    missing = expected_pairs - observed
    ambiguous_graph = any(edges != edge_sets[0] for edges in edge_sets[1:])
    empty.update(
        {
            "status": "unassessed"
            if untyped or ambiguous_graph
            else "incomplete"
            if missing or unexpected or wrong_types
            else "assessed",
            "reason_code": "untyped_stored_bonds"
            if untyped
            else "ambiguous_template_connectivity"
            if ambiguous_graph
            else None,
            "expected_bonded_atom_pairs": _pairs(expected_pairs),
            "missing_bonded_atom_pairs": _pairs(missing),
            "blocked_by_missing_atom_name_pairs": [
                list(pair)
                for pair in sorted(expected_names)
                if not set(pair) <= name_to_index.keys()
            ],
            "unexpected_bond_indices": np.asarray(unexpected, dtype=np.int64),
            "untyped_bond_indices": np.asarray(untyped, dtype=np.int64),
            "conflict_bond_type_indices": np.asarray(wrong_types, dtype=np.int64),
        }
    )
    if template["orders"] is not None:
        reverse = {index: name for name, index in name_to_index.items()}
        missing_orders, conflicts = [], []
        for index, pair in covalent:
            name_pair = tuple(sorted(reverse[a] for a in pair))
            reference = template["orders"].get(name_pair)
            if reference is None:
                continue
            value = orders.get(index)
            if value is None:
                missing_orders.append(index)
            elif value != reference:
                conflicts.append(index)
        empty["bond_order"] = {
            "status": "conflict"
            if conflicts
            else "partial"
            if missing_orders
            else "assessed",
            "reason_code": None,
            "missing_bond_indices": np.asarray(missing_orders, dtype=np.int64),
            "conflict_bond_indices": np.asarray(conflicts, dtype=np.int64),
        }
    return empty


def assess(
    molecular_system, selection, structure_indices, chemical_state, syntax, caller
):
    from molsysmt.basic import get_form, select
    from molsysmt.element.group.amino_acid.get_expected_heavy_atoms import _is_hydrogen

    domains = _domains(molecular_system, caller)
    topology = domains[1]
    if topology is None:
        raise NotWithThisFormError(
            caller=caller,
            form=get_form(molecular_system),
            requested_attribute="group_index",
        )
    n_groups = topology.n_groups
    membership = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    if np.any(membership < 0) or np.any(membership >= n_groups):
        raise StructuralInconsistencyError(
            reason="Residue coverage requires valid atom-to-group membership.",
            caller=caller,
        )
    if selection is None or is_all(selection):
        groups = np.arange(n_groups, dtype=np.int64)
    elif isinstance(selection, str):
        selected = select(
            molecular_system,
            element="atom",
            selection=selection,
            structure_indices=structure_indices,
            chemical_state=chemical_state,
            syntax=syntax,
        )
        groups = np.unique(membership[selected]).astype(np.int64)
    else:
        values = np.asarray(selection)
        if (
            values.ndim != 1
            or (values.size and values.dtype.kind not in "iu")
            or np.any(values < 0)
            or np.any(values >= n_groups)
        ):
            raise ArgumentError("selection", value=selection, caller=caller)
        groups = np.unique(values).astype(np.int64)
    selected_atoms = np.flatnonzero(np.isin(membership, groups)).astype(np.int64)
    readiness = audit_fields(
        molecular_system,
        selected_atoms,
        structure_indices,
        chemical_state,
        syntax,
        caller,
        domains=domains,
    )
    atom_types = dict(
        zip(
            readiness["fields"]["atom_type"]["indices"],
            readiness["fields"]["atom_type"]["values"],
        )
    )
    bond_fields = tuple(
        dict(
            zip(
                readiness["fields"][field]["indices"],
                readiness["fields"][field]["values"],
            )
        )
        for field in ("bond_type", "bond_order")
    )
    rows_by_group = defaultdict(list)
    for index in selected_atoms:
        rows_by_group[int(membership[index])].append(int(index))
    internal, boundary = defaultdict(list), defaultdict(list)
    for index, pair in zip(readiness["bond_indices"], readiness["bonded_atom_pairs"]):
        if np.any(pair < 0) or np.any(pair >= len(membership)):
            continue
        first, second = (int(membership[atom]) for atom in pair)
        if first == second:
            internal[first].append((int(index), tuple(sorted(pair.tolist()))))
        else:
            boundary[first].append(int(index))
            boundary[second].append(int(index))
    cache, entries = {}, []
    invalid_bonds = set(readiness["connectivity"]["invalid_bond_indices"])
    for group_index in groups:
        index = int(group_index)
        atoms = np.asarray(rows_by_group[index], dtype=np.int64)
        names = topology.atoms["atom_name"].iloc[atoms].tolist()
        group_name = topology.groups.at[index, "group_name"]
        group_name = None if pd.isna(group_name) else str(group_name)
        hydrogen_mask = [
            atom_types.get(a) == "H"
            or (atom_types.get(a) is None and isinstance(n, str) and _is_hydrogen(n))
            for a, n in zip(atoms, names)
        ]
        heavy_names = {
            n for n, h in zip(names, hydrogen_mask) if not h and isinstance(n, str)
        }
        template = _template(group_name, heavy_names, cache)
        entry = {
            "group_index": index,
            "group_id": None
            if pd.isna(topology.groups.at[index, "group_id"])
            else str(topology.groups.at[index, "group_id"]),
            "group_name": group_name,
            "atom_indices": atoms,
            "status": "unassessed",
            "reason_codes": [],
            "template": None,
            "heavy_atoms": {
                "status": "unassessed",
                "missing_atom_names": None,
                "unexpected_atom_names": None,
            },
            "hydrogens": {
                "status": "unassessed",
                "reason_code": "no_exact_residue_template",
                "observed_atom_indices": atoms[np.asarray(hydrogen_mask, dtype=bool)],
                "candidates": [],
            },
            "connectivity": {
                "status": "unassessed",
                "reason_code": "no_exact_residue_template",
            },
            "protonation": {
                "status": "unassessed",
                "reason_code": "no_environmental_protonation_assessment",
            },
            "boundary_bond_indices": np.asarray(
                sorted(boundary[index]), dtype=np.int64
            ),
        }
        if template is None:
            entry["reason_codes"] = ["no_exact_residue_template"]
            entries.append(entry)
            continue
        entry["template"] = template["identity"]
        counts = pd.Series(names, dtype=object).value_counts()
        duplicate_names = sorted(str(n) for n in counts.index[counts > 1])
        missing_names = sorted(template["expected"] - heavy_names)
        unexpected_names = sorted(heavy_names - template["expected"])
        element_conflicts, element_unknown = [], []
        for atom, name in zip(atoms, names):
            reference = template["elements"].get(name)
            actual = atom_types.get(atom)
            if reference is None or actual is None:
                element_unknown.append(int(atom))
            elif actual != reference:
                element_conflicts.append(int(atom))
        names_valid = all(isinstance(n, str) and n for n in names)
        mapping_valid = names_valid and not duplicate_names
        entry["heavy_atoms"] = {
            "status": "unassessed"
            if not mapping_valid
            else "incomplete"
            if missing_names or unexpected_names
            else "assessed",
            "expected_atom_names": sorted(template["expected"]),
            "missing_atom_names": missing_names,
            "unexpected_atom_names": unexpected_names,
            "duplicate_atom_names": duplicate_names,
            "element_conflict_atom_indices": np.asarray(
                element_conflicts, dtype=np.int64
            ),
            "element_unassessed_atom_indices": np.asarray(
                element_unknown, dtype=np.int64
            ),
        }
        h_indices = atoms[np.asarray(hydrogen_mask, dtype=bool)]
        entry["hydrogens"] = _hydrogens(
            template,
            {n for n, h in zip(names, hydrogen_mask) if h},
            h_indices,
            mapping_valid
            and not missing_names
            and not unexpected_names
            and not element_conflicts,
        )
        name_to_index = dict(zip(names, atoms)) if mapping_valid else {}
        entry["connectivity"] = _connectivity(
            template,
            name_to_index,
            mapping_valid,
            internal[index],
            readiness,
            h_indices,
            bond_fields,
        )
        for condition, code in [
            (not mapping_valid, "ambiguous_atom_names"),
            (bool(missing_names), "missing_heavy_atoms"),
            (bool(unexpected_names), "unexpected_heavy_atoms"),
            (bool(element_conflicts), "element_conflict"),
            (
                entry["hydrogens"]["status"] == "incomplete",
                "incomplete_hydrogen_inventory",
            ),
            (
                readiness["chemical_state_status"] != "resolved",
                "chemical_state_" + readiness["chemical_state_status"],
            ),
            (
                any(i in invalid_bonds for i, _ in internal[index]),
                "invalid_stored_bonds",
            ),
            (
                entry["connectivity"]["status"] == "incomplete",
                "incomplete_stored_connectivity",
            ),
            (
                len(
                    entry["connectivity"]
                    .get("bond_order", {})
                    .get("conflict_bond_indices", [])
                )
                > 0,
                "bond_order_conflict",
            ),
        ]:
            if condition:
                entry["reason_codes"].append(code)
        entry["status"] = (
            "unassessed"
            if not mapping_valid or readiness["chemical_state_status"] != "resolved"
            else "incomplete"
            if entry["reason_codes"]
            else "assessed"
        )
        entries.append(entry)
    return {
        "schema": "molsysmt.residue_chemical_coverage@1",
        "method": "exact_residue_template_comparison",
        "rule_version": 1,
        "group_indices": groups,
        "groups": entries,
        "chemical_readiness": readiness,
        "summary": {
            status: sum(e["status"] == status for e in entries)
            for status in ("assessed", "incomplete", "unassessed")
        },
        "unassessed_checks": [
            "environmental_protonation",
            "terminal_context",
            "inter_group_chemistry",
            "valence",
            "aromaticity_perception",
            "repair_placement",
            "force_field_coverage",
            "docking_readiness",
        ],
        "software": readiness["software"].copy(),
    }
