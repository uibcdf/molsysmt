---
summary: Coordinate explicit Interactions selection-query names with MolSysViewer.
issue: uibcdf/molsysmt#346
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: measured
area: [api, docs, tests]
guard: tests/interactions/test_public_molsys_h5msm_workflow.py::test_explicit_selection_vocabulary_on_storage_routes
normative: devguide/interactions_query_semantics.md
blocked_by: []
supersedes: []
---

# Coordinate explicit Interactions selection-query names with MolSysViewer

**Reported:** 2026-10-06 by MolSysViewer, counterpart of uibcdf/molsysviewer#168.
**Status:** provider contract implemented and contract-tested; consumer adoption remains owned by uibcdf/molsysviewer#168.

## What

Replace terse graph terminology in the documented public query vocabulary with
the maintainer-approved `involving_selection`, `within_selection`,
`across_selection_boundary` and `between_selections` names. Preserve scientific
membership, sparse representations, occurrence handles, explicit coverage and
all existing detector behavior.

## How

One private mode normalizer serves packed results, edited results and the private
selective HDF5 reader. `query` exposes three canonical values and defaults to
`involving_selection`. `between_selections` retains the separate two-set operation
and exclusivity option; `between` delegates as a validated compatibility method.
Public argument digestion recognizes the canonical names and the new method.

## Why

The maintainer found `incident` unfamiliar and rejected molecule-boundary
interpretations. The explicit names describe an atom-selection boundary even
for variable-size participants. This is an accepted public-contract clarification
within the frozen stabilization scope, not a new detector or scientific criterion.

## Migration decision

Keep legacy query values and `between` as documented provider compatibility
spellings without warnings or a scheduled 1.0 removal. Consumers can migrate
saved query fields explicitly. Stored `evaluation_mode` and detector
`selection_mode` remain unchanged: they declare scientific search scope.
InteractionsDict v1/v2 and H5MSM 0.5 retain their current schemas and metadata.
The [normative contract](../../interactions_query_semantics.md) records exact rules,
consumer ownership and migration boundaries.

## Acceptance and evidence

- Query and between-selection semantics match the explicit predicates for every
  constituent atom, including D/H/A roles and compound rings.
- Nonconsecutive/repeated structure indices, parallel occurrences and empty versus
  unevaluated coverage retain their existing behavior.
- Packed views, invalidated results and recalculated blocks support both vocabularies
  without forcing full-column packing.
- Argument validation and valid `skip_digestion` routes work for the new operation.
- Typed-dictionary and public MolSys/H5MSM round trips preserve scientific scope
  and schema versions; old query spelling remains usable.
- User Guide Foundations, Tools, Cookbook, relevant course and docstrings reflect
  the new names, while scientific scope examples keep their existing values.
- Publish an exact tested provider commit and a handoff to uibcdf/molsysviewer#168.

The first five-module test selection had 113 passes and seven failures in newly
written assertions: four expected the wrong established parallel-observation
distance order, and three attempted an unsupported direct Interactions-to-MolSys
conversion. Correcting the fixture expectations and using the existing public
MolSys/H5MSM attachment route yields 120 passes in 10.34 s. This does not change
observation ordering or expand the conversion graph. Raw logs and JUnit remain
local under the `molsysmt-346-query` prefix.

## Resolution — 2026-10-06

**Contract-tested** in the shared Python 3.14.7 development environment, with
NumPy 2.4.6, h5py 3.16.0, pytest 9.1.1 and 12 pytest workers. Commands run from
the repository root with that environment active:

```bash
python -m pytest tests/interactions tests/native/test_molsys_interactions.py \
  tests/form/file_h5msm tests/form/molsysmt_InteractionsDict \
  -n 12 --dist loadfile --receptor=llm \
  --junitxml=/tmp/molsysmt-346-expanded.xml
python -m pytest --doctest-modules molsysmt/interactions/result.py \
  --receptor=llm --junitxml=/tmp/molsysmt-346-doctest.xml
python devtools/scripts/validate_public_api_stability.py --base HEAD
python devtools/scripts/release_gate.py
```

The expanded selection passes **1,474 tests in 40.16 s**, with zero failures,
errors or skips. Its 635 warnings are 618 historical H5MSM migration warnings
and 17 deliberate memory-budget controls. The result doctests pass **8 tests**.
The closing guard checks literal membership, coverage and occurrence handles
on four storage routes, rather than merely accepting the new strings; it also
protects the validated compatibility wrapper and prevents forced packing.

All eight changed detector/recipe notebooks execute successfully with
`python docs/execute_notebooks.py -q -n 12 -f <changed notebook paths>`.
Their first execution was blocked before cell execution by sandbox socket
permissions; the permitted Jupyter rerun succeeds. Nine Python blocks in
`querying_sparse_interactions.md` execute, and course module 20 changes prose
only, preserving all code cells and their outputs. The first fast-gate run has
13/14 passes because the new report's generated index is not yet refreshed;
the final fast-gate run passes **14/14**, including developer-guide integrity.
Ruff and the public signature guard against the parent commit also pass.

The [bounded validation receipt](../../../devtools/data/interactions_query_vocabulary_346_20261006.json)
retains JUnit and tested runtime/test-file hashes. These are source-contract
checks, not a release certificate, a performance benchmark or consumer UI
qualification. The issue resolution names the authoritative tested source commit.
Installed editable distribution metadata still carries historical development
versions; this work targets the planned **0.23.0** checkpoint without publishing
that version or creating a tag.

No schema migration is required. Provider aliases remain accepted without a
warning or scheduled removal in 1.0. Consumer query/display filter migration
belongs to uibcdf/molsysviewer#168; scientific scope metadata remains literal.
The previously qualified source/wheel pair remains evidence for its original
producer, not for the new query-contract source. Exact candidate and installed
pair qualification remain under uibcdf/molsysmt#334.


## Maintainer clarification — 2026-10-06

After the initial closure, the maintainer explicitly withdraws provider
compatibility spellings because this vocabulary has no public-user adoption.
The earlier decision above records the initial delivery, not the current API.
Only `involving_selection`, `within_selection`, `across_selection_boundary` and
the separate `between_selections` operation are now supported. The old query
modes raise in both normal and trusted routes; `between` is absent. Scientific
`selection_mode`/`evaluation_mode`, saved analysis values and schemas remain
unchanged. The original guard now checks rejection as well as literal membership
across packed, selected, invalidated and replaced results; selective HDF5 controls
also reject previous query names. Provider call sites, fixtures, tests and the
contract benchmark adapter use the canonical API.

The first expanded run passes 1,450 tests and fails 30: 29 still carry previous
query names in test parameter tables, and one is an actual Viewer integration.
Updating those parameter tables preserves their membership assertions. The
corrected provider selection passes **1,479 tests**, with zero failures/errors/
skips and **one explicitly deselected consumer integration**. The result
doctests pass eight tests; 14/14 fast gates and Ruff/signature checks pass.
A small existing contract control verifies 20 oracle queries on 30 atoms and
30 structures; this is a functional check, not a performance claim.

The unchanged test
`tests/interactions/test_scientific_attribution.py::test_real_viewer_preserves_original_bibliography_in_named_analyses_and_sessions`
fails because the current Viewer calls `result.query(mode="incident")`.
Keep this real integration guard intact and qualify it after
uibcdf/molsysviewer#168 updates the consumer. No all-green provider/Viewer pair
or release certification follows from the corrected provider selection.
The closure clarification names the new authoritative source commit and tells
the consumer to migrate executable calls and known saved query/display fields.

Reproduction uses the expanded command above plus
`tests/physchem/test_chemical_template_receptor.py`; the corrected run explicitly
adds `-k 'not test_real_viewer_preserves_original_bibliography_in_named_analyses_and_sessions'`.
The [canonical-only validation receipt](../../../devtools/data/interactions_query_vocabulary_346_canonical_20261006.json)
retains both the initial failure and corrected provider selection, source/test
hashes and the consumer boundary. The original receipt and dated measurements
remain historical evidence.
