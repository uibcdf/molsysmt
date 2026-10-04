---
summary: Native standard-residue repair must reject ambiguous side-chain placement
issue: uibcdf/molsysmt#322
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: high
verification: reproduced
area: [build]
guard: tests/build/add_missing_heavy_atoms/test_standard_residue_preflight.py
normative:
blocked_by: []
supersedes: []
---

# Native standard-residue repair must reject ambiguous side-chain placement

**Reported:** 2026-10-04, during observed receptor preparation for #298.
**Status:** Resolved by bounded native domain preservation and reconstruction checks; local acceptance is recorded below.

## What

Native standard-residue repair filled missing side-chain atoms by rigid template
alignment without applying the bounded preflight used for curated modified
residues. In the pinned 1QKU label-chain A receptor, SER301 lacks OG and LYS302/
LYS303 each lack CG/CD/CE/NZ. The old native route added all nine atoms and
reported an empty missing-heavy inventory, although their conformations had not
been assessed. One modeled LYS303 CB-CG distance was 0.1199 nm.

The guarded public reproduction is:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/build/add_missing_heavy_atoms/test_standard_residue_preflight.py
```

## How

`molsysmt/build/add_missing_heavy_atoms.py` previously ran modified-residue
preflight and its post-placement bond check only for curated templates. Standard
residues directly used the geometric placer. Broad alignment over observed
atoms does not determine missing side-chain torsions or preserve local bond
lengths when the deposited conformation differs from the reference.

The shared private `_residue_repair.assess_residue` now preflights both classes
behind the existing public build tool. Exact names, elements and stored
intragroup connectivity must agree; duplicate names, invalid coordinates,
collinear or insufficient local anchors and multiple missing side-chain atoms
remain unassessed. Known reference bond orders are compared only when that
reference declares them. Existing OXT is allowed independently of the standard
heavy template, whose terminal completion is a separate operation.

Supported local placement uses nearby graph anchors. Every placed-to-observed
bond must differ from its reference length by at most 0.04 nm in every structure.
A failing group remains unchanged with `UnassessedResidueWarning`. This is a
conservative reconstruction policy, not a global geometry or energy validator.

## Why

The #298 receptor preparation must not interpret a completed atom inventory as
validated lysine coordinates. Such geometry affects chemical features and
subsequent interaction calculations requested by uibcdf/pharmacophoremt#22.
Silent side-chain completion could transmit an unassessed rotamer as observed
structural evidence.

## What is measured and what is assumed

**Measured:** the old probe on 1QKU chain A started with 1,990 heavy atoms, added
nine and returned 1,999. Its modeled LYS303 CB-CG length was 0.1199 nm; the
reference side-chain C-C bonds are approximately 0.15 nm. The same reproduction
is now constrained by the guard's pinned fixture and explicit missing-name checks.

**Contract-tested:** the corrected route adds only SER301 OG (1,991 atoms),
retains all observed IDs and physical coordinates, leaves both four-atom lysine
gaps explicit, emits two unassessed diagnostics and does not mutate the source.
Synthetic controls reject collinear/nonfinite anchors, wrong elements and
conflicting names. Existing modified-residue controls retain their bounded cases.

**Assumed:** one locally placed atom is an initial estimate. Its successful local
checks do not prove stereochemistry, clashes, biological context or an energy
minimum. Multiple missing side-chain atoms are unassessed because this tool has
no validated placement for them, not because every such gap is mathematically
impossible to reconstruct. A future validated ring/rotamer method could extend it.

## What was refuted

- Equal atom counts between native repair and PDBFixer are not a scientific
  acceptance criterion. Existing parity tests demanded native reconstruction of
  all gaps even when the placement was unassessed.
- On the bundled 1BRS control the bounded native route adds four atoms while
  PDBFixer adds 78; this difference is now explicit. The independently pinned
  shared repairable subset is groups 282, 325, 385 and 587.
- In the synthetic AlaValPro CB-gap control, native placement repairs ALA and
  PRO but rejects VAL for conflicting placed bond geometry; PDBFixer repairs
  all three. Tests retain exact inventories and the native rejection diagnostic.
- The tutorial's two missing HIS ring atoms remain unassessed; its THR OG1 is
  repaired. The narrative now reports the remaining gaps instead of claiming all
  missing atoms were restored.

## Scope and exclusions

Covers native standard-residue heavy-atom reconstruction and reuse of existing
modified-residue preflight. PDBFixer remains an explicitly separate optional
engine. No rotamer search, force-field minimization, stereochemistry inference,
global clash checks, whole-receptor repair or environmental protonation is added.
Unvalidated coordinate reconstruction remains related to uibcdf/molsysmt#249;
the complete receptor workflow stays partial under uibcdf/molsysmt#298.

## Acceptance criteria

The guard must reject both real lysine gaps, retain their exact missing-name
inventories, permit the single serine placement and preserve source pose/IDs.
Invalid anchor/identity controls and existing modified-residue controls must pass.
Public documentation must distinguish incomplete inventory from unassessed
placement and require inspection of remaining gaps.

## Provenance

Linux development workspace, Python 3.13.14 under the bounded #237 migration
exception, released ArgDigest 0.13.0 override, NumPy 2.4.6, pandas 2.3.3 and
RDKit 2025.09.5 where the fixture workflow uses it. Date: 2026-10-04.
This is targeted contract evidence, not Python 3.14 release qualification or
an installed-artifact, performance or biological benchmark. Commands using the
ArgDigest override record the development environment; that override is not a
runtime requirement or a committed path.

## Local validation checkpoint — 2026-10-04

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/build/add_missing_heavy_atoms \
  tests/build/add_missing_hydrogens/test_add_missing_hydrogens_engine_MolSysMT.py \
  tests/build/add_missing_terminal_cappings/test_add_missing_terminal_cappings_engine_MolSysMT.py \
  --doctest-modules molsysmt/build/add_missing_heavy_atoms.py
```

63 passed in 37.73 s. The 24 warnings comprised 22 reported atom-parameter drops
and two deliberate unassessed VAL controls. Strengthening the terminal preservation
fixture to start with a still-evaluated analysis and no heavy gap then passed
all five domain-preservation cases in 4.64 s. This final focused run replaces that
fixture's earlier evidence without claiming another aggregate suite execution.

The heavy-atom tutorial executed and saved its real outputs (11.9 s). Docstring,
course, public API registry/signature, dependency-import and developer-guide checks
passed. Repository-wide Ruff check and format checks passed. Sphinx HTML exited
0 with existing course/navigation/native-class reference warnings; it is not a
globally clean documentation gate. Hosted CI acceptance is separate.
