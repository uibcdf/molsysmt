#!/usr/bin/env python
"""Aggregate the fast release-readiness gates into a single verdict.

This runs every cheap, deterministic gate (the repository validators plus a public-API
smoke) and prints one PASS/FAIL summary. It is the pre-flight a maintainer runs locally
before triggering the heavy gate (`ci-full.yaml`, the full pytest matrix on all supported
OS/Python combinations), which this script deliberately does NOT run.

Policy: `devguide/release_gate.md`.

Usage:
    python devtools/scripts/release_gate.py            # run all fast gates
    python devtools/scripts/release_gate.py --list     # list the gates only

Exit 0 if every fast gate passes, 1 otherwise. The full pytest matrix is reported as a
required, separate gate that this script does not execute.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "devtools" / "scripts"

# Ordered, explicit list of fast gates (script, human label). Explicit, not globbed, so
# adding a gate is a deliberate act.
VALIDATORS = [
    ("validate_api_stability.py", "Public API stability registry"),
    ("validate_function_tiers.py", "Public function support tiers"),
    ("validate_form_adapters.py", "Form adapter delivery contracts"),
    ("audit_conversion_fidelity.py", "Tier 1 conversion fidelity (accepted-debt baseline)"),
    ("validate_scientific_evidence.py", "Scientific evidence registry"),
    ("validate_dependencies.py", "No top-level soft-dependency imports"),
    ("validate_devguide.py", "Developer-guide integrity"),
    ("validate_course.py", "Four Paths course structure"),
    ("validate_demo_assets.py", "Demo assets / H5MSM fixtures"),
    ("validate_resources.py", "Resource manifests"),
    ("validate_citation.py", "Citation and Zenodo metadata"),
    ("check_rust_hot_paths.py", "Rust kernel hot paths (no libm rounding calls)"),
]

SMOKE = """
import molsysmt as msm
sys = msm.systems['T4 lysozyme L99A']['181l.pdb']
assert msm.get_form(sys) == 'file:pdb'
assert msm.get(sys, n_atoms=True) > 0
mol = msm.convert(sys, to_form='molsysmt.MolSys')
assert msm.get_form(mol) == 'molsysmt.MolSys'
assert len(msm.select(mol, selection='molecule_type=="protein"')) > 0
import molsysmt.structure as st
assert st.get_center(mol).shape == (1, 1, 3)
print('public-API smoke OK')
"""


def run(cmd, label, timeout):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=timeout)
        ok = p.returncode == 0
        tail = (p.stdout.strip().splitlines() or [""])[-1]
        return ok, time.time() - t0, tail, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return False, time.time() - t0, f"TIMEOUT after {timeout}s", ""


def main() -> int:
    if "--list" in sys.argv:
        print("Fast release gates (run before the ci-full pytest matrix):")
        for script, label in VALIDATORS:
            print(f"  - {label}  ({script})")
        print("  - Public-API smoke (import + convert + get + select + get_center)")
        print("\nHeavy gate (NOT run here): ci-full.yaml — full pytest matrix on "
              "ubuntu+macos x {3.11,3.12,3.13}.")
        return 0

    results = []
    for script, label in VALIDATORS:
        path = SCRIPTS / script
        if not path.exists():
            results.append((label, False, 0.0, "MISSING SCRIPT"))
            continue
        ok, dt, tail, _ = run([sys.executable, str(path)], label, timeout=300)
        results.append((label, ok, dt, tail))

    ok, dt, tail, _ = run([sys.executable, "-c", SMOKE], "Public-API smoke", timeout=300)
    results.append(("Public-API smoke", ok, dt, tail if ok else "smoke FAILED"))

    width = max(len(r[0]) for r in results)
    print("Release readiness — fast gates\n" + "=" * (width + 20))
    passed = 0
    for label, gate_ok, dt, tail in results:
        mark = "PASS" if gate_ok else "FAIL"
        passed += gate_ok
        print(f"  [{mark}] {label.ljust(width)}  {dt:5.1f}s  {tail[:60]}")

    total = len(results)
    print("=" * (width + 20))
    print(f"Fast gates: {passed}/{total} passed.")
    print("Heavy gate still required before tagging: a green ci-full.yaml run "
          "(full pytest matrix, ubuntu+macos x {3.11,3.12,3.13}) on the exact, "
          "committed tag candidate. See devguide/release_gate.md.")

    if passed != total:
        print("\nRELEASE GATE: FAIL — fix the gates above before proceeding.")
        return 1
    print("\nRELEASE GATE (fast portion): PASS. Proceed to the ci-full matrix.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
