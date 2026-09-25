# Declarative Serialization Forms

MolSysMT provides a declarative serializer family that is distinct from
both `h5msm` and viewer-oriented payloads. The full family is implemented
and tested as of March 2026.

Implemented forms:

- `molsysmt.MolSysDict`
- `molsysmt.TopologyDict`
- `molsysmt.StructuresDict`
- `file:molsys_yaml`
- `file:topology_yaml`
- `file:structures_yaml`
- `MolSys <-> MolSysDict`
- `MolSysDict <-> file:molsys_yaml`
- `MolSysBuilder <-> MolSysDict`
- `Topology <-> TopologyDict <-> file:topology_yaml`
- `Structures <-> StructuresDict <-> file:structures_yaml`

## Why this exists

The goal is to support:

- human-authored deterministic fixtures;
- small editable molecular systems for testing and debugging;
- a clear declarative counterpart to `MolSysBuilder`.

This serializer family does **not** replace `h5msm`. The roles are different:

- `h5msm` remains the compact native persistence format;
- `molsys_yaml` is intended to stay readable, versionable, and easy to edit.

## MolSysDict 0.1 fidelity boundary

`MolSysDict` schema 0.1 stores atoms, groups, bonds, chains, molecules, entities,
and the structural fields `structure_id`, `time`, `box`, and `coordinates`.
Components are reconstructed during native materialization; their metadata is
not serialized. Velocities, B factors, occupancy, and thermodynamic observables
are available in `StructuresDict`, but not in `MolSysDict` 0.1. Extending this
boundary requires a versioned schema migration.

Conversions from `MolSys` to `MolSysDict` or `file:molsys_yaml` apply atom and
structure selections before serialization. Atom subsets follow the canonical
increasing source-index order used by native extraction.

## Naming model

The design separates:

- semantic in-memory forms:
  - `molsysmt.MolSysDict`
  - `molsysmt.TopologyDict`
  - `molsysmt.StructuresDict`
- file forms:
  - `file:molsys_yaml`
  - `file:topology_yaml`
  - `file:structures_yaml`

Declarative YAML and JSON files use normal `*.yaml` / `*.yml` and `*.json` extensions. Their semantic role is detected from top-level discriminator fields in the payload itself:

- `format: molsysmt`
- `kind: molsys` / `topology` / `structures`

## Relationship with existing JSON payloads

- `ViewerJSON` keeps its viewer-specific role.
- `UniversalJSON` is no longer part of the active form graph.

## Current checkpoint

All three slices are implemented and tested (March 2026). It is enough to:

- serialize a `MolSys` to `MolSysDict`;
- dump that declared state to `file:molsys_yaml`;
- read it back into `MolSysDict`;
- rebuild a `MolSys` from it;
- move declared state directly between `MolSysBuilder` and `MolSysDict`;
- serialize a `Topology` through `TopologyDict` / `file:topology_yaml`;
- serialize `Structures` through `StructuresDict` / `file:structures_yaml`.


## Second slice checkpoint

The second declarative serializer slice is now available:

- `molsysmt.TopologyDict`;
- `file:topology_yaml`;
- `molsysmt.Topology <-> molsysmt.TopologyDict`;
- `molsysmt.TopologyDict <-> file:topology_yaml`.


## Third slice checkpoint

The third declarative serializer slice is now available:

- `file:structures_yaml`;
- `molsysmt.Structures <-> file:structures_yaml`;
- `molsysmt.StructuresDict <-> file:structures_yaml`.
