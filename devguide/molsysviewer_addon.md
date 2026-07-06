# molsysviewer_molsysmt — addon architecture

Workspace **"molsysmt"** inside MolSysViewer.  Each panel is a Python
`AddonPanelWidget` subclass that bridges a MolSysMT function to a live viewer
action.

## Panel map

| # | Panel ID | `widget_class` | MolSysMT module(s) | Viewer bridge |
|---|----------|----------------|--------------------|---------------|
| 1 | basic | `MolSysMTBasicPanel` | `msm.get()`, `msm.select()` | inspect counts, create viewer selections |
| 2 | topology | `MolSysMTTopologyPanel` | `msm.topology.*` | links and topology summaries |
| 3 | structure | `MolSysMTStructurePanel` | `msm.structure.*` | contacts links, analysis summaries, PCA vectors |
| 4 | hbonds | `MolSysMTHBondsPanel` | `msm.hbonds.*` | `view.shapes.links.add_hbonds()` |
| 5 | pbc | `MolSysMTPBCPanel` | `msm.pbc.*` | status and coordinate transforms |
| 6 | physchem | `MolSysMTColorPanel` | `msm.physchem.*` | `view.whole.set_color_by_values()` |
| 7 | molecular_mechanics | `MolSysMTMechanicsPanel` | `msm.molecular_mechanics.*` | vectors, energy summaries, minimization |
| 8 | build | `MolSysMTBuildPanel` | `msm.build.*` | append atoms or replace topology/system as needed |

There is no root-level `transform` panel. Transform-like operations belong under
their real MolSysMT namespaces (`structure`, `pbc`, or `build`).

## Runtime state

All state lives in `view.addons.molsysmt` (`MolSysMTAddonRuntime`, one instance
per view). The runtime holds UI/session state and cached results only; it does
not store a molecular system.

The public namespace is an active facade over the current view. Panels, context
actions, and direct Python calls share the same adapter layer, so GUI actions
and scripted calls remain equivalent. The current runtime also keeps the legacy
private alias `view._molsysmt_addon_runtime` only as a compatibility bridge; new
code should use `view.addons.molsysmt`.

`view.addons.molsysmt.basic.remove(...)`,
`view.addons.molsysmt.basic.add(...)`, `view.addons.molsysmt.basic.set(...)`,
and `view.addons.molsysmt.basic.append_structures(...)` are live-view MolSysMT
operations, not aliases to the corresponding view mutators. They call MolSysMT
to produce or mutate the molecular system, then ask MolSysViewer to reconcile
the visual state through `view.apply_system_edit(...)`. A legacy fallback to the
old view methods exists only for viewer objects that do not yet expose that
primitive.

## Context actions

| ID | Target | Action |
|----|--------|--------|
| inspect-system | structure | fills basic panel with atom/group/chain/structure counts |
| select-and-highlight | structure | runs selection and highlights in viewer |
| remove-selected-atoms | structure | removes selected atoms through `view.addons.molsysmt.basic.remove(...)` |
| color-by-property | structure | colors by last chosen property |
| compute-contacts | structure | computes contact map |
The current spec intentionally does not declare shape providers; panels and
facade calls create concrete MolSysViewer shapes directly.

## Workbench sections

| ID | Panel |
|----|-------|
| system-info | global |
| mvp-overlays | global |
| basic-inspect | basic |
| basic-select | basic |
| topology-bonds | topology |
| topology-dihedrals | topology |
| structure-contacts | structure |
| structure-rms | structure |
| structure-pca | structure |
| hbonds-buch | hbonds |
| pbc-status | pbc |
| pbc-wrapping | pbc |
| physchem-color | physchem |
| mechanics-forces | molecular_mechanics |
| mechanics-energy | molecular_mechanics |
| mechanics-minimization | molecular_mechanics |
| build-preparation | build |
| build-solvation | build |

## Export helpers

| ID | Formats |
|----|---------|
| system-export | json |

## Current verification status

As of 2026-07-06, the addon has passed the focused Python test battery
(`tests/molsysviewer_molsysmt/`: 110 passed), a backend smoke test on real
`MolSysView` demo systems (16 ok, 0 failed), simulated entry-point discovery,
and a Playwright visual smoke of the standalone Add-ons workspace. The visual
smoke confirmed that the MolSysMT workspace and all eight panel tabs render, and
that the `Basic` panel mounts its subsections without JavaScript errors.

The remaining manual validation is a live Jupyter/Qt widget smoke test, because
the static standalone HTML verifies frontend rendering/navigation but not
button-to-Python execution.
