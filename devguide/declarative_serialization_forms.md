# Declarative Serialization Forms

## Purpose

MolSysMT needs a simple, human-readable serialization path for deterministic
fixtures, debugging, and small hand-authored molecular systems.

This new serialization line should not compete with `h5msm`. The intended role
is different:
- `h5msm` remains the native compact and robust persistence format;
- declarative serialization should remain small, legible, editable, and easy to
  version in the repository.

## Design decision

The serialization design is split across two axes:
- semantic in-memory forms;
- physical file forms.

These axes must not be collapsed into a single naming layer.

### In-memory semantic forms

The planned in-memory declarative forms are:
- `molsysmt.MolSysDict`
- `molsysmt.TopologyDict`
- `molsysmt.StructuresDict`

These are semantic forms. They describe what kind of molecular data is held in
memory.

### File forms

The planned file forms are:
- `file:molsys_yaml`
- `file:topology_yaml`
- `file:structures_yaml`

Later, if there is a clear need, the same semantic payloads may also be written
as JSON through:
- `file:molsys_json`
- `file:topology_json`
- `file:structures_json`

The file forms are real MolSysMT forms, just like `file:pdb` or
`file:h5msm`.

## File naming and extensions

The new declarative file forms should use typed extensions so the semantic kind
of the payload is visible from the filename itself.

Planned YAML extensions:
- `*.molsys.yaml`
- `*.topology.yaml`
- `*.structures.yaml`

If JSON support is added later, the parallel extensions should be:
- `*.molsys.json`
- `*.topology.json`
- `*.structures.json`

This rule applies to the new declarative serializer family only. Existing
native formats such as `*.h5msm` keep their current naming and are not part of
this extension redesign.

## Why this split matters

This separation keeps the API coherent:
- `molsysmt.*Dict` objects are native declarative objects in memory;
- `file:*_yaml` and `file:*_json` are serialized forms on disk.

This also keeps the conversion graph clean. For example, a future direct path
such as `file:topology_yaml -> openmm.Topology` makes conceptual sense and does
not need to pretend that the source was a full molecular system.

## Scope for the first slice

The first implemented slice remains deliberately narrow:
- `molsysmt.MolSysDict`
- `file:molsys_yaml`
- `molsysmt.MolSys <-> molsysmt.MolSysDict`
- `molsysmt.MolSysDict <-> file:molsys_yaml`

`TopologyDict` and the serialized topology/structures forms should come after
that first slice.

The canonical first-slice pipeline is therefore:
- `MolSys <-> MolSysDict`
- `MolSysDict <-> file:molsys_yaml`

No direct `MolSysBuilder <-> MolSysDict` conversion is required for the first
slice. That relationship can be added later once the first declarative
serializer contract has settled.

Status:
- implemented in the repository;
- validated through focused tests for `MolSysDict`, `file:molsys_yaml`, and
  supported-form metadata;
- intentionally kept separate from the first `MolSysBuilder` slice.

## Schema shape for `MolSysDict` v1

`MolSysDict` v1 should use a declared, level-oriented schema, not the current
columnar atom-centric style used by `UniversalJSON`.

The expected high-level shape is:
- `metadata`
- `topology`
  - `atoms`
  - `groups`
  - `bonds`
  - `chains`
  - `molecules`
  - `entities`
- `structures`
  - `structure_id`
  - `time`
  - `box`
  - `coordinates`

Each topology level should be represented declaratively, with explicit member
indices at the level where that membership is declared.

`molecular_mechanics` stays out of scope for the first slice.

## Relationship with MolSysBuilder

`MolSysBuilder` is the native editable form for declared molecular systems.
`MolSysDict` should be the declarative serializable counterpart.

The intended long-term direction is:
- `MolSysBuilder` for native in-memory editing;
- `MolSysDict` for declarative in-memory serialization;
- `file:molsys_yaml` for human-authored serialized fixtures.

This means the builder and the declarative serializer should stay aligned in
hierarchy semantics and in the meaning of declared state.

In practice, this means `MolSysBuilder` and `MolSysDict` should describe the
same declared hierarchy with different operational goals:
- the builder is mutable and editable;
- the dict form is serializable and stable.

## Relationship with existing forms

### `molsysmt.ViewerJSON`

`ViewerJSON` keeps its current role. It is a viewer transport format and should
not be repurposed as the general declarative serializer.

### `molsysmt.StructuresDict`

The current `StructuresDict` form should not be treated as the foundation of the
new declarative serializer family. It has a more limited structural role.

It may still inform naming or implementation details later, but it should not
anchor the new design.

### `molsysmt.UniversalJSON`

`UniversalJSON` is the legacy precursor closest to this space, but it is not a
clean long-term contract for the new serializer family.

Current direction:
- `UniversalJSON` is expected to enter a deprecation path toward `1.0`;
- it should not be used as the semantic basis for `MolSysDict`;
- any migration should be explicit and documented.

## Why YAML first

YAML is preferred for the first serialized file form because the initial target
is human-edited fixtures and developer-authored examples.

JSON can still be added later, but YAML is the better first backend for:
- readability;
- hand editing;
- review diffs in version control.

## Non-goals for the first slice

The first declarative serializer slice should not try to solve everything.
These items should stay out of scope initially:
- `molecular_mechanics` serialization;
- direct third-party conversions from the serialized file forms;
- compression features;
- full migration of all current JSON-like forms;
- replacement of `h5msm`.

## Current architectural decision

Before implementation, the repository now treats the following as the intended
architecture:
- semantic forms: `MolSysDict`, `TopologyDict`, `StructuresDict`;
- file forms: `file:molsys_yaml`, `file:topology_yaml`, `file:structures_yaml`;
- `UniversalJSON` in deprecation path;
- `ViewerJSON` retained for visualization-specific transport.

## First-slice implementation checkpoint

The repository now includes:
- native `molsysmt.MolSysDict`;
- form integration for `molsysmt.MolSysDict`;
- file form integration for `file:molsys_yaml`;
- focused round-trip tests through `MolSys`.

This first slice is intentionally conversion-centric. It is sufficient to:
- serialize small deterministic molecular systems to human-readable YAML;
- read them back as `MolSysDict` or `MolSys`;
- use the resulting forms in supported-form discovery and basic attribute
  queries.

Future slices should add:
- `TopologyDict`;
- `StructuresDict`;
- typed YAML file forms for topology and structures;
- optional JSON backends.
