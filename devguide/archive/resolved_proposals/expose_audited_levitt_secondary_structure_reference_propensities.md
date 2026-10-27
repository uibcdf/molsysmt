---
summary: Expose audited Levitt secondary-structure reference propensities
issue: uibcdf/molsysmt#489
status: resolved
opened: 2026-10-26
closed: 2026-10-26
verification: measured
area: [physchem, api, docs]
guard: tests/physchem/test_get_secondary_structure_propensity.py::test_primary_values_forms_selections_and_unit_policy
normative:
blocked_by: []
supersedes: []
---

# Exposing audited Levitt reference propensities

**Requested:** 2026-10-26, maintainer acceptance of the bounded review in
uibcdf/molsysmt#485.
**Status:** Implemented and locally qualified; ready for documented issue closure.

## What

Expose the existing sixty weighted Levitt reference values through experimental
`physchem.get_secondary_structure_propensity`. Require an explicit conformation
category and return a detached group-aligned float64 array of dimensionless
frequency ratios. This lookup neither predicts from sequence nor assigns an
observed structure. The wider reference-scale catalogue remains under #485.

## How

The form-agnostic group-name query delegates to `basic.get`. The reader reuses
`groups/secondary_structure_propensity.py` and strict `group_table_value`, with
no new table or chemical store. Unknown, modified, terminal-cap and dummy names
fail instead of receiving inferred values. Numeric group selections preserve
order and repetitions; empty outputs have shape `(0,)` and dtype float64.
Only the group element is supported. No coordinates or structure indices are
needed. ArgDigest validates the required `conformation` and the explicit
`levitt_1978_weighted` definition; other public arguments retain existing rules.

The three categories are `alpha_helix`, `beta_sheet` and `reverse_turn`. The
reference is Levitt (1978), doi:10.1021/bi00613a026, detailed Tables III–V.
Optional Ackredit credits the original reference scale after successful calls,
including empty selections, while provider absence or failure preserves values.
The boundary contributes to an enclosing session rather than owning a session.
It does not claim execution of the original population-analysis method.

## Why

The #485 source audit checked all sixty existing values against the detailed
original tables and against independent curated entries. A documented lookup
makes these existing data usable without making clients import private tables.
Explicit category and definition avoid conflating ratios, class probabilities,
sequence prediction and observed coordinate assignments.

## Evidence and exclusions

[The research receipt](../../../devtools/data/secondary_structure_propensity_review_20261026.json)
pins the original PDF, independent visual transcription, AAindex accessions and
ProtScale snapshots. The turn vector matches detailed Table V rather than the
differing summary Table II. The table is unchanged; no external runtime code or
new table is copied. Evidence concerns reference lookup, not prediction accuracy,
the original statistical reconstruction or molecular chemical validity.

The output is explicitly dimensionless; changing a length-unit policy cannot
rescale it. These ratios can exceed one and must not be clipped or normalized
to sum to one. An artificial coil remainder, implicit parent mapping, peptide
sum and automatic class assignment were rejected. Only Levitt is exposed; the
Chou/Fasman mixed-year distinction, Deleage/Roux and Lifson/Sander need separate
bounded adoption decisions under #485.

The operation has O(n_groups) output and uses existing NumPy/lookup primitives.
This is an algorithmic estimate, not a benchmark. No runtime HTTP, dependency,
compiled kernel, observed secondary-structure engine or release change is added.

## Acceptance criteria

- All sixty primary-checked values agree across native/dictionary/file inputs.
- Selection order/repetitions, empty dtype/shape, missing information and strict
  unsupported-group/category/population diagnostics are tested.
- Unit-policy independence, detached outputs and unchanged source objects/files
  are protected; optional real-provider attribution and failure are covered.
- Docstrings, API classification, Toolbox, Foundations, Cookbook and all four
  course paths describe the same contract; examples execute without networking.
- Scoped scientific evidence stays partial and identifies its exact oracle.

## Local qualification

The [implementation receipt](../../../devtools/data/secondary_structure_propensity_implementation_20261026.json)
records Linux/Python 3.14.7, dependency versions, source hashes and commands.
The expanded regression passes 1,536 tests in 81.34 seconds with twelve workers
and Pytest Receptor. Another 503 notebook-schema and optional-attribution tests
pass in 8.26 seconds. The public doctest passes; the tutorial and recipe execute.
All five affected course notebooks retain their original code cells and outputs.
The table file is byte-identical to the parent source.

All fourteen fast gates pass. Docstring, API/signature, scientific-registry,
soft-import, Ruff and developer-guide checks pass. The final incremental HTML
build exits zero, with seventeen pre-existing orphan-document warnings and no
new-page diagnostic. Two initial tutorial formatting warnings were corrected.
The initially sandboxed Jupyter launch could not open local kernel ports;
authorized execution outside that restriction passed without changing the
scientific implementation. These are local source checks, not an installed
package, cross-platform, benchmark, full-suite or release-readiness claim.

## Resolution

The guard compares all twenty independently transcribed values for each category
through four forms, selected order/repetitions, empty and scalar selections,
and three length-unit policies. It fails if values, category routing, dtype,
shape or dimensionless unit independence change. Separate tests protect strict
diagnostics, detached values, file/native preservation and optional attribution.
The User Guide, Cookbook, course and public API classification describe the
same experimental contract. Wider table families remain under #485.
