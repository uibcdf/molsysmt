"""
MolSysMT Developer Guide — Viewers and Visualization
"""

# Viewers and Visualization

## Supported Viewers
- `MolSysViewer` (default)
- `NGLView` (optional)

## Policy
- MolSysViewer is the default viewer in the MolSysSuite ecosystem.
- NGLView remains supported as an alternative when installed.
- Viewer backends must be optional and lazily imported.

## API Surface
`molsysmt.basic.view` returns a viewer object without forcing display. Viewer
objects decide how to render themselves (`show()` / rich reprs).

## Documentation
User-facing viewer docs live under `docs/content/user/tools/thirds/`.
