---
summary: Qualify PyParsing 3.3.4 or its published successor for MDTraj selections
issue: uibcdf/molsysmt#486
status: open
opened: 2026-10-26
closed:
verification: upstream
area: [selection, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# Qualifying the published PyParsing fix for MDTraj selection

**Requested:** 2026-10-26 by the maintainer following the resolution of
uibcdf/molsysmt#484.
**Status:** Awaiting a published upstream candidate and explicit compatibility
qualification; no future version is certified.

## What

Track the publication of PyParsing 3.3.4, or the first published successor carrying
the relevant fix, and qualify it against MolSysMT's MDTraj input-selection route.
Keep the existing 3.3.2 development baseline until a replacement has evidence.
This issue is a follow-up to uibcdf/molsysmt#484, not a reopening of its resolved
consumer installation constraint.

## How

1. Check official release metadata and
   [pyparsing/pyparsing#672](https://github.com/pyparsing/pyparsing/issues/672).
   Record the exact published version, wheel/Conda build, source and hashes;
   a promise, branch, tag or source-only success does not prove package delivery.
2. Check Python support and provider requirements, retaining the supported
   Python 3.11 route. MDTraj 1.11.2 itself requires Python >=3.12, so a global
   MDTraj floor increase is not the parser fix for that older interpreter.
3. Compare the candidate with the verified 3.3.2 baseline using the twelve
   symbolic/alias comparisons and the public four-form population matrix.
   Include <=, >=, nested AND/OR/NOT, empty results, group projection and error
   causes. Exercise the existing broader selection/chemical-reference tests;
   review the related infix/token-shape regressions under
   [pyparsing/pyparsing#674](https://github.com/pyparsing/pyparsing/issues/674).
4. Run the appropriate maintained dependency/source checks and record the
   actual provider versions, import origins, platform/interpreter and test
   outcomes. Scope the claim to the combinations actually exercised.
5. If accepted, update the maintained compatibility guidance and any deliberately
   pinned development runtime. If the candidate still fails, retain the baseline
   and send a bounded reproduction to the existing owning upstream issue.

The existing `pyparsing!=3.3.3` exclusion does not block 3.3.4 or another corrected
successor. Removing the exclusion is unnecessary and would re-admit a known
broken artifact. Do not replace it with an unsupported permanent upper ceiling.

## Why

PyParsing 3.3.3 regresses MDTraj's valid symbolic <= and >= comparisons.
The provider acknowledged the regression in
[mdtraj/mdtraj#2190](https://github.com/mdtraj/mdtraj/issues/2190), and its
1.11.2 metadata excludes 3.3.3. The PyParsing maintainer announced a 3.3.4 fix;
MolSysMT needs a visible reminder to receive and verify that actual publication.

## What is measured and what remains unknown

On 2026-10-26, the official PyPI metadata inspected during #484 listed 3.3.3 as
latest; no 3.3.4 artifact was available. With installed MDTraj 1.11.1 on
Linux/Python 3.14.7, the comparison audit passed all twelve cases with PyParsing
3.2.5, 3.3.0, 3.3.1 and 3.3.2; 3.3.3 failed the two non-strict symbolic operators.
After a one-package Conda correction to 3.3.2, 292 scoped tests and fourteen fast
release gates passed in the actual development environment.

These are historical baseline results, not a claim about the unpublished fix.
Exact provenance and commands are retained in
[the #484 receipt](../../devtools/data/mdtraj_parser_compatibility_20261026.json).
The current publication state must be rechecked when this work resumes.

## Acceptance criteria

A published candidate is identified immutably, the affected public population
and broader regression tests pass against actual package imports, interpreter
compatibility is respected, and the accepted/rejected decision is recorded in
the maintained selection/dependency guidance. Close with the existing public
comparison pytest guard and exact qualification evidence; do not close merely
because the upstream issue changes state or a version number becomes visible.

Relevant guard:
`tests/basic/select/test_mdtraj_comparisons.py::test_public_mdtraj_comparison_populations`.
Relevant normative page:
`docs/content/user/foundations/support/selection_syntaxes.md`.

## Scope and exclusions

This is a tracked follow-up, not an automatic polling job or authorization to
publish a component, change tags, patch the provider or broaden the 1.0 feature
scope. It does not block 1.0 while the compatible baseline and exact exclusion
remain effective. Original scientific-descriptor reviews under #473/#475 are
independent. No package or runtime configuration changes are made by opening it.
