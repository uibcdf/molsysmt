# Viewers and Visualization

`molsysmt.basic.view()` currently dispatches to `MolSysViewer` by default and
supports `NGLView` when its optional dependency is available. Viewer packages
must remain lazily imported.

## Viewer objects as forms

MolSysMT registers adapters for:

- `molsysviewer.MolSysView`;
- `nglview.NGLWidget`.

Recognition as a form enables the adapter capabilities that are actually
implemented and tested. It does not require or guarantee the full MolSysMT basic
API. The MolSysViewer adapter currently exposes conversion, `get`, `extract`,
`copy`, `append_structures`, and attribute getters; NGLView exposes a different,
broader set. Always consult adapter code and public delivery tests.

Both viewers are explicitly registered as Tier 1 for compatibility with the
existing support policy. That classification is not independent evidence of
complete capability or scientific fidelity; consult delivery and parity tests
for the workflow being claimed.

## State and fidelity

Viewer state can diverge from the source through selection, trajectory slicing,
interactive edits, representation state, or lossy serialization. Claims that a
viewer is a transparent molecular system require tests for:

- topology and structure retrieved from the current view;
- selection and frame ordering;
- mutations and edits in both directions where supported;
- unit and identifier preservation;
- behavior after widget disposal or backend disconnection.

Visual representations, colors, cameras, and UI selections are not molecular
attributes unless an explicit schema says so.

## Failure behavior

Unavailable viewers should fail with an actionable dependency/capability error.
Notebook rendering and browser success are separate from Python backend
correctness. Headless tests, widget integration tests, and browser tests provide
different evidence and should be reported separately.

The MolSysViewer addon contract and dated verification notes are in
`molsysviewer_addon.md`.
