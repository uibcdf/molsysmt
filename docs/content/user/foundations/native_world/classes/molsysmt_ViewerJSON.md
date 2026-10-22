(user-foundations-native-world-classes-molsysmt-viewerjson)=
# ViewerJSON

`molsysmt.ViewerJSON` is the native lightweight 3D graphics representation in MolSysMT used for WebGL rendering and interactive visualization engines.

---

## Overview and Role

As a user, `molsysmt.ViewerJSON` is the intermediate dictionary schema wrapped by the `ViewerJSON` dataclass when calling `msm.view(molsys)` or converting a system for web rendering. It encapsulates atomic coordinates, element symbols, group/chain labels, bond connectivity, and periodic box dimensions into a pure, serializable JSON schema.

---

## Declarative Schema

`payload.copy()`, Python copies and `msm.copy(payload)` retain the graphics data,
schema descriptions and compression metadata in independent mutable containers.
They do not decode a molecular system, render a scene or certify JSON-safe
contents. See {ref}`Native Copying <user-foundations-resident-copying>`.

The underlying `data` dictionary of `ViewerJSON` follows a standardized graphics payload schema:

| Top-Level Key | Value Type | Description |
| :--- | :--- | :--- |
| **`"version"`** | String (`"0.1"`) | Graphics payload schema version tag. |
| **`"atoms"`** | Dictionary of Lists | Columnar per-atom vectors: `atom_id`, `atom_name`, `group_id`, `group_name`, `chain_id`, `entity_id`, `element_symbol`, `formal_charge`. Native exports also supply `group_index`, `chain_index` and `entity_index` to distinguish repeated labels. |
| **`"bonds"`** | Dictionary | Bond connectivity mapping: `atom_pairs` (`[[atom1, atom2], ...]`) and optional `order` list. |
| **`"structures"`** | List of Dicts | Structure list containing `coordinates` in `nm` `([[x, y, z], ...])`, optional `time` in `ps`, and optional periodic `box` vectors (`v0`, `v1`, `v2` in `nm`). |

---

## Usage and Workflow

```python
import molsysmt as msm

# 1. Convert molecular system to a ViewerJSON object
viewer_obj = msm.convert(molsys, to_form='molsysmt.ViewerJSON')

# 2. Export payload as JSON string or write to gzipped file
json_str = viewer_obj.dumps(indent=2)
viewer_obj.dump("molecular_graphics.json.gz", compression="gzip")

# 3. Render directly in Jupyter notebook or web frontend
view = msm.view(viewer_obj)
```

---

## Identity and Recovery

ID fields are string labels, including leading zeros; they are never parsed as
positions. Native exports include per-atom `group_index`, `chain_index` and
`entity_index`. On native recovery, these columns distinguish repeated labels
and compact represented axes in source index order. Null membership remains
unknown. Invalid indices and conflicting labels, group names or entity
assignments raise a format error.

For older payloads without these columns, chain/entity IDs define identity;
group IDs define identity within a chain. Two groups sharing an ID in the same
chain, or two chains/entities sharing an ID, cannot be distinguished by those
legacy labels alone. Supply positional columns when separate identities matter.

ViewerJSON is a graphics projection: the reader preserves represented atoms,
groups, chains, entities and stored bonds, reconstructs connected components
through the native connectivity tool, and supplies a synthetic molecule per
group. It does not recover omitted molecule labels or the full native hierarchy.
Use H5MSM for full-domain persistence.

## Subset Semantics

Atom subsets preserve the requested order. Bonds survive only when both atoms
are retained; endpoints and every aligned bond column are remapped together.
Repeated atom indices are rejected because extraction does not clone atoms.
Structure selections preserve order and repetitions, including empty selections.
Selected data and wrapper metadata are independent of the source. Graphics data
are selected before copying, so discarded structures are not copied. Empty atom
selections recover native coordinates with shape `(n_structures, 0, 3)`.

Optional group/chain/entity indices retain source positions; the native reader
compacts them on recovery. Legacy endpoint fields gain canonical atom pairs when
extracting atoms. Bond sets remain separate graphics blocks during extraction;
this does not define a multi-set native chemistry import policy.

## Invariants and Performance

- **Pure JSON Primitives**: Native topology exports use Python scalars and containers, including `null` for missing table values. Bond endpoints remain integer positions. `dumps()` and `dump()` use the standard JSON encoder; manually supplied payloads must already satisfy this contract.
- **Built-In Gzip Compression**: Supports direct gzip compression (`compression="gzip"`) for fast network transmission.

---

## API Documentation

Viewer form converters and getters are documented under the [{doc}`Visualization Tools </content/user/tools/index>`].
