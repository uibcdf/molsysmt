---
summary: Scheduled full Linux CI repeats seven unresolved failures across supported Python minors.
issue: uibcdf/molsysmt#515
status: resolved
opened: 2026-10-28
closed: 2026-11-03
severity: medium
verification: measured
area: [ci, tests]
guard: tests/form/molsysmt_TopologyDict/test_direct_queries.py
normative:
blocked_by: []
supersedes: []
---

# Triage repeated full-suite failures

**Status:** resolved by the #255 source corrections and complete qualification;
the 2026-11-03 audit below verifies every originally failing node. No new runtime
patch or weakening of assertions is made for this closeout.

## What

Scheduled ci-weekly.yaml run 40693271675 at source
bb808a8b14f15805477f177c5dbfe1b3ea49aff6 fails in all four Linux/Python
3.11–3.14 cells with the same seven tests. Each reports 7 failed, 22,424 passed,
102 skipped and 40 deselected. The macOS/Python 3.14 test job is cancelled.
The independent 79/79 scientific certificate passes; it does not clear the
ordinary-suite failures or qualify an unexecuted/cancelled platform.

## How

[Original run](https://github.com/uibcdf/molsysmt/actions/runs/40693271675).
Published GH Run Receptor reports the official failure and native failed-step
logs identify these reproducible selectors:

- tests/form/test_coordinate_only_atom_indices.py::test_gro_atom_indices_and_count_follow_coordinate_width:
  the fake GRO object lacks n_atoms.
- tests/_private/test_doctest_module_shadowing.py::test_colliding_basic_symbol_inventory_is_complete:
  discovery/expected inventories differ by compose_atom_maps and permute_atoms.
- tests/basic/test_extract_extended.py::test_extract_sequence_rejects_out_of_range_positions_with_a_catalog_error:
  expected diagnostic regex differs from the emitted out-of-range-axis message.
- tests/basic/test_get_form_battery.py::test_the_battery_covers_the_catalogue:
  PDBQTFileHandler has no exercised or explicitly unreachable battery entry.
- tests/form/molsysmt_TopologyDict/test_direct_queries.py::test_hierarchy_counts_still_finalize_missing_parents,
  MolSysDict parameter: received hierarchy counts [0, 0], expected [3, 1].
- tests/form/openff_Molecule/test_get_topological_attributes.py::test_n_molecules:
  received one, expected zero.
- tests/form/openff_Molecule/test_get_topological_attributes.py::test_n_entities:
  received one, expected zero.

These are hosted observations, not seven locally reproduced scientific defects.
No new full matrix is dispatched by this report. Preserve job/source/dependency
identities when reproducing, because local editable parity is a narrower claim.

## Why

The complete stabilization lane is red. Narrow smoke, detector receiving and
scientific certificates must retain their own scope and cannot clear this
backlog. Consumer context: expert-addon receiving under uibcdf/molsysmt#421 and
uibcdf/molsysviewer#264. This report does not change native algorithms or tests.

## What is measured and what is assumed

GitHub concludes four Linux jobs failure and the macOS test job cancelled.
The same seven assertions are visible on all Linux minors. Local root causes,
intended reader hierarchy/diagnostic behavior and fixture validity remain to be
triaged by the owning component. In particular, an old expectation of zero
molecules/entities for a populated OpenFF molecule is not accepted as scientific
truth merely because a test encodes it.

## What was refuted

A passing 79-case scientific certificate, completed evidence-upload job or prior
bounded smoke is not evidence that the full suite passed. This is not an error
introduced by adding the four later expert wrappers: the failing source precedes
them and the selectors are outside those new detector tools.

## Scope and exclusions

Own the failed weekly gate and its contract-based triage. Split independently
owned mechanisms into linked issues when the diagnoses warrant it. Do not
weaken meaningful assertions, remove exercised forms or rewrite original run
conclusions to obtain green CI. No new detector, package or release is needed
merely to file this report.

## Acceptance criteria

Reproduce/classify the cases; reconcile stale fixtures/inventories/assertions
against intended public behavior and fix real defects where independently
established. Preserve addressable guards for the actual mechanisms and obtain
reviewed official full-suite success on the corrected exact source. Keep the
original failed/cancelled evidence and actual optional-provider skips visible.

## Dependencies and risks

MolSysMT owns native reader, form, diagnostic and test semantics. The consumer
cannot resolve a hierarchy or molecule-count contract through an addon wrapper.
No scientific workaround is introduced downstream.

## Resolution audit — 2026-11-03

Correction **7b983af32ac4efcc3adb7c4c0617a38957ecc41e** is included in final #255
source **de7ffad2aef18ff3bccd184133dc69e081cb506e**. The reviewed
[full matrix 41572981893](https://github.com/uibcdf/molsysmt/actions/runs/41572981893)
is officially completed/successful on that exact source and Viewer
ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352. Eight full test jobs and the controlled
Viewer build pass. The PR-only aggregate is skipped on manual dispatch; it is
not a missing test cell.

Fresh downloads of all eight official full-suite artifacts are checked for the
seven exact original test identities, including the MolSysDict parameter of the
hierarchy query. Every target appears exactly once per cell and has no skipped,
failure or error element: **56 original-node executions pass**. This is seven
regressions repeated on eight cells, not 56 new scientific cases. Each Linux
cell has 23,672 passes / 102 skips; each macOS cell has 23,671 passes / 103 skips.
No cell has failures/errors. The separate 40 extended LEaP cases remain outside
the unchanged default selection; no original target is among those exclusions.

| Original mechanism | Reconciled contract and retained guard |
| --- | --- |
| GRO metadata fixture | The real reader assigns `n_atoms` during construction. The fixture now supplies it and forbids `read()`, protecting count/index queries from consuming coordinates. `tests/form/test_coordinate_only_atom_indices.py`. |
| Doctest function/module inventory | Both actual public exports are admitted to the exact callable inventory and exercised by its existing parameterized controls. `tests/_private/test_doctest_module_shadowing.py`. |
| Sequence bounds | The out-of-range request retains ArgumentError and the form-specific diagnostic assertion. The original expectation is not weakened. `tests/basic/test_extract_extended.py`. |
| PDBQT handler discovery | The previously absent handler now has a real file-backed construction route, exercised by the full form battery. `tests/basic/test_get_form_battery.py`. |
| Dictionary hierarchy | The original `[3, 1]` group/chain expectation survives for both TopologyDict and MolSysDict, with three finalized molecule occurrences. `tests/form/molsysmt_TopologyDict/test_direct_queries.py`. |
| OpenFF molecule/entity counters | One connected caffeine molecule has one molecule occurrence and one entity, despite zero groups. The stale zero expectations are corrected; the separate zero-group assertion remains. `tests/form/openff_Molecule/test_get_topological_attributes.py`. |

The hierarchy module named in the front matter guards the original dictionary
failure; the companion guards in the table remain part of the complete suite.
No single narrow guard is claimed to replace that suite.

The retained #255 source record owns complete matrix evidence, warnings and
optional omission reasons. This audit checks the original targets independently
in its JUnit artifacts and preserves their hashes/identities locally. It does
not reclassify the original four failed Linux jobs or cancelled macOS job as
successful. Nor does historical full-matrix success qualify a later source or
an installed package pair.

Current source **13f72af2c9630bf768e03b59e2c973d5c6def4f4** additionally passes
all six affected modules locally: **310 passes**, zero skips/failures, exit 0,
34.60 s and 29 visible warnings. The finalized receptor evidence is complete.
A real bundled 648-atom GRO file also returns the exact count and atom-index
range while `read()` is forbidden and its cursor remains unchanged. Inspecting
only a class attribute would be insufficient: the provider sets this metadata
on the reader instance. No new test double assumption is accepted without
that actual-provider check.

The ignored `.pytest_cache/stabilization-534-535/` receipts retain artifact IDs,
per-cell JUnit hashes and target outcomes, the provider probe and canonical local
test results. No full matrix is dispatched again and no product code is changed
by this audit. Current #534/#535 source CI remains separately tracked.
