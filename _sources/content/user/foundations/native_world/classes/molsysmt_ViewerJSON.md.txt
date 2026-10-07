(user-foundations-native-world-classes-molsysmt-viewerjson)=
# ViewerJSON

`molsysmt.ViewerJSON` is the native lightweight 3D graphics representation in MolSysMT used for WebGL rendering and interactive visualization engines.

---

## Overview and Role

As a user, `molsysmt.ViewerJSON` is the intermediate dictionary schema wrapped by the `ViewerJSON` dataclass when calling `msm.view(system)` or converting a system for web rendering. It encapsulates atomic coordinates, element symbols, residue/chain labels, bond connectivity, and periodic box dimensions into a pure, serializable JSON schema.

---

## Declarative Schema

The underlying `data` dictionary of `ViewerJSON` follows a standardized graphics payload schema:

| Top-Level Key | Value Type | Description |
| :--- | :--- | :--- |
| **`"version"`** | String (`"0.1"`) | Graphics payload schema version tag. |
| **`"atoms"`** | Dictionary of Lists | Columnar per-atom vectors: `atom_id`, `atom_name`, `group_id`, `group_name`, `chain_id`, `entity_id`, `element_symbol`, `formal_charge`. |
| **`"bonds"`** | Dictionary | Bond connectivity mapping: `atom_pairs` (`[[atom1, atom2], ...]`) and optional `order` list. |
| **`"structures"`** | List of Dicts | Frame list containing `coordinates` in `nm` `([[x, y, z], ...])`, optional `time` in `ps`, and optional periodic `box` vectors (`v0`, `v1`, `v2` in `nm`). |

---

## Usage and Workflow

```python
import molsysmt as msm

# 1. Convert molecular system to a ViewerJSON object
viewer_obj = msm.convert(system, to_form='molsysmt.ViewerJSON')

# 2. Export payload as JSON string or write to gzipped file
json_str = viewer_obj.dumps(indent=2)
viewer_obj.dump("molecular_graphics.json.gz", compression="gzip")

# 3. Render directly in Jupyter notebook or web frontend
view = msm.view(viewer_obj)
```

---

## Invariants and Performance

- **Pure JSON Primitives**: All internal values are strictly primitive Python types (`dict`, `list`, `str`, `int`, `float`, `None`).
- **Built-In Gzip Compression**: Supports direct gzip compression (`compression="gzip"`) for fast network transmission.

---

## API Documentation

Viewer form converters and getters are documented under the [{doc}`Visualization Tools </content/user/tools/index>`].
