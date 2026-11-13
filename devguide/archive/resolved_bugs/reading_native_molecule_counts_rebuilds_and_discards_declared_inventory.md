---
summary: Reading native molecule counts rebuilds and discards declared inventory
issue: uibcdf/molsysmt#740
status: resolved
opened: 2026-11-12
closed: 2026-11-12
severity: high
verification: reproduced
area: [native, attribute]
guard: tests/form/molsysmt_Topology/test_readonly_inventory_counts.py
normative: devguide/native_queries.md
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
chemistry or change scientific detectors. The count fallbacks and applicable nullable parent projections are corrected
in the working source. The affected runtime cohort has completed; documentation receiving and final
checks remain due before closure.

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


The [owning investigation receipt](../../../devtools/data/native_nullable_membership_receiving_739_20261112.json)
retains the independent labelled-row witness and exact execution metadata.
This remains a failed preservation control; #739 receiving does not close it.


## Bounded correction in progress — 2026-11-12

The getter audit finds exactly two destructive rebuild calls in the native
Topology query adapter: molecule and entity system counts. Both are removed.
Declared counts include unused parent rows, remain live after explicit inventory
edits and do not clear dirty flags. Native MolSys wrappers and get/info/select/
label-edit preflights reuse these corrected owners; explicit rebuild methods
and their local inference helpers are unchanged.

Applicable single-parent reads reveal an additional twelve-case failure after
the count fix: missing group-to-molecule, group-to-entity and molecule-to-entity
links become invalid NumPy index arrays. Twelve existing getters now share a
private vectorized stored-parent reader with the existing atom lookup formatter.
They preserve source order/repetitions and return None for unknown index, ID,
name and type values. No missing parent is reconstructed or used as position 0.
Many-to-many chain/group traversal and foreign/dictionary finalization keep their
separate contracts; no chemical owner, dependency floor or kernel is changed.

The first 32-case draft includes eight invalid fixture attempts to replace an
attached four-atom topology with an atom-free topology. The native shared-axis
guard correctly refuses those. A separately constructed atom-free fixture gives
a valid baseline of 27 failures and eight controls. After removing the two
count fallbacks, 33 cases pass and two test-side entity-plural lookups fail;
correcting that lookup preserves the intended all-table source comparisons.
The parent-read baseline then has twelve IndexErrors and 43 passes. These raw
outcomes are retained rather than relabelled or discarded.

The expanded receiving passes 76 cases without warnings or omissions, including
stored parent names/types, unknown/zero parent inventories, empty selections,
nonconsecutive/repeated queries, live counts and deterministic public docstrings.
Those are bounded contract controls, not a complete-source, installed, scientific
or final-pair certificate. Relevant existing reconstruction/conversion tests and
updated documentation receiving are the next checks.

## Affected cohort and supervisor recovery — 2026-11-12

The wider native Topology adapter, hierarchy/query/selection and basic summary
cohort completes with 1,566 passing cases, no failures/errors/omissions and three
expected legacy H5MSM warnings. Its pytest child exits 0; the completed durable
record, JUnit and independently rechecked 8,158 input hashes agree. Peak service
memory is 573,022,208 bytes with no own swap or OOM; minimum observed host
available memory is 13,734,129,664 bytes. Brief host memory full-pressure avg10
reaches 1.02 and subsides without crossing the reserve.

A tool-server restart interrupts the original interactive output connection.
The exterior service subsequently exits 120, with MainPID 0. That supervisor
result is failed and is retained separately from the successful pytest child;
no preserved traceback establishes the exact output/flush failure stage. The
passing cohort is not rerun merely to replace this operational evidence. Later
receiving uses a detached service with durable logs and an independently checked
terminal supervisor result. Neither this recovery nor the bounded tests supply
a complete-source, installed or final-candidate gate.

## Resolution — 2026-11-12

Source a3cf6b3a5 corrects both native count fallbacks and the twelve applicable
nullable parent getters. The module guard compares every stable table and both
dirty flags around public/native count, info and selection reads, then checks
independent expected inventories and parent values. A deliberate label edit
changes only its addressed label. Live inventory changes, atom-free/empty rows,
unknown parent indices/IDs/names/types and repeated/nonconsecutive selections
are covered. This catches the original data loss rather than merely checking
a count's type or agreement with an already-mutated source.

Five affected actual HTML articles build without warnings. Receiving verifies
the new read-only explanation, all 160 local destinations, four intended
canonical get/info alias links and no unlinked API roles. All 100 complete
executable notebook cells, outputs and metadata are unchanged. The maintained
native query/conversion contracts and User Guide, course and Cookbook now
distinguish reading declared inventory from explicit reconstruction.

Fifteen offline fast gates and repository Ruff checks pass. The later detached
checks, HTML and article services have independently verified terminal exit 0;
the earlier cohort's exterior exit 120 remains a failed supervisor event, not
a passing release gate. The
[receiving receipt](../../../devtools/data/native_inventory_read_receiving_740_20261112.json)
preserves native results, input fingerprints, provider provenance, resource
limits, fixture mistakes and the recovery. No new dependency, native binary,
scientific algorithm or serialized format is introduced. Final scientific,
complete-source/nightly, installed-pair and publication gates remain separate.
