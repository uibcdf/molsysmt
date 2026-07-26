#!/usr/bin/env python
"""Auditing direct Tier 1 conversion fidelity coverage.

The direct conversion graph is discovered from adapter ``_convert_to`` maps.
The compact baseline records accepted non-exhaustive coverage debt; it is not a
claim that those routes are fully verified. New debt fails the audit.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = (
    REPOSITORY_ROOT
    / "devtools"
    / "data"
    / "tier1_conversion_fidelity_baseline.json"
)


def _direct_tier1_edges() -> tuple[list[str], list[dict[str, Any]]]:
    """Returning the direct Tier 1-to-Tier 1 conversion graph."""

    from molsysmt._private.form_tier import FORM_TIERS
    from molsysmt._private.conversion_report import (
        get_conversion_audit_scopes,
        is_conversion_audit_exhaustive,
    )
    from molsysmt.form import _dict_modules

    forms = sorted(name for name, tier in FORM_TIERS.items() if tier == 1)
    edges = []
    for source in forms:
        source_module = _dict_modules[source]
        for target, converter in sorted(source_module._convert_to.items()):
            if FORM_TIERS.get(target) != 1:
                continue
            if isinstance(converter, str):
                converter_reference = f"{source_module.__name__}.{converter}"
                converter_registration = "lazy"
            elif callable(converter):
                converter_reference = (
                    f"{converter.__module__}.{converter.__name__}"
                )
                converter_registration = "callable"
            else:
                converter_reference = repr(converter)
                converter_registration = "invalid"

            source_attributes = {
                name for name, available in source_module.attributes.items() if available
            }
            target_attributes = {
                name
                for name, available in _dict_modules[target].attributes.items()
                if available
            }
            capability_delta = sorted(source_attributes - target_attributes)
            audited_scopes = get_conversion_audit_scopes(source, target)
            is_exhaustive = is_conversion_audit_exhaustive(source, target)
            edges.append(
                {
                    "source": source,
                    "target": target,
                    "converter": converter_reference,
                    "converter_registration": converter_registration,
                    "coverage": (
                        "exhaustive_preflight"
                        if is_exhaustive
                        else "scoped_preflight"
                    ),
                    "audited_scopes": list(audited_scopes),
                    "is_exhaustive": is_exhaustive,
                    "possible_outcomes": (
                        ["exact", "rejected"]
                        if source == target
                        else ["equivalent", "lossy", "rejected"]
                    ),
                    "potentially_unrepresentable_attributes": capability_delta,
                }
            )
    return forms, edges


def _edge_pairs(edges: list[dict[str, Any]]) -> set[tuple[str, str]]:
    """Returning source-target pairs for non-exhaustive edges."""

    return {
        (edge["source"], edge["target"])
        for edge in edges
        if not edge["is_exhaustive"]
    }


def _encode_masks(
    forms: list[str], edges: set[tuple[str, str]]
) -> dict[str, str]:
    """Encoding an edge set as one target bit mask per source form."""

    target_indices = {name: index for index, name in enumerate(forms)}
    masks = {}
    for source in forms:
        mask = 0
        for edge_source, target in edges:
            if edge_source == source:
                mask |= 1 << target_indices[target]
        if mask:
            masks[source] = hex(mask)
    return masks


def _decode_masks(payload: dict[str, Any]) -> set[tuple[str, str]]:
    """Decoding compact source masks into direct edge pairs."""

    forms = payload["form_order"]
    output = set()
    for source, hexadecimal_mask in payload["accepted_non_exhaustive_masks"].items():
        mask = int(hexadecimal_mask, 16)
        output.update(
            (source, target)
            for index, target in enumerate(forms)
            if mask & (1 << index)
        )
    return output


def _baseline_payload(
    forms: list[str], edges: list[dict[str, Any]]
) -> dict[str, Any]:
    """Building the compact accepted-debt baseline payload."""

    return {
        "schema_version": 1,
        "description": (
            "Accepted direct Tier 1 conversion edges whose fidelity report is "
            "not exhaustive. Presence records debt, not verified fidelity."
        ),
        "form_order": forms,
        "accepted_non_exhaustive_masks": _encode_masks(
            forms, _edge_pairs(edges)
        ),
    }


def build_audit() -> dict[str, Any]:
    """Building the generated fidelity matrix and baseline comparison."""

    forms, edges = _direct_tier1_edges()
    current_debt = _edge_pairs(edges)
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    accepted_debt = _decode_masks(baseline)
    new_debt = sorted(current_debt - accepted_debt)
    resolved_debt = sorted(accepted_debt - current_debt)
    invalid_edges = [
        (edge["source"], edge["target"])
        for edge in edges
        if edge["converter_registration"] == "invalid"
    ]
    self_edge_sources = {
        edge["source"] for edge in edges if edge["source"] == edge["target"]
    }
    missing_self_edges = sorted(set(forms) - self_edge_sources)

    return {
        "schema_version": 1,
        "scope": "direct Tier 1-to-Tier 1 registered conversions",
        "summary": {
            "tier1_forms": len(forms),
            "direct_edges": len(edges),
            "exhaustive_preflight_edges": len(edges) - len(current_debt),
            "non_exhaustive_preflight_edges": len(current_debt),
            "forms_with_identity_edges": len(self_edge_sources),
            "new_non_exhaustive_debt": len(new_debt),
            "resolved_non_exhaustive_debt": len(resolved_debt),
        },
        "violations": {
            "invalid_converter_registrations": invalid_edges,
            "new_non_exhaustive_edges": new_debt,
        },
        "observations": {
            "forms_without_identity_edges": missing_self_edges,
        },
        "resolved_non_exhaustive_edges": resolved_debt,
        "edges": edges,
    }


def _print_human_report(report: dict[str, Any]) -> None:
    """Printing a compact human-readable audit report."""

    summary = report["summary"]
    print("Tier 1 conversion fidelity audit")
    print(f"Tier 1 forms: {summary['tier1_forms']}")
    print(f"Direct Tier 1 edges: {summary['direct_edges']}")
    print(
        "Exhaustive preflight coverage: "
        f"{summary['exhaustive_preflight_edges']}"
    )
    print(
        "Accepted non-exhaustive preflight debt: "
        f"{summary['non_exhaustive_preflight_edges']}"
    )
    print(
        "Forms with registered identity edges: "
        f"{summary['forms_with_identity_edges']}"
    )
    print(f"New non-exhaustive debt: {summary['new_non_exhaustive_debt']}")
    print(
        "Resolved non-exhaustive debt: "
        f"{summary['resolved_non_exhaustive_debt']}"
    )
    violations = report["violations"]
    for name, entries in violations.items():
        if entries:
            print(f"{name}: {entries}")
    for name, entries in report["observations"].items():
        if entries:
            print(f"{name}: {entries}")


def main() -> int:
    """Running the command-line audit."""

    parser = argparse.ArgumentParser(
        description="Audit direct Tier 1 conversion fidelity coverage."
    )
    parser.add_argument(
        "--json", action="store_true", help="Print the generated full matrix as JSON."
    )
    parser.add_argument(
        "--print-baseline",
        action="store_true",
        help="Print a compact baseline for the current registered graph.",
    )
    arguments = parser.parse_args()

    forms, edges = _direct_tier1_edges()
    if arguments.print_baseline:
        print(json.dumps(_baseline_payload(forms, edges), indent=2, sort_keys=True))
        return 0

    report = build_audit()
    if arguments.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        _print_human_report(report)

    return int(any(report["violations"].values()))


if __name__ == "__main__":
    raise SystemExit(main())
