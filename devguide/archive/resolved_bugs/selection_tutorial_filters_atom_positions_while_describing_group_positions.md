---
summary: Selection tutorial filters atom positions while describing group positions.
issue: uibcdf/molsysmt#755
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: low
verification: reproduced
area: [docs]
guard: devtools/tests/test_basic_tutorial_data.py::test_selection_example_selects_backbone_names_in_groups_10_to_29
normative:
blocked_by: []
supersedes: []
---

# A selection example filters the wrong positional axis

**Reported:** 2026-11-14, by comparing executed output with the lesson's description.
**Status:** corrected; independent selected-index guard and actual notebook receiving pass.

## What

The selection tutorial's variable example promises atoms named CA, C, O or N
in groups 10 through 29. It instead applies `atom_index==@indices`. The code
runs successfully but returns eleven atoms rather than the eighty atoms
specified by that explanation in the bundled TcTIM structure.

## How

Change only that predicate to `group_index==@indices`. Preserve the variable
binding demonstration, source indices, atom-name restriction and group range.
The regression executes the actual example, including its final expression,
and compares the result with independent atom-name/group-membership arrays.
It does not merely inspect the spelling of the predicate. The original code
fails by the actual eleven-versus-eighty array mismatch while the other four
offline-loading controls pass. The complete corrected notebook is executed
again rather than retaining outputs from the earlier wrong selection.

## Why

A successful cell or a nonempty result can still teach the wrong molecular
selection. The atom axis and the group axis are different positional spaces.

## What is measured and what is assumed

The baseline is one genuine failure and four passes. The corrected full
selection notebook executes all 47 code cells. There is no evidence of a
selection-engine defect: each original predicate selects what it asks for.

## What was refuted

Checking only notebook exit status, or that all expected variable names appear,
would admit the original wrong selection. The expected result is independently
computed from the loaded system's stored labels and group membership.

## Scope and exclusions

This corrects one documented predicate and its actual output, without changing
public APIs, selection ordering, chemistry, connectivity or scientific profiles.
The runtime and resource boundaries are recorded with the #334 example receipt.

## Acceptance criteria

- The actual variable example selects the independently expected atom indices.
- The full selection notebook executes with its bundled input and saved output.
- The original mismatch, focused result and relevant checks remain inspectable.

## Receiving record

The [dated #334 receipt](../../../devtools/data/documentation_examples_receiving_334_20261114.json)
retains original unsuccessful attempts, actual runtime identities, full notebook
execution, strict full-site rendering and selected-article/asset receiving.
