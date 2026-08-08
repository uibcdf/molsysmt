#!/usr/bin/env python
"""
audit_converter_routing.py

Finds converters that call another form's converter on their own `item`.

Every `molsysmt/form/<plugin>/to_<target>.py` receives an `item` of the plugin's own form.
When it needs an intermediate form it must call the sibling in its own directory -- the
converter that goes *from this form* -- not the one with the matching name in the target's
plugin, which goes *from that form*. The two have identical names, so the mistake reads as
correct and survives review:

    # in molsysmt_MolSys/to_openmm_System.py
    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    tmp_item = to_openmm_Topology(item, ...)      # item is a MolSys, not a Topology

That one produced `TypeError: 'Chains_DataFrame' object is not callable` from inside a form
module, and made two declared conversion targets unreachable. It was found by hand.

This is the static version of that search: for each converter, resolve where each imported
name came from, and report a call whose first argument is literally `item` when the callee
came from a different plugin. Passing a converted `tmp_item` to another plugin is normal
and is not reported.

**A hit is a candidate, not a verdict.** Two forms can be compatible enough that reusing a
converter is deliberate. Read each one before changing it.

Usage:
    python devtools/scripts/audit_converter_routing.py
"""
import ast
import os
import pathlib
import sys

REPO_ROOT = pathlib.Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
FORM_ROOT = REPO_ROOT / "molsysmt" / "form"


def imported_from(tree, plugin):
    """Local name -> the plugin that defines it."""

    origin = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        if node.level == 0 and node.module.startswith('molsysmt.form.'):
            parts = node.module.split('.')
            if len(parts) >= 3:
                for alias in node.names:
                    origin[alias.asname or alias.name] = parts[2]
        elif node.level == 1:                       # from .to_x import to_x
            for alias in node.names:
                origin[alias.asname or alias.name] = plugin
    return origin


def audit():
    findings = []
    declared = {entry.name for entry in os.scandir(FORM_ROOT) if entry.is_dir()}

    for path in sorted(FORM_ROOT.glob('*/to_*.py')):
        plugin = path.parent.name
        tree = ast.parse(path.read_text())
        origin = imported_from(tree, plugin)

        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
                continue
            source = origin.get(node.func.id)
            if source is None or source == plugin:
                continue
            first = node.args[0] if node.args else None
            if isinstance(first, ast.Name) and first.id == 'item':
                findings.append({
                    'path': str(path.relative_to(REPO_ROOT)),
                    'line': node.lineno,
                    'callee': node.func.id,
                    'source': source,
                    'plugin': plugin,
                    'source_exists': source in declared,
                })
    return findings


def main():
    findings = audit()
    missing = [f for f in findings if not f['source_exists']]

    for finding in findings:
        mark = '  [plugin does not exist]' if not finding['source_exists'] else ''
        print(f"{finding['path']}:{finding['line']}: {finding['callee']} comes from "
              f"{finding['source']}, but item is a {finding['plugin']} item{mark}")

    print(f"\nCandidates: {len(findings)}")
    if missing:
        print(f"Of those, {len(missing)} import from a plugin directory that does not "
              f"exist, so they would fail on the first call.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
