---
summary: Generated CCD reader tests leak miniature amino-acid catalogues across tests
issue: uibcdf/molsysmt#597
status: active
opened: 2026-11-05
closed:
severity: medium
verification: reproduced
area: [data, tests]
guard: tests/data/databases/test_ccd_generators.py::test_generated_tables_deliver_bonds_through_existing_readers
normative:
blocked_by: []
supersedes: []
---

# Generated CCD receiving replaces another test's cached catalogue

## What

The CCD receiving fixture monkeypatches an installed catalogue path and names
inside the same process as ordinary reference consumers. A warm real ALA cache
ignores the miniature fixture; a cold fixture leaves miniature ALA variants in
that cache after paths are restored. Hosted PR CI exposes the warm case and a
serial CCD/conversion run exposes the reverse leak.

## How

Receive each generated catalogue through the existing public group reader in a
separate interpreter. Its fixture lifetime then includes every derived cache.
The parent first warms the real ALA catalogue, checks the generated alternate
atom-name map in the child, and confirms unchanged real parent lookup results.
The generated fixture and caller maps retain the same exact [[4, 9]] assertion.
No production cache invalidation or catalogue-replacement API is introduced.

## Why and evidence

A test-only mutable catalogue must not redefine an immutable runtime snapshot
for unrelated tests. The serial receiving selection now passes 72 cases,
including all generator cases followed by GRO/PDB/NMR conversion guards. This
is local source evidence; it does not replace hosted exact-candidate gates.
Guard above exercises both the generated reader and retained warm parent data.

## Scope and provenance

Test isolation only. No production science, dependency, package or schema change.
Linux/Python 3.14.7; main ed09f6453 plus PR 1c88e785b and local receiving changes.
Hosted baseline: job 127683524087, run 42153312659. Local receipt:
.pytest_cache/543-serial-conversion-repaired.xml (not a release artifact).
