# Native Structures Contract

**Status:** normative for `molsysmt.Structures` and structural-growth tools.

## Representation

`Structures` represents zero or more observations along one shared structure
axis. A representation may be deliberately limited: coordinates are not
required, and a time-only, box-only, velocity-only, or thermodynamic-only
object is valid. `n_structures` is inferred from every materialized
frame-aligned attribute rather than only from coordinates, velocities, or box.

The following attributes are frame-aligned when present:

- `structure_id`, `time`, `coordinates`, `velocities`, and `box`;
- `b_factor`, `alternate_location`, and `occupancy`;
- `temperature`, `potential_energy`, and `kinetic_energy`.

Every materialized attribute must have the same first-axis length. Coordinates,
velocities, B factors, and occupancy also share one atom axis. Absence means
that an attribute is unavailable for the complete object; it never means that
an untracked suffix or prefix of frames has values.

## Validation boundaries

Construction validates all supplied series even when argument digestion is
skipped. `n_structures`, `n_atoms`, and append operations also validate the
current object so a later direct assignment cannot hide an inconsistent state.
Misaligned constructor or existing-object state raises
`StructuralInconsistencyError`; inconsistent lengths in one append payload
raise `ArgumentLengthError`.

## Transactional append

`Structures.append()`, `append_structures()`, and `concatenate_structures()`
validate the current object, the complete incoming block, atom-count
compatibility, and attribute availability before mutation. Failure leaves the
target unchanged.

The `attribute_policy` argument controls attributes present in only one block:

- `intersection` is the default. The result retains only attributes available
  in both blocks and emits one `StructuralAttributeDropWarning` listing the
  discarded series.
- `strict` rejects one-sided attributes without changing the target.

Two non-empty blocks must share at least one frame-aligned attribute. Otherwise
intersection would erase the only evidence for their structure axes, so the
operation is rejected.

Incoming topology remains optional. Coordinate-only XTC, DCD, XYZ, and native
structures may be appended when atom counts agree; atom ordering is then the
caller's responsibility. This rule is independent from chemical-state
association. A classical system with one chemical state continues to associate
new structures with that state implicitly.

## Atom-axis addition

`Structures.add()` combines systems along the atom axis while preserving the
existing structure axis. Coordinates, velocities, B factors, and occupancy are
handled as one aligned family:

- an attribute available in both inputs is concatenated on axis 1;
- an attribute available in only one input is dropped with one
  `StructuralAttributeDropWarning` under the default `attribute_policy='intersection'`,
  or rejects the operation under `'strict'`;
- structure-count mismatch is rejected before mutating the target;
- a source carrying no structural series at all is a topology-only addition. It has no
  structure axis to disagree about, so the count comparison does not apply and the
  target's atom-aligned series are dropped by the ordinary one-sided rule;
- the complete candidate payload is validated before assignment.

This is the same intersection rule used for structure-axis append. MolSysMT 1.0
does not represent a B factor, occupancy, velocity, or coordinate array that is
available for only a prefix or suffix of the combined atom axis.

Structure-aligned data is not one family, because adding atoms does not affect all of
it the same way. The rules follow from what each value describes:

- **The structure axis keeps its identity.** `structure_id`, `time` and `time_step`
  remain the target's: `add()` extends the atom axis and leaves the structure axis
  untouched.
- **The periodic box remains the target's**, because `add()` never reinterprets the
  unit cell. When the two inputs disagree, or when only one of them is periodic, an
  `IncompatibleBoxWarning` (`MSM-WARN-STRUCT-007`) reports it. Coordinates expressed
  under a different cell are not comparable, and combining them silently would hide
  that.
- **`temperature`, `potential_energy` and `kinetic_energy` are dropped** whenever atoms
  are actually added, and reported in the same `StructuralAttributeDropWarning`. They
  describe the system as a whole, the system changed, and neither target precedence nor
  any additive rule would make the old value describe the new system. They survive only
  when nothing was added — an empty selection leaves the system unchanged.
- **`alternate_location` is atom-aligned in meaning** although it is stored per
  structure: its content is a mapping keyed by atom index. The source's entries are
  merged with their keys shifted by the size of the target's atom axis.

`MolSys.add()` extends this to the state the structures payload does not reach:

- **Bioassemblies from both systems are combined**, with the incoming `chain_indices`
  shifted by the target's chain count — assemblies are keyed by chain, not by atom. An
  incoming identifier that already exists is renamed and reported with a
  `BioassemblyIdentifierCollisionWarning` (`MSM-WARN-STRUCT-008`); identifiers are source
  data and are not required to be unique across systems.
- **`atoms_ff` is atom-aligned** and therefore governed by `attribute_policy`. When both
  systems carry force-field parameters the tables are concatenated; when only one does,
  the combined table would parameterize part of the atom axis, so the whole molecular
  mechanics block is cleared under `intersection` and the operation is rejected under
  `strict`. A partially parameterized system is not parameterized.

`add()` takes one target and one source. A list is one molecular system split into
complementary items, exactly as `convert` reads it, and is assembled before the
addition. A composite target cannot be grown in place, because the assembled result is
a new object.

**Only `molsysmt.MolSys` and `molsysmt.Structures` accept an addition.** The dispatcher
selects the implementation by the *target* form, and every other adapter declares the
bounded limitation by raising the catalogued `NotImplementedMethodError`. A source may
be given in any form: it is converted to the target's form first. Adding a third target
form is a contract change and needs its own delivery tests;
`test_only_two_forms_implement_add` pins the current set so it cannot grow by accident.

These rules were decided by the [atom-axis `add()` semantic
audit](archive/resolved_proposals/atom_axis_add_semantic_audit.md) as D1-D7 and are guarded by
`tests/basic/add/test_add_audit_decisions.py`.

## Deferred partial-series model

Version 1.0 does not synthesize per-structure validity masks or sentinel values
for partially sampled observables. Such a model would require dtype-specific
null semantics, `has_attribute()` rules, conversion-report behavior, and a
versioned H5MSM representation. If accepted later, it is an H5MSM 0.5 candidate
rather than an implicit extension of 0.4. The independent-layer requirements
for that version are recorded in
[H5MSM 0.5 Modular Layer Contract](pending_proposals/h5msm_0_5_modular_layers.md).

## Required evidence

Changes to this contract require tests for:

- coordinate-free partial representations and frame-count inference;
- constructor, direct-assignment, frame-axis, and atom-axis inconsistencies;
- atomic failure without partial mutation;
- intersection warnings and strict rejection;
- coordinate-only sources without topology;
- `Structures`, `StructuresDict`, `MolSys`, `append_structures()`, and
  `concatenate_structures()` parity;
- extraction, YAML, and H5MSM round trips after structural growth.
