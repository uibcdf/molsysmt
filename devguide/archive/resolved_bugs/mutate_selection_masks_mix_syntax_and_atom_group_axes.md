---
summary: Mutation selection masks mix syntax and atom/group axes.
issue: uibcdf/molsysmt#568
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [build, selection]
guard: tests/build/mutate/test_mutate_selection_contract.py
normative:
blocked_by: []
supersedes: []
---

# Resolving mutation targets before reconstruction

## What

`build.mutate` interprets public atom selections as group masks and omits their
syntax during ID/name resolution. Index-keyed requests ignore selection. Both
engines duplicate this resolver. Invalid group keys reach table writes, and an
empty target plan still invokes whole-system repair.

## How

On main `ccff2557f576f004461c96950d36a8b6e465e91f`, construct native AlaValPro.
Name-keyed VAL-to-GLY succeeds with `selection='group_index==1'`; `selection=
'resid 1', syntax='MDTraj'` fails in the MolSysMT parser. The equivalent atom
indices 10 through 25 fail as out-of-range group indices. The same cases fail
with explicit PDBFixer. Numeric invalid group keys can create spurious table rows
in the independent working copy before another operation rejects them.

The first regression run exits 1: 18 failures and 12 passes. One failure is an
overstrict new test assumption: the existing PDBFixer conversion uses PDB text,
quantizing retained coordinates to 0.001 angstrom. Its receiving comparison must
allow half that resolution (0.00005 nm); native retained coordinates remain exact.
The local JUnit artifact is `.pytest_cache/mutate-568-baseline.xml`.

## Why

Public selectors must identify the same target groups independently of syntax,
mutation specification and selected engine. Viewer PR #543 is a receiving
consumer, not the owner of a selector workaround. The report originated in that
PR; this native fix does not admit its expanded addon API.

## Resolution contract

- Resolve selection on the atom axis using supported `select`/`get` operations.
  Any selected atom enables its entire group. Boolean masks cover all atoms;
  integer selections are atom indices. Repeated atoms do not repeat mutations.
- Intersect all valid mutation requests with enabled groups, including explicit
  group-index requests. Empty selection, empty requests and disjoint valid
  requests return an independent same-form copy without rebuilding anything.
- Group indices are non-negative integer positions, never Boolean values or IDs.
  Resolve IDs as literal string labels, independent of query parsing; reject
  unknown labels and selected ambiguous labels. Selection can disambiguate IDs.
- Validate mutation-string source names and conflicting repeated target requests
  before either engine receives a working object. Preserve native diagnostics.
- Keep bounded reconstruction behavior and optional-provider limitations explicit.
  Native heavy repair can be restricted to target groups; existing hydrogen
  completion and PDBFixer repair retain their documented whole-system scope.

## Acceptance and exclusions

The public regression module compares native, MDTraj and numeric selections;
partial/empty/repeated/disjoint inputs; invalid indices; duplicate IDs; source-name
checks; target association; original independence; and retained atom geometry.
Both reconstruction engines are exercised when installed, without downloads.
The native `skip_digestion` boundary must preserve safety-critical target checks.

No new rotamer, hydrogen-orientation, minimization or chemical-state algorithm is
introduced. This is contract/parity receiving, not scientific coordinate
validation or installed multi-platform qualification. No new dependency, Rust
kernel, unit convention or storage schema is required.

## Implementation and receiving

The implementation composes public `select`/`get` to resolve atom membership and
literal group metadata. One private mutation-plan resolver serves both engines.
Its feature-specific parser is not a new general API: independently useful
selection and lookup operations already have supported public owners. Targets
are sorted, deduplicated and checked before conversion or table edits. Native
heavy reconstruction delegates to the existing selected-group tool. Empty plans
use public `copy` without preparation.

PDBFixer's inspected `applyMutations` builds an integer-ID map across chains
sharing its requested chain ID. Duplicate effective addresses can overwrite one
another even after source selection has identified one group. A private provider
preflight rejects ambiguity before `applyMutations`; it does not introduce a new
method. Native quoted/hyphenated labels resolve without query interpolation.

ArgDigest preserves Boolean/integer selector types before syntax-specific
coercions and exposes keyword-only `skip_digestion`. SMonitor wraps the operation
and supplies catalog diagnostics. Existing DepDigest-protected converters and
selectors own lazy optional-provider checks; empty plans require no reconstruction
engine. This fix adds no scientific attribution or quantity-conversion boundary.

The first expanded run exits 1 with 492 passes and one test-double failure:
patching exported `basic.convert` was retained by an unrelated lazy viewer import.
Tests now assert output/source integrity without patching that shared boundary.
The same selection then passes **493 tests**. Published floors pass **69 mutation
controls**, with actual origins verified from cached ArgDigest 0.14.0, DepDigest
0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 payloads. Only this floor run disables
the SMonitor pytest entry point under the existing #524 limitation; runtime
diagnostics stay active.

The native doctest passes; the full mutation tutorial executes in **12.3 s**.
Its name-keyed example declares `keys='group_name'`, and its paired instruction
is corrected. Four course mutation blocks replace the unavailable `new_group_name`
call and capture the independent return value. Public tests execute those actual
blocks on local systems; they do not certify complete network-backed lessons.
Existing unexecuted course-cell metadata remains unexecuted. Foundations,
Cookbook and course core explain the atom/group axis and bounded repair scope.

## Previous checkpoint correction

The ccff2557f smoke run 42095546341 failed at the public-signature gate, before
scientific tests: #504's intentional keyword-only `structure_indices` extension
had no signature-registry declaration. That declaration now names its guard,
alongside #568's `skip_digestion` extension. The unchanged validator reports zero
unauthorized signature drifts against `HEAD~1`; strict checks are not weakened.
This corrects review metadata, not the historical hosted result.


## Final receiving

The corrected broader selection exits 0: **1,478 passes**, including the exact
online/offline collection guards and the real occupancy/reinsertion assertion.
The failed first attempt remains in the receipt, with download failures separate
from the stale expectation. Documentation/API-registry receiving has 593 passes;
these overlapping runs are not additive. See
[the receiving receipt](../../../devtools/data/mutation_selection_receiving_568_577_20261105.json)
for commands, identities, counts and limits. Hosted, installed-platform and live
provider qualification remain separate.


## Final engine-audit addendum — 2026-11-05

The last optional-branch review reproduced a pre-existing hydrogen-policy defect:
mutating every AlaValPro group to GLY with PDBFixer returned zero H from an input
containing 21 H. The decision was made after mutation had removed those atoms.
The engine now records H presence from the source before reconstruction, matching
the documented native/optional contract. This changes no H-placement method.
Four new cases exercise both engines with and without input H. Final targeted
receiving exits 0 with **100 mutation tests**, and the published-floor contract
module exits 0 with **73 tests**. The earlier 1,478-case broader result precedes
this narrowly tested branch correction; its unchanged-path evidence is retained
without representing it as a rerun on the final bytes.
