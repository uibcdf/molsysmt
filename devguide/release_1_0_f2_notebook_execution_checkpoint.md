# F2 Notebook-Execution Checkpoint

**Date:** 2026-07-28  
**Stage:** F2 — applicable Common Core and changed-behavior notebook execution  
**Status:** `READY TO LAND`; exact-commit rerun pending
**Base commit:** `2340d1eff`
**Repository mutation during execution:** source, tests, and notebook corrections
remain uncommitted

## Scope

F2 covers the complete 20-notebook Common Core plus every Path notebook affected
by the current API and behaviour changes. Comparing the course at the F1
migration commit `f5d96218b` with the current tree identifies 20 changed
notebooks. Their union with the Common Core contains **37 notebooks**: 20 Common
Core notebooks and 17 additional Path notebooks.

Earlier evidence that five lifecycle notebooks executed belongs only to the
MolSysBuilder vertical and does not prove this union. Stored notebook output is
not accepted as execution evidence.

## Method

The audit loaded notebooks with `nbformat` and executed them in memory through
`nbclient.NotebookClient`, using:

- a fresh Python kernel for every notebook;
- each notebook's directory as its working directory;
- a 90-second cell timeout;
- the active MolSysMT Python 3.13 development environment;
- no persistence of executed cells or outputs back into the repository.

The first lane comprised 26 deterministic notebooks. The second lane comprised
11 notebooks previously deferred for network access, viewer interaction, or
both. Permission was required to start local Jupyter kernels and perform the PDB
downloads used by the lessons.

Interactive lessons were executed through their explicit headless path. In
particular, Common Core 06 verifies viewer construction and the absence/presence
contract for the last selection event, but this run does not claim to simulate a
human click in the widget.

## Final Execution Result

- deterministic lane: **26 passed, 0 failed**;
- network/headless lane: **11 passed, 0 failed**;
- complete F2 union: **37 passed, 0 failed**.

This result is evidence for the current uncommitted tree based on
`2340d1eff`. F2 must not be marked formally `DONE` until these changes are
landed and the 37-notebook selection is rerun at the resulting exact commit.

## Corrections Made

### Library defects

- scalar `chain_id` values now broadcast through the public `set()` contract;
- `compare()` handles absent bonded-pair arrays as empty connectivity instead of
  raising an axis error;
- `merge()` only forwards `keep_ids` to adapters that accept it;
- extraction from composite topology/trajectory inputs materializes a native
  `MolSys` before native extraction;
- composite conversion reconciles structure-to-chemical-state association and
  replaces structure-aligned series atomically;
- mixed topological and structural `get()` requests work when the selected pipe
  produces a native `Structures` object;
- BCIF and compressed BCIF now declare the already implemented
  `bonded_atom_pairs` and `inner_bonded_atom_pairs` capabilities, so the public
  `get()` API calls their tested getters.

Every corrected public behaviour has focused regression coverage.

The current worktree validation records:

- 142 focused regressions passing under `pytest-receptor` with `-n 12`;
- the four composite-conversion regressions passing again after the final
  defensive adjustment;
- Ruff passing for `molsysmt` and `tests`;
- valid JSON for every changed notebook;
- developer-guide and Four Paths validators passing;
- the fast release gate passing 12/12;
- `git diff --check` passing.

### Course contract corrections

- native-form examples use supported conversion targets and access patterns;
- iterator examples use `structure` terminology and the current `chunk`
  contract;
- trajectory lessons use existing manifest keys, valid structure ranges, and
  the public `concatenate_structures()` location;
- partial topology/trajectory lessons request coordinates explicitly;
- covalent-connectivity examples materialize native topology where appropriate
  and use the binary selection expression
  `all bonded to atom_index==10`;
- PDB Frontier uses a structure with confirmed alternate locations and passes
  PDB text through the PDB handler;
- interactive selection has an explicit, informative headless branch rather
  than assuming a click occurred.

### User Guide synchronization

The `extract`, `merge`, and `set` User Guide notebooks were updated and each
executed successfully in a clean kernel. They describe composite extraction,
structure terminology, and scalar-label broadcasting respectively.

## Separately Recorded Debt

The course uses explicit attributes for trajectory iteration. A separate public
contract remains defective: constructing `Iterator` without explicit attributes
can fail for coordinate-only and topology-plus-trajectory inputs. It is recorded
with reproductions and acceptance criteria in
`pending_bugs/iterator_without_explicit_attributes_fails_for_partial_forms.md`.
It does not invalidate the F2 notebook result and must not be hidden by it.

## Closure Gate

To change F2 from `READY TO LAND` to `DONE`:

1. run focused pytest coverage and repository validators;
2. inspect the complete diff and land the bounded F2 change;
3. rerun all 37 notebooks from clean kernels at the exact resulting commit;
4. record the commit, environment, command/runner, and 37/37 result here;
5. update `release_1_0_status.md` and advance to F3.

No additional notebook-design work is known to be required for F2.
