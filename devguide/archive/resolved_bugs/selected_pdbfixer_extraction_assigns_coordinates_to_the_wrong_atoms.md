---
summary: Selected PDBFixer extraction assigns coordinates to the wrong atoms
issue: uibcdf/molsysmt#744
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: high
verification: reproduced
area: [form, extract, structure, units]
guard: tests/form/pdbfixer_PDBFixer/test_selected_extraction.py
normative:
blocked_by: []
supersedes: []
---

# Keeping PDBFixer selected atoms and coordinates aligned

## What

Successful selected extraction and conversion to the same PDBFixer form can
place coordinates on the wrong atom identities. Four valid public controls under
nm/pm policies select source atoms [3, 1]; names appear in canonical order [1, 3]
while geometry keeps [3, 1], a 0.2 nm discrepancy in the tiny fixture. Source data
stay unchanged. This is a pre-1.0 scientific-correctness bug, not a new feature.

## How

The subset branch obtains coordinates in requested order but reconstructs an
OpenMM Topology using canonical source order. It also calls the OpenMM
Topology-to-itself adapter with a PDBFixer object and trusted digestion skipped,
instead of using the PDBFixer-to-OpenMM Topology converter. That violates the
callee's explicit native context even where its universal delegation happens to
accept the object. Correspondence must be normalized once for both fields.

## Why

Matching atom counts and units do not establish atomic correspondence. A valid
result must align identities, bonds and physical geometry. The needed reusable
bridge already exists in this form; a feature-local reconstruction or guessed
remapping is unnecessary.

## Correction in progress — 2026-11-13

The branch sorts the validated atom indices before both acquisitions and calls
its own to_openmm_Topology converter. The established OpenMM-to-PDBFixer tool
then reconstructs the selected object with unit-bearing coordinates. Its PDB
coordinate precision and single-pose capacity remain explicit; extraction does
not perform chemical repair, hydration or energy minimization.

The affected PDBFixer cohort passes 41 cases with one expected legacy H5MSM
warning, including the four numeric-identity alignment guards. The first draft's
four failures occur earlier because its oracle requests an unsupported system-
coordinate getter. Correcting only the oracle to element='atom' then exposes the
four true alignment failures. Both raw attempts are retained and distinguished.

## Acceptance criteria

- Both public selected routes return source atom order [1, 3], correct coordinate
  shape (1, 2, 3) and independently expected positions in nm and pm policies.
- Source names, geometry and inventory remain unchanged.
- Reuse owning conversion/quantity tools with a valid trusted delegation context.
  Preserve current whole-copy/reuse and single-pose/reconstruction limits.
- Update docstrings, form documentation and applicable generic/course/Cookbook
  explanations, then receive the affected runtime and actual HTML articles.
- Preserve baseline/oracle/harness failures and exact source/provider/resource
  scope. No installed, complete-source/scientific or final-pair gate is implied.


## Completed receiving — 2026-11-13

Published b16c43a0d and the immutable owning implementation 6dd779adc have
independent public-tree verification. The final joint selection passes 340
cases; all 95 form notebooks have explicit receiving ownership and actual HTML
link checks. Twenty-three selected pages build without warnings, preserving
code/output/metadata, headings and anchors. The affected runtime cohorts and
original failed witnesses remain separately recorded.

See the [receiving receipt](../../../devtools/data/remaining_form_reference_receiving_727_20261113.json)
and [current form contract](../../forms_and_conversions.md). This closes the
reported mechanism, not every conversion/scientific/performance capability.
CuPy, complete-source/scientific gates, installed final-pair acceptance and
publication remain outside this scope.
