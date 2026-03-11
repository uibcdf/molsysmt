# Declarative Serialization Forms

MolSysMT is introducing a declarative serializer family that is distinct from
both `h5msm` and viewer-oriented payloads.

The current first slice is intentionally small:

- `molsysmt.MolSysDict`
- `file:molsys_yaml`
- `MolSys <-> MolSysDict`
- `MolSysDict <-> file:molsys_yaml`

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

Typed YAML extensions make the semantic role visible from the filename:

- `*.molsys.yaml`
- `*.topology.yaml`
- `*.structures.yaml`

## Relationship with existing JSON payloads

- `ViewerJSON` keeps its viewer-specific role.
- `UniversalJSON` is not the semantic basis of this new serializer line and is
  expected to move toward deprecation for the `1.0` line.

## Current checkpoint

The first slice is already implemented and tested. It is enough to:

- serialize a `MolSys` to `MolSysDict`;
- dump that declared state to `file:molsys_yaml`;
- read it back into `MolSysDict`;
- rebuild a `MolSys` from it.

Later slices should expand this family to topology-only and structures-only
forms, plus optional JSON backends.


## Second slice checkpoint

The second declarative serializer slice is now available:

- `molsysmt.TopologyDict`;
- `file:topology_yaml`;
- `molsysmt.Topology <-> molsysmt.TopologyDict`;
- `molsysmt.TopologyDict <-> file:topology_yaml`.
