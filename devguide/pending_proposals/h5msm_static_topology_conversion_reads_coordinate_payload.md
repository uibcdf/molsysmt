---
summary: Avoid reading coordinate payloads for whole H5MSM topology conversion.
issue: uibcdf/molsysmt#655
status: active
opened: 2026-11-08
closed:
verification: measured
area: [convert, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Static topology conversion reads an unrelated structural layer

**Reported:** 2026-11-08, while preparing the accepted sequence-fit GUI intent
under #421. **Status:** bounded baseline reproduced; implementation is pending.

## What

A complete, coordinate-free `msm.convert(path, to_form='molsysmt.Topology')`
currently enters modular resident MolSys loading before choosing its target.
Reuse the existing topology-layer reader for an admitted whole-topology request.
This is a conversion optimization, distinct from #643's delivered query route.

## How

On clean public source `2325038e8c68157f5c730693ffbb8535f0b45540`, the bounded
probe writes 5,000 structures by 62 atoms, then intercepts HDF5 dataset access.
The conversion attempts `/structures/coordinates` with
`slice(0, 704, None)`, despite requesting only Topology. The first payload read
is rejected before allocation. `basic.convert` calls
`maybe_read_modular_h5msm` before target dispatch; that helper unconditionally
calls the resident modular reader.

Initially admit only a scalar path, the Topology target, all atoms/structures,
canonical syntax and no strict/report/naming/extra converter options. Preserve
other conversion routes. Read the stored topology in its own declared index
space, without joining unrelated chemical, coordinate or interaction axes.
Retain the existing missing-topology error and selected-layer validation.

## Why

A sequence-guided reference needs stable group/name context alongside one
selected coordinate slab. Converting that context must not first read the
unrelated trajectory. Keeping the optimization at the conversion boundary
makes it useful to every consumer rather than adding a GUI-specific reader.

## What is measured and what is assumed

- The corrected native-class fixture fails at the first coordinate read:
  one failing case, 2.83 seconds of pytest, peak charged service memory
  217,378,816 bytes; no resource-cap or OOM event.
- Registered source inputs remain unchanged. The private receipt retains the
  bounded one-CPU/two-GiB invocation and exact source/backend fingerprints.
- The initial fixture instead used the unexported `msm.Structures` spelling and
  failed before the intended observation. It is retained separately and is not
  evidence of this conversion behavior.
- No complete-series I/O, unbounded-RAM or throughput benchmark is claimed.
  The source reader uses blocks; an attempted first block does not measure a
  whole execution. The intended improvement is absence of unrelated payload I/O.

## What was refuted

Using another image/sequence implementation in the GUI does not solve static
input loading. A blanket domain-only conversion could change spatial selection,
explicit structure scopes, reports or naming overrides; those routes remain
unchanged until separately received. No new H5MSM format version is necessary.

## Scope and exclusions

Receive complete native Topology conversion from a single H5MSM 0.5 path with
default whole-domain arguments. Static tables and their validation may still be
read in full; this is not a universal constant-memory conversion claim. Other
requested targets, selections, reports, overrides and composite inputs keep
the existing semantics. No chemical preparation, association inference,
scientific algorithm, optional engine or public parameter is added.

#604 remains a separately queued pairwise/clustering capability. This step does
not implement it, alter frozen release gates or add a progress-scorecard leaf.

## Acceptance criteria

1. The admitted route reads no coordinate, chemical-state or interaction payload.
2. All stable tables, string IDs, naming declarations and detached ownership are
   preserved. Missing/corrupt topology fails before unrelated payload reads.
3. String/Path inputs, absent optional domains and an active nondefault unit
   policy retain the contract. Unrequested layer validation stays distinct from
   complete-file validation.
4. Explicit selection/report/naming/option and legacy/native/composite routes
   retain their previous behavior.
5. Receive focused conversion/form/ownership regressions, applicable governance,
   docstrings and documentation/course references, with exact scope and all
   failed attempts preserved before public delivery and closure.

## Dependencies and risks

The existing modular reader and native Topology own decoding. ArgDigest and
SMonitor remain at their public boundaries; the private helper has no decorator.
No new optional-dependency or scientific-attribution boundary exists. Maintain
original index spaces and avoid changing spatial-query or report semantics.
