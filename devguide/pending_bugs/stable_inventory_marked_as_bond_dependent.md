---
summary: Bond-requirement metadata marks stable inventory as connectivity-dependent.
issue: uibcdf/molsysmt#534
status: open
opened: 2026-11-03
closed:
severity: medium
verification: reproduced
area: [attribute, basic]
guard:
normative:
blocked_by: []
supersedes: []
---

# Stable inventory and bond-requirement metadata disagree

**Reported:** MolSysViewer's provider-owned metadata facade under
uibcdf/molsysviewer#264 and uibcdf/molsysmt#421.
**Status:** independently reproduced; dependency-contract review is pending.

## What

On source 27c6bd3c0b4adfc1b7c3b635b9f30bcf6ffa0cab, pure Topology reads
`molecule_index`, `molecule_id` and `entity_index` from atoms, and `atom_index`
from molecules. The public `bonds_are_required_to_get_attribute` helper returns
True for all four, despite the absence of a chemical facade and the stable
inventory classification.

## How

`molsysmt/attribute/bonds_are_required_to_get_attribute.py` lists stable molecule,
entity and some chain attributes alongside chemical fields. Its source-element
list also treats every molecule/entity query as bond-dependent. The helper is
used in planning and foreign-form selection; actual failures in each consumer
have not been established by this metadata reproduction.

## Why

Provider metadata must distinguish stored stable membership from state-local
components/connectivity. A consumer must not infer a chemical prerequisite or
restore Topology chemical storage to compensate for an inaccurate declaration.

## Acceptance and boundaries

Review the distinction between reading stored fields and constructing missing
inventory in a foreign conversion. Cover all stable element axes with independent
expected requirements, plus bonds/components and the source-element axis.
Exercise pure Topology, absent chemistry and zero-state chemistry and affected
get/selection planning. Preserve genuine graph prerequisites. Do not change a
static list without checking the callers' inference contract or equate stable
molecules with chemical components. No correction is implemented by this report.

## Provenance

2026-11-03, Linux, existing Python 3.14.7 development environment. Public native
queries on the bundled pentalanine H5MSM source reproduce all four cases; its
legacy-format warning is expected. No Viewer or consumer-side normalizer is used.
