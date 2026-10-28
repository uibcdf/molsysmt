---
summary: Scheduled full Linux CI repeats seven unresolved failures across supported Python minors.
issue: uibcdf/molsysmt#515
status: open
opened: 2026-10-28
closed:
severity: medium
verification: upstream
area: [ci, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Triage repeated full-suite failures

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
