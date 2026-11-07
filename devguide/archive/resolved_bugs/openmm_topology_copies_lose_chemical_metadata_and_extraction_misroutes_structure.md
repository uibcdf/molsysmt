---
summary: OpenMM topology copies lose chemical metadata and extraction misroutes structures
issue: uibcdf/molsysmt#626
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [form, metadata, extract]
guard: tests/form/openmm_Topology/test_copy_and_extract_metadata.py
normative:
blocked_by: []
supersedes: []
---

# Preserving OpenMM topology copy and extraction data

**Reported:** 2026-11-06 during #524 runtime receiving under #334.
**Status:** Implemented and locally received; public delivery and board closeout follow.

## What

Public `msm.copy(openmm_topology)`, unrestricted extraction, selected extraction
and same-form conversion lose formal charges and bond type/order. Literal
source charges `[1, 0, -1, None]` become all unknown. Explicit double/single
bonds become bonds with unknown type/order. A topology-only extraction with
`structure_indices=[0]` additionally returns zero atoms from a four-atom source.

## How

The manual builders in the OpenMM Topology copy/extract adapters omit chemistry
fields. Copy duplicates the unrestricted extraction builder. Extraction uses
both atom and structure arguments to choose its branch, then interprets the
string `all` as a set of characters when only structure indices were supplied.
The form has a periodic-box property but no coordinate-structure axis.

Delegate copy to the existing general extraction owner and preserve known/unknown
fields there. Ignore the structure compatibility argument consistently with
other topology-only adapters. Keep full-copy empty parents, subset compaction,
label/insertion-code identity, box units, and existing copy/alias semantics.

## Why

Stored chemistry can silently change through routine independent copies or
identity conversion, without a recalculation. Structure-only compatibility
arguments must not erase the atom domain. This is an included adapter defect,
not a limitation to conceal with a higher provider floor.

## What is measured and what is assumed

The cached `626-openmm-copy-probe.json` records literal source/results with
OpenMM 8.6.1. The OpenMM 8.2.0 receiving profile independently shows copy losing
charges after direct export succeeds. The old OpenMM 8.1.1 wheel cannot use
NumPy2 array bindings; that separate unsupported-provider failure does not prove
this owner defect. The original OpenMM declaration was unbounded.

## What was refuted

The OpenMM API floor is 8.2.0 because exports pass formalCharge. That API is
present, and the original source keeps it in direct exports; owner copy/subset
builders then discard it. This is separate from #592's proposed live Context/
Simulation/State copy semantics: the current defect concerns ordinary
openmm.app.Topology inventory/chemistry/box data, not an executed runtime clone.

## Scope and exclusions

Preserve declared atoms, groups/chains and labels, insertion codes, charges,
bond type/order and periodic box. Keep full copies of empty inventory parents,
existing external source ordering/deduplication and independent outputs. The
structure argument remains dispatch compatibility only; it creates no coordinate
axis. Do not add chemistry perception, energy evaluation, opaque Python-extension
copy promises or live-runtime cloning. Native ChemicalStates ownership is unchanged.

## Acceptance criteria

- Public copy/extraction/identity conversion preserve known and unknown charges,
  bond type/order, source labels/insertion codes and dense retained atom indices.
- Explicit structure compatibility lists do not change atom selection or alias
  policy; source objects stay unchanged.
- Box values and units, full empty-parent inventories, and empty atom subsets
  retain their independent contracts.
- Meaningful maintained counterexamples fail before repair and pass afterwards,
  including actual minimum/newer provider receiving. Public docs/doctests,
  affected checks and independently received source precede owner closure.

## Provenance

Linux x86_64; original add779264 source with existing Python 3.14.7/OpenMM 8.6.1,
plus a verified public OpenMM 8.2.0 wheel on existing Python 3.12.12. No environment
or native backend is modified by these probes.

## Resolution — 2026-11-06

Source `207d054cbc3281e43a291d759d9160ebadf61c9d`.

Copy and identity conversion now use the same extractor. Its builder preserves
known/unknown formal charges, bond type/order, label/insertion-code identity,
periodic-box values and independent objects. Explicit atom subsets remain in
source order with dense axes and deduplication. Full copies retain empty groups
and chains; atom subsets omit empty parents. The topology-only structure
argument no longer alters atom selection or unrestricted alias semantics.

A related zero-atom full-extraction failure was exposed by the same guard: the
generic group-inventory route made a native round trip and lost provider-only
insertion codes. Unrestricted same-form class extraction now remains with its
own adapter. Explicit hierarchy selections and file/string handling retain
their existing routes. The legacy MolSysDict adapter preserves the `all`
sentinel when selecting only structures, preventing that delegation change
from deleting declared atom-free groups/chains. Four controls protect both
structure selection and copy/alias/source-independence behavior there.

Before repair, the maintained 23-case OpenMM selection fails 19 and passes four
with native exit 1. The first joint attempt's XML has 49 cases but its terminal
output was lost; it is not accepted as native-exit evidence. The unchanged
counterexamples were rerun before repair with their native exit retained.
After repair, all 25 expanded OpenMM controls and the formal-charge export tests
pass in both actual public-provider profiles:2,098 cases on OpenMM 8.2.0/
Python 3.12 and the same 2,098 on OpenMM 8.6.1/Python 3.14, without omissions.
The ordinary 3.14 joint documentation/native/dependency receiving has 1,060
passes and two new fixture errors; the corrected legacy fixture separately
passes all four cases. Scopes overlap and are not additive coverage claims.

Public copy/extract/identity docstrings and the OpenMM topology form overview
now explain metadata, empty parents, source ordering and structure compatibility.
Course, Foundations and Cookbook review found no conflicting examples. All
notebook executable cells, outputs, IDs and metadata are preserved.

The shared [receiving receipt](../../../devtools/data/openmm_runtime_receiving_524_20261106.json)
retains commands, native exits, actual artifacts/import origins, original failed
attempts and documentation preservation. No shared environment or native backend
is replaced; no installed MolSysMT artifact, Viewer pair or release is qualified.
