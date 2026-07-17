#!/usr/bin/env python
"""Validating the machine-readable public API stability contract."""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "devtools/data/public_api_stability.json"
GENERATED_DOC_PATH = REPO_ROOT / "devguide/api_stability_registry.md"
ALLOWED_STABILITIES = {"stable", "experimental", "outside-contract"}
ALLOWED_LIFECYCLES = {"active", "deprecated"}
VERSION_PATTERN = re.compile(r"^(?:pre-1\.0|\d+\.\d+\.\d+)$")


def _read_registry(path: Path = REGISTRY_PATH) -> dict:
    """Read the API registry without importing MolSysMT."""
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _literal_assignment(tree: ast.Module, name: str, source: Path):
    """Return one literal module assignment."""
    matches = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == name for target in targets):
            matches.append(node.value)
    if len(matches) != 1:
        raise ValueError(f"{source}: expected one {name} assignment, found {len(matches)}")
    try:
        return ast.literal_eval(matches[0])
    except (ValueError, TypeError) as error:
        raise ValueError(f"{source}: {name} must be a literal") from error


def discover_exports(source: Path, discovery: str) -> set[str]:
    """Discover intentionally public exports from source code using AST only."""
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    if discovery == "lazy-root":
        registry = _literal_assignment(tree, "_LAZY_ATTRIBUTES", source)
        if not isinstance(registry, dict) or not all(isinstance(name, str) for name in registry):
            raise ValueError(f"{source}: _LAZY_ATTRIBUTES must be a string-keyed dictionary")
        return set(registry)
    if discovery != "package-init":
        raise ValueError(f"Unsupported discovery mode {discovery!r}")

    exports = set()
    explicit_all = None
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname or alias.name
                if name != "*" and not name.startswith("_"):
                    exports.add(name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                exports.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets):
                explicit_all = set(ast.literal_eval(node.value))
    return explicit_all if explicit_all is not None else exports


def discover_lazy_registry(source: Path) -> dict:
    """Return the literal lazy registry from a root module."""
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    registry = _literal_assignment(tree, "_LAZY_ATTRIBUTES", source)
    if not isinstance(registry, dict):
        raise ValueError(f"{source}: _LAZY_ATTRIBUTES must be a dictionary")
    return registry


def inventory(registry: dict, repo_root: Path = REPO_ROOT) -> set[str]:
    """Return all fully qualified exports in the tracked scopes."""
    output = set()
    for scope, metadata in registry["tracked_scopes"].items():
        source = repo_root / metadata["source"]
        for name in discover_exports(source, metadata["discovery"]):
            output.add(f"{scope}.{name}")
    return output


def validate_registry(registry: dict, repo_root: Path = REPO_ROOT) -> list[str]:
    """Return registry contract violations."""
    errors = []
    if registry.get("schema_version") != "molsysmt.api-stability@1":
        errors.append("schema_version must be 'molsysmt.api-stability@1'.")

    scopes = registry.get("tracked_scopes")
    symbols = registry.get("symbols")
    if not isinstance(scopes, dict) or not scopes:
        return errors + ["tracked_scopes must be a non-empty object."]
    if not isinstance(symbols, dict):
        return errors + ["symbols must be an object keyed by fully qualified name."]

    try:
        discovered = inventory(registry, repo_root)
    except (OSError, SyntaxError, ValueError) as error:
        return errors + [str(error)]
    registered = set(symbols)
    for name in sorted(discovered - registered):
        errors.append(f"Unclassified public export: {name}")
    for name in sorted(registered - discovered):
        errors.append(f"Stale or nonexistent registry symbol: {name}")

    for name, entry in sorted(symbols.items()):
        if "._private." in name or name.startswith("molsysmt._private"):
            errors.append(f"Internal symbol cannot be registered: {name}")
        if not isinstance(entry, dict):
            errors.append(f"{name}: registry entry must be an object.")
            continue
        stability = entry.get("stability")
        if stability not in ALLOWED_STABILITIES:
            errors.append(f"{name}: invalid stability {stability!r}.")
        lifecycle = entry.get("lifecycle", "active")
        if lifecycle not in ALLOWED_LIFECYCLES:
            errors.append(f"{name}: invalid lifecycle {lifecycle!r}.")
        introduced = entry.get("introduced")
        if not isinstance(introduced, str) or not VERSION_PATTERN.fullmatch(introduced):
            errors.append(f"{name}: introduced must be a semantic version or 'pre-1.0'.")
        owner = entry.get("owner")
        if not isinstance(owner, str) or not owner:
            errors.append(f"{name}: owner is required.")
        for field in ("documentation", "contract_tests"):
            relative_path = entry.get(field)
            if not isinstance(relative_path, str) or not relative_path:
                errors.append(f"{name}: {field} is required.")
            elif not (repo_root / relative_path).exists():
                errors.append(f"{name}: {field} path does not exist: {relative_path}")
        subtree_stability = entry.get("subtree_stability")
        if subtree_stability is not None:
            if name.count(".") != 1:
                errors.append(f"{name}: subtree_stability is only valid for root namespaces.")
            if subtree_stability not in {"experimental", "outside-contract"}:
                errors.append(
                    f"{name}: subtree_stability must be experimental or outside-contract."
                )
            if subtree_stability != stability:
                errors.append(f"{name}: subtree_stability must match namespace stability.")
        if lifecycle == "deprecated":
            for field in ("deprecated_since", "replacement", "removal_not_before"):
                if not entry.get(field):
                    errors.append(f"{name}: deprecated symbols require {field}.")
            for field in ("deprecated_since", "removal_not_before"):
                value = entry.get(field)
                if value and not VERSION_PATTERN.fullmatch(value):
                    errors.append(f"{name}: {field} must be a semantic version.")
            replacement = entry.get("replacement")
            if replacement and replacement not in symbols:
                errors.append(f"{name}: replacement is not registered: {replacement}")
        elif any(field in entry for field in ("deprecated_since", "replacement", "removal_not_before")):
            errors.append(f"{name}: deprecation metadata requires lifecycle='deprecated'.")

    for scope, metadata in scopes.items():
        if metadata["discovery"] != "lazy-root":
            continue
        lazy_registry = discover_lazy_registry(repo_root / metadata["source"])
        for export, target in lazy_registry.items():
            qualified_name = f"{scope}.{export}"
            child_scope = qualified_name
            if isinstance(target, str) and child_scope not in scopes:
                if not symbols.get(qualified_name, {}).get("subtree_stability"):
                    errors.append(
                        f"Untracked public namespace requires subtree_stability: {qualified_name}"
                    )
    return errors


def validate_transition(previous: dict, current: dict) -> list[str]:
    """Return forbidden compatibility transitions between two registries."""
    errors = []
    previous_symbols = previous.get("symbols", {})
    current_symbols = current.get("symbols", {})
    for name, previous_entry in sorted(previous_symbols.items()):
        current_entry = current_symbols.get(name)
        if current_entry is None:
            if previous_entry.get("stability") == "stable":
                errors.append(f"Stable symbol removed from registry: {name}")
            continue
        if previous_entry.get("stability") == "stable" and current_entry.get("stability") != "stable":
            errors.append(
                f"Stable symbol cannot be demoted to {current_entry.get('stability')}: {name}"
            )
        if (
            previous_entry.get("lifecycle", "active") == "deprecated"
            and current_entry.get("lifecycle", "active") != "deprecated"
        ):
            errors.append(f"Deprecated lifecycle cannot be reverted silently: {name}")
    return errors


def render_document(registry: dict) -> str:
    """Render the normative human-readable view of the registry."""
    counts = {stability: 0 for stability in sorted(ALLOWED_STABILITIES)}
    deprecated = 0
    for entry in registry["symbols"].values():
        counts[entry["stability"]] += 1
        deprecated += entry.get("lifecycle") == "deprecated"

    lines = [
        "# Public API Stability Registry",
        "",
        "<!-- Generated by devtools/scripts/validate_api_stability.py. Do not edit manually. -->",
        "",
        "This is the human-readable view of the normative registry in",
        "`devtools/data/public_api_stability.json`. The validator discovers exports",
        "with the Python AST, so it does not import MolSysMT or optional dependencies.",
        "",
        "## Summary",
        "",
        "| Classification | Symbols |",
        "| --- | ---: |",
    ]
    for stability in ("stable", "experimental", "outside-contract"):
        lines.append(f"| {stability} | {counts[stability]} |")
    lines.extend((f"| deprecated lifecycle | {deprecated} |", "", "## Symbols", ""))

    for scope in registry["tracked_scopes"]:
        scope_symbols = [
            (name, entry)
            for name, entry in sorted(registry["symbols"].items())
            if name.rsplit(".", 1)[0] == scope
        ]
        lines.extend(
            (
                f"### `{scope}`",
                "",
                "| Symbol | Stability | Lifecycle | Introduced |",
                "| --- | --- | --- | --- |",
            )
        )
        for name, entry in scope_symbols:
            lifecycle = entry.get("lifecycle", "active")
            if lifecycle == "deprecated":
                lifecycle = (
                    f"deprecated {entry['deprecated_since']}; use `{entry['replacement']}`; "
                    f"not removed before {entry['removal_not_before']}"
                )
            lines.append(
                f"| `{name}` | {entry['stability']} | {lifecycle} | {entry['introduced']} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    """Validate the registry and optionally rewrite its generated view."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-doc", action="store_true")
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Previous registry used to reject forbidden stability transitions.",
    )
    args = parser.parse_args(argv)
    registry = _read_registry()
    errors = validate_registry(registry)
    if args.baseline is not None:
        errors.extend(validate_transition(_read_registry(args.baseline), registry))
    expected_document = render_document(registry)
    if args.write_doc:
        GENERATED_DOC_PATH.write_text(expected_document, encoding="utf-8")
    elif not GENERATED_DOC_PATH.exists() or GENERATED_DOC_PATH.read_text(encoding="utf-8") != expected_document:
        errors.append("Generated API stability document is missing or stale; run with --write-doc.")
    if errors:
        print("Public API stability registry violations:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"API stability registry valid: {len(registry['symbols'])} symbols classified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
