---
summary: Component rebuild discards unchanged metadata despite preservation flags
issue: uibcdf/molsysmt#324
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: reproduced
area: [attribute, build]
guard: tests/native/test_component_metadata_rebuild.py::test_rebuild_preserves_labels_by_membership_after_row_reordering
normative:
blocked_by: []
supersedes: []
---

# Component rebuild discards unchanged metadata

**Reported:** 2026-10-04 while extending uibcdf/molsysmt#298 to add selected bonds.
**Status:** Resolved; native metadata preservation and affected preparation/persistence routes passed 216 tests and public doctests.

## What

`Topology.rebuild_components(redefine_ids=False, redefine_names=False,
redefine_types=False)` discards all component metadata when rebuilding indices,
even if each atom set is unchanged and only component row numbers change.
The new direct guard reproduces the failure on source `21332f34f`:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
    tests/native/test_component_metadata_rebuild.py::test_rebuild_preserves_labels_by_membership_after_row_reordering
```

It failed in 0.22 s: the expected string ID was missing; comparing the missing
value with the expected label raised pandas' ambiguous-NA TypeError.

## How

`molsysmt/native/topology.py:Topology.rebuild_components` replaces the entire
component table before consulting the metadata redefinition flags. False flags
skip regeneration without transferring the old values.

The fix uses the owning native inference layer: compute the new connectivity
partition with the existing Rust primitive, then match old/new components by
exact atom-set equality. Per-new-component minimum/maximum old row reductions
exclude merges; equal membership counts exclude splits. Unknown or out-of-table
old memberships cannot authorize transfer. Preserve only fields whose flag is
False. Unmatched labels remain genuinely missing, rather than the legacy string
`"nan"`. True flags retain their existing regeneration/inference behavior.

## Why

Users lose curated component IDs, names and types despite explicitly requesting
preservation. A selected ligand graph completion cannot safely reuse this
native tool until unrelated unchanged components retain their metadata.
The consumer work serves uibcdf/dockingmt and uibcdf/pharmacophoremt through
uibcdf/molsysmt#298; no sibling implementation is changed here.

## What is measured and what is assumed

**Reproduced:** the direct native test fails before the fix and passes after it.
**Inspected:** the previous implementation unconditionally resets the table.
**Algorithmic bound:** matching uses linear time and memory in atom/component
counts, with compact NumPy reductions; this is not a measured speed or RAM benchmark.

## What was refuted

Component row number is not identity: a reordered unchanged atom set must retain
its requested labels. Conversely, a merged or split set must not inherit an
arbitrary old component label. Count equality alone is also insufficient: the
old/new membership reductions must establish one old row for the full new set.
Reconciliation of unrelated partitions inside chemical preparation is excluded.

## Scope and exclusions

The resolved chemical state's component membership/table and the existing
MolSys wrapper are covered. Other chemical states, molecular hierarchy and
coordinates are not rebuilt. No new form dispatch, dependency or public API
signature is introduced. Preserved labels do not certify chemical identity,
connectivity completeness or template authenticity.

## Acceptance criteria

- Reordered identical memberships preserve each requested field.
- Merges, splits, unknown and out-of-table memberships do not inherit labels.
- Each true flag affects only its own metadata field; defaults still regenerate.
- Forced rebuilds and empty systems behave deterministically.
- Other states remain unchanged; the MolSys wrapper uses the same native rule.
- Native/form extraction and template H5MSM regressions pass.

## Provenance

Linux local development, Python 3.13.14 under the bounded uibcdf/molsysmt#237
exception, released ArgDigest 0.13.0, NumPy 2.4.6 and pandas 2.3.3.
Reproduction source: `21332f34f794648cd899aa6b0c6b565ae534cb4f` plus the new guard.

## Resolution and validation — 2026-10-04

The guard compares all three metadata columns with independent expected labels
following a nontrivial component-row reorder. It fails if table reconstruction
clears labels or copies them by old row number. Additional tests reject stale
labels after merges/splits and unresolved membership, exercise each flag,
forced reconstruction, independent states, empty domains and the MolSys wrapper.

Command:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
    tests/native/test_component_metadata_rebuild.py \
    tests/native/test_topology_operations.py tests/native/test_hierarchy.py \
    tests/native/test_molsys.py tests/physchem/test_chemical_template.py \
    tests/physchem/test_chemical_template_connectivity.py \
    tests/physchem/test_chemical_template_selection.py \
    tests/physchem/test_chemical_template_est.py \
    tests/physchem/test_chemical_template_receptor.py \
    tests/form/file_h5msm/test_chemical_states_v04.py \
    tests/form/file_h5msm/test_chemical_states_v05_probe.py \
    tests/form/file_h5msm/test_extract.py \
    --doctest-modules molsysmt/native/topology.py \
    molsysmt/physchem/apply_chemical_template.py \
    molsysmt/physchem/assess_chemical_template.py
```

Result: **216 passed in 81.46 s**. The 62 warnings comprise 47 intentional legacy
H5MSM deprecation notices and 15 existing pandas future warnings. Ruff checks
and formatting, dependency-import validation, docstring fidelity, course
structure, public API classification and the signature guard passed. Sphinx
HTML built successfully with existing reference/toctree warnings, including the
pre-existing Topology API-page target; this is not a warning-free build claim.

The provider fix enables #298's bounded selected bond completion through the
same native tool. Its consumer preflight rejects unrelated stored partitions
needing reconciliation. That preparation proposal remains partial and retains
its own acceptance scope. Current normative behavior is recorded in
`devguide/ALGORITHMS.md`; Foundations, Toolbox, Cookbook and course Module 12
reflect the public behavior.
