#!/usr/bin/env python
"""Inventory declared direct conversion routes and planned executable smoke coverage.

This command checks the plan and accepted unexecuted debt, not execution. Run
both ``test_declared_native_edges.py`` and ``test_declared_h5msm_edges.py`` under
``tests/conversion_truth`` for execution evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = REPO_ROOT / "devtools/data/conversion_execution_baseline.json"


def declared_edges():
    """Discover registered direct routes without importing converter implementations."""
    from molsysmt import configure
    from molsysmt.form import _dict_modules

    with configure.context(show_all_capabilities=True):
        return {
            (source, target)
            for source, module in _dict_modules.items()
            for target in getattr(module, "_convert_to", {})
        }


def read_plan(path=BASELINE_PATH):
    return json.loads(path.read_text())


def planned_edges(graph, plan):
    """Select currently profiled edges from the actual declared graph."""
    return {
        (source, target)
        for source, target in graph
        if source in plan["source_forms"] and target in plan["target_forms"]
    }


def audit_plan(graph, plan):
    """Report planned cases and explicit debt; never label either as executed."""
    selected = planned_edges(graph, plan)
    deferred = graph - selected
    accepted = {
        (source, target)
        for source, entry in plan["accepted_unexecuted_edges"].items()
        for target in entry["targets"]
    }
    errors = []
    if plan.get("schema_version") != 1:
        errors.append("Unsupported conversion-execution plan schema.")
    for axis in ("source_forms", "target_forms"):
        names = plan[axis]
        if not names or len(set(names)) != len(names):
            errors.append(f"{axis} must be a nonempty unique form list.")
    for source, entry in plan["accepted_unexecuted_edges"].items():
        if not entry.get("reason", "").strip():
            errors.append(f"{source}: unexecuted edges require a reason.")
        if len(entry["targets"]) != len(set(entry["targets"])):
            errors.append(f"{source}: duplicate deferred targets.")
    errors.extend(
        f"New unexecuted edge: {source} -> {target}"
        for source, target in sorted(deferred - accepted)
    )
    errors.extend(
        f"Stale unexecuted debt: {source} -> {target}"
        for source, target in sorted(accepted - deferred)
    )
    return {
        "profile": plan["profile"],
        "declared_edges": len(graph),
        "planned_smoke_edges": len(selected),
        "accepted_unexecuted_edges": len(deferred),
        "errors": errors,
        "execution": "not performed by this audit",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit_plan(declared_edges(), read_plan())
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(
            f"Conversion execution plan: {report['declared_edges']} declared, {report['planned_smoke_edges']} planned smoke edges, {report['accepted_unexecuted_edges']} accepted unexecuted edges. Execution not performed by this audit."
        )
        for error in report["errors"]:
            print(error)
    return int(bool(report["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
