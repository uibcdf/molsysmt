---
summary: Retire the legacy MolSysViewer addon in favor of native backend integration
issue: uibcdf/molsysmt#354
status: resolved
opened: 2026-10-09
closed: 2026-10-09
verification: measured
area: [packaging, docs, api]
guard: devtools/tests/test_native_viewer_integration.py::test_current_source_distribution_does_not_advertise_or_include_legacy_addon
normative: devguide/molsysviewer_addon.md
blocked_by: []
supersedes: []
---

# Retiring the legacy MolSysViewer addon

**Reported:** 2026-10-09 by MolSysViewer under uibcdf/molsysviewer#186.
**Status:** Provider source reconciliation completed; replacement artifact qualification remains paused.

## What

The maintainer has authorized native MolSysMT-backed Studio workflows rather
than a second workspace mirroring the entire scientific API. Before correction, provider
packaging registered `molsysmt = molsysviewer_molsysmt` under
`molsysviewer.addons`, includes the separate integration package, and requires
those obsolete files/declarations in wheel, sdist and installed-runtime gates.
Retire that provider surface while preserving scientific APIs, form adapters,
interaction results and H5MSM 0.5.

## How

- Remove the addon entry point and package discovery inclusion, and retire
  tracked addon source and addon-only tests. Their complete implementations
  remain in Git history; generic scientific functionality already lives in the
  owning public MolSysMT modules.
- Reverse packaging gates to reject obsolete addon files/entry points rather
  than require them. Source discovery is exercised through setuptools, not
  just a string match. Wheel checks inspect actual archive roots and parsed
  entry-point metadata; installed checks inspect only the MolSysMT distribution.
  Independent domain addons are not a provider-owned surface to remove.
- Retain native public-runtime scientific checks. Test existing public Buch
  calculations, named sparse analyses/H5MSM and the MolSysView form adapter.
- Maintain migration guidance in `molsysviewer_addon.md`, visualization guidance,
  Foundations, Toolbox, Cookbook and Common Core Module 6. Notebook code and
  outputs are unchanged. Archive the original architecture and withdraw the
  addon worker-thread proposal; do not claim its design was implemented.

## Why

A registered legacy entry point advertises a workspace rejected by the next
Viewer. Keeping package validators dependent on it would recreate the obsolete
surface in later artifacts. Native integration keeps scientific computation in
MolSysMT and scene/UI/session reconciliation in MolSysViewer.

## Evidence and source boundaries

Before correction, regression controls fail because source discovery advertises
and includes the addon, archive validators accept its files/registration, and
there is no installed metadata rejection route. These are package-contract
checks, not scientific defects in a detector.

Start from MolSysMT `0018c544de0a0c70fd88ae0b6408898f0f22e59b`, clean main.
The bounded suite-state inspection finds MolSysViewer main synchronized with its
remote but carrying 67 independent changed/untracked paths. Preserve all of them;
this work does not edit or commit any Viewer source. Local cross-component tests
use that development worktree, not a qualified replacement installed artifact.
Python 3.14.7 in the shared development environment; preserved native extension.

The preceding #352/#353 exact head's automatic Ruff, suite policy, package
governance, developer-guide and CI smoke runs all pass. That evidence belongs
to its producer, not this new cleanup.

## Scope and exclusions

The source transition is admitted before 1.0 as reconciliation of the accepted
Viewer integration under #334. #348 (state-aware induced connectivity) and #350
(rejected aromatic-candidate diagnostics) explicitly request new capabilities,
not defects in documented defaults; they are classified Post-1.0.

No new detector, dependency, broad API mirroring, thread protocol or browser
redesign is introduced. Do not change frozen package bytes, refs, citation
records or earlier qualification receipts. Do not build, upload, promote or
qualify a replacement candidate during the publication pause. New-source package
gates apply to future artifacts, not retroactive interpretation of old receipts.
Existing static documentation HTML preserves its original embedded runtime and
is refreshed during final documentation qualification with the agreed Viewer.

## Acceptance

- No shipped or advertised legacy addon from the current source configuration.
- Reject reintroduction through source, wheel, sdist and installed metadata.
- Keep unrelated entry-point groups and other distributions' domain addons valid.
- Existing native form, interaction and H5MSM workflows pass focused regressions.
- Public migration and lifecycle documentation agrees with ownership and scope.
- Archived design is preserved, obsolete proposal withdrawn, indexes updated.

## Resolution and validation — 2026-10-09

Current source removes 28 addon Python modules and its eight test/support files.
The package no longer advertises the workspace. Artifact gates reject its
package or entry points, including a renamed registration; installed inspection
requires a file inventory and leaves unrelated entry-point groups alone.
The source guard exercises real setuptools discovery with both package names
present in a bounded fixture and asserts no tracked addon Python source remains.

The first broad local discovery test traversed unrelated build/documentation
output and the run was interrupted after 67/69 tests. This is incomplete
verification, not a passing campaign. The final guard uses the same real
setuptools implementation and repository configuration on a bounded inventory,
so the property is protected without depending on development output size.
An optional broad Numba inventory and disk traversal were also stopped; they
supply no completed gate evidence and are not credited as passes.

Final focused results from the shared environment:

- `python -m pytest devtools/tests/test_native_viewer_integration.py
  devtools/tests/test_validate_rust_wheel.py --receptor=llm -n12`:
  **24 passed**, covering source/installed metadata and wheel admission.
- `python -m pytest devtools/tests/test_validate_rust_sdist.py
  devtools/tests/test_rust_wheel_workflow.py
  devtools/tests/test_installed_runtime_dependencies.py
  tests/interactions/test_public_molsys_h5msm_workflow.py
  tests/interactions/hbonds/test_buch_results.py
  tests/form/molsysviewer_MolSysView --receptor=llm -n12`:
  **47 passed**, covering sdist/workflow/dependency contracts plus public Buch,
  named sparse/H5MSM results and native viewer extraction.

The two final runs cover **71 disjoint cases**; none are skipped.

No new installed wheel/Conda package or browser/session qualification is claimed.
The original source checkout's installed editable metadata can still advertise
its previous entry point until it is reinstalled; this work changes future
package metadata, without rewriting the shared environment or old file bytes.

Repository-wide `ruff check .` and `ruff format --check .` pass.
`python devtools/scripts/release_gate.py` passes **14/14 fast gates**, including
dependency/source-route audits, delivery contracts, developer-guide integrity,
course structure (156 notebooks), resources/citation and public-API smoke.
Neither this result nor the scoped tests resume the paused heavy artifact gates.
