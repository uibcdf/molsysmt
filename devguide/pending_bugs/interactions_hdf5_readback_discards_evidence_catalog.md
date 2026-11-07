---
summary: HDF5 interaction readback discards unused evidence labels and changes catalog codes.
issue: uibcdf/molsysmt#642
status: active
opened: 2026-11-07
closed:
severity: high
verification: inspected
area: [form, data]
guard:
normative:
blocked_by: []
supersedes: []
---

# Interaction evidence catalog fidelity on HDF5 readback

## What

DockingMT reports a complete typed-payload difference after invalidating the
only evaluated structure, copying the molecular system and writing/reading
H5MSM 0.5. The original nonempty evidence-label catalog becomes empty. The
consumer preserves both positive-to-unevaluated attempts as failed; its
already-empty-source positive control does not clear this failure.

## How

The immutable consumer source and custody manifest are published under
uibcdf/dockingmt#80 at `d71fd6b114392a95fcbbf65c78a19608d92ee79f`.
The original carrier and producer, complete pre-write/restored payloads, one-field
delta and frozen worker are linked from the provider issue. Its single delta is
`hbonds.evidence_labels`: expected `["baker_hubbard_hbond_geometry"]`, restored
`[]`. Occurrence count remains zero and evaluated coverage remains unevaluated;
no changed coordinates or lost live occurrences are asserted.

Owner inspection on published source `96b73b3f3` confirms that
`molsysmt/interactions/result.py::Interactions._read_group` reads the stored
label table but reconstructs per-occurrence strings before constructor use.
The constructor then infers a new table from only active rows. Empty or partial
usage therefore can lose unused labels and change numeric catalog positions.
The constructor already accepts an explicit evidence-label table and codes.

This is inspected owner source plus published consumer evidence, not yet an
independent current-source reproduction. Acquire the immutable relevant bytes
and/or reproduce with a small native typed fixture before correction claims.

## Why

Complete typed serialization must preserve supported evidence catalogs and
code identity, including an analysis without active occurrences. Do not repair
this by discarding metadata in DockingMT, inferring new coverage, rerunning a
detector or normalizing a catalog implicitly on load. The shared native reader
also serves standalone `.h5i`; inspect and execute that route separately.

## Plan and acceptance

1. Independently reproduce positive-to-unevaluated and partial-unused/reordered
   evidence-table readback with complete typed-payload equality, including source
   independence and unchanged evaluated coverage.
2. Preserve the actual stored label table and numeric codes through the existing
   constructor. Retain schema/version, producer/provenance, maps, units, periodic
   fields and occurrence identity; no format bump is implied by reader fidelity.
3. Exercise standalone `.h5i`, named full/interaction-only H5MSM and the public
   write/read conversion routes, including evaluated-empty and unevaluated
   controls. Test multiple labels and retained nontrivial codes.
4. Receive the supplied consumer carrier or its independently verified relevant
   payloads without weakening complete equality. Hand the published provider fix
   back to DockingMT #80 for its separate installed/client receiving.

This is the next included-workflow data-integrity priority under #334, ahead of
#640/#641 message cleanup and the next GUI expansion. No provider-local or
consumer-local workaround is accepted as resolution.
