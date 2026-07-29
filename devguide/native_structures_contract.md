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
  `StructuralAttributeDropWarning`;
- structure-aligned metadata such as time, box, and energies remains that of
  the target because the structure axis itself is not extended;
- structure-count mismatch is rejected before mutating the target;
- the complete candidate payload is validated before assignment.

This is the same intersection rule used for structure-axis append. MolSysMT 1.0
does not represent a B factor, occupancy, velocity, or coordinate array that is
available for only a prefix or suffix of the combined atom axis.

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
