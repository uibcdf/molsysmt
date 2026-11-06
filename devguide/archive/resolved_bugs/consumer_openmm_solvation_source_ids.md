---
summary: OpenMM solvate rejects nonnumeric or missing atom IDs.
issue: uibcdf/molsysmt#574
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [build, solvate, molsysviewer]
guard: tests/build/solvate/test_source_identifiers.py::test_source_atom_and_group_ids_are_preserved
normative:
blocked_by: []
supersedes: []
---

# OpenMM solvate rejects nonnumeric or missing atom IDs

**Status:** open; reported from native reproductions during addon receiving.

## What

`build.solvate(..., engine="OpenMM")` fails with a bare `ValueError` when the first atom has a valid nonnumeric ID. IDs are labels, not integer atom indices. Missing IDs in bundled pentalanine reproduce the same failure.

Found independently of Viewer while receiving the expert addon under #421 / PR #543 and uibcdf/molsysviewer#264. No Viewer import is needed.

## How

Reproduced on published native source `ccff2557f576f004461c96950d36a8b6e465e91f` (same solvate implementation as the preceding receiving basis), Linux/Python 3.14.7, OpenMM 8.6.1, NumPy 2.4.6 and pandas 2.3.3:

```python
import molsysmt as msm

molsys = msm.build.add_missing_terminal_cappings(
    msm.build.build_peptide("AlaValPro")
)
msm.set(molsys, element="atom", selection=[0], atom_id="alpha")
msm.build.solvate(
    molsys, engine="OpenMM",
    box_shape="cubic", clearance="0.35 nm",
)
# ValueError: invalid literal for int() with base 10: 'alpha'
```

The explicitly prepared, numeric-ID control solvates successfully. Also reproduced with structure 0 of bundled `traj_pentalanine.h5msm`, whose missing atom IDs lead to `int('None')`.

The failure occurs after solvent construction in `molsysmt/build/solvate.py:503`:

```python
list_atoms = list(modeller.topology.atoms())
atom_id = int(list_atoms[0].id)
```

The following loop renumbers atoms from this value. The analogous group/residue-ID conversion also needs review, but a separate nonnumeric-group reproduction is not claimed here.

## Why

Valid input labels or absent optional IDs prevent solvation for native users and bound consumers. Requiring the addon to silently rewrite source IDs would weaken correspondence and hide a scientific-provider limitation. The input system remained unchanged in the checked failure path.

## Acceptance criteria

- Support admitted nonnumeric/missing atom labels, or define and validate a narrower input contract before constructing solvent, with a meaningful native diagnostic.
- Define the output ID/mapping policy without conflating labels with indices or silently changing the input.
- Add native pytest controls for numeric, nonconsecutive numeric, nonnumeric and missing IDs; verify successful solvent construction, input ownership and output correspondence.
- Review group-ID handling under the same declared policy and cover admitted cases.
- Keep this separate from explicit ion-count semantics, multi-structure selection and force-field readiness.

Evidence: PR #543 commit `6a14ac271d593d961d369acd5aafe35530e49982`, `test_nonnumeric_identifier_rejection_is_native_and_source_is_preserved` in `tests/molsysviewer_molsysmt/test_solvation_tools.py`, and `devtools/data/molsysviewer_tools_solvation_receiving_20261105.json`. That consumer test currently preserves the limitation; it must be updated when the native repair arrives and is not a passing guard for the requested fix.

Record to accompany the report through PR #543: `devguide/pending_bugs/openmm_solvate_rejects_nonnumeric_atom_ids.md`. No native fix or backend fallback is proposed in the addon.


## Scope and evidence

The recorded native source and existing receiving environment are explicit above.
The earlier receiving receipts remain immutable; filing does not certify a repair,
change an API, or qualify a package. No new numerical measurement is asserted in
this documentation-only handoff. Native scientific correction belongs to MolSysMT.

## What was refuted

The failure is reproduced by direct MolSysMT calls without a Viewer instance.
The consumer facade is not its cause and does not repair it. Other engines,
force fields and broader preparation protocols are outside the executed scope.

## Consumer receiving resolution — 2026-11-05

Native owner source 8c2661293 includes the published repair. Receiving retains
this original consumer reproduction alongside the independent owner's report;
neither is deleted or overwritten. The native guard named above passes within
the 362-case directed receiving gate. Addon selection/ownership boundaries are
kept separate from this native correction. See the paired owner report in this
directory for the scientific implementation and detailed native coverage.
