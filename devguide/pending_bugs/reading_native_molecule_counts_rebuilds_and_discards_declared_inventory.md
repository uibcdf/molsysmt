---
summary: Reading native molecule counts rebuilds and discards declared inventory
issue: uibcdf/molsysmt#740
status: open
opened: 2026-11-12
closed:
severity: high
verification: reproduced
area: [native, attribute]
guard:
normative:
blocked_by: []
supersedes: []
---

# Count queries must preserve declared native inventory

## What

A system-level molecule count query on a native Topology with explicit molecule
rows but unknown group-to-molecule links reconstructs the molecule table.
Two labelled rows become one inferred row. The same inference was observed
indirectly during a public parent-edit selection while isolating #739.

```python
import pandas as pd
import molsysmt as msm
from molsysmt.native import Topology

molsys = Topology(n_atoms=4, n_groups=2, n_molecules=2, n_entities=2)
molsys.molecules['molecule_id'] = pd.array(['declared-0', 'declared-1'], dtype='string')
msm.get(molsys, element='system', n_molecules=True)
# 1; molsys.molecules now has one row with molecule_id '0'.
```

## How

molsysmt/form/molsysmt_Topology/get_topological_attributes.py contains a legacy
fallback in get_n_molecules_from_system: missing group molecule links trigger
rebuild_molecules(force=True). The read discards existing stable inventory and
labels. Review analogous count/parent-read fallbacks within their applicable
native scope; do not infer their complete impact from this one witness.

## Why

Native Topology owns stable inventories. Unknown parent links are not evidence
that explicitly declared molecule rows should be replaced. System counts must
not erase labels or change later selection cardinality. Queries, reconstruction
and scientific perception need distinct responsibilities, including partial
systems. This is a pre-1.0 data-integrity finding; it does not request a new
scientific algorithm or a downstream BindingMT workaround.

## What is measured and what is assumed

The bounded witness has native exit 1 because its read-only preservation
assertion fails. Before: n_molecules=2, IDs declared-0/declared-1. Returned
count: 1. After: n_molecules=1, ID 0. The retained runtime uses pandas 2.3.3.
Only an ephemeral four-atom object is mutated; repository inputs are unchanged.
The command runs in the existing one-CPU, 1.5-GiB, zero-own-swap service and
uses about 116 MiB, with no host memory pressure.

The original observation came from a missing-parent fixture during #739.
A fully declared fixture isolates that independent nullable-setter defect.
The separate labelled-row witness establishes this read-side data loss; it is
not dismissed as a fixture error or fixed by weakening the expected inventory.

## Scope and exclusions

First cover system inventory counts and public native selection preflights,
then inspect related native parent reads for the same destructive fallback.
Retain explicit rebuild operations for callers intentionally requesting
reconstruction. Do not broaden optional-engine conversions, invent missing
chemistry or change scientific detectors. No fix or final receiving is claimed.

## Acceptance criteria

- Native count reads preserve all existing tables, labels, row counts and absent
  memberships, including partial native systems and empty declared parent rows.
- MolSys and Topology, native get/info and applicable public preflight paths
  follow the stable-inventory contract.
- Parent projection does not replace missing correspondence with silent
  reconstruction; explicit rebuild operations retain their separate behavior.
- Regressions compare source tables before/after reads and verify independent
  expected counts, not only output types or count self-consistency.
- Review relevant conversion/reconstruction callers and update maintained
  documentation without reintroducing a chemical facade on Topology.

## Provenance

2026-11-12 local date, shared Linux host, Python 3.14.7, pandas 2.3.3 and retained
support-provider composition. Source is the active 97b688c61-based checkout;
#739's setter edits do not change the getter owner. The witness and its exact
execution/input hashes are retained with the #739 investigation record. Work
order: finish #739 receiving, address this defect, then resume #727's remaining
external class articles. Existing final-pair qualification/publication pause
and original milestone accounting remain unchanged.
