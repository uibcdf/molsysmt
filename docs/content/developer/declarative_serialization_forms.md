# Declarative Serialization Forms

MolSysMT is introducing a declarative serializer family that is distinct from
both `h5msm` and viewer-oriented payloads.

The current first slice is intentionally small:

- `molsysmt.MolSysDict`
- `file:molsys_yaml`
- `MolSys <-> MolSysDict`
- `MolSysDict <-> file:molsys_yaml`
- `MolSysBuilder <-> MolSysDict`

## Why this exists

The goal is to support:

- human-authored deterministic fixtures;
- small editable molecular systems for testing and debugging;
- a clear declarative counterpart to `MolSysBuilder`.

This serializer family does **not** replace `h5msm`. The roles are different:

- `h5msm` remains the compact native persistence format;
- `molsys_yaml` is intended to stay readable, versionable, and easy to edit.

## Naming model

The design separates:

- semantic in-memory forms:
  - `molsysmt.MolSysDict`
  - future `molsysmt.TopologyDict`
  - future `molsysmt.StructuresDict`
- file forms:
  - `file:molsys_yaml`
  - future `file:topology_yaml`
  - future `file:structures_yaml`

Declarative YAML and JSON files use normal `*.yaml` / `*.yml` and `*.json` extensions. Their semantic role is detected from top-level discriminator fields in the payload itself:

- `format: molsysmt`
- `kind: molsys` / `topology` / `structures`

## Relationship with existing JSON payloads

- `ViewerJSON` keeps its viewer-specific role.
- `UniversalJSON` is no longer part of the active form graph.

## Current checkpoint

The first slice is already implemented and tested. It is enough to:

- serialize a `MolSys` to `MolSysDict`;
- dump that declared state to `file:molsys_yaml`;
- read it back into `MolSysDict`;
- rebuild a `MolSys` from it;
- move declared state directly between `MolSysBuilder` and `MolSysDict`.

Later slices should expand this family to topology-only and structures-only
forms, plus optional JSON backends.


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
