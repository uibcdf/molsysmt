# Declarative Serialization Forms

MolSysMT provides human-readable YAML forms for small deterministic fixtures,
debugging, and hand-authored systems. They complement rather than replace H5MSM,
which is the compact native persistence path for larger data.

## Implemented forms

In memory:

- `molsysmt.MolSysDict`;
- `molsysmt.TopologyDict`;
- `molsysmt.StructuresDict`.

On disk:

- `file:molsys_yaml`;
- `file:topology_yaml`;
- `file:structures_yaml`.

The YAML forms require the optional `yaml` dependency. JSON counterparts are
not currently part of this declarative family. `molsysmt.ViewerJSON` remains a
viewer transport form.

## Discriminator and version

Declarative payloads use top-level fields:

```yaml
format: molsysmt
kind: molsys  # or topology / structures
version: "0.1"
```

File detection reads content rather than assigning semantics from the `.yaml`
extension alone. New schema versions require explicit migration and backwards-
compatibility tests; `version` must not be ignored when incompatible changes are
introduced.

## Schemas

`MolSysDict` contains metadata, a level-oriented topology (`atoms`, `groups`,
`bonds`, `chains`, `molecules`, `entities`), and a deliberately small structural
payload (`structure_id`, `time`, `box`, and `coordinates`). Components are
reconstructed when the payload is materialized; component metadata is not stored
by schema version 0.1. `TopologyDict`
contains the same topology levels without the enclosing `topology` key.
`StructuresDict` is the existing dictionary-based structural form; its YAML
serializer stores structural fields under `structures`.

Structural YAML values are serialized in canonical units when the corresponding
schema carries them:

- coordinates and box: nm;
- time: ps;
- velocities: nm/ps;
- B factors: nm²;
- occupancy: dimensionless.

In particular, velocities, B factors, occupancy, and thermodynamic observables
are supported by `StructuresDict` but are not fields of `MolSysDict` schema 0.1.
Adding them to `MolSysDict` requires a versioned schema migration rather than
silently changing the meaning of existing payloads.

Element IDs materialized into native MolSysMT objects must remain strings.

## Builder relationship

`MolSysBuilder <-> MolSysDict` preserves declared state without applying native
hierarchy fallback. `MolSysDict -> MolSys` materializes through the builder and
`build()`. Tests must distinguish declared-state fidelity from the completed
native hierarchy.

## Fidelity and intended scale

Round-trip tests cover the implemented forms, but YAML is not intended for
large trajectories or high-throughput storage. Tests must cover schema version,
units, IDs, ordering, missing optional fields, malformed content, and dependency
absence. Unknown fields and future versions need an explicit policy before the
format can be called long-term stable.

Conversion selection is part of the contract: `MolSys -> MolSysDict` and
`MolSys -> file:molsys_yaml` apply both the requested atom selection and
`structure_indices`. Atom subsets are materialized in canonical increasing
source-index order, consistently with native `MolSys.extract`.
