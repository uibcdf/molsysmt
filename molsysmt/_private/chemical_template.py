"""Checking explicit template correspondence before a bounded chemical transaction."""

from copy import deepcopy

import numpy as np
import pandas as pd

from molsysmt._private.chemical_readiness import _domains, _state
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

_ATOM_FIELDS = (
    "formal_charge",
    "is_aromatic",
    "n_unpaired_electrons",
    "n_implicit_hydrogens",
    "n_explicit_hydrogens",
    "allows_implicit_hydrogens",
    "stereochemistry",
)
_BOND_FIELDS = (
    "bond_type",
    "bond_order",
    "fractional_bond_order",
    "is_aromatic",
    "is_conjugated",
    "stereochemistry",
    "stereo_atom1_index",
    "stereo_atom2_index",
    "joins_components",
)


def _value(table, field, index):
    if table is None or field not in table:
        return None
    value = table.at[index, field]
    if pd.isna(value) or (
        isinstance(value, str)
        and value in {"unknown", "unspecified", "nan", "None", "<NA>", ""}
    ):
        return None
    return value.item() if isinstance(value, np.generic) else value


def _context(system, state_selection, argument, caller):
    if state_selection == "structure":
        raise ArgumentError(
            argument,
            value=state_selection,
            caller=caller,
            message="Template operations require a state index or resolved reference, independent of coordinate frames.",
        )
    domains = _domains(system, caller)
    source, topology, states, n_atoms, links = domains
    state, index, status = _state(source, states, state_selection, None, links, caller)
    return dict(
        source=source,
        topology=topology,
        states=states,
        state=state,
        n_atoms=int(n_atoms),
        chemical_state_index=index,
        chemical_state_status=status,
    )


def _issue(report, status, reason, *, side=None, field=None, index=None):
    report["issues"].append(
        dict(
            status=status,
            reason_code=reason,
            side=side,
            field=field,
            index=None if index is None else int(index),
            diagnostic_code="MSM-ERR-STRUCT-003",
        )
    )


def _edges(context, report, side, *, allow_fragments=False):
    from molsysmt._private.rust_backend import (
        get_component_index_from_bonded_atom_pairs,
    )

    state, n_atoms = context["state"], context["n_atoms"]
    if state is None:
        return None
    table, edges = state.bonds, {}
    for index in table.index:
        a, b = _value(table, "atom1_index", index), _value(table, "atom2_index", index)
        if (
            a is None
            or b is None
            or not isinstance(a, int)
            or isinstance(a, bool)
            or not isinstance(b, int)
            or isinstance(b, bool)
            or not 0 <= a < n_atoms
            or not 0 <= b < n_atoms
            or a == b
            or tuple(sorted((a, b))) in edges
        ):
            _issue(
                report,
                "conflict",
                "invalid_stored_relationship",
                side=side,
                index=index,
            )
            return None
        edges[tuple(sorted((a, b)))] = int(index)
        kind = _value(table, "bond_type", index)
        if kind not in {None, "covalent"}:
            _issue(
                report,
                "unassessed",
                "noncovalent_relationship_outside_scope",
                side=side,
                index=index,
            )
        if _value(table, "joins_components", index) is False:
            _issue(
                report,
                "unassessed",
                "cut_component_relationship",
                side=side,
                index=index,
            )
    pairs = np.asarray(list(edges), dtype=np.int64).reshape(-1, 2)
    for index in table.index:
        label = _value(table, "stereochemistry", index)
        refs = [
            _value(table, field, index)
            for field in ("stereo_atom1_index", "stereo_atom2_index")
        ]
        ends = [_value(table, field, index) for field in ("atom1_index", "atom2_index")]
        if label not in {None, "E", "Z", "cis", "trans"}:
            _issue(
                report,
                "unassessed",
                "unsupported_bond_stereochemistry",
                side=side,
                index=index,
            )
        if label is not None or any(ref is not None for ref in refs):
            if (
                any(
                    not isinstance(ref, int)
                    or isinstance(ref, bool)
                    or not 0 <= ref < n_atoms
                    for ref in refs
                )
                or refs[0] == refs[1]
                or any(ref in ends for ref in refs)
                or any(
                    tuple(sorted((ref, end))) not in edges
                    for ref, end in zip(refs, ends)
                )
            ):
                _issue(
                    report,
                    "conflict",
                    "invalid_stereo_reference_atoms",
                    side=side,
                    index=index,
                )
    components = get_component_index_from_bonded_atom_pairs(pairs, np.int64(n_atoms))
    if not n_atoms or (not allow_fragments and len(np.unique(components)) != 1):
        _issue(report, "unassessed", "isolated_connected_component_required", side=side)
    context["edges"] = edges
    return edges


def _compare(
    report, source_table, template_value, side_field, index, axis, *, aromatic=False
):
    actual = _value(source_table, side_field, index)
    if template_value is None:
        if actual is not None:
            _issue(
                report,
                "unassessed",
                "aromatic_representation_requires_normalization"
                if aromatic
                else "template_field_not_declared",
                side="template",
                field=side_field,
                index=index,
            )
        return
    record = dict(axis=axis, field=side_field, index=int(index), value=template_value)
    if actual is None:
        record["origin"] = "declared_template"
        report["assigned_fields"].append(record)
    elif actual == template_value:
        record["origin"] = "preserved_source"
        report["preserved_fields"].append(record)
    else:
        status = (
            "unassessed"
            if aromatic or side_field.startswith("stereo_atom")
            else "conflict"
        )
        reason = (
            "aromatic_representation_requires_normalization"
            if aromatic
            else "stereo_reference_requires_normalization"
            if side_field.startswith("stereo_atom")
            else "explicit_assignment_conflict"
        )
        _issue(report, status, reason, side="source", field=side_field, index=index)


def evaluate(
    molecular_system,
    template,
    atom_correspondence,
    template_provenance,
    chemical_state,
    template_chemical_state,
    caller,
    connectivity_policy="require_same_graph",
):
    """Return a detached preflight plus private contexts; mutate neither input."""
    from molsysmt import __version__
    from molsysmt.basic import get_form
    from molsysmt.element.atom import is_atom_type

    # The public boundary validates arguments; private work owns detached copies.
    mapping = np.asarray(atom_correspondence).copy()
    provenance = deepcopy(template_provenance)
    source = _context(molecular_system, chemical_state, "chemical_state", caller)
    reference = _context(
        template, template_chemical_state, "template_chemical_state", caller
    )
    ns, nt = source["n_atoms"], reference["n_atoms"]
    if (
        ns != nt
        or len(mapping) != ns
        or set(mapping[:, 0]) != set(range(nt))
        or set(mapping[:, 1]) != set(range(ns))
    ):
        raise ArgumentError(
            "atom_correspondence",
            value=atom_correspondence,
            caller=caller,
            message="The map must cover every source and template atom exactly once, including explicit hydrogens.",
        )
    mapping = mapping.astype(np.int64)
    atom_map = dict(mapping.tolist())
    report = dict(
        schema="molsysmt.chemical_template@1",
        status="unassessed",
        method=(
            "explicit_template_graph_completion"
            if connectivity_policy == "complete_from_template"
            else "explicit_template_correspondence"
        ),
        rule_version=2 if connectivity_policy == "complete_from_template" else 1,
        source=dict(
            forms=get_form(molecular_system),
            n_atoms=ns,
            chemical_state_index=source["chemical_state_index"],
            chemical_state_status=source["chemical_state_status"],
        ),
        template=dict(
            forms=get_form(template),
            n_atoms=nt,
            chemical_state_index=reference["chemical_state_index"],
            chemical_state_status=reference["chemical_state_status"],
        ),
        atom_correspondence=mapping.copy(),
        template_provenance=provenance,
        connectivity_policy=connectivity_policy,
        added_bonds=[],
        assigned_fields=[],
        preserved_fields=[],
        issues=[],
        coverage=dict(
            atom_map="exhaustive_bijection",
            graph="unassessed",
            hydrogen_policy=provenance["hydrogen_policy"],
            explicit_hydrogen_atom_indices=np.empty(0, dtype=np.int64),
            completeness_justification=None,
        ),
        unassessed_checks=[
            "template_authenticity",
            "valence",
            "environmental_protonation",
            "stereogenicity",
            "conformer_quality",
            "force_field_coverage",
            "docking_readiness",
        ],
        software={"molsysmt": __version__},
        units={"formal_charge": "elementary_charge"},
    )
    for side, context in (("source", source), ("template", reference)):
        if context["topology"] is None:
            _issue(report, "unassessed", "stable_element_inventory_required", side=side)
        if context["state"] is None:
            _issue(
                report,
                "unassessed",
                "chemical_state_" + context["chemical_state_status"],
                side=side,
            )
    if report["issues"]:
        return report, source, reference
    source_atoms, template_atoms = source["topology"].atoms, reference["topology"].atoms
    state, ref_state = source["state"], reference["state"]
    hydrogen_indices = []
    for ti, si in mapping:
        actual, expected = (
            _value(source_atoms, "atom_type", si),
            _value(template_atoms, "atom_type", ti),
        )
        if (
            actual is None
            or expected is None
            or not is_atom_type(actual)
            or not is_atom_type(expected)
        ):
            _issue(
                report,
                "unassessed",
                "supported_elements_required",
                field="atom_type",
                index=si,
            )
        elif actual != expected:
            _issue(
                report,
                "conflict",
                "element_correspondence_conflict",
                field="atom_type",
                index=si,
            )
        if actual == "H":
            hydrogen_indices.append(int(si))
        a, b = (
            _value(source_atoms, "isotope", si),
            _value(template_atoms, "isotope", ti),
        )
        if a != b:
            _issue(
                report,
                "unassessed" if a is None or b is None else "conflict",
                "isotope_correspondence_unresolved",
                field="isotope",
                index=si,
            )
        for field in _ATOM_FIELDS:
            value = _value(ref_state.atom_attributes, field, ti)
            if value is None and field != "stereochemistry":
                _issue(
                    report,
                    "unassessed",
                    "template_field_not_declared",
                    side="template",
                    field=field,
                    index=ti,
                )
            if (
                provenance["hydrogen_policy"] == "explicit_atoms"
                and field in {"n_implicit_hydrogens", "n_explicit_hydrogens"}
                and value not in {None, 0}
            ):
                _issue(
                    report,
                    "conflict",
                    "explicit_atom_hydrogen_policy_conflict",
                    side="template",
                    field=field,
                    index=ti,
                )
            _compare(
                report,
                state.atom_attributes,
                value,
                field,
                si,
                "atom",
                aromatic=field == "is_aromatic",
            )
    report["coverage"]["explicit_hydrogen_atom_indices"] = np.asarray(
        sorted(hydrogen_indices), dtype=np.int64
    )
    source_edges, template_edges = (
        _edges(
            source,
            report,
            "source",
            allow_fragments=connectivity_policy == "complete_from_template",
        ),
        _edges(reference, report, "template"),
    )
    if ref_state.connectivity_completeness != "complete":
        _issue(
            report, "unassessed", "template_connectivity_not_complete", side="template"
        )
    if source_edges is not None and template_edges is not None:
        mapped_edges = {
            tuple(sorted((atom_map[a], atom_map[b]))): (a, b, index)
            for (a, b), index in template_edges.items()
        }
        missing = set(mapped_edges) - set(source_edges)
        unexpected = set(source_edges) - set(mapped_edges)
        can_complete = (
            connectivity_policy == "complete_from_template"
            and state.connectivity_completeness != "complete"
            and not unexpected
        )
        if unexpected or (missing and not can_complete):
            _issue(
                report,
                "conflict",
                "stored_graph_requires_reconciliation",
                side="source",
            )
            report["coverage"]["missing_source_atom_pairs"] = np.asarray(
                sorted(set(mapped_edges) - set(source_edges)), dtype=np.int64
            ).reshape(-1, 2)
            report["coverage"]["unexpected_source_atom_pairs"] = np.asarray(
                sorted(set(source_edges) - set(mapped_edges)), dtype=np.int64
            ).reshape(-1, 2)
        else:
            report["coverage"]["graph"] = (
                "completion_from_declared_template"
                if missing
                else "same_stored_relationships"
            )
            report["coverage"]["completeness_justification"] = (
                "exhaustive_mapping_to_declared_complete_template"
            )
        for pair in sorted(set(mapped_edges)):
            _, _, ti = mapped_edges[pair]
            si = source_edges.get(pair)
            ta = _value(ref_state.bonds, "is_aromatic", ti)
            sa = None if si is None else _value(state.bonds, "is_aromatic", si)
            aromatic_difference = ta is True or sa is True
            kind = _value(ref_state.bonds, "bond_type", ti)
            order = _value(ref_state.bonds, "bond_order", ti)
            fraction = _value(ref_state.bonds, "fractional_bond_order", ti)
            if (
                kind != "covalent"
                or ta is None
                or (ta is not True and order not in {1, 2, 3})
                or (ta is True and order not in {None, 1, 2, 3})
            ):
                _issue(
                    report,
                    "unassessed",
                    "supported_template_bond_chemistry_required",
                    side="template",
                    index=ti,
                )
            if fraction is not None and (ta is not True or fraction != 1.5):
                _issue(
                    report,
                    "unassessed",
                    "unsupported_fractional_order",
                    side="template",
                    index=ti,
                )
            added = dict(
                template_bond_index=ti,
                atom1_index=int(pair[0]),
                atom2_index=int(pair[1]),
                evidence="user_defined",
            )
            for field in _BOND_FIELDS:
                value = _value(ref_state.bonds, field, ti)
                if field in {"stereo_atom1_index", "stereo_atom2_index"}:
                    source_first = (
                        pair[0]
                        if si is None
                        else _value(state.bonds, "atom1_index", si)
                    )
                    template_first = atom_map[
                        _value(ref_state.bonds, "atom1_index", ti)
                    ]
                    column = (
                        field
                        if source_first == template_first
                        else (
                            "stereo_atom2_index"
                            if field == "stereo_atom1_index"
                            else "stereo_atom1_index"
                        )
                    )
                    value = _value(ref_state.bonds, column, ti)
                    value = None if value is None else atom_map.get(value)
                if si is None:
                    if value is not None:
                        added[field] = value
                    continue
                _compare(
                    report,
                    state.bonds,
                    value,
                    field,
                    si,
                    "bond",
                    aromatic=aromatic_difference
                    and field in {"bond_order", "fractional_bond_order", "is_aromatic"},
                )
            if si is None and can_complete:
                report["added_bonds"].append(added)
    report["status"] = (
        "conflict"
        if any(i["status"] == "conflict" for i in report["issues"])
        else "unassessed"
        if report["issues"]
        else "compatible"
    )
    return report, source, reference


def apply(molecular_system, report, source, caller):
    """Copy the source and fill only the assessed missing chemical assignments."""
    from molsysmt.basic import convert
    from molsysmt.native import MolSys, Topology

    if report["status"] != "compatible":
        first = report["issues"][0]
        error = StructuralInconsistencyError(
            reason=f"Chemical template is {report['status']}: {first['reason_code']} "
            f"({first['side']}, {first['field']}, index {first['index']}). Inspect error.report.",
            caller=caller,
        )
        error.report = deepcopy(report)
        raise error
    if isinstance(molecular_system, MolSys):
        result = molecular_system.copy()
    elif isinstance(molecular_system, Topology):
        topology = molecular_system.copy()
        result = MolSys._from_partial_domains(
            topology=topology, chemical_states=topology._chemical_states_domain
        )
    else:
        result = convert(molecular_system, to_form="molsysmt.MolSys").copy()
    index = source["chemical_state_index"]
    states = result.chemical_states.copy()
    state = states._states[index]
    for record in report["assigned_fields"]:
        table = state.atom_attributes if record["axis"] == "atom" else state.bonds
        if record["field"] not in table:
            table[record["field"]] = pd.NA
        table.at[record["index"], record["field"]] = record["value"]
    state._normalize_atom_attribute_columns()
    added_bonds = report["added_bonds"]
    original_count = len(state.bonds)
    if added_bonds:
        original_pairs = state.bonds[["atom1_index", "atom2_index"]].to_numpy(
            dtype=np.int64
        )
        added_table = pd.DataFrame(
            [
                {k: v for k, v in bond.items() if k != "template_bond_index"}
                for bond in added_bonds
            ]
        )
        state.bonds = Topology._concatenate_bond_tables(state.bonds, added_table)
    changed = (
        bool(report["assigned_fields"])
        or bool(added_bonds)
        or state.connectivity_completeness != "complete"
    )
    state.connectivity_completeness = "complete"
    invalidated = sorted(result.interactions) if changed else []
    if changed:
        result.chemical_states = states
    if added_bonds:
        with result.topology._using_chemical_state(index):
            result.topology.rebuild_components(
                redefine_types=False, redefine_names=False
            )
    applied = deepcopy(report)
    applied["status"] = "applied"
    applied["invalidated_analysis_names"] = invalidated
    if added_bonds:
        final_pairs = state.bonds[["atom1_index", "atom2_index"]].to_numpy(
            dtype=np.int64
        )
        final_index = {
            tuple(sorted(pair)): i for i, pair in enumerate(final_pairs.tolist())
        }
        applied["source_bond_correspondence"] = np.asarray(
            [
                (i, final_index[tuple(sorted(pair))])
                for i, pair in enumerate(original_pairs.tolist())
            ],
            dtype=np.int64,
        ).reshape(-1, 2)
        for bond in applied["added_bonds"]:
            bond["bond_index"] = final_index[(bond["atom1_index"], bond["atom2_index"])]
    else:
        indices = np.arange(original_count, dtype=np.int64)
        applied["source_bond_correspondence"] = np.column_stack((indices, indices))
    from molsysmt import _ackredit
    from molsysmt._private.scientific_citations import SOFTWARE

    items = [
        dict(
            id=f"software:{name}:{version}",
            type="software",
            **deepcopy(SOFTWARE[name]),
            version=version,
            roles=["executed_software"],
        )
        for name, version in applied["software"].items()
    ]
    applied["attribution"] = dict(
        schema="molsysmt.scientific_attribution@1", target=caller, items=items
    )
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller)
    return dict(molecular_system=result, report=applied)
