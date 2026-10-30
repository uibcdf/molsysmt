---
summary: Pandas 3.1 native composition and fixture compatibility blocks source qualification
issue: uibcdf/molsysmt#526
status: open
opened: 2026-10-30
closed:
severity: medium
verification: reproduced
area: [form, tests, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# Pandas 3.1 source-qualification failures

What — Six native/composition tests fail on Pandas 3.1.0 in the exact-source
chemical-domain candidate. This blocks the complete source matrix for #255.
No new numerical or interaction-profile discrepancy is demonstrated by this run.

How — Run `ci-full.yaml` on MolSysMT
`9fb77c3583b44dda31c0466348369de137301df9` with Viewer
`ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352`. The inspected Linux/Python 3.13
[job](https://github.com/uibcdf/molsysmt/actions/runs/41141703873/job/124357390441)
installs `pandas-3.1.0-np2py313h4900a6c_0` and returns **23,624 passed / 6 failed /
102 skipped / 40 deselected**, exit 1, 2081.10 seconds. The separate registered
scientific execution passes 79/79 with no skips in each of the eight platform/
Python cells; that narrow success does not clear these full-suite failures.

Why — Copy-on-Write/read-only NumPy views, inferred column-index dtypes and the
deprecated `copy` keyword expose contracts that local Pandas 2.3.3 did not test.
Distinguish fixture construction assumptions from actual library requirements;
do not suppress warnings, disable dtype assertions or cap Pandas speculatively.

## Reproduced cases

- `tests/native/test_chemical_state_storage.py::test_incomplete_graph_restricts_declarations_without_inventing_a_partition`
  (`partial`, `unavailable`): DataFrame column-index dtype differs (StringDtype
  versus object). Establish the intended canonical schema before changing a
  constructor or oracle.
- `tests/form/molsysmt_Topology/test_composition_pandas_compatibility.py::test_composition_preserves_values_without_copy_deprecations`
  (`add`, `merge`): the warning guard catches deprecated `copy` arguments from
  `molsysmt/native/_chemical_merge.py:86`. Preserve composition independence,
  scientific fields and bounded allocation when modernizing the call.
- `tests/native/test_chemical_component_assignments.py::test_unknown_membership_cannot_project_a_label_to_another_row`
  and `tests/native/test_chemical_state_queries.py::test_empty_declared_components_and_unknown_membership_remain_distinct`:
  fixture writes target a read-only NumPy view. Construct the intended stored
  counterexample explicitly; copying a view without storing the modified data
  would silently stop testing the unknown-membership condition.

## Scope and acceptance

Run these cases on both existing Pandas 2.3.3 and the controlled current-Pandas
lane. Preserve nonaliasing, unknown versus known-empty components, nullable fields
and numerical/state behavior. Keep all assertions that protect those semantics.
Reexecute the final exact-source gate after correction. Record old failed runs,
actual environments and remaining optional skips separately from passing scopes.
Do not mutate the shared development environment merely to make versions match.

The earlier old-package/strict-Viewer-doc Pandas warning observation was delivered
as context in the runtime-floor review #524. This issue owns the concrete new
source defect; #524 continues to own version-floor governance. Source fixes do
not retroactively qualify public MolSysMT 0.23.0 or an installed 1.0 artifact.

Record — devguide/pending_bugs/pandas_3_1_native_composition_and_fixture_compatibility_blocks_source_qualificat.md
