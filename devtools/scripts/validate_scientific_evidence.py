#!/usr/bin/env python
"""Validating scientific evidence separately from public API stability."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_ROOT = REPO_ROOT / "tests/scientific_truth/evidence"
REGISTRY_PATH = EVIDENCE_ROOT / "registry.json"
TOLERANCES_PATH = EVIDENCE_ROOT / "tolerances.json"
CAPABILITIES_DIR = EVIDENCE_ROOT / "capabilities"
API_REGISTRY_PATH = REPO_ROOT / "devtools/data/public_api_stability.json"
GENERATED_DOC_PATH = REPO_ROOT / "devguide/scientific_evidence_matrix.md"
ALLOWED_STATUSES = {"validated", "partial", "gap"}
ALLOWED_EVIDENCE_CLASSES = {
    "analytic",
    "external",
    "metamorphic",
    "parity",
    "versioned-reference",
}
INDEPENDENT_EVIDENCE_CLASSES = {"analytic", "external", "versioned-reference"}


def _read_json(path: Path) -> dict:
    """Read one JSON object."""
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def read_evidence_registry(
    evidence_root: Path = EVIDENCE_ROOT,
) -> tuple[dict, list[str]]:
    """Assemble the domain-split evidence registry and report duplicate symbols."""
    registry = _read_json(evidence_root / "registry.json")
    registry["tolerances"] = _read_json(evidence_root / "tolerances.json")
    registry["capabilities"] = {}
    errors = []
    capability_files = sorted((evidence_root / "capabilities").glob("*.json"))
    if not capability_files:
        return registry, ["No capability registry files were discovered."]
    for path in capability_files:
        domain_capabilities = _read_json(path)
        if not isinstance(domain_capabilities, dict):
            errors.append(f"{path}: capability file must contain an object.")
            continue
        for name, entry in domain_capabilities.items():
            if name in registry["capabilities"]:
                errors.append(
                    f"Duplicate scientific capability across domain files: {name}"
                )
                continue
            if isinstance(entry, dict) and entry.get("domain") != path.stem:
                errors.append(
                    f"{name}: domain {entry.get('domain')!r} does not match file {path.stem!r}."
                )
            registry["capabilities"][name] = entry
    return registry, errors


def stable_scientific_api(api_registry: dict, scopes: list[str]) -> set[str]:
    """Return Stable API symbols that belong to governed scientific scopes."""
    return {
        name
        for name, entry in api_registry["symbols"].items()
        if name.rsplit(".", 1)[0] in scopes and entry["stability"] == "stable"
    }


def evidence_scopes(registry: dict, api_registry: dict) -> dict[str, set[str]]:
    """Keep mandatory Stable coverage separate from explicitly reviewed claims."""
    return {
        "Stable": stable_scientific_api(api_registry, registry["stable_api_scopes"]),
        "Claimed": set(registry.get("claimed_api_symbols", [])),
    }


def _call_name(node: ast.Call) -> str:
    """Return the final component of a called function name."""
    function = node.func
    if isinstance(function, ast.Name):
        return function.id
    if isinstance(function, ast.Attribute):
        return function.attr
    return ""


def _has_assertion_bearing_operation(function: ast.AST) -> bool:
    """Return whether a test contains an explicit outcome-bearing operation.

    This is a hygiene check against empty evidence nodes, not a claim that a
    syntactic assertion is a scientifically adequate oracle. Oracle adequacy is
    governed by the evidence metadata and review contract; actual outcomes are
    established separately by ``execute_scientific_evidence.py``.
    """
    for node in ast.walk(function):
        if isinstance(node, ast.Assert):
            return True
        if isinstance(node, ast.Call):
            name = _call_name(node)
            if name.startswith("assert_") or name in {"fail", "raises", "warns"}:
                return True
    return False


def _test_node_exists(repo_root: Path, node_id: str) -> tuple[bool, str | None]:
    """Return whether an assertion-bearing path::function pytest node exists."""
    if node_id.count("::") != 1:
        return False, "must use path.py::test_function syntax"
    relative_path, function_name = node_id.split("::")
    path = repo_root / relative_path
    if not path.is_file():
        return False, f"test file does not exist: {relative_path}"
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as error:
        return False, f"test file cannot be parsed: {error}"
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    function = functions.get(function_name)
    if function is None:
        return False, f"test function does not exist: {node_id}"
    if not _has_assertion_bearing_operation(function):
        return False, f"test function has no assertion-bearing operation: {node_id}"
    return True, None


def scientific_test_nodes(registry: dict) -> list[str]:
    """Return the sorted unique pytest nodes cited by the evidence registry."""
    return sorted(
        {
            item["test"]
            for entry in registry["capabilities"].values()
            for item in entry["scientific_evidence"]
        }
    )


def validate_registry(
    registry: dict,
    api_registry: dict,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Return all scientific evidence registry violations."""
    errors = []
    if registry.get("schema_version") != "molsysmt.scientific-evidence@1":
        errors.append("schema_version must be 'molsysmt.scientific-evidence@1'.")
    scopes = registry.get("stable_api_scopes")
    capabilities = registry.get("capabilities")
    tolerances = registry.get("tolerances")
    if (
        not isinstance(scopes, list)
        or not scopes
        or not all(isinstance(item, str) for item in scopes)
    ):
        return errors + ["stable_api_scopes must be a non-empty list of strings."]
    if not isinstance(capabilities, dict):
        return errors + ["capabilities must be an object keyed by public API symbol."]
    if not isinstance(tolerances, dict) or not tolerances:
        return errors + ["tolerances must be a non-empty object."]
    status_definitions = registry.get("status_definitions")
    if (
        not isinstance(status_definitions, dict)
        or set(status_definitions) != ALLOWED_STATUSES
    ):
        errors.append(
            "status_definitions must define exactly validated, partial, and gap."
        )
    elif not all(
        isinstance(description, str) and description.strip()
        for description in status_definitions.values()
    ):
        errors.append("Every status definition must be a non-empty string.")

    claimed = registry.get("claimed_api_symbols", [])
    if not isinstance(claimed, list) or not all(
        isinstance(name, str) for name in claimed
    ):
        return errors + ["claimed_api_symbols must be a list of public API symbols."]
    if len(claimed) != len(set(claimed)):
        errors.append("claimed_api_symbols must not contain duplicates.")
    for name in claimed:
        entry = api_registry["symbols"].get(name)
        if entry is None or entry.get("stability") not in {"stable", "experimental"}:
            errors.append(
                f"Claimed scientific API must be Stable or Experimental: {name}"
            )
    experimental_scopes = registry.get("experimental_api_scopes", [])
    if not isinstance(experimental_scopes, list) or not all(
        isinstance(scope, str) and scope for scope in experimental_scopes
    ):
        return errors + ["experimental_api_scopes must be a list of namespace strings."]

    stable = stable_scientific_api(api_registry, scopes)
    expected = stable | set(claimed)
    registered = set(capabilities)
    for name in sorted(expected - registered):
        errors.append(
            f"{'Stable' if name in stable else 'Claimed'} scientific API is missing evidence classification: {name}"
        )
    for name in sorted(registered - expected):
        errors.append(
            f"Evidence entry is outside Stable and Claimed scientific scopes: {name}"
        )

    for tolerance_name, tolerance in sorted(tolerances.items()):
        if not isinstance(tolerance, dict):
            errors.append(f"Tolerance {tolerance_name}: entry must be an object.")
            continue
        for field in ("atol", "rtol"):
            value = tolerance.get(field)
            if not isinstance(value, (int, float)) or value < 0:
                errors.append(
                    f"Tolerance {tolerance_name}: {field} must be non-negative."
                )
        for field in ("applies_to", "rationale"):
            if (
                not isinstance(tolerance.get(field), str)
                or not tolerance[field].strip()
            ):
                errors.append(f"Tolerance {tolerance_name}: {field} is required.")

    for name, entry in sorted(capabilities.items()):
        if not isinstance(entry, dict):
            errors.append(f"{name}: capability entry must be an object.")
            continue
        status = entry.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{name}: invalid status {status!r}.")
        for field in ("domain", "claim", "periodic_behavior", "contract_test_area"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{name}: {field} is required.")
        units = entry.get("units")
        if (
            not isinstance(units, list)
            or not units
            or not all(isinstance(unit, str) for unit in units)
        ):
            errors.append(f"{name}: units must be a non-empty list of strings.")
        contract_area = entry.get("contract_test_area")
        if isinstance(contract_area, str) and not (repo_root / contract_area).exists():
            errors.append(f"{name}: contract test area does not exist: {contract_area}")

        evidence = entry.get("scientific_evidence")
        if not isinstance(evidence, list):
            errors.append(f"{name}: scientific_evidence must be a list.")
            evidence = []
        independent = False
        for index, item in enumerate(evidence):
            prefix = f"{name}: evidence[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object.")
                continue
            evidence_class = item.get("class")
            if evidence_class not in ALLOWED_EVIDENCE_CLASSES:
                errors.append(f"{prefix} has invalid class {evidence_class!r}.")
            independent |= evidence_class in INDEPENDENT_EVIDENCE_CLASSES
            oracle = item.get("oracle")
            if not isinstance(oracle, str) or not oracle.strip():
                errors.append(f"{prefix} requires oracle provenance.")
            tolerance = item.get("tolerance")
            comparison = item.get("comparison", "tolerance")
            if comparison == "exact":
                if tolerance is not None:
                    errors.append(
                        f"{prefix} exact comparison cannot declare a tolerance."
                    )
            elif comparison == "tolerance":
                if tolerance not in tolerances:
                    errors.append(
                        f"{prefix} references unknown tolerance {tolerance!r}."
                    )
            else:
                errors.append(f"{prefix} has invalid comparison {comparison!r}.")
            test_node = item.get("test")
            if not isinstance(test_node, str):
                errors.append(f"{prefix} requires a pytest node id.")
            else:
                if not test_node.startswith("tests/scientific_truth/"):
                    errors.append(
                        f"{prefix} must reference the governed Scientific Truth suite."
                    )
                exists, reason = _test_node_exists(repo_root, test_node)
                if not exists:
                    errors.append(f"{prefix}: {reason}")

        gap = entry.get("gap")
        if status == "validated":
            if not independent:
                errors.append(
                    f"{name}: validated status requires independent evidence."
                )
            if gap is not None:
                errors.append(f"{name}: validated status requires gap=null.")
        elif status == "partial":
            if not evidence:
                errors.append(f"{name}: partial status requires some evidence.")
            if not isinstance(gap, str) or not gap.strip():
                errors.append(
                    f"{name}: partial status requires an explicit remaining gap."
                )
        elif status == "gap":
            if evidence:
                errors.append(
                    f"{name}: gap status cannot register scientific evidence."
                )
            if not isinstance(gap, str) or not gap.strip():
                errors.append(f"{name}: gap status requires an actionable explanation.")
    return errors


def render_document(registry: dict, api_registry: dict) -> str:
    """Render a reviewable Markdown matrix from the normative evidence data."""
    capabilities = registry["capabilities"]
    scopes = evidence_scopes(registry, api_registry)
    lines = [
        "# Scientific Evidence Matrix",
        "",
        "<!-- Generated by devtools/scripts/validate_scientific_evidence.py. Do not edit manually. -->",
        "",
        "The normative sources live under `tests/scientific_truth/evidence/`.",
        "The statuses below classify registered evidence; they are not an execution",
        "record. `validate_scientific_evidence.py` checks structure without running",
        "pytest. Release evidence requires the separate zero-skip execution certificate",
        "from `execute_scientific_evidence.py` on the exact candidate commit.",
        "A gap means that governed independent evidence is absent; it does not by",
        "itself mean that the function is untested or scientifically incorrect.",
        "Claimed is an explicit evidence-review scope, not approval of manuscript",
        "wording or promotion to a Stable API. Counts are per scope; a symbol may",
        "belong to both. APIs outside these scopes are not certified by this matrix.",
        "",
        "## Summary",
        "",
        "| Status | Stable APIs | Claimed APIs |",
        "| --- | ---: | ---: |",
        *[
            f"| {status} | "
            + " | ".join(
                str(
                    sum(
                        capabilities[name]["status"] == status
                        for name in names
                        if name in capabilities
                    )
                )
                for names in scopes.values()
            )
            + " |"
            for status in ("validated", "partial", "gap")
        ],
        f"| total | {len(scopes['Stable'])} | {len(scopes['Claimed'])} |",
        "",
        "## Governed tolerances",
        "",
        "| Name | atol | rtol | Rationale |",
        "| --- | ---: | ---: | --- |",
    ]
    for name, tolerance in registry["tolerances"].items():
        lines.append(
            f"| `{name}` | {tolerance['atol']:.6g} | {tolerance['rtol']:.6g} | "
            f"{tolerance['rationale']} |"
        )

    for scope, names in scopes.items():
        lines.extend(
            (
                "",
                f"## {scope} scientific APIs",
                "",
                "| API | Stability | Status | Declared claim and scope | Evidence | Gap |",
                "| --- | --- | --- | --- | --- | --- |",
            )
        )
        for name in sorted(names):
            if name not in capabilities:
                continue
            entry = capabilities[name]
            evidence = (
                "<br>".join(
                    f"{item['class']}: `{item['test']}` "
                    f"({item.get('tolerance') or item.get('comparison', 'tolerance')})"
                    for item in entry["scientific_evidence"]
                )
                or "—"
            )
            gap = entry["gap"] or "—"
            stability = (
                api_registry["symbols"].get(name, {}).get("stability", "unknown")
            )
            claim = entry["claim"].replace("|", "\\|")
            lines.append(
                f"| `{name}` | {stability} | {entry['status']} | {claim} | {evidence} | {gap} |"
            )
    other = sorted(
        name
        for name, entry in api_registry["symbols"].items()
        if entry["stability"] == "experimental"
        and name.rsplit(".", 1)[0] in registry.get("experimental_api_scopes", [])
        and name not in capabilities
    )
    lines.extend(
        [
            "",
            "## Experimental symbols outside the reviewed scopes",
            "",
            "This namespace inventory includes public operations and configuration",
            "symbols. These symbols have not been classified here; absence is not",
            "a scientific gap assessment. Expand the explicit Claimed inventory",
            "after reviewing each operation's claim and available evidence.",
            "",
            *[f"- `{name}`" for name in other],
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    """Validate the evidence matrix and optionally rewrite its generated view."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-doc", action="store_true")
    args = parser.parse_args(argv)
    registry, load_errors = read_evidence_registry()
    api_registry = _read_json(API_REGISTRY_PATH)
    errors = load_errors + validate_registry(registry, api_registry)
    expected_document = render_document(registry, api_registry)
    if args.write_doc:
        GENERATED_DOC_PATH.write_text(expected_document, encoding="utf-8")
    elif (
        not GENERATED_DOC_PATH.exists()
        or GENERATED_DOC_PATH.read_text(encoding="utf-8") != expected_document
    ):
        errors.append(
            "Generated scientific evidence matrix is missing or stale; run with --write-doc."
        )
    if errors:
        print("Scientific evidence registry violations:")
        for error in errors:
            print(f"- {error}")
        return 1
    counts = {
        status: sum(
            entry["status"] == status for entry in registry["capabilities"].values()
        )
        for status in ("validated", "partial", "gap")
    }
    print(
        "Scientific evidence registry structure valid (tests not executed): "
        f"{counts['validated']} validated declarations, {counts['partial']} partial, "
        f"{counts['gap']} gaps."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
