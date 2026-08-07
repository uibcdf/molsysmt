(user-foundations-native-world-classes-molsysmt-viewerjson)=
# ViewerJSON

`molsysmt.ViewerJSON` is the native lightweight 3D graphics representation in MolSysMT used for WebGL rendering and interactive visualization engines.

---

## Overview and Role

As a user, `molsysmt.ViewerJSON` is the intermediate dictionary schema generated when calling `msm.view(system)`. It encapsulates atomic coordinates, color palettes, molecular representations, and camera angles into a pure JSON schema recognized by WebGL renderers.

---

## Declarative Schema

Inside `molsysmt.ViewerJSON`, graphics data is organized as a structured JSON dictionary:

| Top-Level Key | Value Type | Description |
| :--- | :--- | :--- |
| **`"atoms"`** | List of Dicts | 3D positions, element symbols, and atom radii. |
| **`"bonds"`** | List of Dicts | Covalent bond connectivity pairs for wireframe/stick rendering. |
| **`"representations"`** | List of Dicts | Style specifications (`"cartoon"`, `"spacefill"`, `"licorice"`) and color schemes. |

---

## Usage and Workflow

```python
import molsysmt as msm

# 1. Convert molecular system to ViewerJSON schema
viewer_json = msm.convert(system, to_form='molsysmt.ViewerJSON')

# 2. Render directly in notebook or web frontend
view = msm.view(viewer_json)
```

---

## Invariants and Performance

- **Lightweight Web Standard**: Optimized for minimal JSON payload transport over web sockets and Jupyter notebook widgets.

---

## API Documentation

Viewer form converters are documented under native visualization forms.
