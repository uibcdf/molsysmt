---
summary: Native cookbook recipes retain retired chemistry ownership and stale H5MSM defaults
issue: uibcdf/molsysmt#769
status: resolved
opened: 2026-11-16
closed: 2026-11-17
severity: medium
verification: measured
area: [docs]
guard: tests/documentation/test_sparse_interaction_recipe.py::test_sparse_recipe_preserves_coverage_handles_and_chemical_owner
normative:
blocked_by: []
supersedes: []
---

# Native cookbook recipes retain retired contracts

**Reported:** 2026-11-16, during #334's frozen I0–I5 native documentation cohort.
**Status:** corrected, contract-tested and locally rendered; final-pair qualification remains separate.

## What

The Common Core capstone also described covalent partitioning as Topology work although its code already called ChemicalStates. That explanation and its API links now agree with the actual owner.

The sparse-interaction recipe says that chemical setters and bond edits belong
to `molsys.topology`. Topology has no such facade after the domain refactor.
The copy recipe calls an omitted-version write H5MSM 0.5 although it writes
1.0, and points to a version-specific 0.5 helper as general migration guidance.
The interaction and fixed-state-H recipes also describe 0.5 as the saving route
without distinguishing explicit older-schema output from today's default.

## How

`docs/content/user/cookbook/querying_sparse_interactions.md` retains an old
owner-notification paragraph next to a newer example asserting that Topology
has no bonds. `copying_disk_systems.md` calls `write_layers` without a version.
Current source defaults and ChemicalStates mutation notifications establish
the actual behavior; no molecular or schema implementation change is needed.

The correction uses ChemicalStates as the owner, checks invalidation of prior
evaluated-empty coverage after a bond edit, and keeps a detached chemical copy
and the old result's coverage unchanged. The copy recipe checks the actual
root version before taking byte-equivalent snapshots. Version-specific 0.5
migration remains documented separately. MolSysMT text uses structures.

## Why

A reader following these explanations could select a removed API or confuse
byte-preserving copying with migration to the default schema. These are user
workflow explanations, not evidence of a new chemical detection defect.

## Evidence and limits

Both complete existing recipes execute under nm/ps and pm/fs. The first new
sparse-recipe guard incorrectly assumed replacement coverage was sorted; actual
coverage is [0, 3, 1]. That test expectation was corrected to compare the intended
population. Its original failure is retained and is not a MolSysMT defect.
The baseline and corrected controls are retained in the
[finite receiving record](../../../devtools/data/independent_native_work_334_20261116.json).
They do not qualify scientific detectors, a final installed pair or publication.

## Acceptance

- Whole recipes preserve copy independence, source maps, occurrence handles and
  evaluated-empty versus unevaluated coverage under both policies.
- The actual default file root is checked; explicit older-schema helpers keep
  their stated output.
- ChemicalStates bond editing clears current coverage while the old result,
  detached chemistry and stable inventory retain their independent meaning.
- Strict rendering and affected article inspection succeed before closure.

## Local closeout — 2026-11-17

The complete strict site builds successfully, then the visually reviewed code
folding is rebuilt strictly. All 54 selected articles and their local links,
anchors and twelve figures are received. Seven static browser reading views
have no local HTTP or page errors; the changed examples are visually inspected.
The seven final example controls pass with no skips after the layout correction.
Original failed attempts and their exact interpretations remain retained.
This receiving neither renders a live molecular canvas nor qualifies an installed
release pair. No scientific runtime or native binary is changed.
