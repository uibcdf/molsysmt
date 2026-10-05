"""Comparing observed H parents with exact heavy-compatible group variants."""

from collections import defaultdict

import numpy as np


def prepare_context(readiness, atom_names):
    """Index already-audited fields and incident edges once for the report."""
    fields = {name: field["values"] for name, field in readiness["fields"].items()}
    incident = defaultdict(list)
    for index, pair in zip(readiness["bond_indices"], readiness["bonded_atom_pairs"]):
        for atom in set(pair):
            incident[int(atom)].append((int(index), tuple(sorted(pair.tolist()))))
    return {
        "fields": fields,
        "atom_rows": {
            int(atom): row for row, atom in enumerate(readiness["atom_indices"])
        },
        "bond_rows": {
            int(bond): row for row, bond in enumerate(readiness["bond_indices"])
        },
        "atom_names": atom_names,
        "incident": incident,
        "invalid_bonds": set(readiness["connectivity"]["invalid_bond_indices"]),
        "templates": {},
        "parents": {},
    }


def _value(context, field, index, *, bond=False):
    """Read an audited field without making a separate dictionary per field."""
    row = context["bond_rows" if bond else "atom_rows"].get(index)
    return None if row is None else context["fields"][field][row]


def candidates(group, selected, group_reasons, context):
    """Return typed per-H parent evidence, leaving global chemistry unassessed."""
    from molsysmt._private.residue_chemical_coverage import _template

    atoms = group["hydrogens"]["observed_atom_indices"].copy()
    names = context["atom_names"]
    mapping = {names[atom]: int(atom) for atom in group["atom_indices"]}
    template = None
    if not group_reasons:
        template = _template(
            group["group_name"],
            set(group["heavy_atoms"]["expected_atom_names"]),
            context["templates"],
        )
    parents = np.full(len(atoms), -1, dtype=np.int64)
    eligible = np.zeros(len(atoms), dtype=bool)
    selected_mask = np.zeros(len(atoms), dtype=bool)
    offsets, variants, issues, pairs = [0], [], [], []
    joint = []
    if template is not None and not template["modified"]:
        observed = {names[atom] for atom in atoms}
        joint = [
            index
            for index, variant in template["candidates"]
            if observed <= set(variant["atoms"])
        ]
    for row, atom in enumerate(atoms):
        atom = int(atom)
        name = names[atom]
        reasons = list(group_reasons)
        reference_parents, matching = [], []
        if not reasons:
            if _value(context, "atom_type", atom) != "H":
                reasons.append("hydrogen_element_unassessed")
            if template["modified"]:
                reasons.append("heavy_only_template")
            else:
                key = (group["group_name"], tuple(sorted(template["expected"])), name)
                if key not in context["parents"]:
                    matches = [
                        (index, variant)
                        for index, variant in template["candidates"]
                        if name in variant["atoms"]
                    ]
                    parent_sets = [
                        {
                            b if a == name else a
                            for a, b in variant["bonds"]
                            if a == name or b == name
                        }
                        for _, variant in matches
                    ]
                    all_parents = (
                        sorted(set().union(*parent_sets)) if parent_sets else []
                    )
                    consensus = (
                        bool(parent_sets)
                        and all(len(value) == 1 for value in parent_sets)
                        and len(all_parents) == 1
                    )
                    context["parents"][key] = (
                        [index for index, _ in matches],
                        all_parents,
                        consensus,
                    )
                matching, reference_parents, consensus = context["parents"][key]
                if not matching:
                    reasons.append("unrecognized_hydrogen_name")
                elif template["elements"].get(name) != "H":
                    reasons.append("hydrogen_reference_element_conflict")
                elif not consensus:
                    reasons.append("ambiguous_hydrogen_parent")
                else:
                    parent_name = reference_parents[0]
                    parent = mapping.get(parent_name)
                    reference_element = template["elements"].get(parent_name)
                    if reference_element in (None, "H"):
                        reasons.append("unsupported_hydrogen_parent_element")
                    elif parent is None:
                        reasons.append("missing_hydrogen_parent")
                    elif _value(context, "atom_type", parent) != reference_element:
                        reasons.append("hydrogen_parent_element_conflict")
                    else:
                        parents[row] = parent
        variants.extend(matching)
        offsets.append(len(variants))
        for field in (
            "formal_charge",
            "n_unpaired_electrons",
            "n_implicit_hydrogens",
            "n_explicit_hydrogens",
        ):
            value = _value(context, field, atom)
            if value is not None and value != 0:
                reasons.append("nonstandard_stored_hydrogen_assignment")
        aromatic = _value(context, "atom_is_aromatic", atom)
        if aromatic is not None and bool(aromatic):
            reasons.append("nonstandard_stored_hydrogen_assignment")
        if parents[row] >= 0:
            pair = tuple(sorted((atom, int(parents[row]))))
            selected_mask[row] = set(pair) <= selected
            for bond, observed_pair in context["incident"].get(atom, []):
                if bond in context["invalid_bonds"]:
                    reasons.append("invalid_stored_hydrogen_bond")
                elif observed_pair != pair:
                    reasons.append("conflicting_stored_hydrogen_partner")
                else:
                    if _value(context, "bond_type", bond, bond=True) not in (
                        None,
                        "covalent",
                    ):
                        reasons.append("conflicting_stored_hydrogen_bond_type")
                    aromatic = _value(context, "bond_is_aromatic", bond, bond=True)
                    if _value(context, "bond_order", bond, bond=True) not in (
                        None,
                        1,
                    ) or (aromatic is not None and bool(aromatic)):
                        reasons.append("conflicting_stored_hydrogen_bond_order")
            if not reasons:
                eligible[row] = True
                if selected_mask[row]:
                    pairs.append(pair)
        if reasons:
            issues.append(
                {
                    "atom_index": atom,
                    "atom_name": name,
                    "reference_parent_names": list(reference_parents),
                    "reason_codes": list(dict.fromkeys(reasons)),
                }
            )
    return {
        "atom_indices": atoms,
        "parent_atom_indices": parents,
        "eligible_mask": eligible,
        "selected_mask": selected_mask,
        "variant_offsets": np.asarray(offsets, dtype=np.int64),
        "variant_indices": np.asarray(variants, dtype=np.int64),
        "joint_variant_indices": np.asarray(joint, dtype=np.int64),
        "inventory_status": "unassessed"
        if group_reasons
        or (template is not None and template["modified"])
        or (len(atoms) and not joint)
        else "compatible_subset",
        "issues": issues,
    }, pairs
