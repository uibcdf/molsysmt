#!/usr/bin/env python
"""Validate public-function support tiers.

Support tier is derived from the API-stability registry, not from a second registry
(see devguide/archive/resolved_proposals/function_support_tier_classification.md):

    stable            -> Tier 1 (contractual)
    experimental      -> Tier 3 (experimental / niche)
    outside-contract  -> outside the core contract

Explicit ``@support_tier(N)`` decorators override the derived tier. This validator:

- derives a tier for every leaf symbol in devtools/data/public_api_stability.json;
- finds every ``@support_tier(N)`` decorator in molsysmt/ via AST (no import);
- checks each decorated function is consistent with its stability-derived tier;
- prints the tier distribution.

Exit 0 on success, 1 on any contradiction. Imports nothing from MolSysMT.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REGISTRY = REPO / "devtools" / "data" / "public_api_stability.json"
PACKAGE = REPO / "molsysmt"

STABILITY_TO_TIER = {
    "stable": 1,
    "experimental": 3,
    "outside-contract": None,   # outside the core support contract
}


def load_registry():
    data = json.loads(REGISTRY.read_text())
    return data["symbols"], set(data["tracked_scopes"])


def find_support_tier_decorators():
    """Return list of (qualified_name, tier_int, module_dotted) for @support_tier(N)."""
    found = []
    for py in PACKAGE.rglob("*.py"):
        if "__pycache__" in py.parts:
            continue
        try:
            tree = ast.parse(py.read_text(), filename=str(py))
        except SyntaxError:
            continue
        module = "molsysmt." + ".".join(py.relative_to(PACKAGE).with_suffix("").parts)
        module = module.replace(".__init__", "")
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            for dec in node.decorator_list:
                if (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name)
                        and dec.func.id == "support_tier" and dec.args
                        and isinstance(dec.args[0], ast.Constant)):
                    found.append((node.name, dec.args[0].value, module))
    return found


def main() -> int:
    symbols, scopes = load_registry()
    errors: list[str] = []

    # Derive tiers for leaf symbols (exclude scope-root container entries).
    tiers = {"Tier 1": 0, "Tier 3": 0, "outside-contract": 0, "unknown": 0}
    derived = {}
    for name, meta in symbols.items():
        if name in scopes:
            continue  # submodule container, not a function
        stab = meta.get("stability")
        if stab not in STABILITY_TO_TIER:
            errors.append(f"{name}: unknown stability {stab!r} (no tier mapping)")
            tiers["unknown"] += 1
            continue
        t = STABILITY_TO_TIER[stab]
        derived[name] = t
        tiers["Tier 1" if t == 1 else "Tier 3" if t == 3 else "outside-contract"] += 1

    # Reconcile @support_tier decorators with the derived tiers.
    decorated = find_support_tier_decorators()
    for fname, tier, module in decorated:
        # Candidate public names for a decorated function (the source module, and the
        # re-export convention where a file NAME.py is re-exported as its parent.NAME).
        pkg = module.rsplit(".", 1)[0]
        candidates = {f"{module}.{fname}", f"{module}", f"{pkg}.{fname}"}
        match = next((derived[c] for c in candidates if c in derived), None)
        if match is None:
            errors.append(
                f"{module}.{fname}: @support_tier({tier}) but no matching public symbol "
                f"in the stability registry"
            )
        elif match != tier:
            errors.append(
                f"{module}.{fname}: @support_tier({tier}) contradicts stability-derived "
                f"Tier {match}"
            )

    print("Public-function support tiers (derived from API stability):")
    for k, v in tiers.items():
        if v:
            print(f"  {k}: {v}")
    print(f"  @support_tier decorators found: {len(decorated)} "
          f"({', '.join(sorted({m for _, _, m in decorated})) or 'none'})")

    if errors:
        print("\nFunction-tier validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("Function-tier classification valid: every public function has a tier; "
          "decorators are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
