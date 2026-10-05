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

Declarative payloads use top-level fields. MolSys and Topology retain version
0.1; newly serialized Structures payloads use version 0.2:

```yaml
format: molsysmt
kind: molsys  # or topology / structures
version: "0.1"  # "0.2" for new structures files
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

Legacy Structures YAML 0.1 and the structural payload of MolSys YAML 0.1
use the following negotiated canonical units:

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

### Structures YAML 0.2

The supported quantity fields above use PyUnitWizard `QuantityRecord`
serialization, bound to `structures.<field>` and converted explicitly to the
negotiated unit. Each record carries its values, unit descriptor, shape, dtype
and integrity digest. Readers verify the record and the expected field and
unit; session policy is not a unit source. This is record integrity, not
authentication of the molecular system. Non-finite values use the codec's
base64 representation; finite values use readable JSON-compatible lists.

Sparse `alternate_location` remains a list of mappings keyed by **local integer
atom indices**, one per structure. Each entry contains location labels and
optional atom ID labels, occupancy, B factors and coordinates. Nested B factors
and coordinates use records bound to `alternate_location.b_factor` and
`alternate_location.coordinates`, with nm² and nm respectively. Site counts,
coordinate shapes and finite alternate coordinates are checked. Coordinate
arrays, when present, also establish the structure count and atom-index bounds.
NumPy scalar keys/labels are converted to Python scalar types for YAML.

Readers accept 0.1 top-level canonical values and legacy label-only alternate
entries. Legacy nested geometry has no negotiated unit and is rejected; a bare
number array cannot be upgraded by guessing. Unsupported or missing schema
versions and malformed 0.2 records raise `FormatError`.

Migrate a readable 0.1 file through the public dictionary form:

```python
molsys = msm.convert(old_file, to_form='molsysmt.StructuresDict')
msm.convert(molsys, to_form='file:structures_yaml', output_filename=new_file)
```

The file-to-file adapter remains a byte-preserving copy, including the original
schema version. No implicit in-place file migration is introduced. The optional
YAML dependency remains lazy; PyUnitWizard 0.28.1 supplies the record API and
empty-array codec fixes required by this boundary. Both package recipes,
runtime environments and the controlled CI source pin follow that public floor.

Atom selections in native/dictionary structural conversions remap sparse site
keys to the resulting local axis, using the same native remapping helper as
`Structures.extract`. Query selections keep source keys. Selecting a
StructuresDict directly into another StructuresDict still requires an explicit
supported conversion/extraction route; its legacy subset extractor remains
unimplemented. This change does not introduce that separate capability.

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
