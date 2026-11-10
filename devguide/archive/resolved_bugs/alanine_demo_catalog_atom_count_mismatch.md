---
summary: Alanine demo catalog atom counts contradict the public bundled inventory.
issue: uibcdf/molsysmt#677
status: resolved
opened: 2026-11-09
closed: 2026-11-09
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


## Resolution — 2026-11-09

The public inventory, manifest and both catalog descriptions agree at 22. Both original notebook code cells execute in an owned kernel with source/interpreter identity verified; code/anchors/IDs are retained and the generated HTML is inspected. Dataset and manifest bytes are unchanged.

Clean c643a728f receives 170 expanded placement/repair/writer/doctest controls,
sixteen tiny benchmark/evidence controls, fourteen fast gates and five inspected
HTML pages. Failures remain distinct, including corrected fixture assumptions.
The [core receipt](../../../devtools/data/incoming_core_receiving_677_679_680_684_20261110.json)
and [consumer receipt](../../../devtools/data/terminal_audit_consumer_receiving_679_20261110.json)
retain exact source identities and limits. This adds no weighted milestone bonus
and does not qualify installed/platform/final-candidate or addon GUI behavior.
