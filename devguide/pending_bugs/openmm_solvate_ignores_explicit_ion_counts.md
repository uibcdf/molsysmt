---
summary: OpenMM solvate silently ignores explicit n_anions and n_cations.
issue: uibcdf/molsysmt#575
status: open
opened: 2026-11-05
closed:
severity: high
verification: reproduced
area: [build, solvate, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# OpenMM solvate silently ignores explicit n_anions and n_cations

**Status:** open; reported from native reproductions during addon receiving.

## What

`build.solvate(..., engine="OpenMM", n_anions=2, n_cations=2, ionic_strength="0 molar")` accepts explicit counts but returns zero ions for the checked neutral solute. It neither applies the requested counts nor rejects them as unsupported.

This is reproduced without Viewer while receiving #421 / PR #543 and uibcdf/molsysviewer#264. Explicit-count support must be implemented or rejected explicitly; successful return must not imply that ignored scientific parameters were applied.

## How

Native source `ccff2557f576f004461c96950d36a8b6e465e91f`, Linux/Python 3.14.7, OpenMM 8.6.1, NumPy 2.4.6 and pandas 2.3.3:

```python
import molsysmt as msm

molsys = msm.build.add_missing_terminal_cappings(
    msm.build.build_peptide("AlaValPro")
)
solvated = msm.build.solvate(
    molsys, engine="OpenMM",
    box_shape="cubic", clearance="0.35 nm",
    anion="Cl-", n_anions=2,
    cation="Na+", n_cations=2,
    ionic_strength="0 molar",
)
print(msm.get(solvated, n_ions=True))
# 0
```

The default-count control also returns zero ions; the explicitly capped source is neutral and remains unchanged.

A second independent control uses bundled pentalanine structure 0. Explicitly assigning numeric atom/group labels isolates the separate ID-conversion defect: default counts and requested 2/2 both produce **914 atoms, 284 waters and zero ions**, with cubic edge **2.19531297293865 nm**.

Inspection: all OpenMM `modeller.addSolvent` branches forward `ionicStrength`, `positiveIon` and `negativeIon`, but never consume `n_anions` or `n_cations`. These parameters are present in the public signature and are used by a different native-engine branch. This report does not claim that PDBFixer or every engine was executed.

## Why

The returned molecular composition can disagree silently with an explicit preparation request. Downstream simulation and visualization users need to know which parameters were applied. The addon forwards the values unchanged and must not introduce a second ion-placement algorithm to compensate.

## Acceptance criteria

- Declare the supported per-engine contract for explicit counts, neutralization and nonzero ionic strength, including precedence or incompatibility of those controls.
- Apply supported explicit counts and verify actual ion species/populations, or reject unsupported combinations before solvent construction with an actionable diagnostic.
- Add native pytest cases for zero, positive, mixed and invalid counts, neutral/charged solutes, neutralization, ionic-strength combinations, admitted box geometries and equivalent units. Assert source ownership, actual composition and charge under the declared contract.
- Preserve ordinary supported default/ionic-strength behavior; do not mark the fix complete merely by changing the addon test expectation.

Evidence: PR #543 commit `6a14ac271d593d961d369acd5aafe35530e49982`, `test_explicit_openmm_counts_are_forwarded_without_hidden_compensation` in `tests/molsysviewer_molsysmt/test_solvation_tools.py`, and `devtools/data/molsysviewer_tools_solvation_receiving_20261105.json`. The current consumer test documents the limitation, not a successful implementation of explicit counts.

Record to accompany the report through PR #543: `devguide/pending_bugs/openmm_solvate_ignores_explicit_ion_counts.md`.


## Scope and evidence

The recorded native source and existing receiving environment are explicit above.
The earlier receiving receipts remain immutable; filing does not certify a repair,
change an API, or qualify a package. No new numerical measurement is asserted in
this documentation-only handoff. Native scientific correction belongs to MolSysMT.

## What was refuted

The failure is reproduced by direct MolSysMT calls without a Viewer instance.
The consumer facade is not its cause and does not repair it. Other engines,
force fields and broader preparation protocols are outside the executed scope.
