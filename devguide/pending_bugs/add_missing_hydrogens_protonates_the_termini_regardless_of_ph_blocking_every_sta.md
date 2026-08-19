---
summary: add_missing_hydrogens protonates the termini regardless of pH, blocking every standard force field.
issue: uibcdf/molsysmt#176
status: partial
opened: 2026-08-19
closed:
severity: high
verification: measured
area: [build, scientific-integrity]
blocked_by: []
supersedes: []
guard: tests/build/test_terminal_protonation_follows_ph.py
normative:
---

# The native hydrogen builder ignores pH at both termini

**Reported:** 2026-08-19, while verifying the README's structure-preparation example
after [`uibcdf/molsysmt#175`](https://github.com/uibcdf/molsysmt/issues/175) unblocked
it. The example got as far as `openmm.Simulation` and stopped there.
**Status:** partial. The C-terminal half is fixed and guarded. The N-terminal rule is
in place and unit-tested, but cannot correct a structure that arrives over-protonated,
because neither function removes a hydrogen. That remainder is stated under *Scope*.

## What

`build.add_missing_hydrogens(engine='MolSysMT')` places `HXT` on the C-terminal
carboxylate at every pH. A protonated C-terminus (COOH) has no residue template in
AMBER or CHARMM, so the prepared system cannot be simulated.

```python
import molsysmt as msm
mol = msm.convert(msm.systems['chicken villin HP35']['1vii.pdb'], to_form='molsysmt.MolSys')
mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')
mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')
msm.convert(mol, to_form='openmm.Simulation', forcefield='AMBER14')
```

```
ValueError: No template found for residue 35 (PHE).  The set of heavy atoms matches
NTYR, but the residue is missing 1 H atom.
```

The message misleads twice — it names an N-terminal tyrosine template for a C-terminal
phenylalanine, and it reports a *missing* hydrogen where the problem is an extra one.
Removing that single atom makes the identical call succeed:

```python
mol = msm.remove(mol, selection="atom_name=='HXT'")
msm.convert(mol, to_form='openmm.Simulation', forcefield='AMBER14')   # Simulation
```

## How

`molsysmt/element/group/amino_acid/get_expected_hydrogens.py:127-134`:

```python
if present_atom_names is not None:
    present_heavy_for_oxt = {a for a in present_atom_names if not _is_hydrogen(a)}
    if 'OXT' not in present_heavy_for_oxt:
        remove_hs.update(h for h in all_hs_set if h in ('HXT',))
elif not is_c_terminal:
    remove_hs.update(h for h in all_hs_set if h in ('HXT',))
```

`HXT` is removed only when `OXT` is **absent**. `OXT` is present on any well-formed
C-terminus — including one `add_missing_terminal_cappings` has just built — so the
proton is kept.

The rule is answering a different question from the one that matters. It asks *does
this residue have a terminal oxygen at all*, which is a topology question, and never
asks *should that oxygen carry a proton at this pH*, which is the chemistry question.
Both are needed; only the first is asked.

Directly above it is the pH rule table that does ask the second question:

| residue | rule |
|---|---|
| ASP | remove `HD2` at pH ≥ 4.4 |
| GLU | remove `HE2` at pH ≥ 4.4 |
| HIS | remove `HD1` at pH ≥ 6.5 |
| LYS | remove `HZ3` at pH ≥ 10.5 |

The C-terminal carboxylate has no entry, although with pKa ≈ 2–3 it is the most
reliably deprotonated of the set at physiological pH — more so than the ASP and GLU
side chains that are handled.

## Why

Two failures, and the quiet one is worse.

**Loudly:** no natively prepared protein reaches a force field. `build → solvate →
openmm.Simulation` is the workflow the README leads with, and it terminates here for
every protein with a free C-terminus.

**Quietly:** the returned system states a protonation that is wrong at the pH the caller
asked for. A caller who does not route through OpenMM — computing charges, writing a
PDB, feeding another tool — receives no error at all. The function's contract is to
protonate *according to the provided pH*, and for the termini it does not.

The N-terminus is equally pH-blind. It carries `H1`/`H2`/`H3` at pH 12, where pKa ≈ 9.6
leaves a neutral amine. It never raises, because NH3+ has a template in every force
field, so it will not be found by the failure that found this one.

## What is measured and what is assumed

Measured, on `1VII` after `add_missing_terminal_cappings`, varying only pH:

| pH | `HXT` | N-terminal hydrogens |
|---|---|---|
| 1.0 | 1 | `H1`, `H2`, `H3` |
| 4.0 | 1 | `H1`, `H2`, `H3` |
| 7.4 | 1 | `H1`, `H2`, `H3` |
| 12.0 | 1 | `H1`, `H2`, `H3` |

Identical at every pH, so neither terminus consults it.

Measured: removing the one `HXT` is sufficient for `createSystem` to succeed on 1VII —
the C-terminus is the only blocker there, not one of several.

Measured: the same failure on `1L2Y`, residue 19 SER, *"similar to CTHR, but is missing
1 H atom and 1 C atom"*.

Assumed, not checked: that `engine='OpenMM'` and `engine='PDBFixer'` handle both termini
correctly. They delegate to `Modeller.addHydrogens(pH=...)` and
`PDBFixer.addMissingHydrogens(pH=...)`, which is why they are offered as the workaround,
but neither was run for this report.

Assumed, not checked: the pKa values quoted are textbook figures for free amino acids,
not measured here. They set the direction of the rule, not its threshold; choosing the
threshold is part of the fix.

## What was refuted

**That `add_missing_terminal_cappings` was at fault.** It was the first suspect, since
the traceback names a terminal residue and the capping step runs just before. It is not:
`get_missing_terminal_cappings` reports `{}` for 1VII, the capping step adds nothing,
and the C-terminal residue afterwards holds a correct `OXT`. The extra atom appears in
the *next* step. This is worth recording because the failure points at the wrong
function twice — once through OpenMM's message, once through the call order.

**That this was a consequence of #175.** It is not, and it predates that fix: the same
`No template found` failure appeared on 1L2Y at the very start of the audit, before any
change. #175 merely unblocked the pipeline far enough to reach it.

## Scope and exclusions

Covers `engine='MolSysMT'` in `add_missing_hydrogens`, and the terminal rules in
`get_expected_hydrogens`.

Not covered:

- The side-chain rules, which are present and were not evaluated for correctness here.
  Only the *absence* of terminal entries is claimed.
- `engine='OpenMM'` and `engine='PDBFixer'`.
- OpenMM's misleading diagnostic. Upstream, and it would have cost nothing here had the
  atom list been inspected first.
- Whether the pH thresholds used by the existing side-chain rules are right.

## Acceptance criteria

- The C-terminal carboxylate is deprotonated above its pKa threshold and protonated
  below it, rather than tracking the presence of `OXT`.
- The N-terminal amine is neutral above its threshold and charged below it.
- `1VII` and `1L2Y` complete `build → solvate → openmm.Simulation` with `AMBER14` at
  pH 7.4 without hand-editing.
- A guard that asserts terminal protonation across a pH range, not only at 7.4 — a test
  fixed at one pH would pass on a rule that ignores pH entirely, which is the defect.
- The guard asserts on the atom list, not only on `createSystem` succeeding, so the
  N-terminal half is covered too. It has a template either way and would otherwise go
  untested.

## Dependencies and risks

Changing terminal protonation changes the total charge of every natively prepared
system, and therefore the counter-ion count `solvate` computes for a target ionic
strength. Any stored reference system built through this path shifts by one proton per
terminus.

## Provenance

Linux 7.0.0-28-generic, Python 3.13.14, OpenMM as packaged in
`molsyssuite@uibcdf_3.13`, MolSysMT `0.21.0+325.g7cedab74a` at `ef4d13db1`, 2026-08-19.
Systems `chicken villin HP35` (`1vii.pdb`) and `Trp-Cage` (`1l2y.pdb`) from
`molsysmt.systems`.

## Resolution, and one correction to this report

**Corrected.** This document claimed 1VII arrives with all-heavy atoms. It does not:
1VII is an NMR structure carrying 301 hydrogens of 596 atoms, and 1L2Y carries 150 of
304. The count was assumed from a `n_atoms` figure and never checked. It matters,
because it changes what the N-terminal half of the fix can do.

**C-terminus — fixed.** `get_expected_hydrogens` now removes `HXT`/`HO2` at pH >= 3.2.
The existing OXT rule stays: it asks whether the terminal oxygen exists, which is a
topology question, and the new one asks whether it should carry a proton, which is the
chemistry question. Both are needed and they compose, since the rules only add to
`remove_hs`.

Measured on 1VII: `HXT` present at pH 1.0, 2.0, 3.0 and absent at 4.0, 7.4, 9.0, 12.0.
The full `build -> solvate -> openmm.Simulation` path completes with AMBER14 at pH 7.4.

**N-terminus — rule added, effect bounded.** The third proton is not placed by
`add_missing_hydrogens` at all; it is placed by `add_missing_terminal_cappings`, step
A3, which chose between NH3+ and NH2 without consulting the `pH` it already accepts and
already documents as governing protonation states. That step is now pH-aware, and
`get_expected_hydrogens` carries the matching rule for the path where the variant does
include `H3`.

Both are correct and unit-tested: for a residue with `H1`/`H2` and no `H3`, the third
proton is expected at pH 7.4 and not at pH 12.0. Neither can help 1VII or 1L2Y, whose
`H3` is in the deposited file. **Neither function removes a hydrogen**, which is the
remaining gap and is not a threshold question.

**Not resolved, and why this stays `partial`:** a structure that arrives protonated in a
way the requested pH contradicts is passed through unchanged. Making
`add_missing_hydrogens` remove hydrogens changes its contract and its name stops
describing it, so it is a separate decision rather than an extension of this fix.

**The pH model is unchanged and remains an approximation.** Fixed thresholds from
free-amino-acid pKa values, as `structure_preparation_pipeline.md` already stated for
all three engines. What changed is that the statement is now also in the public
docstring of `add_missing_hydrogens`, with the consequence spelled out — a buried or
electrostatically shifted residue can titrate more than a pH unit from its threshold —
and that the docstring says the function only adds. Deferring PROPKA-style
environment-dependent pKa is a schedule decision; leaving it undisclosed to callers was
not, and that part is now closed.
