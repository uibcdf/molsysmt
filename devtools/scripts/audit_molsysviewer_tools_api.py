"""Inventory declared scientific API paths and actual bound-addon exposure.

This is a source inventory, not scientific, installed or release qualification.
Format adapters, native classes/configuration and third-party bridges are outside
its functional scope. Historical hbonds aliases are retained as a separate group.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import inspect
import json
import subprocess
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCOPES = (
    "basic",
    "topology",
    "structure",
    "pbc",
    "physchem",
    "build",
    "molecular_mechanics",
    "interactions",
    "element",
    "h5msm",
    "hbonds",
)


def _children(module):
    filename = getattr(module, "__file__", None)
    if not filename or Path(filename).name != "__init__.py":
        return []
    names = set(getattr(module, "__all__", ()))
    for node in ast.parse(Path(filename).read_text()).body:
        if isinstance(node, ast.ImportFrom):
            names.update(
                alias.asname or alias.name for alias in node.names if alias.name != "*"
            )
    return [
        name
        for name in sorted(names)
        if not name.startswith("_")
        and isinstance(getattr(module, name, None), types.ModuleType)
        and getattr(module, name).__name__.startswith(module.__name__ + ".")
    ]


def _scan(module, path, facade):
    rows = []
    names = getattr(module, "__all__", None) or list(vars(module))
    for name in sorted(names):
        value = getattr(module, name)
        if (
            name.startswith("_")
            or not inspect.isfunction(value)
            or not value.__module__.startswith("molsysmt.")
        ):
            continue
        signature = inspect.signature(value)
        primary = next(
            (
                arg
                for arg in signature.parameters
                if arg
                in {"molecular_system", "to_molecular_system", "molecular_systems"}
            ),
            None,
        )
        bound = getattr(facade, name, None) if facade is not None else None
        original = inspect.unwrap(value)
        rows.append(
            dict(
                path=f"{path}.{name}",
                module=path,
                signature=str(signature),
                exposed=callable(bound),
                primary_parameter=primary,
                input_kind="primary"
                if primary in {"molecular_system", "to_molecular_system"}
                else "explicit_collection"
                if primary
                else "explicit_inputs",
                implementation=f"{original.__module__}:{original.__qualname__}",
            )
        )
    for child in _children(module):
        rows.extend(
            _scan(
                getattr(module, child),
                f"{path}.{child}",
                getattr(facade, child, None) if facade is not None else None,
            )
        )
    return rows


def collect_inventory():
    """Read native declarations and real per-view methods without calling science."""
    native = importlib.import_module("molsysmt")
    host = importlib.import_module("molsysviewer")
    with host.new_view() as view:
        addon = view.addons.molsysmt  # Missing discovery/host compatibility must fail.
        rows = [
            row
            for scope in SCOPES
            for row in _scan(getattr(native, scope), scope, getattr(addon, scope, None))
        ]
    modules = {}
    for scope in SCOPES:
        selected = [row for row in rows if row["path"].split(".")[0] == scope]
        modules[scope] = dict(
            native_paths=len(selected),
            exposed_paths=sum(row["exposed"] for row in selected),
            missing=[row["path"] for row in selected if not row["exposed"]],
        )
    return dict(
        schema="molsysmt.viewer-api-inventory@1",
        scope="Source exposure only; qualification is separate.",
        native_source=str(Path(native.__file__).resolve()),
        host_source=str(Path(host.__file__).resolve()),
        exclusions=[
            "form adapters",
            "native classes and methods",
            "configuration",
            "third-party bridges",
            "datasets",
        ],
        modules=modules,
        functions=rows,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, help="Write the full JSON source inventory."
    )
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT))
    result = collect_inventory()
    result["source_head"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    result["working_tree_has_changes"] = bool(
        subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT)
    )
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    for scope, counts in result["modules"].items():
        print(
            f"{scope:22} {counts['exposed_paths']:3}/{counts['native_paths']:<3} exposed"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
