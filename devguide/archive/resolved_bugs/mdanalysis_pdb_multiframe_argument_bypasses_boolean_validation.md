---
summary: MDAnalysis PDB multiframe argument bypasses boolean validation
issue: uibcdf/molsysmt#432
status: resolved
opened: 2026-10-23
closed: 2026-10-23
severity: low
verification: reproduced
area: [argdigest, form]
guard: tests/form/MDAnalysis_Universe/test_pdb_multiframe.py
normative:
blocked_by: []
supersedes: []
---

# MDAnalysis PDB export bypasses its argument boundary

**Reported:** 2026-10-23, while adding the MDAnalysis Universe profile under #181.
**Status:** Resolved; both argument-boundary failures have executable guards.

## What

The MDAnalysis.Universe PDB converter declares multiframe=True but has no
registered boolean digester. Invalid values reach the external writer from both
the public converter and msm.convert. A normal direct call with
structure_indices=[0, 1] also fails: ArgDigest normalizes it to an ndarray, and
MDAnalysis's writer compares frames == 'all' in a scalar conditional.

## How

Ten guards with multiframe=0, 1, 'no', None and [] fail before the repair:
a patched external writer is reached instead of an ArgumentError. The existing
destination must remain byte-identical for these rejected inputs.
A positive direct two-structure control fails separately with the NumPy ambiguous
truth-value error. Three other positive controls execute.

The owning repair registers the boolean value contract and converts validated
structure-index arrays to the list accepted by the external API. None and 'all'
retain their existing backend meanings. The public signature, default and valid
single-/multiple-structure behavior do not change. The named external argument
multiframe is retained; MolSysMT documentation describes structures.

## Why

An unvalidated writer option can produce unintended output or reach a side-effect
boundary. The direct converter must accept the same normalized indices it asks
ArgDigest to produce. Neither warning suppression nor weakening digestion fixes
that boundary. No scientific algorithm, unit conversion, dependency floor or
Ackredit calculation boundary is introduced here.

## Acceptance criteria

- Direct/public conversion rejects nonboolean flags before invoking the writer
  or changing an existing destination.
- True writes two selected MODEL structures; False writes one explicitly selected
  structure, with the expected literal coordinates and atom records.
- Actual direct/public selected-index calls execute without the ndarray truth error.
- #181 executes the declared MDAnalysis routes without missing-digester notices.

## Verification

Primary guard: tests/form/MDAnalysis_Universe/test_pdb_multiframe.py.
The final combined regression passes 379 tests, zero failures/skips, in 34.31
seconds with twelve workers and Pytest Receptor. It includes all fourteen mirrored
MDAnalysis guards, the entire conversion-truth suite and argument contracts.
All 27 warnings are legacy H5MSM notices. The fourteen fast gates and
whole-checkout Ruff lint/format checks pass. The
[receipt](../../../devtools/data/conversion_execution_mdanalysis_20261023.json)
records the exact command, versions and tested source hashes. The larger conversion
execution profile is tracked separately by #181; it is reachability evidence,
not certification of every converted molecular attribute.

The converter docstring and User Guide state the boolean option and selected
structure behavior. The conversion tutorial and Common Core Module 1 execute
successfully (59.5 and 11.9 seconds). The combined converter/composition
doctest selection passes one executable example; the converter itself has no
doctest example. Public docstring validation passes 250 functions and the
parent-signature comparison has zero unauthorized drifts.
