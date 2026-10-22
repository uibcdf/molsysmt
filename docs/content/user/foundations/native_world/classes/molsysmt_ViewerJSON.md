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
| **`"atoms"`** | Dictionary of Lists | Columnar per-atom vectors: `atom_id`, `atom_name`, `group_id`, `group_name`, `chain_id`, `entity_id`, `element_symbol`, `formal_charge`. |
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

## Invariants and Performance

- **Pure JSON Primitives**: Native topology exports use Python scalars and containers, including `null` for missing table values. Bond endpoints remain integer positions. `dumps()` and `dump()` use the standard JSON encoder; manually supplied payloads must already satisfy this contract.
- **Built-In Gzip Compression**: Supports direct gzip compression (`compression="gzip"`) for fast network transmission.

---

## API Documentation

Viewer form converters and getters are documented under the [{doc}`Visualization Tools </content/user/tools/index>`].
