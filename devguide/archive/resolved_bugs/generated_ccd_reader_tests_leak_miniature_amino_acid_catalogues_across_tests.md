---
summary: Generated CCD reader tests leak miniature amino-acid catalogues across tests
issue: uibcdf/molsysmt#597
status: resolved
opened: 2026-11-05
closed: 2026-11-06
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

## Resolution — 2026-11-06

Current serial receiving runs the generated CCD cases followed by GRO and complete NMR conversion in the same parent interpreter: 51 cases pass, without failure or omission. Generated readers run in a child after warming real parent ALA data, retain the exact alternate-name [[4, 9]] result and leave parent reference results unchanged. Production immutable caches are neither cleared nor replaced.

Verified source: cddc3f3a613282693126549654233d2fd1d739a4. Existing implementation originated in
ab789897bad51a7258f366aadc01840895d6366e; no new production fix is claimed by
this closeout. The new NMR guard belongs to the received source above.
[Exact source, JUnit digests and scope](../../../devtools/data/ordered_bug_closeout_594_598_20261106.json)
retain these independent profiles and their overlapping counts. Existing failed
full-suite history, remaining version-matrix/installed gates and release authority
are not changed by this bounded bug closure.
