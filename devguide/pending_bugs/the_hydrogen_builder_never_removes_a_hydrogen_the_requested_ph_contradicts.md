---
summary: The hydrogen builder never removes a hydrogen the requested pH contradicts.
issue: uibcdf/molsysmt#178
status: open
opened: 2026-08-19
closed:
severity: medium
verification: measured
area: [build, scientific-integrity]
guard:
normative:
blocked_by: []
supersedes: []
---

# Preparation adds hydrogens but never takes any away

**Reported:** 2026-08-19, split off from
[`uibcdf/molsysmt#176`](https://github.com/uibcdf/molsysmt/issues/176), which fixed the
protonation rules and could not fix this.
**Status:** open. It is a contract question, not a threshold one.

## What

`add_missing_hydrogens` and `add_missing_terminal_cappings` only add. A hydrogen already
present that the requested pH contradicts is passed through, so the returned system
states a protonation the caller did not ask for.

```python
import molsysmt as msm
mol = msm.convert(msm.systems['chicken villin HP35']['1vii.pdb'], to_form='molsysmt.MolSys')
mol = msm.build.add_missing_terminal_cappings(mol, pH=12.0, engine='MolSysMT')
mol = msm.build.add_missing_hydrogens(mol, pH=12.0, engine='MolSysMT')
# N-terminus is still H1, H2, H3 — a charged NH3+ at pH 12
```

## How

`molsysmt/build/add_missing_hydrogens.py:339`:

```python
missing_hs = [h for h in expected_hs if h not in present_hs]
```

There is no branch for the other direction. `expected_hs` is correct — the rules added
in #176 are unit-tested and give `H1`, `H2` without `H3` at pH 12 — but nothing consults
the difference the other way round.

## Why

The rules cannot act on what is already there, and what is already there is common:
1VII carries 301 hydrogens of 596 atoms and 1L2Y 150 of 304. Both are NMR structures,
and both arrive with `H3` on the N-terminal amine.

**This one is silent, which is what separates it from the half that was fixed.** The
C-terminal defect in #176 produced a visible failure, because a COOH terminus has no
force-field template and `createSystem` refused it. NH3+ has a template everywhere, so
an over-protonated amine reaches a simulation at the wrong formal charge with nothing
raised anywhere.

## What is measured and what is assumed

Measured: hydrogen counts in the two shipped systems, and the N-terminal atom names
after preparation at pH 12.0 with both build steps.

Measured: `get_expected_hydrogens('MET', present_atom_names=heavy + ['H1', 'H2'],
pH=12.0, is_n_terminal=True)` omits `H3`, and includes it at pH 7.4. The rule is right;
the application is one-directional.

Assumed, not checked: that the same asymmetry affects the side chains — an input
carrying `HD2` on an aspartate at pH 7.4 should be equally untouched. It follows from
the same line, but was not run.

## What was refuted

**That #176 could resolve this by fixing the rules.** It could not, and the belief that
it had rested on a wrong measurement: the #176 report stated that 1VII arrives with
all-heavy atoms. It does not. Both halves of #176 were implemented before the hydrogen
count was checked.

## Scope and exclusions

Covers `engine='MolSysMT'`.

Excluded, deliberately: what the fix should be. A function that removes hydrogens is not
described by the name `add_missing_hydrogens`, so the question is where removal belongs
and under which argument — a new function, an argument on the existing one, or a
separate reconciliation step. That is an API decision.

Also excluded: `engine='OpenMM'` and `engine='PDBFixer'`, unmeasured here.

## Acceptance criteria

- A caller who asks for pH 12 on a structure carrying `H3` receives a system whose
  N-terminus is neutral, or an explicit refusal — but not silence.
- Whatever the mechanism, it is discoverable from the API rather than only from the
  developer guide.
- A guard covering both directions: a hydrogen that must be added, and one that must be
  removed, at the same pH.

## Provenance

Linux 7.0.0-28-generic, Python 3.13.14, MolSysMT at `d77786517`, 2026-08-19. Systems
`chicken villin HP35` (`1vii.pdb`) and `Trp-Cage` (`1l2y.pdb`) from `molsysmt.systems`.
