---
summary: Native solvation uses the optional OpenMM reader for its water template.
issue: uibcdf/molsysmt#339
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: medium
verification: measured
area: [build, form]
guard: tests/build/test_readme_native_preparation.py
normative:
blocked_by: []
supersedes: []
---

# Native solvation uses the optional OpenMM reader for its water template

**Reported:** 2026-10-05 while qualifying the README under S4/#334.
**Status:** resolved; native water loading and connectivity are explicit.

## What

With imports of OpenMM and PDBFixer blocked, the README preparation failed in
`solvate(engine='MolSysMT')`. The PDB template conversion attempted the legacy
OpenMM bond inference, retained no inferred edges and left molecule indices
undefined. Water tiling then raised a pandas missing-integer `ValueError`.

```bash
python -m pytest tests/build/test_readme_native_preparation.py::test_readme_native_preparation_without_openmm_or_pdbfixer
```

The pre-fix run failed, with 7 presentation checks passing. The import guard
rejects attempts to import either optional engine, including when installed.

## How

The native branch in `molsysmt/build/solvate.py` used an unqualified conversion
of its bundled water file. It now reads PDB or GRO without optional inference,
uses the existing public `build.add_missing_bonds(engine='MolSysMT')` tool and
rebuilds the native semantic hierarchy before tiling. Water bond interpretation
remains in the general water/connectivity tools, rather than a second local
implementation in the solvation consumer.

## Why

Native preparation must work without optional repair engines. The bug was hidden
by environments containing OpenMM, so the earlier S3 profiles did not qualify
that absence. This correction belongs to the existing native solvation profile;
no new method or supported water model is admitted by #334.

## What is measured and what is assumed

Measured: the README preparation succeeds with both optional imports forbidden.
All four existing native water models (TIP3P, SPC/E, SPC and TIP4P-EW) succeed,
retain the expected three/four sites per water and add exactly two O–H edges
per water. The full solvation/presentation/citation selection passes 48 tests
with zero skips in 33.43 s, including the solvation doctest.

The legacy H5MSM fixture intentionally emits its deprecation warning. Two
TIP4P-EW checks warn about the existing unrecognized `M` virtual-site name;
these checks establish site/edge accounting, not force-field parameterization.
No claim is made about arbitrary solvent or ligand chemistry.

## What was refuted

Changing only the README engine argument was insufficient: water loading had
its own implicit backend. Delegating the PDB template to the newer bounded
protein covalent-inference route also left water molecule indices absent; it
is not the appropriate water-template provider. Passing a PDB-only policy to
GRO failed its signature contract. The existing general water-template bond
tool handles both forms without those assumptions.

## Scope and exclusions

Existing native water templates and their semantic indices. No change to the
OpenMM/PDBFixer branches, covalent criteria, format contracts or dependency floors.

## Acceptance criteria

The guard executes the README's native preparation and all existing native
water models under forbidden optional imports, asserting structure/box and
water atom/bond counts. Reintroducing the implicit reader breaks this guard.

## Provenance

Linux, Python 3.14.7, NumPy 2.4.6, pandas 2.3.3, ArgDigest 0.13.0 and
PyUnitWizard 0.28.1 controlled providers, 2026-10-05. The
[checkpoint artifact](../../../devtools/data/public_presentation_20261005.json)
retains commands, scope, versions and source hashes.
