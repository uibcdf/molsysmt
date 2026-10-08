---
summary: Promote ChemicalStates to an independent native MolSys domain
issue: uibcdf/molsysmt#254
status: partial
opened: 2026-09-29
closed:
verification: measured
area: [api, form, native]
guard:
normative:
blocked_by: []
supersedes: []
---

# Promote ChemicalStates to an independent native MolSys domain

## Published acceptance reconciliation — 2026-10-07

The [updated consumer packet](../interactions_molsysviewer_review.md#published-consumer-acceptance--2026-10-07)
records explicit acceptance from the now-closed uibcdf/molsysviewer#114 and
the published 0.23.0/0.24.0 pair's 8/8 source and 16/16 installed matrices.
Earlier awaiting-feedback statements remain historical checkpoints. This
acceptance preserves the experimental API and existing workload limits.

The issue stays partial because its criteria explicitly retain exact-1.0
release recertification. Implementation and published consumer delivery are
complete; final-candidate obligations remain under #334. No new feature is
added to the frozen scope.

## S2 acceptance reconciliation — 2026-10-05

The independent-domain, bond-authority, association, partial native-system and
public H5MSM guards passed in the 279-test Python 3.14 provider selection.
The [review packet](../interactions_molsysviewer_review.md#s2-stabilization-review--2026-10-05)
identifies the acceptance-to-guard mapping and
[dated artifact](../../devtools/data/interactions_review_packet_20261005.json).
This qualifies supported native/persistence behavior; it does not certify
every form, every public lifecycle document or an installed release candidate.
Criterion 6 still requires the applicable final checks. The proposal remains
partial; retiring `Topology.bonds` remains post-1.0 under #255.

## Current checkpoint — 2026-10-01

Independent native ownership and the public H5MSM 0.5 route are implemented.
`MolSys.chemical_states` owns the public domain; `Topology.chemical_states` is
removed and `Topology.bonds` remains a selected-state compatibility facade.
State-only and other supported partial `MolSys` combinations no longer require
inventing topology or structures. Public conversion writes 0.5, with chemical
states stored beside topology rather than nested under it. The public native
implementation and the normative [H5MSM format contract](../h5msm_format.md)
define current behavior.

Guards include `tests/native/test_chemical_states.py`,
`tests/native/test_molsys_chemical_state_association.py` and
`tests/form/file_h5msm/test_public_h5msm_v05.py`. Final lifecycle and
exact-candidate release recertification remain open; this checkpoint does not
close the proposal merely because native ownership exists. Retirement of the
remaining public `Topology.bonds` facade is post-1.0 under `uibcdf/molsysmt#255`.
The 2026-09-29 checkpoint below records the incremental migration sequence;
its early private-probe and 0.4-writer statements are historical, not the current
public contract.

## What

Make `ChemicalStates` a native information domain with one physical
authority for each state's bonds, component partition, and discrete chemical
assignments. `MolSys` must expose that domain independently of its stable
`Topology` and `Structures`. Existing `Topology.bonds`,
`Topology.components`, and state-dependent attribute access remain
compatibility facades over the selected state, without duplicating storage.

This change is part of the pre-1.0 H5MSM 0.5 modular-layer decision. The
independent file domain and the native object domain have related but
separate contracts; their implementation must be tested together.

## How

1. Define a public `ChemicalStates` class with its own ordered state
   inventory, nullable reference-state index, and explicit atom domain.
   Preserve zero, one, and multiple states; state IDs remain string labels,
   while positional indices identify states.
2. Move authoritative state storage out of `Topology`. Give `Topology` a
   single non-owning compatibility route to the collection when one is
   associated. No second bond table or inferred chemistry is allowed.
3. Make `MolSys` own the collection and the structure-to-state association.
   Copy, extract, remove, add, append, and conversion must propagate or
   explicitly reject incompatible state/domain changes.
4. Keep standalone `Topology` workflows functional through a documented
   compatibility association. A topology-only object may have no chemical
   states; access to bonds then reports unavailable chemistry rather than
   inventing an empty graph.
5. H5MSM 0.5 stores `/topology`, `/chemical_states`,
   `/structures`, and `/interactions` as optional siblings. Read legacy
   0.3/0.4 into the new native authority, and write 0.5 without duplicate
   covalent records. State-only files carry a minimal atom index domain.

## Why

The accepted ChemicalState v1 implementation stores
`Topology._chemical_states` and `Topology._reference_chemical_state_index`
privately, while `MolSys` owns a nullable structure-to-state array. That
was the lower-risk initial boundary. The pre-1.0 H5MSM 0.5 decision now
requires state-only molecular payloads and an independent
`/chemical_states` layer. Making states a native domain avoids synthesizing
a topology merely to load such a payload and gives chemistry its own
lifecycle.

Source inspection found direct private-state references in at least 32 source
modules and 16 test modules. These counts show the migration surface, not an
implementation estimate. The [architecture reassessment](attribute_centric_molecular_system_model.md#reassessment-for-the-pre-10-h5msm-05-gate-2026-09-29)
records the alternatives and their costs.

## Acceptance criteria

1. One and only one authoritative state collection owns covalent bonds.
   `Topology.bonds` and `Topology.components` resolve the same object or
   data through the selected state, with no independent copy.
2. State-only, topology-only, and full `MolSys` objects preserve absence
   versus known-empty chemistry. A multi-state object without an explicit
   reference fails visibly on ambiguous convenience access.
3. Stable atom indices, state indices, source maps, and
   structure-to-state associations survive copy, extract, remove, add, and
   append where defined; unsupported combinations fail before partial
   mutation.
4. Existing `get`, `set`, `select`, `has_attribute`, and form adapters
   preserve their accepted chemical-state semantics or receive an explicitly
   documented compatibility change with tests.
5. H5MSM 0.5 round-trips all supported partial-layer combinations and
   preserves the 0.3/0.4 migration contract. It stores no second bond
   authority under topology.
6. Public docstrings, doctests, User Guide, Cookbook, Four Paths course,
   API stability registry, dependency checks, Ruff, and exact-commit
   release gates reflect the result before 1.0.

## Dependencies and risks

- `uibcdf/molsysmt#251` and `uibcdf/molsysmt#252` cover the independent
  interaction result and its native/H5MSM integration. Neither domain may
  silently interpret an observed interaction as a covalent bond.
- A reference from `Topology` to `ChemicalStates` must not create
  independent ownership, stale aliases after copying, or duplicate
  serialization. Standalone topology and legacy pickle migration need tests.
- Chemical states encode discrete graphs and assignments. Continuous
  electronic observables are not silently moved into this domain.

## Implementation checkpoint (2026-09-29)

The first native slice now exports `molsysmt.ChemicalStates` and stores the
ordered state records in that collection. `Topology.bonds` and
`Topology.components` remain facades over the reference state, while
`MolSys.chemical_states` exposes the domain. A standalone collection can represent zero
states and can append empty states. Copy, atom extraction, pickle restoration,
legacy H5MSM 0.3/0.4 reading, and builder growth have focused coverage.

The broad native and conversion selection covering `tests/native`,
`tests/form/file_h5msm`, `tests/form/molsysmt_Topology`,
`tests/form/molsysmt_MolSys`, and native dictionary adapters passed after
the migration. The H5MSM 0.4 loader needed to size its atom domain before
loading state records; the builder needed to advance the domain when adding
an atom. These were real ordering dependencies exposed by the new validation.

This is **not yet the completed independent-domain contract**. A native
`MolSys` still requires a `Topology`, and standalone `Topology` keeps an
internal `ChemicalStates` reference to support its bond facade. H5MSM still writes the 0.4
layout with states nested under topology. A 0.5 writer and reader, partial
layer combinations, and interaction persistence remain required before this
proposal can close. Do not report the 0.4 compatibility tests as evidence of
0.5 support.

The native `ChemicalStates` and typed `ChemicalStatesDict` are now registered
as experimental Tier 3 forms. Their `msm.convert()` round trip preserves the
atom domain, ordered states, nullable reference, state metadata, component
membership, covalent bond columns, atom attributes, dtypes, and explicit null
masks without a topology payload. The dictionary uses NumPy columns and is
not directly JSON-compatible. This in-memory form does not satisfy the
separate H5MSM 0.5 persistence gate.

Direct conversion from a complete `Topology` or `MolSys` to either form now
copies the chemical-state collection. Contract tests exercise both sources,
both targets, state and bond preservation, copy independence, and rejection of
an atom selection that cannot yet be remapped by these converters.

The next private H5MSM 0.5 probe writes `ChemicalStates` at root
`/chemical_states`, with a versioned layer schema and explicit local atom
count. It round-trips without a topology group, including zero or multiple
states, nullable columns, and an absent reference state. It can coexist with
the independent `/interactions` probe. The existing 0.4 path still creates
its legacy compatibility links and passes its regression tests. This is a
codec experiment, not a public 0.5 reader or writer; `MolSys` ownership and
the complete optional-layer contract remain open.

The public `Topology.chemical_states` property was removed during this
pre-1.0 migration. `MolSys` now holds an explicit reference to its
`ChemicalStates` object, synchronized with the topology's private
compatibility reference. Replacing `MolSys.chemical_states` updates the bond
facade. A topology already attached to one `MolSys` cannot be assigned to a
second without copying it. This does not yet enable a topology-free `MolSys`
or complete the independent-domain contract. `Topology.bonds` remains public
through 1.0; its proposed post-1.0 retirement is tracked by
`uibcdf/molsysmt#255`.

A private 0.5 state-only reader now constructs a native `MolSys` without
inventing a topology or an empty structures layer. The partial constructor
validates the atom domain, and copy and pickle preserve the absent layers.
Tests distinguish zero states from one empty state and verify that covalent
records survive a state-only file round trip. This is a narrow ownership
probe: the public `MolSys` form adapters still assume topology for many
operations, and the 0.5 file form is not registered publicly. Those routes
must be made domain-aware before a partial `MolSys` is advertised as a
supported general-purpose object.

The topology-free probe now also round-trips a native object containing
chemical states, atom-aligned structures, a nullable structure-to-state
assignment, and named sparse interaction analyses. Shared atom and structure
axes require declared identity links. A missing or reordered link is rejected
instead of guessing a remapping. Frame-only structural data can coexist with
the chemical-state atom domain without inventing a structural atom axis.
Copy and pickle preserve this topology-free combination. The native object
still cannot represent the distinction between an absent interaction layer
and a present-empty interaction collection, so the reader rejects the latter.

The `molsysmt.MolSys` form adapter now checks domain presence before
delegating attribute availability. For these experimental partial objects,
public `msm.get` can return the atom count, chemical-state inventory,
available structural series, and structure-to-state indices; requests for
attributes of absent domains return `None`. Direct conversion to a missing
native topology or structures domain fails explicitly. The registered
`file:h5msm` writer remains 0.4 and rejects partial native systems before
creating a file. `MolSysDict` 0.1 also rejects them because its schema
requires both domains. Explicit state selection and topology-dependent
chemistry queries still require the remaining adapter work.
The public `get` path also now preserves a missing chemical-state ID as
`None` instead of the string `"None"`; the nullable-ID behavior has a
focused regression test.

The native partial-domain constructor and private H5MSM 0.5 probes now retain
an absent `ChemicalStates` layer as `None`. Topology-only,
structures-only, and topology-plus-structures payloads preserve that absence
through file round trips, copy, and pickle. A topology carrying private
chemical-state records cannot be mislabeled as chemistry-absent. Frame-only
structures keep their atom count unknown, distinct from a known zero-atom
axis. A separate topology-plus-chemical-states probe completes native
round-trip coverage of the seven primary presence combinations. Public
file-form registration, optional interaction-only combinations, edits,
and lossless handling of additional fields remain open.
