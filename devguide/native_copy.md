# Resident native copy contract

**Role:** normative. This document describes implemented copying boundaries.
Implementation and source qualification are recorded in the
[#121 record](archive/resolved_proposals/native_copy_protocol.md); measurements belong in
[the operational benchmark guide](benchmarking/native_copy.md).

## Supported resident operations

MolSys and Structures provide independent `.copy(deep=True)` snapshots.
`deep=False` and Python `copy.copy` instead fork protected coordinate/box
handles and replace affected blocks on writes. Canonical tables, other mutable
series and named analysis handles remain independent in both modes. Python
`copy.deepcopy` uses eager geometry and the caller's memo. No resident copy
requires form discovery, native construction, migration, inference, remapping,
serialization or disk I/O.

Topology, ChemicalStates and MolecularMechanics copy their canonical mutable
tables eagerly. Interactions independently copies handles, metadata, array
headers and lazy query/replacement state; proven immutable observation bytes
may remain shared. MolSysBuilder preserves incomplete staging without calling
`build()`. Typed payload wrappers copy their mutable payload without decoding or
validating a schema. Plain dictionary forms keep normal Python shallow-copy
semantics; they do not become molecular owners.

## Ownership and edits

A complete MolSys copy binds copied topology, structures and chemistry to the
new system. Topology remains pure inventory and never traverses a chemical
collection. MolSys binds its independently copied ChemicalStates once. Missing domains remain absent. Standalone domain
copies omit their old weak owner whether it was stored in the instance mapping
or an extension slot. The internal weak ownership link does not retain its former system.

Controlled coordinate/box writes invalidate the affected structures in the
edited copy. Controlled chemical changes and chemical-state inventory appends
invalidate every named analysis on that owner; recording preparation history
does not apply chemistry. Prior snapshots remain historical results. See
[interaction validity](interactions_api.md) for the complete mutation boundary.
Raw table/array writes and uncoordinated domain/axis changes require explicit
invalidation. This is not a general observer or a chemical dependency graph.

`msm.remove` is a coordinated subset operation: its False default returns an
independent result, while explicit True prepares a complete native subset and
then replaces the target's domains together, returning None. Old domain handles
are detached; named analyses follow extraction's source maps and coverage rather
than a new calculation. Attached standalone domains cannot be resized in place.
File inputs require an explicit independent output target. See the
[removal tutorial](../docs/content/user/tools/basic/remove.ipynb).

## Graph identity and extension data

Tuples containing only exact built-in strings are immutable and may be reused
through the memo. This avoids re-copying large relation/role catalogs one label
at a time. String subclasses, tuple subclasses and containers with mutable
members retain their ordinary copy protocols.

Python's shared deepcopy memo preserves repeated object references and cycles
across supported native domains, canonical tables, ordinary extension data and
containing containers. This means object identity, not every storage-sharing
relationship between distinct NumPy or pandas views. Copying an analysis before
its protected raw arrays is required when enclosing graph order would otherwise
replace an immutable column with mutable storage; the reverse order is refused.

Native copies preserve concrete supported subclass types without invoking their
constructors. Instance attributes and initialized slots participate in the same
memo. Slots are read and restored through their actual declaring-class storage:
parent/child slots with the same name remain distinct, private name mangling is
preserved, unset slots stay unset and iterator-declared slots are not lost.
Ordinary slot getters are not used to discover a hidden base slot. Native owner
and transient-state exclusions apply to slots as well as instance attributes.

Extensions with their own copy hooks follow those hooks and Python's memo
protocol. Native copying does not turn live files, locks, sessions or arbitrary
external resources into independently copyable data. A failing resource copy
must not transfer the source's native domain ownership. Resource reopening and
Simulation configuration/reference behavior are separate contracts.

## Tables and persistence boundaries

Canonical scalar, string, nullable and numeric molecular columns are copied
eagerly, preserving indices, IDs, dtypes and the declared chemistry. This is not
general pandas table copy-on-write. Arbitrary mutable objects inside cells and
table metadata follow pandas' own copy protocols; recursive independence and
cross-table metadata aliases are outside the qualified molecular-data boundary.
Store client metadata as ordinary extension data when shared-memo semantics
are needed, subject to its own copy protocol.

Resident extension support does not add fields to H5MSM or dictionary schemas.
Python serialization follows each class's own protocol. ChemicalStates's
name-based pickle state preserves ordinary extension slots and omits its owner;
it refuses a stored slot whose name is also declared by another class, rather
than silently losing a hidden base value. Such subclasses need their own serialization hook. Native copying
itself preserves both values and does not use that pickle state.

## Guards and qualification

- `tests/native/test_copy_boundaries.py`: canonical table aliases in both graph
  orders, slotted owner detachment/rebinding with real analysis validity,
  shadowed/iterator/private/unset slots and explicit resource/serialization limits.
- `tests/native/test_molsys_copy.py`, `test_structure_copy.py` and
  `test_remaining_copy.py` under the same directory: resident allocation modes,
  partial domains, units, extension graphs and independence.
- `tests/interactions/test_copy.py`: sparse/lazy state, immutable bytes, metadata
  and enclosing graph order.
- `tests/native/test_inherited_constructors.py`: normal validated construction
  and subsequent subclass copying. This does not register a new molecular form.

These guards qualify the named source boundaries. They do not certify every
external extension, installed client, platform, scientific profile or release.

Further investigations are tracked separately: large mutable-observable storage
in [#405](https://github.com/uibcdf/molsysmt/issues/405),
[safer mutation boundaries](pending_proposals/post_1_0_safer_native_mutation_boundaries.md)
in #407 and [representative client qualification](pending_proposals/post_1_0_native_copy_client_qualification.md)
in #408. These proposals do not extend the implemented contract above.
