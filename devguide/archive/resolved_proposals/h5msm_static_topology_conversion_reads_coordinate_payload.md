---
summary: Avoid reading coordinate payloads for whole H5MSM topology conversion.
issue: uibcdf/molsysmt#655
status: resolved
opened: 2026-11-08
closed: 2026-11-08
verification: measured
area: [convert, performance]
guard: tests/form/file_h5msm/test_topology_v05_probe.py::test_default_topology_conversion_reads_no_other_layer_payload
normative: devguide/SCALABILITY.md
blocked_by: []
supersedes: []
---

# Static topology conversion reads an unrelated structural layer

**Reported:** 2026-11-08, while preparing the accepted sequence-fit GUI intent
under #421. **Status:** source-qualified; public delivery and board closeout are recorded separately below.

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

## Tracked-guard fixture admission

The first tracked negative run stops in fixture writing because its explicit
association omitted the required source_name/target_name keys. It executes one
of two parameter cases under maxfail and does not reach conversion. The fixed
fixture declares both unnamed endpoints explicitly; this changes no public
implementation or payload-read assertion. Keep both negative attempts.

## First directed receiving

The first integrated profile passes 103/109 cases. Six new table comparisons
fail because hand-built fixtures assigned ID columns as object dtype, while
native loading correctly restores the canonical pandas string ID dtype. The
corrected expected tables explicitly normalize only ID columns and retain full
DataFrame dtype/value/index checks. No production output, coordinate/I/O guard
or unrelated field is relaxed. Existing native/legacy ownership and naming
cases remain in the same profile; preserve the original six failures.

## Corrected directed receiving

All 109 selected tests pass after canonicalizing expected ID columns only.
The one-CPU/two-GiB service peaks at 271,421,440 charged bytes, observes at least
16,212,611,072 available host bytes and records no cap, OOM or reserve stop.
The declared working tree is unchanged during execution; this is local source
receiving, not installed-package or full-suite evidence. Final clean-source
qualification and public delivery remain pending.

The whole-Topology target now has the same stored-only meaning as the existing
single-layer reader. For old group-free topology layers 1/2 whose molecule
membership exists only in associated reference chemistry, that membership stays
unknown in this projection. A joint `MolSys` load remains the supported legacy
reconstruction; the existing migration test now contrasts both public routes.
This is an explicit projection boundary, not a claim that implicit legacy
reconstruction can be retained without chemistry.

## Resolution — 2026-11-08

Accepted as a bounded stored-topology projection in source
`10d43b2a92a45b85b4a742a06b2548fce165dd6c`. The existing public selected-layer
reader owns decoding; conversion admits only the documented default whole-domain
case. No chemical reconstruction is hidden inside this coordinate-free target.

Clean receiving passes **1,181 cases**, including the public convert doctest,
legacy files, modular queries, naming, ownership, complementary inputs and reports.
The HDF5 guard rejects every structural, chemical-state or interaction dataset
access during the admitted route; the pre-change tracked guard fails at the
first coordinate read. Positive tables, canonical string IDs, naming declarations,
missing/corrupt topology, nm/pm session policy and contextual fallbacks are checked.
The old group-free migration case contrasts projection with joint reconstruction.

Fourteen fast gates and HTML compilation pass on that same clean source. Five
rendered pages retain the scope and limits, and both edited notebooks retain every
executable cell and saved output. Six existing HTML title warnings are unchanged.
Whole-tree Ruff check and format check pass. All 8,567 owner inputs (including the
unchanged Rust binary) and 2,463 verified Viewer-export inputs are unchanged in
each final run. No runtime Viewer change or graphical-intent credit is claimed.

The source service peaks at **820,248,576 bytes**, fast checks at **417,345,536
bytes** and HTML at **1,337,757,696 bytes**. Individual one-CPU/two-GiB caps and
reserve monitors remain active during their brief overlap; no cap/OOM/reserve
stop occurs. These are receiving costs, not conversion throughput or total-memory
benchmarks. The portable [receipt](../../../devtools/data/h5msm_static_topology_receiving_655_20261108.json)
retains all seven pytest attempts, commands, outcomes, fixture corrections,
resources and fingerprints. Public-delivery identity is maintained in the
[release ledger](../../release_1_0_status.md) after publication. #604 and the
requested OpenMM/openmmtools capability study remain separate queued work.
