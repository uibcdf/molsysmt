# Viewers and Visualization

## Supported Viewers
- `MolSysViewer` (default)
- `NGLView` (optional)

## 🥇 The "System-Transparent" Viewer Policy
As of MolSysMT 1.0.0, visualization objects are no longer just "output widgets"; they are **active molecular systems**.

1. **Introspection**: You can call `msm.get(view, coordinates=True)` or `msm.select(view, selection='protein')` directly on a viewer object.
2. **Parity**: The state shown in the viewer (coordinates, topology) must match the underlying MolSysMT model.
3. **Form Implementation**: Every viewer must have a corresponding form module in `molsysmt/form/` (e.g., `molsysviewer_MolSysView`) that implements the full suite of MolSysMT basic functions (`get`, `set`, `select`, `extract`).

## MolSysViewer (The House Standard)
MolSysViewer is the primary visualization engine. It is optimized for MolSysMT through the `ViewerJSON` format, which ensures high-speed data transfer between Python and the browser.

- **Hardening**: The `molsysviewer_MolSysView` form is now a Tier 2 hardened form.
- **Lazy Loading**: The `molsysviewer` backend is only loaded when `msm.view()` is called.

## NGLView (The Community Standard)
NGLView is fully supported as a robust alternative.

- **Adapter**: MolSysMT uses a custom `MolSysMTTrajectory` adapter to pipe data into NGLView.
- **Hardening**: The `nglview_NGLWidget` form is now recognized by `get_form()` and `is_a_molecular_system()`.

## API Surface
`molsysmt.basic.view` returns a viewer object. This object must implement the MolSysMT API, allowing it to be used as input for further analysis or conversion.
