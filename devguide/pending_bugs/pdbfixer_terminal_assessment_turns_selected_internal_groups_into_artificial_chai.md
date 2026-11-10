---
summary: PDBFixer terminal assessment turns selected internal groups into artificial chain ends
issue: uibcdf/molsysmt#689
status: active
opened: 2026-11-10
closed:
severity: high
verification: reproduced
area: [build, selection]
guard:
normative:
blocked_by: []
supersedes: []
---

# PDBFixer terminal assessment turns selected internal groups into artificial chain ends

## What

On unchanged source c25c517a5, the public group-scoped assessment of the internal
Val group of `build_peptide('AlaValPro', engine='MolSysMT')` returns
`{1: ['OXT']}` rather than `{}` with `engine='PDBFixer'`. Both numeric `[1]`
and `selection='group_index==1'` reproduce it. `selection='resid 1',
syntax='MDTraj'` instead fails because an internal selection uses MolSysMT syntax.

## How

`build/get_missing_terminal_cappings.py` extracts the requested selection before
calling PDBFixer's missing-terminal detection. An internal selected group becomes
the last group of that temporary chain. The earlier source-group selection also
omits the supplied `syntax`. This is independent of the repaired native graph
recognizer (#686) and native numeric-axis contract (#679).

## Why

The read-only preparation report invents a terminal deficiency from an analysis
selection. A user or later workflow could consequently repair a nonexistent
chemical end. Group selections must filter a full-context assessment rather than
change its molecular meaning. The measured defect is a report, not a claimed
corrupt-coordinate run.

## What is measured and what is assumed

The four-case initial guard yields three failures and one pass: two artificial
termini, one lost-syntax error, and the genuine C-terminal source-index control.
One CPU/2 GiB, existing Python 3.14.7 development environment, unchanged backend,
PDBFixer/OpenMM and published PyUnitWizard 0.28.1 overlay. Original failures are
retained in the receiving artifacts; this is source evidence, not installed or
release qualification.

## What was refuted

The group selection is valid and the same peptide's actual C-terminal group
remains source index 2. No source relabelling or backbone modification is needed
to trigger the error. This is not a defect in PDBFixer's independent chemistry:
the consumer supplies a truncated system and omits the query syntax.

## Scope and exclusions

Resolve source group scope using the supplied syntax, retain full molecular
context for the optional detector, then filter its result onto source groups.
Preserve the source and typed empty scope. Do not change PDBFixer's scientific
algorithm, native endpoint criteria or the distinct atom scope of terminal
addition. Full-context conversion costs remain those of this optional adapter;
no sparse or streaming chemistry claim is introduced.

## Acceptance criteria

Internal selections produce no artificial ends; genuine termini retain source
group indices; native and MDTraj queries and numeric group selections agree.
Empty selection avoids constructing the detector, and a supplied PDBFixer object
retains its existing attributes. The whole affected terminal suite, public
validation and documentation must remain accurate.

## Implementation receiving — 2026-11-10

The full-source optional-detector route and supplied-syntax filter pass 92
affected native/PDBFixer assessment, terminal addition and chemical endpoint
cases, without failures or skips. The first six-case attempt exposed a fixture
assumption about an uninitialized optional-detector attribute; it remains
recorded, and the corrected source-preservation guard checks attribute absence.
Original three failures remain preserved. Combined-source, fast/documentation
receiving and public closeout remain pending. Existing tutorial/course code
cells and outputs are unchanged; narrative explains full-source PDBFixer scope.
