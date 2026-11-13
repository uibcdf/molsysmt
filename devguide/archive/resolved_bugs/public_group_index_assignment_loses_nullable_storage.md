---
summary: Public group-index assignment loses nullable storage after full replacement
issue: uibcdf/molsysmt#739
status: resolved
opened: 2026-11-12
closed: 2026-11-12
severity: high
verification: reproduced
area: [native, form, set]
guard: tests/form/molsysmt_Topology/test_nullable_membership_assignment.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Retaining nullable stable membership storage

## What

BindingMT reports a public three-step group-index edit that fails after a
whole-column replacement. The native schema declares Int64, but native
Topology setters replace it with pandas-inferred int64. The next missing-value
assignment depends on the pandas version instead of the declared native schema.
Applicable atom chain, group molecule and molecule entity columns have the
same whole-replacement defect.

```python
from molsysmt.native import MolSys
import molsysmt as msm

molsys = MolSys(n_atoms=2, n_groups=1)
msm.set(molsys, element='atom', selection=[0], group_index=[None])
msm.set(molsys, element='atom', group_index=[0, 0])
msm.set(molsys, element='atom', selection=[0], group_index=[None])
```

## How

The inspected source blob ecb3e821f734150f4a46a9bab8b0db8cd69bfe75 matches
BindingMT's report and the retained development source. Direct whole-column
assignment discards nullable storage. Some parent projections similarly
publish inferred lists/NumPy arrays. A projected chain edit also stages into
an integer NumPy array, which cannot accept an unknown member.

The correction reuses one private native-table assignment primitive to stage
nullable Int64 values before publishing a column. Public native forms retain
ArgDigest and use catalogued ArgumentError for invalid values. Full supported
numeric parent projections retain explicit unknowns and nullable storage;
first-source value policy remains unchanged. Missing chain members do not
establish a replacement chain inventory. Complete known chain assignments
retain the existing reconstruction policy.

## Why

A supported native edit must not change later missing-value semantics merely
because an earlier assignment happened to contain only known integers.
Inference of floating/object storage also weakens typed transport expectations.
This is an admitted correctness repair before further #727 documentation work,
not a new hierarchy API, geometry kernel or BindingMT workaround.

## What is measured and what is assumed

The declared-hierarchy baseline has eight dtype failures, two passing three-step
witnesses and two pandas FutureWarnings. In this retained runtime the witness
warns/coerces rather than raising BindingMT's TypeError. The schema violation is
reproduced; the reporter's exact newer runtime is not newly qualified.
Ten initial corrected controls pass; 33 expanded controls now pass without
warnings, including invalid-value source preservation and nullable projections.
The affected cohort passes 221 setter/hierarchy/doctest cases, retaining one
expected legacy-H5MSM warning. The final 49 focused controls also pass without warnings, including
invalid-length preservation. Final receiving passes 51 controls, including two public docstrings. Four
strictly built actual articles have 131 valid local destinations, an explicit
canonical alias link and no unlinked Python roles.

## What was refuted

The first eight-failure test draft used a nonexistent root MolSys constructor.
The corrected import is molsysmt.native.MolSys, as in the reporter's witness.
An early parent fixture also exposes a separate read-side inventory mutation,
now tracked in #740 with a labelled-row witness. The final fixture declares its
parent relations to isolate nullable editing; it does not certify read-side
inference. The constructor error is a test-draft error, and the count mutation
is not counted as a #739 setter failure.

The first expanded cohort has 31 passes and two failures: a real projected
chain integer-buffer limitation, and an unsupported chain-to-molecule public
assignment expectation. The typed staging buffer corrects the former. The
existing public refusal of the latter is preserved and negatively guarded;
no digestion bypass or new editing route is added.

## Scope and exclusions

Canonical nullable stable parent columns and supported numeric full projections
are covered. Source positions and string IDs remain distinct. Coordinates,
chemical states, H5MSM, analysis invalidation and native kernels are unchanged.
This does not redesign parent bounds, hierarchy reconstruction, unsupported
projections or projected subset-conflict semantics. Staging protects the named
column from invalid type/length publication; a multi-attribute call remains
sequential and is not one transaction. Raw dataframe writes retain their own
responsibility. No new pandas/dependency floor or installed qualification is
claimed.

## Acceptance criteria

- Whole and selected public edits retain Int64 and explicit unknown membership.
- MolSys and Topology share the same behavior, preserving unrelated columns.
- Invalid noninteger/length input fails before publishing that column.
- Supported parent projections retain nullable storage and unknowns.
- Missing chain membership preserves declared chain rows; unsupported routes
  retain explicit refusals and source preservation.
- Relevant setter/hierarchy regressions, doctests, maintained documentation and
  actual affected HTML receiving pass before closeout.

## Provenance

2026-11-12 local date, shared Linux host, retained Python 3.14.7/support-provider
runtime. Exact pandas, module paths and inputs belong in the receiving record.
Tests use one CPU, a 1.5 GiB cap and zero own swap, preserving a conservative
6.5 GiB host reserve. The complete incoming board has 658 issues, 96 open,
including #739, and no open PRs at intake.

## Received outcome — 2026-11-12

Implementation 8cc066c84 and the indexed-alias documentation correction
83eb35cf1 receive the supported native editing contract. The
[receipt](../../../devtools/data/native_nullable_membership_receiving_739_20261112.json)
retains all original failed drafts, exact runtime/input identities, affected
221-case cohort, final 49 focused controls, 51-case docstring receiving,
four actual articles and the independent #740 count-mutation witness.
The initial actual-article pass finds an unlinked root set alias despite its
131 valid existing destinations. The correction targets the canonical indexed
basic.set API without changing the visible alias; subsequent strict receiving
requires zero unlinked roles and the intended alias link itself.

Fifteen initial offline gates and Ruff pass. No exact reporter/pandas-3,
complete-source/nightly, installed or final-pair qualification is claimed.
#740 remains independently open and takes priority over the remaining #727
external-class documentation review. The original milestone score and release
pause are unchanged.
