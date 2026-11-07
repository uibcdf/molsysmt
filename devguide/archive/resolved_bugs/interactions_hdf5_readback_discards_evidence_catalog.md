---
summary: HDF5 interaction readback discards unused evidence labels and changes catalog codes.
issue: uibcdf/molsysmt#642
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: high
verification: measured
area: [form, data]
guard: tests/interactions/test_evidence_catalog_persistence.py::test_complete_evidence_catalog_payload_survives_all_public_storage_routes
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

Owner reproduction against baseline `26e2793d629c17bda6f9e670ad24a95d272c059a`
fails 32 of 48 small public-route cases; the 16 genuinely empty/full-use controls
pass. The failures independently establish unused-catalog loss under both
normal and pm/fs policies, rather than inferring the outcome from source.

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

This included-workflow data-integrity correction takes priority under #334,
ahead of #640/#641 message cleanup and the next GUI expansion. No provider-local
or consumer-local workaround is accepted as resolution.

## Resolution and executed receiving — 2026-11-07

The shared reader now passes the stored integer evidence column and complete
label table to the existing typed constructor. It no longer reconstructs that
catalog from strings on active rows. Constructor/ArgDigest integer, dtype and
int32-range checks precede conversion; cross-column code bounds remain checked.
No schema, detector, chemical assignment, scientific profile, dependency or
compiled backend changes. Stored producer versions are not replaced by the
version reading the file.

The [portable receiving receipt](../../../devtools/data/interaction_evidence_catalog_receiving_642_20261107.json)
records commands, identities, original failures and immutable input digests:

- **56 new regression cases:** 48 combinations of four public routes, six
  catalog/coverage states and two unit policies; five malformed stored-code
  rejections; three legacy interaction-codec-1 controls. Equality checks all
  typed dictionary fields, array shapes/dtypes and list/tuple distinctions.
  The guard fails on the original reader; matching active query rows alone
  cannot satisfy it.
- **3,098 integrated cases pass**, native exit 0, including all 56 new cases,
  interaction queries/edits/copying, standalone persistence, full/layer H5MSM,
  native dictionaries and geometry/chemistry-edit invalidation. Existing 719
  warnings retain their original scopes: 702 legacy-format warnings and 17
  deliberate small-memory-budget controls. These are not omitted tests.
- **11 result-module doctests pass**, native exit 0, after docstring updates.
  An earlier directed 194-case pass overlaps the integrated selection; counts
  must not be added as independent coverage.
- **Eight real-carrier route/policy checks pass:** both named analyses retain
  their complete typed payloads through standalone `.h5i`, layers, full-system
  write/read and public convert, under nm/ps and pm/fs policies. Full-system
  routes also retain coordinates and the complete chemical-state payload.

### Independent consumer custody and scope

The owner verifies the original manifest SHA-256 plus six relevant compressed
members and their decoded bytes at consumer source
`d71fd6b114392a95fcbbf65c78a19608d92ee79f`. This is not a claim to have independently
verified all 210 manifest entries. The original positive carrier is separately
verified at `daa6da9cecad53eddbb83663b8d3ffec2e431097`; all seven stored/decoded
hash pairs are retained in the receipt.

Reading the already-written failing carrier with the corrected reader now
matches the consumer's entire immutable pre-write diagnostic payload. The owner
also receives the original positive 3,238-atom/one-structure carrier, invalidates
hbonds publicly, copies and reassociates it, and verifies every field against
that same pre-write export. A subsequent typed recursive comparison protects
both analyses on every new route, including dtype, shape and sequence type.
Original source objects and all retained immutable input bytes remain unchanged.

No detector, preparation, docking search, energy calculation, client wheel or
viewer is rerun. The producer remains
`5952053328aac6f737e22906e984c0f9eb938dd7`, with its stored MolSysMT version
`0.23.0+368.g00abb958f`. Both historical consumer failures retain their failed
status; this new provider-source receiving does not rewrite their outcomes or
qualify the consumer's installed binding. DockingMT #80 retains that acceptance.

Binary acquisition initially fails through UTF-8-only transport. The successful
route obtains GitHub Contents API JSON/base64, then verifies compressed/decoded
digests before molecular operations. An initial standalone probe import of a
pytest-only test namespace fails before molecular work; the corrected audit
probe uses its own explicit typed comparison. The first passing probe's JSON
content comparison and hbonds-only standalone scope remain distinct from the
subsequent eight complete typed/two-analysis checks. These authoring/transport
attempts are retained, not treated as library failures or successful receiving.

The normative contract, public save/load docstrings, User Guide, Cookbook and
native-forms course now describe full catalog/code preservation after
invalidation. Course code cells and saved outputs are unchanged. Final local
governance, HTML and clean-source scientific checks are tracked in the delivery
receipt; package/platform/client-session acceptance remains separate.
