# Conversion Fidelity WIP Exposes Multiple Contract Gaps

## Status

- **State:** resolved
- **Resolved:** 2026-07-28
- **Severity:** formerly release-blocking for landing the fidelity WIP and
  making the conversion-fidelity release gate operational
- **Scope:** conversion reporting, native dictionary schemas and adapters,
  strict conversion semantics, and PDB fidelity
- **Design context:**
  [Conversion Fidelity Matrix and MolSysDict Schema Evolution](../../pending_proposals/conversion_fidelity_and_molsysdict_v1.md)

## Resolution

The failure inventory below describes the original investigation state. The
three test modules are now tracked and pass together:

```text
40 passed
```

The executable fidelity audit now imports and runs successfully. Its closure
snapshot reports 75 Tier 1 forms, 481 direct Tier 1 edges, 39 exhaustive
preflight routes, 442 explicitly accepted non-exhaustive routes, zero new
non-exhaustive debt, and 28 resolved debt entries.

Stages 1–4 were implemented in focused commits before this record was archived:
conversion issues carry scopes, the native dictionary routes have exhaustive
profiles, strict mode rejects audited non-chemical losses, thermodynamic and
PDB adapter gaps have regression coverage, and PDB fidelity is green. The final
working-tree gap was native dictionary extraction: the implementations existed
without being exported by their form packages. The resolution exports both
adapters and adds public regressions for canonical atom order, requested
structure order, coordinate alignment, hierarchy remapping, and bond remapping.

The 442 accepted non-exhaustive routes are not hidden or declared lossless.
They remain classified release debt governed by the fidelity baseline and the
Tier 1 promotion policy; they do not keep this historical implementation bug
open.

## Summary

The current failure is not a single missing helper. Three untracked
conversion-fidelity test modules expose **38 failures across at least six
independent gaps**. The tracked conversion-truth tests listed below remain
green, so the new failures must not be described as a regression of all
existing conversion behavior. They are stronger WIP contracts that the
implementation does not yet satisfy.

The work must be resolved in staged, reviewable changes. Combining the scope
contract, schema repairs, adapter repairs, and PDB semantics in one change would
obscure causality and make regression review unnecessarily difficult.

## Evidence

### Untracked WIP tests

| Test module | Current result |
| --- | ---: |
| `tests/conversion_truth/test_conversion_report_native_scopes.py` | 13 failed |
| `tests/conversion_truth/test_coordinate_trajectory_fidelity.py` | 4 failed |
| `tests/conversion_truth/test_pdb_fidelity.py` | 21 failed, 1 passed |
| **Total** | **38 failed, 1 passed** |

### Tracked tests that remain green

| Test module | Passed |
| --- | ---: |
| `tests/conversion_truth/test_h5msm_fidelity.py` | 5 |
| `tests/conversion_truth/test_native_bond_seam_adapters.py` | 23 |
| `tests/conversion_truth/test_native_roundtrips.py` | 2 |
| `tests/conversion_truth/test_native_selection_contracts.py` | 2 |
| `tests/conversion_truth/test_builder_bond_metadata.py` | 1 |

These results were reported from the current working tree. They must be
reproduced with normal pytest as the authority when each resolution stage is
implemented.

## Independent Gaps

### 1. Missing Audit-Scope API

`molsysmt/_private/conversion_report.py` exposes
`build_conversion_report()` but not:

- `get_conversion_audit_scopes(source, target)`
- `is_conversion_audit_exhaustive(source, target)`

The untracked `devtools/scripts/audit_conversion_fidelity.py` imports these
functions and therefore exits during import. Consequently, the proposed release
gate does not currently execute on the WIP tree.

### 2. `ConversionIssue` Has No Scope

`ConversionIssue` records `attribute`, `reason`, and `kind`, but it cannot
identify whether a loss belongs to chemical state, structures, topology, or
another declared scope. The WIP tests require `issue.scope`, including values
such as `chemical_state` and `structures`.

### 3. Native Dictionary Forms Are Not Audited Exhaustively

`build_conversion_report()` currently derives audited scopes inline:

```python
("all",) if same_form else ("chemical_state",)
```

This makes only identity conversions exhaustive. The native schema-bearing
pairs must also be exhaustive:

- `MolSys` to `MolSysDict`
- `Structures` to `StructuresDict`
- `Topology` to `TopologyDict`

The audit must use the declared schema and central attribute classifications,
not the fixed `_CHEMICAL_ATTRIBUTES` subset. The reported inventory contains
118 classified attributes:

- 31 chemical-state attributes;
- 21 structural attributes;
- 76 topological attributes.

### 4. Strict Conversion Ignores Non-Chemical Losses

`strict=True` currently fails to reject detected losses outside the chemical
subset. Losses such as `velocities` and `bioassembly` must raise
`NotCompatibleConversionError` when the source declares them and the selected
conversion cannot preserve them.

Strictness must apply to every audited scope. It must not silently mean
"strict only for chemical-state attributes."

### 5. Independent Schema and Adapter Defects

The WIP exposes at least four separate implementation defects:

- missing `evidence` schema support (`KeyError: 'evidence'`);
- missing thermodynamic series support for `temperature` in `StructuresDict`
  (`KeyError: 'temperature'`);
- a `to_molsysmt_MolSys()` adapter that does not accept `skip_digestion`;
- a PDB parsing or conversion path that attempts `int("fram")`, suggesting a
  truncated or misaligned header.

Each defect needs its own focused regression test and change. Passing one is not
evidence that the others are resolved.

### 6. PDB Fidelity Is a Separate Workstream

`test_pdb_fidelity.py` contains approximately 16 distinct causes, including
atom and group identifier behavior, expected reporting of `atom_id` loss,
strict-mode expectations, and at least one missing exception. It shares the
scope-contract dependency with the first two stages, but it is not one bug with
the native-dictionary audit.

## Ordered Resolution Plan

### Stage 1 — Establish the Audit-Scope Contract

Implement the common vocabulary before changing conversion behavior:

1. Add a backward-compatible `scope: str` field to `ConversionIssue`.
2. Add `get_conversion_audit_scopes(source, target)` and
   `is_conversion_audit_exhaustive(source, target)` to
   `molsysmt/_private/conversion_report.py`.
3. Make those helpers the single source of truth for conservative static route
   coverage used by the generated graph audit.
4. Let `build_conversion_report()` start from that static contract and
   strengthen it only when an inspected instance supplies additional evidence.
5. Register exhaustive form pairs explicitly as their complete audits land,
   instead of deriving policy from an inline identity expression.

**Closes:** the audit-script import failure and the missing issue-scope contract.

**Does not yet close:** assertions expecting native dictionary conversions to
report `("all",)` based on exhaustive schema traversal. That behavior belongs
to Stage 2.

**Acceptance criteria:**

- the audit script imports and reaches its audit logic;
- scope helpers have focused unit tests;
- existing callers constructing `ConversionIssue` without `scope` remain
  compatible;
- scope metadata is consistent between the report and individual issues;
- a static identity route remains representation-scoped without execution
  evidence, while an inspected same-form instance may be classified more
  strongly.

### Stage 2 — Audit Native Dictionary Forms Against Their Schemas

1. Traverse the declared attributes for each audited scope using:
   - `is_chemical_state_attribute()`;
   - `is_structural_attribute()`;
   - `is_topological_attribute()`.
2. Compare source capabilities and target schemas explicitly.
3. Attach the correct scope to every issue.
4. Make `strict=True` reject every detected loss in an audited scope, not only
   chemical losses.

**Closes:** the main body of
`test_conversion_report_native_scopes.py` and the non-chemical strictness gap.

**Acceptance criteria:**

- the three native dictionary pairs are reported as exhaustive;
- all 118 currently classified attributes participate according to scope;
- `velocities` and `bioassembly` losses are reported and rejected in strict
  mode;
- no fixed private list becomes a second attribute-policy authority.

### Stage 3 — Repair Schema and Adapter Gaps Independently

Resolve each defect in a separate focused change:

1. `evidence` schema support;
2. `temperature` series support in `StructuresDict`;
3. `skip_digestion` compatibility in the implicated
   `to_molsysmt_MolSys()` adapter;
4. the PDB `int("fram")` parsing or conversion defect.

**Acceptance criteria:** each change has a minimal regression test, explains
the intended contract, and passes independently of the remaining Stage 3 items.

### Stage 4 — Close PDB Fidelity as Its Own Workstream

After Stages 1 and 2 stabilize reporting semantics:

1. classify the remaining PDB failures by root cause;
2. preserve source identifiers faithfully where the contract requires it;
3. report unavoidable losses accurately;
4. align strict-mode failures with the stable audit contract;
5. avoid changing canonical selection ordering or native string-ID invariants
   as a side effect.

**Acceptance criteria:**

- all assertions in `test_pdb_fidelity.py` pass for documented reasons;
- failures are not hidden by weakening expectations;
- PDB round trips and strict-loss behavior agree with the conversion report;
- each distinct root cause remains reviewable in focused commits.

## Release and Integration Impact

Earlier green conversion-audit measurements remain historical evidence for the
then-tracked surface. They do not establish that the current untracked WIP is
releasable. Before the fidelity audit can count as a 1.0 gate:

1. Stages 1–4 must be resolved or explicitly re-scoped by a documented release
   decision.
2. The audit script and its tests must be tracked.
3. The audit must execute from a committed tree.
4. Normal pytest must confirm the tracked and WIP conversion-truth surfaces
   together.
5. The complete release matrix must run against that same commit.

Until then, the correct status is: **existing tracked conversion contracts are
green; the stronger untracked fidelity contracts are not implemented, and the
proposed audit gate cannot currently start.**
