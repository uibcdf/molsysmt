---
summary: Form tutorial API roles render as unlinked code despite a warning-free build
issue: uibcdf/molsysmt#727
status: partial
opened: 2026-11-12
closed:
severity: medium
verification: reproduced
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Receiving actual form implementation links

## What

Native form tutorials use Python func/mod roles for adapter objects that have
no indexed Sphinx API target. Full strict HTML can finish with zero warnings
while those references render as unlinked code. Actual compiled MolSys,
Topology and Structures operation/conversion tables show this defect. Link
inspection that considers only existing hrefs cannot detect missing intended
links, even when every link it sees resolves.

## How

Complete HTML on 1b98c2b1d and targeted MolSys receiving on 2bf21835f finish
with zero warnings. Inspect actual article tables: their implementation and
converter references have code.xref elements without enclosing anchors.
The source objects exist; their existence is different from a rendered link.
The bounded #725/#726 article proof remains valid for its 130/16 actual local
destinations, not for unlinked intended API references.

## Why

Users cannot follow the advertised API/implementation references. A good guard
must check the intended references, not accept an empty/partial set merely
because the existing links resolve. This is owning documentation/indexing debt,
not a demonstrated Sphinx provider bug or a scientific/runtime failure.

## Partial correction and acceptance

The MolSys tutorial now replaces all 57 role occurrences with clearly labelled
links to immutable published owning source/docstrings. Every operation/module
and registered conversion route must retain its real source destination; this
is not a new placeholder API page. Keep general user APIs linked to indexed
Sphinx targets. Runtime attribute/delivery, H-count semantics and bond ownership
retain #726's separate guards. Actual HTML must contain every intended source
link and no unlinked adapter role; source/reference existence alone is insufficient.

Topology and Structures retain this unlinked-reference debt; the wider form
inventory is not yet audited. Continue per-form review before claiming full
closure, respecting live route limits, source identities, supported signatures,
conversion declarations and notebook code/output preservation. No shared guide,
provider, dependency floor, scientific algorithm or release is changed.

## Evidence and next action

Private before-DOM counts, exact role/source map and corrected source/HTML
receiving belong to the #725/#726 combined receipt. Its declaration-only source
checks do not claim installed/provider execution for every optional converter.
Close this issue only after the remaining intended form references are audited
and repaired or explicitly scoped with an owned disposition.
