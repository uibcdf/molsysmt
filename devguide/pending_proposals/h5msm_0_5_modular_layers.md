# H5MSM 0.5 Modular Layer Contract

**Status:** proposed; design checkpoint, not an H5MSM 0.5 implementation

**Target:** post-1.0 unless a current correctness defect requires earlier work

**Related contract:** [Native Structures Contract](../native_structures_contract.md)

## Motivation

MolSysMT deliberately accepts molecular-system forms with partial information.
A sequence may have no coordinates, a trajectory may have no topology, and a
chemical-state representation need not carry a complete stable topology.
H5MSM must preserve that philosophy instead of requiring artificial empty
objects merely to satisfy one fixed hierarchy.

The current H5MSM 0.4 organization couples chemical states too closely to
topology and can make an absent layer indistinguishable from an automatically
created empty scaffold. Extending that organization incrementally would make
readers infer semantics from storage accidents.

## Required Capability

The format must support every non-empty combination of the three principal
native information layers:

| Topology | Chemical states | Structures | Valid use |
| --- | --- | --- | --- |
| present | absent | absent | stable inventory and hierarchy only |
| absent | present | absent | chemical-state information only |
| absent | absent | present | topology-free trajectory or observations |
| present | present | absent | stable inventory plus chemical states |
| present | absent | present | classical fixed-topology trajectory |
| absent | present | present | chemical-state trajectory without a full stable topology |
| present | present | present | complete molecular-system representation |

An entirely empty container may be technically readable for tooling, but it is
not a meaningful molecular-system payload and need not be a normal write
target.

## Proposed Root Layout

H5MSM 0.5 should store three optional sibling groups:

```text
/
├── topology/          # optional
├── chemical_states/   # optional
└── structures/        # optional
```

No layer is a prerequisite for another. Cross-layer associations are explicit
datasets or references, not implied by nesting.

Examples include:

- a structure-to-chemical-state association when both layers exist;
- a chemical-state atom-domain reference when topology exists;
- an explicit local atom domain when a chemical state exists without topology.

The exact reference encoding must be decided in the H5MSM repository after
testing append, slicing, and partial-read behavior. This proposal fixes the
semantic contract, not the low-level HDF5 encoding.

## Presence Semantics

Readers and writers must distinguish three states for every principal layer:

1. **Absent:** the root group does not exist and the file makes no claim about
   that information domain.
2. **Present but empty:** the group exists intentionally, carries its schema
   metadata, and contains a valid zero-length representation.
3. **Present with data:** the group exists and contains one or more domain
   records.

An absent layer must not be materialized as an empty native object merely for
convenience. Conversely, a deliberately empty layer must not be reported as
absent.

`has_attribute()` and conversion-fidelity reports should answer from semantic
payload presence, not from the existence of scaffolding created by a reader.

## Minimal Independent Domains

### Topology

Topology owns stable atom inventory, grouping and hierarchy. It must not need
coordinates or chemical-state payloads.

### Chemical states

A chemical-state-only file needs enough information to define the domain to
which its state data apply. This may be a minimal local atom domain such as an
atom count and stable local indices. It must not require inventing atom names,
groups, molecules, or other topology.

When topology is also present, the state layer should reference its atom
domain explicitly and validate compatible cardinality.

### Structures

A structures-only file may contain any valid complete-axis combination of
coordinates, velocities, box, time, thermodynamic series, B factors,
occupancies, alternate locations, and structure identifiers. It must not
require topology.

Atom-aligned structural arrays define their own atom-axis cardinality. Files
with only non-atom-aligned structural series are valid and may have unknown
atom cardinality.

## Association Rules

- With one chemical state and no explicit per-structure association, all
  structures are associated with that state.
- With multiple chemical states, an association dataset is required whenever
  structures are claimed to have resolved states.
- Missing association information means unavailable information; it must not
  be replaced by a fabricated state.
- Topology and structures may coexist without a chemical-state layer. This is
  the normal compact representation for many classical trajectories.
- Layer cardinalities are validated only where a semantic relationship is
  declared. The mere coexistence of layers must not create an undocumented
  inference.

## H5MSM 0.4 Compatibility and Migration

The 0.4 reader must remain stable while MolSysMT approaches 1.0. The modular
layout should therefore be introduced as a versioned 0.5 schema, not as an
ambiguous reinterpretation of existing files.

A 0.4-to-0.5 migrator should:

1. detect which 0.4 groups contain semantic payload rather than scaffolding;
2. promote topology, chemical states, and structures into sibling 0.5 groups;
3. reconstruct only associations demonstrated by 0.4 data;
4. preserve absence instead of manufacturing empty layers;
5. report any ambiguous inference through the conversion-fidelity machinery.

The 0.5 reader may expose a common MolSysMT object model for both versions, but
must retain the source schema version in provenance.

## Acceptance Criteria

The design is ready for implementation only when the H5MSM and MolSysMT sides
agree on:

- the schema and ownership of all three optional root layers;
- the encoding of cross-layer references and local atom domains;
- absent versus present-empty semantics;
- append behavior for files that do not contain all layers;
- selection and partial-read behavior;
- conversion-fidelity and strict-mode reporting;
- 0.4 migration and compatibility policy.

Implementation evidence must include:

1. one round trip for each of the seven valid layer combinations;
2. explicit absent/present-empty/present-data tests for every layer;
3. topology-free structural append and slicing;
4. chemical-state-only storage with a minimal atom domain;
5. single-state implicit and multi-state explicit structure associations;
6. cross-layer cardinality rejection without partial file mutation;
7. 0.4-to-0.5 migration fixtures;
8. lazy or selective reads proving that omitted layers are not loaded or
   synthesized.

## Non-Goals

- implementing per-structure missing-value masks for partially sampled
  observables; that is a related but independent decision;
- forcing every MolSysMT form to expose all three layers;
- inferring a chemically rich topology from coordinates alone;
- changing the stable H5MSM 0.4 reader during the MolSysMT 1.0 stabilization
  path without demonstrated necessity.

## Recommended Scheduling

Stabilize the current H5MSM 0.4 integration for MolSysMT 1.0. Treat this 0.5
contract as an independent post-1.0 workstream that can proceed while the paper
is written or reviewed. Promote it onto the 1.0 critical path only if testing
shows that 0.4 cannot faithfully represent an advertised Tier-1 use case.
