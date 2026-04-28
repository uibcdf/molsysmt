# molsysviewer_molsysmt — addon architecture

Workspace **"molsysmt"** inside MolSysViewer.  Each panel is a Python
`AddonPanelWidget` subclass that bridges a MolSysMT function to a live viewer
action.

## Panel map

| # | Panel ID | `widget_class` | MolSysMT module(s) | Viewer bridge |
|---|----------|----------------|--------------------|---------------|
| 1 | system   | `MolSysMTSystemPanel`     | `msm.get()`                       | display only |
| 2 | select   | `MolSysMTSelectPanel`     | `msm.select()`                    | `view.whole.set_color_by_values()` |
| 3 | color    | `MolSysMTColorPanel`      | `msm.physchem.*`, `msm.structure.get_rmsf()`, `msm.structure.get_secondary_structure()` | `view.whole.set_color_by_values()` |
| 4 | structure | `MolSysMTStructurePanel` | `msm.structure.*` (contacts, RMSD, RMSF, PCA) | `view.shapes.add_links()`, `view.shapes.add_displacement_vectors()` |
| 5 | transform | `MolSysMTTransformPanel` | `msm.structure.center()`, `least_rmsd_fit()`, `least_rmsd_align()`, `align_principal_axes()` | `view.load(ms, mode="replace")` |
| 6 | hbonds   | `MolSysMTHBondsPanel`     | `msm.hbonds.get_buch_hbonds()`    | `view.shapes.links.add_hbonds()` |
| 7 | topology | `MolSysMTTopologyPanel`   | `msm.topology.*` (bondgraph, dihedral_quartets) | `view.shapes.add_links()` |
| 8 | pbc      | `MolSysMTPBCPanel`        | `msm.pbc.*` (has_pbc, wrap, unwrap) | `view.load(ms, mode="replace")` |
| 9 | mechanics | `MolSysMTMechanicsPanel` | `msm.molecular_mechanics.*` (forces, energy, minimization) | `view.shapes.add_displacement_vectors()` |
| 10 | build   | `MolSysMTBuildPanel`      | `msm.build.*` (add_missing_*, make_bioassembly, mutate, solvate) | `view.load(ms, mode="replace")` |

## Runtime state

All state lives in `MolSysMTAddonRuntime` (one instance per view, stored as
`view._molsysmt_addon_runtime`).  Fields are grouped by panel to avoid collisions.

## Context actions

| ID | Target | Action |
|----|--------|--------|
| inspect-system | structure | fills system panel with atom/group/chain/structure counts |
| select-and-highlight | structure | runs selection and highlights in viewer |
| color-by-property | structure | colors by last chosen property |
| compute-contacts | structure | computes contact map |
| fit-to-reference | structure | RMSD-fits to reference structure |
| compute-hbonds | structure | computes H-bonds and renders links |
| wrap-to-pbc | structure | wraps to PBC box and reloads |
| build-bioassembly | structure | expands asymmetric unit and reloads |

## Shape providers

| ID | Shape type | Panel |
|----|-----------|-------|
| contacts-links | links | structure |
| hbond-links | h-bond links | hbonds |
| displacement-vectors | arrows | structure, mechanics |
| bond-links | links | topology |

## Workbench sections

| ID | Panel |
|----|-------|
| system-info | system |
| structure-stats | structure |

## Export helpers

| ID | Formats |
|----|---------|
| system-export | json |
