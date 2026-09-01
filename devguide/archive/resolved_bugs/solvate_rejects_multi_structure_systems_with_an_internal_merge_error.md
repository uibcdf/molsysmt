---
summary: solvate rejects multi-structure systems with an internal merge error.
issue: uibcdf/molsysmt#184
status: resolved
opened: 2026-08-19
closed: 2026-09-01
severity: medium
verification: reproduced
area: [build]
guard: tests/build/solvate/test_solvate_engine_MolSysMT.py::test_solvate_rejects_multiple_structures_before_engine_work
normative:
blocked_by: []
supersedes: []
---

# Bug: `build.solvate` fails on any system with more than one structure

**Reported:** 2026-08-19, during an external audit, on the first bundled system tried.
**Status:** resolved on 2026-09-01. `solvate()` now rejects a multi-structure input
before dispatching to any engine and explains how to select one structure.

## What

`msm.build.solvate` raises on any molecular system carrying more than one structure. The
failure surfaces from the internal merge, names an internal caller, and describes the
symptom rather than the precondition:

```bash
$ python -c "
import molsysmt as msm
mol = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'], to_form='molsysmt.MolSys')
print(msm.get(mol, n_structures=True))
msm.build.solvate(mol, box_shape='cubic', clearance='10 angstroms', engine='MolSysMT')"
38
molsysmt._private.smonitor.exceptions.StructuralInconsistencyError: Structural
inconsistency detected: Inconsistent number of structures: 38 vs 1. Ensure that the
atoms, residues, or frames match between the systems being compared or merged.
```

Selecting a single structure first succeeds in 2.2 s:

```bash
$ python -c "
import molsysmt as msm
mol = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'], to_form='molsysmt.MolSys', structure_indices=[0])
out = msm.build.solvate(mol, box_shape='cubic', clearance='10 angstroms',
                        water_model='TIP3P', ionic_strength='0.15 molar', engine='MolSysMT')
print(msm.get(out, n_atoms=True, n_waters=True))"
[7678, 2453]
```

## How

`molsysmt/build/solvate.py:630` merges the solute with a single-structure water block:

```python
solvated = merge([solute, all_water], skip_digestion=True)
```

`molsysmt/form/molsysmt_Structures/merge.py:89` requires every merged item to carry the
same number of structures and raises when they disagree. The water block is built once,
so the counts can only agree when the solute has exactly one structure.

Nothing upstream states the precondition. The digestion layer does not check it, and the
docstring's `Raises` section names only `NotImplementedError` for an unsupported engine
or water model. The number 38 in the message is the user's; the 1 is an internal
construction detail they have no way to interpret.

## Why

**It is the first thing an evaluator tries.** `1l2y` is the bundled Trp-Cage entry and a
38-model NMR ensemble, so a reader following the preparation examples with a bundled
system meets this immediately. The same holds for any PDB entry solved by NMR and for any
system loaded from a trajectory.

**The error teaches the wrong thing.** It reads as a defect in the user's system —
mismatched atoms or frames between two things they merged — when the user merged nothing.
A reader who trusts it will look for corruption in an ensemble that is fine.

**The workaround is invisible.** `structure_indices=[0]` is correct, cheap, and nowhere
suggested.

Severity is `medium`: no incorrect result is produced, a one-argument workaround exists,
and `build` is classified `experimental` in
`devtools/data/public_api_stability.json`, so the 1.x contract is not at stake.

## What is measured and what is assumed

Measured: the failure and its message on `1l2y.h5msm` with 38 structures under both
`engine='MolSysMT'` and the default `engine='OpenMM'`; the success and 2.2 s runtime with
`structure_indices=[0]`; the two source locations.

Assumed — *estimate*: that solvating each structure independently is the behaviour a user
would expect from a multi-structure input. It is not obviously right. An NMR ensemble
solvated per model yields 38 different water counts and 38 different boxes, which is a
different object from what most callers want, and the honest outcome may be a clear
refusal rather than a loop.

## What was refuted

*The failure is specific to the MolSysMT engine.* It is not; the default `OpenMM` engine
fails identically, at the same merge.

*`merge` is at fault.* It is not. Refusing to merge a 38-structure item with a
1-structure item is the documented contract of `molsysmt.Structures.merge`. The defect is
that `solvate` reaches it with operands it constructed itself.

## Scope and exclusions

Covers `build.solvate` and the precondition it does not declare.

Excludes the other `build` entry points until each is checked: `make_water_box`,
`remove_overlapping_molecules`, and `add_missing_hydrogens` were not exercised with
multi-structure input in this audit, and assuming they share the defect without measuring
it would put an unverified claim in the queue.

Excludes the question of what solvating an ensemble *should* mean, unless the resolution
chooses the loop. If it chooses refusal, that decision belongs here; if it chooses the
loop, it is a feature and belongs in a proposal.

## Acceptance criteria

1. `msm.build.solvate` on a multi-structure system either solvates every structure or
   raises an `ArgumentError` naming `solvate`, the structure count, and
   `structure_indices` as the remedy — before any internal merge is attempted.
2. The docstring states the precondition or the per-structure behaviour, and the `Raises`
   section agrees with the code.
3. A test covers a multi-structure input for both engines and asserts the chosen
   behaviour. This is the `guard`.

## Provenance

Reproduced 2026-08-19 on Linux 7.0.0-28-generic x86_64, Python 3.13.14, MolSysMT
`0.21.0+325.g7cedab74a` at repository commit `b9a2098e4`, OpenMM available in the
environment.

## Resolution

`solvate()` now reads the public structure count before engine dispatch. Inputs with
more than one structure raise `ArgumentError` naming `solvate()`, the observed count,
and `structure_indices` as the remedy. This deliberately refuses to invent
per-structure solvent topologies: independently solvated frames may differ in box,
water count, ion count and consequently atom axis.

The guard uses the original 38-structure Trp-Cage ensemble and verifies the same public
error for the MolSysMT, OpenMM and PDBFixer engines. The validated branch precedes all
three engine branches, so rejection occurs before engine-specific construction work.
The API docstring, User Guide solvation tutorial and Module 25 of all four course paths
now state the single-structure precondition and the explicit selection remedy.
