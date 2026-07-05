# molsysviewer_molsysmt addon — implementation plan

This is the working plan for turning the current `molsysviewer_molsysmt`
prototype into a reliable MolSysViewer integration. It is the companion of
[`molsysviewer_molsysmt_addon_assessment.md`](molsysviewer_molsysmt_addon_assessment.md),
which holds the architectural analysis and the verified facts this plan builds
on.

## How to use this document

- Each step is a checkbox. Mark it `[x]` when it is done **and verified**, not
  when it is merely written.
- Keep the "Status" line under each phase in sync (`not started` /
  `in progress` / `done`).
- When a step reveals a new decision or risk, record it in the assessment
  document, not here — this file stays a checklist.
- Do not start a later phase before the phase it depends on is green, unless the
  dependency is explicitly noted as optional.

Status legend: `[ ]` pending · `[~]` in progress · `[x]` done.

## Decisions locked for this plan

These follow the assessment's recommended options. They can be revisited, but
the plan assumes them so work is not blocked:

1. **Packaging**: one installer, separate import. `molsysviewer_molsysmt` ships
   inside the single `molsysmt` distribution (as it does today — `packages.find`
   with `namespaces=true` already picks it up as a top-level package) and is
   imported separately as `import molsysviewer_molsysmt` (never `molsysmt.<...>`).
   This is the TopoMT pattern. A second distribution buys nothing here because
   `molsysmt` permanently depends on `molsysviewer` (for `msm.view()`), so the
   viewer is always installed anyway and addon + molsysmt + molsysviewer always
   travel together; splitting would add a second `pyproject`, a conda
   multi-output recipe, and a double-inclusion test for no real gain.
   `molsysmt`'s dependency on `molsysviewer` stays untouched and is independent
   from the addon. Addon imports must still stay light and lazy (Phase 1) so
   importing the addon does not eagerly pull MolSysViewer. Discovery uses the
   entry point declared in `molsysmt`'s own `pyproject.toml` (Phase 7), backed by
   `KNOWN_ADDON_MODULES`.
2. **Source of truth**: the runtime holds **no** molecular system, and the
   public API takes **no** `molecular_system` argument. Operations pass the view
   itself (as the `molsysviewer_MolSysView` form) to the MolSysMT verbs —
   `msm.<verb>(view, ...)` — falling back to `view.molsys` (the public read-only
   property, the same object as `view._molsys`) only for a verb that does not
   accept the form. Transforms push a new object back via
   `view.load(new_ms, mode="replace")`.
3. **Public surface & API shape** (resolves assessment Decision #5):
   `view.addons.molsysmt` (via `state_factory`) is the public per-view namespace
   and an **active facade** mirroring the MolSysMT module layout (`.basic`,
   `.structure`, `.pbc`, `.build`, `.physchem`, …). Entries fall in three tiers:
   - **A — alias** to a native viewer method where MolSysViewer already owns the
     operation with full reconciliation (`basic.remove` → `view.remove`,
     `basic.add` → `view.add`). Pure discoverability, zero re-implementation — an
     alias is not a thin wrapper.
   - **B — viewer-aware implementation** for MolSysMT ops with no native viewer
     method that still need viewer coordination.
   - **C — addon-native surface** (e.g. `.show` / `.overlays`) for flows with no
     MolSysMT analog: compute-and-render overlays, coloring, workflows.
   Only entries that add value over calling MolSysMT directly belong here — a
   bare `msm.verb(view)` passthrough does not. Session/tag bookkeeping lives on
   the namespace state; `view._molsysmt_addon_runtime` stays a compatibility
   alias. Fine-grained placement (e.g. `.structure.contacts(show=True)` vs
   `.show.contacts`) is left to settle with usage.
4. **Science location**: all scientific logic lives in an `adapters/` layer.
   Panels, context actions, and the public namespace all call the adapters.
5. **Navigation**: the full feature catalog is organized as a few parent panels
   with third-level subsections, not one root tab per verb family.
6. **Diagnostics**: optional-backend failures go through SMonitor plus a compact
   user-facing panel error state, never a raw traceback.

## MVP scope

The addon's unique value is **MolSysMT analysis + viewer overlay** — computations
MolSysViewer does not provide, rendered or colored in the viewer. That is the MVP:

- `basic` (inspect current viewer system and run MolSysMT selections) — the
  source-of-truth proof. **Done.**
- `physchem` (color by a small set of robust MolSysMT properties — a Tier C overlay).
- `contacts` (compute contacts, render as links — a Tier C overlay).
- `basic.select` (run `msm.select`, create/update a viewer region or active selection);
  MolSysViewer selections already resolve MolSysMT syntax, so the value here is
  the highlight/region flow, not the bare `select`.

**System-mutating operations are NOT re-implemented.** `view.remove` and
`view.add` already exist natively in MolSysViewer and fully reconcile viewer
state (regions/selections/shapes/…). The addon exposes them as **aliases** under
`basic.*` (Tier A); it does not rebuild them. So `remove`/`add` are out of the
"build" scope — only their aliasing is in scope.

Everything else (`pbc`, `hbonds`, `topology`, `molecular_mechanics`, `build`)
is staged beyond the first vertical slices. `transform` is not a public panel:
its operations belong under the real MolSysMT namespaces (`structure`, `pbc`,
or `build`, depending on the verb).

---

## Phase 0 — Close the study gaps

Status: `done`

- [x] Study the current addon reference on the `feature/navigate-panel-redesign`
      branch as the source of truth for the new structure:
      `docs/content/developer/addons.md`, plus the `dummy_addon` and `topomt`
      reference implementations (state_factory + `__getitem__` dataclass,
      subsections, lifecycle, ESM cleanup). This supersedes older examples.
- [x] Skim `molsysviewer_elasnetmt` for ideas only. Finding: it also uses
      `push_state`, so it is useful for adapter/runtime organization but **not**
      a template for the current `addon_states` state-sync path.
- [x] Read `molsysmt/form/molsysviewer_MolSysView/` in depth: confirm which
      attributes/operations the view-as-form supports directly and where a
      standalone `to_molsysmt_MolSys` materialization is actually required.
- [x] Confirm concrete return shapes for the MVP verbs on a real demo system
      (`msm.select`, `structure.get_contacts`): element level, indices, units.
- [x] Confirm the viewer-side APIs the MVP needs against a live view
      (`view.molsys`, `view.molecular_system`, `view.regions`/active selection,
      `view.whole.set_color_by_values`, `view.shapes.add_links`).

Exit criteria: no unknowns remain for the four MVP operations. **Met.**

### Findings (verified live on `demo["dialanine"]`)

- **System handle**: `view.molsys` (read-only property) is the reliable handle
  and **is** the same object as `view._molsys`. `view.molecular_system` is
  **not** dependable — it holds the original `load(...)` argument (a source-file
  path string on demos). Adapters use `view.molsys` / the view-as-form.
- **View-as-form works**: `msm.get_form(view)` → `molsysviewer.MolSysView`. The
  form pipes topological/structural/any attributes through `molsysmt.MolSys` by
  transiently converting `view._molsys` (no persistent duplicate). Decision #2
  confirmed.
  - `msm.get(view, n_atoms=True)` → `int` (counts work through the form).
  - `msm.select(view, 'atom_name=="CA"')` → `list` of atom indices, **identical**
    to `msm.select(view.molsys, ...)`. Indices are in MolSys space;
    `view._index_mapper` (an `IndexMapper`) exists for views loaded with a subset
    — must be honored when creating selections/regions or rendering.
  - `msm.structure.get_contacts(view, ...)` → boolean `ndarray` contact map of
    shape `(n_structures, n_sel, n_sel)`; for links, derive index pairs
    (e.g. `np.argwhere`) — request an explicit output form in the adapter.
  - Adapters can take `view` directly; **no `molecular_system` argument**.
- **Viewer APIs present**: `view.whole.set_color_by_values`/`reset_colors`,
  `view.shapes.add_links`, `view.shapes.links.add_hbonds`, `view.regions`
  (`RegionsManager`), `view.selections` (`SelectionsManager`).
- **Cleanup API is `view.shapes.clear(tag=...)`**, not `remove`. The prototype
  bug in `panels/hbonds.py`, `panels/topology.py`, and `panels/mechanics.py`
  has been fixed and covered by shape-cleanup panel tests.

## Phase 1 — Source-of-truth bridge and namespace foundation

Status: `done`

- [x] Add a `create_molsysmt_state(view)` factory and wire it as
      `AddonSpec.state_factory` behind an `_accepts_keyword(...)` capability
      guard (TopoMT pattern).
- [x] Rework `runtime.py`: `ensure_runtime(view)` prefers `view.addons.molsysmt`
      and falls back to `view._molsysmt_addon_runtime` only for test doubles;
      both point at the same object. Added `__getitem__` for dict-style lookup.
- [x] Remove the runtime-owned `molecular_system` field. The runtime holds only
      UI/session state and cached results; all operations resolve the system from
      the active view or materialize from `view.molsys` at action time.
- [x] Keep the active-view back-reference and facade namespaces out of the
      dataclass field list. `_view`, `basic`, `structure`, `show`, and
      `overlays` are normal runtime attributes initialized in `__post_init__`,
      so `dataclasses.asdict(runtime)` does not traverse the full viewer or
      facade cycles.
- [x] Add a small system-access helper (`access.py`: `system_for_verbs`,
      `system_object`, `has_system`, `materialize_system`) that returns the view
      itself for the MolSysMT verbs, materializing a standalone MolSys only when
      required.
- [x] Rework `addon.py` to lazy construction: expose
      `addon`/`ADDON`/`get_addon`/`lifecycle` via module-level `__getattr__`;
      move every MolSysViewer/heavy import inside `get_addon()` / action
      functions so importing the package does not pull MolSysViewer in. The
      package `__init__` is lazy too (reentrancy-guarded `__getattr__`, TopoMT
      pattern), and specs are imported from `molsysviewer.addons`.
- [x] Extend the molsysmt test battery
      (`tests/molsysviewer_molsysmt/`) with Phase 1 coverage:
      public namespace, `state_factory`, dual `ensure_runtime`, dict-style
      lookup, access helpers, and a subprocess lazy-import test. **41 passed.**

Exit criteria: `view.addons.molsysmt` resolves; importing the addon does not
import MolSysViewer; adapters can operate on the view without a runtime-held
system. **Met**.

### Findings / notes

- **Environment caveat**: the `molsysviewer` importable in this dev env is the
  `main` checkout (`/home/diego/repos@uibcdf/molsysviewer`), which lacks the new
  addon structure. The addon targets the `feature/navigate-panel-redesign`
  worktree. Until that branch is installed/merged, run the tests with the
  worktree first on the path:
  `PYTHONPATH=/home/diego/repos@uibcdf/molsysviewer__feature-navigate-panel-redesign:/home/diego/repos@uibcdf/molsysmt`.
- **Verified live**: bare `import molsysviewer_molsysmt` pulls neither
  MolSysViewer nor MolSysMT; `get_addon()` carries `state_factory`;
  `view.addons.molsysmt` returns the runtime with the private alias synced;
  `molsysviewer.addons.register_module("molsysviewer_molsysmt")` discovers the
  spec cleanly.
- **Form bug (not MVP-blocking)**: `msm.extract(view, ...)` on the view-as-form
  raises (`extract() got an unexpected keyword argument 'atom_indices'` — the
  form's `extract` signature is incompatible). `materialize_system` extracts from
  `view.molsys` instead. Worth fixing in the `molsysviewer_MolSysView` form later.

## Phase 2 — Adapter layer and first vertical slice (`system`)

Status: `done`

- [x] Create `adapters/` with a `system` adapter
      (`adapters/system.py::system_counts`) that reads counts
      (atoms/residues/chains/structures) from the view-as-form.
- [x] Rewire the `system` panel `handle_action(...)` to call the adapter and
      `has_system(view)`; no science in the widget handler, no read of the
      deprecated `molecular_system` shim.
- [x] Public Python equivalent: the adapter itself
      (`molsysviewer_molsysmt.adapters.system.system_counts(view)`). Note: `system`
      is a pure read (a thin wrapper over `msm.get`), so it is **not** promoted to
      a facade method — you would use `msm.get(view, ...)` directly. The active
      facade (Decision #5, now resolved) lands in Phase 3 for the overlay flows.
- [x] Migrate panel state from message-driven `push_state` to synced
      `addon_states`: Python handlers call `set_state(...)`; ESM panels hydrate
      with `model.get(...)` and subscribe to `change:<key>` events; tests assert
      `widget.state` / `view.widget.addon_states` instead of captured messages.
- [x] Extend the test battery: adapter reads-from-view + raises-without-system;
      the panel inspect test now uses a real demo view (no runtime seeding).

Exit criteria: opening the `system` panel on a real loaded viewer shows correct
counts with **no manual runtime seeding** (verified: `demo["dialanine"]` →
`{n_atoms:22, n_residues:3, n_chains:1, n_frames:1}`), and the same result is
reachable from Python via the adapter. **Met** (43 passed). Namespace-method
binding awaits Decision #5.

## Phase 3 — Active facade + MVP overlay flows (`color`, `contacts`, `select`)

Status: `done`

- [x] Introduce the **active facade** on `view.addons.molsysmt` (resolves
      assessment Decision #5): a `_view` back-ref set by `state_factory`, the
      state dataclass for bookkeeping, and sub-namespaces mirroring MolSysMT
      (`.basic`, `.structure`, …) plus an addon-native `.show`/`.overlays` area.
      Update the namespace tests to the new shape.
- [x] Tier A aliases: `view.addons.molsysmt.basic.remove` → `view.remove`,
      `basic.add` → `view.add` (native, fully reconciling; **no** re-implementation).
- [x] `color` flow (Tier C overlay) + panel: pure `adapters` compute the
      per-element MolSysMT property values; the facade flow validates element
      cardinality/units and calls `view.whole.set_color_by_values(...)`.
      Implemented the first robust property set (`charge`, `mass`,
      `atomic_radius`) through `view.addons.molsysmt.show.color_by(...)`,
      `show.reset_colors()`, and the Color panel. The MolSysViewer rebuild now
      remaps and replays per-atom color overrides after `view.remove(...)`, so
      color overlays can rely on the native reconciliation path. Verified with
      `tests/molsysviewer_molsysmt/`.
- [x] `contacts` flow (Tier C overlay) + panel: pure `adapters` compute contact
      index pairs from `structure.get_contacts` (explicit output form); the facade
      flow renders links via `view.shapes.add_links` and tracks tags for cleanup
      (+ a `clear` counterpart). Implemented through
      `adapters.structure.contact_pairs(...)`,
      `view.addons.molsysmt.show.contacts(...)`,
      `show.clear_contacts(...)`, and the Structure panel contacts action.
      Verified with `tests/molsysviewer_molsysmt/`.
- [x] `select` flow + panel: `msm.select(view, ...)` → create/update a viewer
      active selection with index-space mapping; not just coloring. Implemented
      through `adapters.select.select_indices(...)`,
      `view.addons.molsysmt.show.select(...)`,
      `show.clear_selection(...)`, and the Basic panel. Element-level selections
      resolve to atom indices for `view.selections` and activation. Verified with
      `tests/molsysviewer_molsysmt/`.
- [x] Reorganize panels into parent panels + third-level subsections using
      `AddonSectionSpec` with `meta={"panel": ...}` and
      `data-molsysviewer-addon-section` containers. Covered by spec tests for
      section metadata and panel tests for the matching ESM containers.
- [x] Once the MVP panels no longer read `runtime.molecular_system`, remove it
      from the runtime dataclass — the deferred deletion from Phase 1.

Exit criteria: the MVP overlay flows work end to end from the GUI and from
`view.addons.molsysmt`, share pure adapters, clean up their own shapes/tags, and
`basic.remove`/`basic.add` alias the native viewer methods.

## Phase 4 — Spec cleanup

Status: `done`

- [x] Remove or implement the declared-but-missing contributions
      (`context.*`, `workbench.*`, `shapes.*`, `exports.*`). Nothing in the
      `AddonSpec` should point to a module that cannot be imported. Implemented
      MVP `context.py`, `workbench.py`, and `exports.py`; removed phantom shape
      providers.
- [x] Make `AddonSpec` mirror the MolSysMT public namespaces instead of the
      earlier GUI-invented categories. Public panels are now `basic`,
      `topology`, `structure`, `hbonds`, `pbc`, `physchem`,
      `molecular_mechanics`, and `build`; there is no root-level `transform`
      panel. Context actions now cover `inspect-system`,
      `select-and-highlight`, `color-by-property`, and `compute-contacts`.

Exit criteria: every entry in the `AddonSpec` resolves to a real importable
target. **Met** (`tests/molsysviewer_molsysmt/`: 106 passed).

## Phase 5 — Diagnostics and soft-dependency policy

Status: `done`

- [x] Define the soft-dependency error policy (per assessment Decision #6):
      intercept optional-backend import/compute failures, log through SMonitor,
      push a compact user-facing error state to the panel. Implemented
      `molsysviewer_molsysmt.diagnostics`: import/backend failures show a short
      "Missing optional dependency..." message, compute failures show one compact
      line, and SMonitor emission is best-effort with addon/panel/action context.
- [x] Apply it to any MVP operation with an optional backend; document the
      pattern for post-MVP panels to follow. The MVP panels (`basic`,
      `physchem`, `structure`) now route unexpected action failures through
      `panel_error_state(...)`; expected "No molecular system" states stay
      explicit.

Exit criteria: a missing optional backend produces a clean panel error state and
an SMonitor diagnostic, never a raw traceback. **Met** for MVP panels
(`tests/molsysviewer_molsysmt/`: 106 passed).

## Phase 6 — Tests from real viewer flows

Status: `done for addon MVP`

- [x] Add integration tests that start from a real loaded demo viewer
      (`dialanine`/`pentalanine`/…) and then exercise each MVP panel/adapter —
      no manual runtime seeding, no mocks. Covered with
      `molsysviewer.demo["dialanine"]` for `basic` inspect/select, `physchem`
      color, `structure` contacts, `hbonds`, and context-action dispatch.
- [x] Test adapters directly, then test panel routing to the adapters.
- [x] Test cleanup: shapes/tags created by an operation are removable/resettable.
      Covered from the panel paths for color reset, selection clear, and contact
      link cleanup.
- [x] Test the soft-dependency error path.
- [x] Reorganized the tests from the single `test_molsysviewer_molsysmt_addon.py`
      into a package `tests/molsysviewer_molsysmt/` (themed files: `test_spec`,
      `test_panels`, `test_flows_select_color`, `test_flows_analysis`,
      `test_flows_mutations`, `test_foundation`) with a `conftest.py`. The
      conftest only adds the repo root to `sys.path`; MolSysViewer must be
      importable from the environment (no hardcoded worktree path).

Exit criteria: the MVP is covered by tests that would fail if the source-of-truth
bridge regressed. **Met for the addon MVP** (`tests/molsysviewer_molsysmt/`: 106
passed). The full MolSysMT suite is not currently a useful gate in this dev
environment: an earlier run accumulated unrelated failures in conversion/build/
NGLView/OpenMM areas before being interrupted.

## Phase 7 — Packaging entry point

Status: `done`

- [x] Once the import path is stable, declare the entry point in `molsysmt`'s
      `pyproject.toml` (the single distribution). Use the **module** form for
      now so MolSysViewer's current loader registers both the `AddonSpec` and
      lifecycle (`on_enable`, `on_disable`, `on_context_action`):

```toml
[project.entry-points."molsysviewer.addons"]
molsysmt = "molsysviewer_molsysmt"
```

      A callable entry point such as `molsysviewer_molsysmt:get_addon` is clearer
      aesthetically, but the current MolSysViewer discovery path registers only
      the returned `AddonSpec` in that case and does not recover lifecycle from
      the source module. That host improvement is tracked in MolSysViewer's
      pending proposals.
- [x] Verify discovery via `molsysviewer.addons.discover(...)` finds the addon
      through the entry point (not only via `KNOWN_ADDON_MODULES`).

Exit criteria: a clean environment discovers the addon from packaging metadata.
**Met** for the current development setup by testing the declared TOML entry
point and simulating the corresponding module entry point in
`molsysviewer.addons.discover(...)`; lifecycle is preserved. Verified with
`tests/molsysviewer_molsysmt/`.

## Phase 8 — Expand beyond the MVP

Status: `done`

- [x] Add namespace panels on the settled bridge + adapter + subsection pattern:
      `topology`, `pbc`, `hbonds`, `molecular_mechanics`, and `build`.
      `hbonds` is migrated through `adapters.hbonds.buch_hbond_links(...)`,
      `view.addons.molsysmt.show.hbonds(...)`, and `show.clear_hbonds(...)`.
      The visible namespace panels no longer use `runtime.molecular_system` as
      their source of truth; `pbc`, `topology`, `molecular_mechanics`, and
      `build` now resolve from the active view or materialize from `view.molsys`
      before replacing the viewer. `topology`, `pbc`, `molecular_mechanics`,
      `build`, and the non-contact `structure` actions (`rmsd`, `rmsf`, `pca`)
      now have dedicated adapters. The legacy `transform.py` panel was removed;
      transform-like actions must live under their real MolSysMT namespaces.
      Verified with `tests/molsysviewer_molsysmt/` (106 passed).
- [x] For system-mutating operations, reuse MolSysViewer's **self-reconciling**
      primitives instead of a destructive `view.load(new_ms, mode="replace")`:
      - **Coordinate-only ops** (`pbc` wrap/mic/unwrap, `molecular_mechanics`
        minimize) route through `view.set_coordinates(...)` — rebuild with no
        `atom_index_map`, preserving regions/selections/colors/shapes.
      - **Atom-appending ops** (detected when the original atoms keep their
        indices — `build` solvate, add-hydrogens, and typically bioassembly): the
        adapter returns the appended delta and the panel applies it with
        `view.add(...)`, which also preserves overlays.
      - **Non-append restructures** fall back to `view.load(mode="replace")` — a
        genuine "new view", overlays cleared by design. The MolSysMT-side
        selected `add_missing_bonds` bug was fixed in `get_missing_bonds`
        (selection filtering now preserves bond pairs instead of flattening
        them), and the build adapter now calls it with `in_place=False`.
        Covered by build/get-missing-bonds regression tests.
      The panels also report the reconciliation mode back to the UI
      (`coordinates`, `append`, `replace`, or `noop`) plus a compact warning
      about overlay preservation/reset.
      Covered by `test_pbc_wrap_preserves_viewer_overlays`,
      `test_build_solvate_appends_and_preserves_overlays`, and focused panel
      state tests for minimization, replacement, and no-op build flows.
- [x] `on_active_selection_changed` hook for selection-driven context items
      (assessment Decision #10), registered behind a capability guard. When atoms
      are selected it offers a **"expand to whole residues"** item; the handler
      (`context.expand_selection_to_residues`) expands via MolSysMT and updates
      the active selection. This drove a small MolSysViewer-core addition,
      **`view.active_selection.set(selection)`** (public counterpart of the
      existing `clear()`), so the addon sets the active selection through a public
      API instead of poking `view._send` / `view._last_active_selection_event`.
      Covered by `test_active_selection_hook_returns_items_for_selection`,
      `test_lifecycle_exposes_active_selection_hook`,
      `test_context_expand_residues_sets_whole_residue_active_selection`, and (in
      MolSysViewer) `test_active_selection_set_*`. TopoMT was also refactored to
      use this public API for its simplex selection; the old `view._send` /
      `view._last_active_selection_event` fallback was removed, and its 177
      addon tests stay green.
- [x] Give expensive and mutating actions clearer UX semantics: explicit user
      confirmation where needed (energy minimization and potentially
      destructive build operations), progress/error wording, and visible
      distinction between in-place coordinate updates, atom-appending updates,
      no-op operations, and full view replacement. Verified with
      `tests/molsysviewer_molsysmt/` (106 passed).

Exit criteria: each added panel meets the same end-to-end bar as the MVP before
the next is started. **Met** for the namespace panels currently exposed by the
addon.

---

## Progress summary

- Phase 0 — Close the study gaps: `done`
- Phase 1 — Source-of-truth bridge and namespace foundation: `done`
- Phase 2 — Adapter layer and first vertical slice (`system`): `done`
- Phase 3 — Active facade + MVP overlay flows: `done`
- Phase 4 — Spec cleanup: `done`
- Phase 5 — Diagnostics and soft-dependency policy: `done`
- Phase 6 — Tests from real viewer flows: `done for addon MVP`
- Phase 7 — Packaging entry point: `done`
- Phase 8 — Expand beyond the MVP: `done`

## Verification log

### 2026-07-05

- Python addon test battery:
  `PYTHONPATH=/home/diego/repos@uibcdf/molsysviewer__feature-navigate-panel-redesign:/home/diego/repos@uibcdf/molsysmt pytest tests/molsysviewer_molsysmt -q`
  passed with **106 passed**.
- Manual backend smoke on real `MolSysView` demo systems passed with **16 ok,
  0 failed**. Covered public namespace discovery, basic inspect/select/clear,
  physchem color/reset, structure contacts/clear, topology bonds/dihedrals/clear,
  H-bonds compute/clear, PBC check/wrap, and build add-bonds.
- Packaging/discovery was verified by simulating the declared module entry point
  through `molsysviewer.addons.discover(...)`; the addon was found as
  `molsysmt`, lifecycle was preserved, and the exposed panel list matched the
  current eight-panel spec.
- Browser visual smoke was run with Playwright against a generated standalone
  HTML view using `molsysviewer.demo["dialanine"]` and the
  `molsysviewer_molsysmt` addon module. The Add-ons panel opened, the MolSysMT
  workspace was visible, all eight panel tabs rendered, and the `Basic` panel
  mounted its subsections (`Inspect`, `Select`, `MVP Overlays`, `System Info`)
  with no JavaScript console errors. Screenshots were written to
  `/tmp/molsysviewer_molsysmt_workspace.png` and
  `/tmp/molsysviewer_molsysmt_basic_panel.png`.
- Remaining manual check: run the addon in a live Jupyter notebook/Qt widget
  session and click through actions that require the Python backend. The static
  standalone HTML smoke verifies frontend navigation/rendering, not live
  button-to-Python execution.
