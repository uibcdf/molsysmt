---
summary: Alanine demo catalog atom counts contradict the public bundled inventory.
issue: uibcdf/molsysmt#677
status: active
opened: 2026-11-09
closed:
severity: low
verification: reproduced
area: [docs, data]
guard: tests/test_demo_catalog.py
normative:
blocked_by: []
supersedes: []
---

# Reconciling the alanine catalog with its actual inventory

## What / How / Why

The human-facing summary and file description say 12 atoms. The actual public
get(n_atoms=True) returns 22, agreeing with the independent demo manifest.
The numerical guard reproduces this contradiction before metadata repair.
Change only the two catalog descriptions, preserve the manifest/dataset and
re-execute the dynamic catalog notebook. The guard compares both descriptions
with the real public inventory, not a second maintained count table.

## Acceptance

The metadata consistency guard passes; the notebook executes both code cells
and publishes the actual descriptions. Preserve its source, anchors and catalog
architecture. No data bytes, scientific method, units or public API change.

## Notebook receiving

The two original code cells execute in an owned Jupyter kernel after a separate
source/interpreter identity probe. Both generated catalog descriptions show 22
atoms; source/anchors/cell IDs are preserved. The complete executed probe artifact
is retained privately; the public notebook contains only its original cells and
actual outputs. The kernel's local TCP warning is retained, not suppressed.
