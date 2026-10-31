---
summary: Pandas 3.1 native composition and fixture compatibility blocks source qualification
issue: uibcdf/molsysmt#526
status: active
opened: 2026-10-30
closed:
severity: medium
verification: reproduced
area: [form, tests, deps]
guard: tests/form/molsysmt_ChemicalStatesDict/test_roundtrip.py::test_encoded_columns_are_mutable_and_detached_with_copy_on_write
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
  (`add`, `merge`): the warning guard catches deprecated Series.astype `copy` arguments inside concatenation in
  `molsysmt/native/_chemical_merge.py:86`. Preserve composition independence,
  scientific fields and bounded allocation when modernizing the call.
- `tests/native/test_chemical_component_assignments.py::test_unknown_membership_cannot_project_a_label_to_another_row`
  and `tests/native/test_chemical_state_queries.py::test_empty_declared_components_and_unknown_membership_remain_distinct`:
  fixture writes expose a real codec defect: native conversion returns a
  read-only null mask despite the mutable-transport contract. The fixture's raw
  mask edit is intentional. Repair the encoder; copying a mask only in the test
  without storing the edited data would stop testing the intended counterexample.

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


## Implemented correction and local verification — 2026-10-30

Native encoding now creates independent writable values and masks. Direct
`to_numpy(..., na_value=..., copy=True)` supplies values in one conversion rather
than filling/casting an intermediate Series; the extension-array null mask avoids
the read-only Series view, with a copy fallback for an immutable mask. Existing
negative membership controls remain unchanged. The new Copy-on-Write regression
first fails on the original encoder (run 169), then verifies writeability, source
independence and the edited payload's native round trip.

Component restriction preserves the source column-axis dtype, including trusted
legacy object indexes. A private native table-column routine is reused by stable
Topology and chemical composition: it uses per-column nullable promotion and
explicit empty-column copies, avoiding both deprecated copy arguments and
DataFrame all-NA inference. An initial left-dtype coercion exposed two partial-
hierarchy errors; the correction retains unknown parents. No source atom is
assigned to a fabricated group/chain/component to make composition work.

Local evidence uses the existing Python 3.14.7/Pandas 2.3.3 environment, without
an auxiliary environment or package upgrade:

- Run 168 with Copy-on-Write and future string inference reproduces five failures
  among the six selectors. It also exposes an additional old-Pandas table-concat
  warning. Run 171 has one remaining concat warning after the first corrections;
  run 172 passes 17 cases after the common table path is introduced.
- Run 170 passes 302 focused native/codec cases under the ordinary configuration.
- Run 173 has an invalid test-directory selection (exit 5); it is not test evidence.
- Run 174 passes 4,258 cases with two partial-hierarchy setup errors from the
  initial cast. Those errors are preserved; run 175 passes their corrective scope.
- Run 176 passes all 4,260 broad native/form/composition/H5MSM cases. Two new
  empty-array concat warnings are subsequently addressed through explicit copies.
- Run 177 passes 19 cases with both future options enabled, including the original
  membership/dtype cases and the partial hierarchy. Run 178 passes **4,262 cases
  and doctests**, zero failures/errors/skips, exit 0, 130.93 seconds; remaining
  legacy/projection warnings stay visible.
- Strict Sphinx run 179 passes without warning suppression; fast gate 181 passes
  14/14, and the registered scientific executor passes 79/79 with zero skips.
  Its dirty-tree certificate is development evidence, not release qualification.

Docstrings, the native-dictionary foundation, conversion tutorial/cookbook and
course Module 04 now state the native transport-buffer ownership contract.
Notebook code cells and saved outputs are retained. No reference assertion is
removed, dtype check disabled, warning filtered or speculative Pandas cap added.

**Still open:** qualify the actual corrected source on Pandas 3.1 through the
controlled matrix. The local future options reproduce relevant contracts but
are not a substitute for running that version. Keep #526 and #255 open until
that source gate and their separate acceptance conditions are satisfied.
