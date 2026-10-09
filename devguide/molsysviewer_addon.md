# Native MolSysViewer integration

**Role:** normative provider/consumer boundary
**Decision:** uibcdf/molsysmt#354, coordinated with uibcdf/molsysviewer#186

MolSysMT supplies the native molecular-system, scientific calculation and H5MSM
backend used by MolSysViewer. It does not ship or advertise a separate
`molsysviewer_molsysmt` package, `molsysviewer.addons` entry point, Studio
workspace, panel facade or `view.addons.molsysmt` namespace. Domain addons
remain owned by their providers and MolSysViewer's independent extension API.

## Supported paths

- Use `msm.view(molecular_system)` for the supported form-agnostic visualization
  route. The `molsysviewer.MolSysView` form adapters remain available.
- Use MolSysViewer's native loading, selections and `view.interactions` APIs
  for its supported Studio workflows. MolSysMT calculates scientific results;
  MolSysViewer validates, attaches named analyses and controls their presentation.
- Direct MolSysMT interaction calculations return the documented optional
  `Interactions` result. They do not need an addon and do not automatically
  attach every calculation. Named analyses accompany a `MolSys` and persist
  through the supported H5MSM 0.5 public conversion paths.
- For an operation beyond the native Studio surface, use the public MolSysMT
  tool and then reload the result or reconcile it through the Viewer-owned
  `view.apply_system_edit` API with the required index correspondence. Coordinates,
  topology edits, cached interactions and scene state obey their respective
  documented invalidation/reconciliation contracts.

This is not a promise that Studio mirrors every public MolSysMT function.
Viewer owns its GUI, sessions, selections, scene state and reconciliation API;
MolSysMT owns the scientific operation and molecular data fidelity.

## Migration

Replace calls to the removed `view.addons.molsysmt` facade with native Viewer
operations where provided, or with public `msm.basic`, `msm.build`,
`msm.structure`, `msm.topology`, `msm.pbc`, `msm.physchem` and
`msm.interactions` tools. Do not restore the old addon namespace or silently
rewrite legacy serialized UI/session state. Viewer owns scene/session migration.

The removed adapters wrapped existing public tools; their panel state and
rendering projection were UI-specific, not another scientific engine. Their
source and tests remain in Git history. The
[archived architecture](archive/assessments/molsysviewer_addon_before_retirement_20261009.md)
records the old surface without presenting it as current behavior.

## Packaging and evidence

Current-source wheels, source distributions and installed-runtime checks must
reject legacy addon files and declarations. Native Rust/resource/form metadata
and public runtime checks remain required. No new dependency is introduced.
The installed check inspects MolSysMT's own distribution, so it does not reject
other components' domain addons.

Previously qualified files and their source receipts remain unchanged. New
validators describe future artifacts produced from this source; they do not
retroactively qualify or rewrite old candidates. Provider cleanup alone does
not qualify a new Viewer candidate, browser runtime or installed package pair.
The 1.0 publication pause and exact-candidate gates remain authoritative.
Pre-generated documentation HTML contains its original embedded Viewer runtime;
refresh it through the normal final documentation qualification with the agreed
Viewer source, rather than rewriting frozen JavaScript snapshots by hand.
