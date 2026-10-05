---
summary: Post-1.0 individual interaction editing
issue: uibcdf/molsysmt#335
status: open
opened: 2026-10-05
closed:
verification: inspected
area: [api, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Post-1.0 individual interaction editing

## What

Design additions/removals of individual interaction observations and optional reclamation of unused relation/participant definitions after 1.0. Preserve this deferred part of #251/#252 independently of their existing result contract.

## How

Compare an explicit edit builder, batched edits and immutable overlays against the actual workloads. Preserve compound/many-body participants, parallel observations, periodic images, coverage, scope, units and original execution provenance. Define occurrence/relation index stability within snapshots and explicit remapping when compaction changes a catalog. Avoid assuming a compiled backend, sparse tensor or mutable per-observation Python object is preferable without measurements.

## Why

The public result already offers queries, remapping, invalidation, compatible `replace_structures` and `compact`. Those are independently useful but do not supply arbitrary observation editing or unused-catalog pruning. The maintainer requests preserving this earlier design goal without enlarging 1.0.

## What is inspected and what is assumed

Source inspection of `molsysmt/interactions/result.py` confirms the existing operations. Their executed evidence is in [#252's record](implement_experimental_sparse_interactions_results_and_queries.md#provider-closure-checklist). No new editor, benchmark or proven complexity bound is delivered here.

## What was refuted

Compatible structure replacement is not an individual-occurrence editor. Dropping unused definitions without declaring index changes would violate existing handles. Neither full repacking after every edit nor speculative backend replacement is an accepted design decision.

## Scope and exclusions

Post-1.0 under the [scope freeze](../release_1_0_scope.md). Preserve current immutable snapshots and explicit source correspondence. Direct file append/recovery is #336; source chemical assignments remain outside the interaction observation store.

## Acceptance criteria

- Define additions/removals, duplicates, empty-evaluated coverage and catalog pruning with explicit snapshot/index semantics.
- Exercise varied arity, parallel images, source-axis remapping and preserved old views against an independent record oracle.
- Benchmark batched and sparse edits, atom/structure removals and serialization, separating result storage, retained snapshots, working memory and process RSS.
- Document the chosen supported API, scope, provenance and file compatibility; include its own meaningful guards.

## Dependencies and risks

The existing result/native/H5MSM contracts in #251/#252 remain the base. MolSysViewer editing may provide use cases under uibcdf/molsysviewer#114 without making this a Viewer 1.0 requirement.
