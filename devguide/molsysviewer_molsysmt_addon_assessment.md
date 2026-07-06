# molsysviewer_molsysmt addon assessment

This note records what has been learned so far about the incipient
`molsysviewer_molsysmt` addon, what still needs to be understood, and the
technical issues that must be addressed before it can become a reliable
MolSysViewer integration.

## Purpose

The goal is to expose useful MolSysMT capabilities inside MolSysViewer through
a first-class addon workspace. This is not a greenfield effort. The repository
already contains an initial `molsysviewer_molsysmt/` package with an
`AddonSpec`, ten panel widgets, a runtime dataclass, lifecycle hooks, and tests.

The addon is therefore best treated as an early broad prototype that needs
architectural tightening, not as an empty scaffold.

## Addon model

MolSysViewer addons are Python packages named like `molsysviewer_<name>` that
expose one of:

- `addon`
- `ADDON`
- `get_addon()`

The exposed object must resolve to a `molsysviewer.AddonSpec`.

The `AddonSpec` is declarative. It can contribute:

- workspaces
- panels
- context actions
- addon sections
- shape providers
- style helpers
- export helpers
- tool modes
- lifecycle hooks
- a `state_factory` for the public `view.addons.<name>` namespace

Interactive panels require `AddonPanelSpec.widget_class`, pointing to a
subclass of `molsysviewer.AddonPanelWidget`. Without `widget_class`, a panel is
metadata only. With `widget_class`, MolSysViewer can mount an anywidget panel in
the Add-ons workspace.

The intended division of responsibility is:

- JavaScript panel code sends user intentions.
- Python owns the scientific logic.
- Python uses MolSysViewer public APIs to alter regions, selections, colors,
  shapes, camera state, or loaded systems.
- Panel actions should have an equivalent Python-callable implementation so
  GUI workflows remain reproducible.

## Host integration

MolSysViewer has two addon levels:

- `molsysviewer.addons`: global host registry.
- `view.addons`: per-view projection of the host registry.

The host registry discovers addons through:

- Python entry points in the `molsysviewer.addons` group.
- the fixed `KNOWN_ADDON_MODULES` list when discovery is called with
  `include_known_modules=True`.

`KNOWN_ADDON_MODULES` already includes `molsysviewer_molsysmt`, so the current
package can be discovered by name when it is importable. However,
`pyproject.toml` does not yet declare a `molsysviewer.addons` entry point, so
packaged discovery still depends on the fixed known-module path or manual
registration.

Each `MolSysView` owns a `ViewAddonsManager`. It applies lifecycle hooks,
handles view-local enable/disable overrides, resolves panel widgets, and
reports discovery or lifecycle failures to the frontend runtime.

The per-view addon **state namespace** is part of this same manager. When code
accesses `view.addons.<name>` for a registered addon, `ViewAddonsManager`
lazily calls that addon's `state_factory(view)` the first time, caches the
result, and returns the same instance on every later access. If the addon
declares no factory it installs an empty `SimpleNamespace` instead, and if the
factory raises it falls back to one as well, so the attribute never fails hard.
Registered addon namespaces are also what `dir(view.addons)` advertises
(alongside `view.addons.manager`), so the slot is discoverable rather than a
hidden convention. This is the ordered extension point an addon should use for
its public per-view state and API, instead of attaching private attributes
directly to the view.

The host also supports a **third level of panel navigation** (subtabs). An
`AddonSectionSpec` registered with `target_panel="addons"` and
`meta={"panel": "<panel_id>"}` becomes a subsection shown only while that parent
panel is active. The panel's ESM `render` marks where each subsection's content
lives with a container carrying
`data-molsysviewer-addon-section="<addon_name>:<section_id>"`; MolSysViewer then
renders the subtab buttons and toggles visibility reactively. This mechanism is
confirmed on the `feature/navigate-panel-redesign` branch, documented in
`docs/content/developer/addons.md` ("Panel Subsections and Tab Navigation"), and
demonstrated by `molsysviewer/addon_templates/dummy_addon.py`. It lets an addon
group many tools under a few parent panels instead of one root tab per
capability, and is the basis for the grouped panel layout recommended below.

## Current implementation

The current addon package defines:

- `AddonSpec(name="molsysmt")`
- workspace `molsysmt`
- ten panels:
  - `system`
  - `select`
  - `color`
  - `structure`
  - `transform`
  - `hbonds`
  - `topology`
  - `pbc`
  - `mechanics`
  - `build`
- eight context actions
- four shape providers
- two addon sections
- one export helper
- lifecycle hooks:
  - `on_enable`
  - `on_disable`
  - `on_context_action`
- `MolSysMTAddonRuntime`, stored on the view as
  `view._molsysmt_addon_runtime`

The panel code is not just declarative. Each panel has an embedded ESM UI and a
Python `handle_action(...)` implementation. The implementation calls real
MolSysMT modules and real MolSysViewer APIs such as:

- `view.load(..., mode="replace")`
- `view.whole.set_color_by_values(...)`
- `view.whole.reset_colors()`
- `view.shapes.add_links(...)`
- `view.shapes.add_displacement_vectors(...)`
- `view.shapes.links.add_hbonds(...)`
- `view.shapes.remove(...)`

The MolSysMT functions referenced by the panels mostly exist in the current
tree, including `structure.get_contacts`, `structure.get_rmsd`,
`structure.get_rmsf`, `structure.principal_component_analysis`,
`structure.center`, `structure.least_rmsd_fit`, `structure.align_principal_axes`,
`pbc.wrap_to_pbc`, `pbc.wrap_to_mic`, `pbc.unwrap`, `hbonds.get_buch_hbonds`,
`topology.get_bondgraph`, `topology.get_dihedral_quartets`,
`molecular_mechanics.get_forces`, `molecular_mechanics.get_potential_energy`,
`molecular_mechanics.potential_energy_minimization`, and several `build.*`
functions.

## Central problem

The central integration problem is the molecular-system source of truth.

The panels read and mutate:

```python
runtime.molecular_system
```

but MolSysViewer already owns the loaded system. The reliable public handle is
the read-only `view.molsys` property — verified live, it returns the
`molsysmt.MolSys` and is the same object as the private `view._molsys`. Note
that `view.molecular_system` is **not** a dependable system handle: it holds
whatever was passed to `load(...)` (on the demo view it is the source-file path
string), so addons should use `view.molsys`. Addons must read that public
surface rather than reach into the private `view._molsys` attribute, which the
panel widget contract forbids. The current lifecycle hook creates or enables the
addon runtime, but it does not reliably seed `runtime.molecular_system` from the
viewer.

Most viewer APIs the panels call exist today, verified live: `view.load` accepts
`mode="replace"`; `view.whole.set_color_by_values`/`reset_colors`,
`view.shapes.add_links`, `view.shapes.add_displacement_vectors`, and
`view.shapes.links.add_hbonds` are all present. Two prototype calls are wrong,
however: `view.shapes.remove(...)` (used in the hbonds, topology, and mechanics
panels) does not exist — the cleanup API is `view.shapes.clear(tag=...)`. So the
core failure is the source-of-truth wiring, plus a few incorrect API calls to
fix.

Consequences:

- In real use, a panel may report "No molecular system attached" even when the
  viewer has a loaded system.
- Transforming panels can set `runtime.molecular_system = new_ms` and call
  `view.load(new_ms, mode="replace")`, creating two potential sources of truth.
- If the user loads a different system through the viewer, the runtime can
  still point to the old system.
- Tests can pass if they seed `runtime.molecular_system` manually, while the
  real viewer flow remains broken.

The addon needs one explicit rule:

- either always resolve the current molecular system from the view at action
  time, and use runtime only for cached results/UI state;
- or keep a runtime working copy, with strict synchronization after every
  viewer load, replace, append, extract, or transform.

The first option is simpler and better aligned with the existing MolSysViewer
architecture. It is also directly supported by infrastructure that already
exists: MolSysMT registers `MolSysView` as a native form (see
`molsysmt/form/molsysviewer_MolSysView/`). Because of that, the MolSysMT verbs
can take the view itself as their argument — `msm.get(view, ...)`,
`msm.select(view, ...)`, `msm.extract(view, ...)` — with no separately held
molecular system. This reframes the decision: the preferred design is probably
not "seed `runtime.molecular_system` from the view" but "hold no system in the
runtime at all, and operate on the view-as-form at action time". The runtime
then keeps only cached results and UI state. Operations that transform the
system produce a new object that is pushed back through
`view.load(new_ms, mode="replace")`, which makes the view (as form) the single
source of truth again on the next action.

## MolSysViewer owns reconciliation, MolSysMT owns mutation semantics

A late but important verification: MolSysViewer already implements the hard part
of live edits — reconciling viewer state after the underlying molecular system
changes. That includes remapping and replaying regions, selections, visibility,
colors, shapes, annotations, measurements, scene look, and the index mapper.

The architecture direction has been refined since the first assessment. The
viewer should keep the reconciliation primitive, but the molecular edit
semantics should live in the MolSysMT addon:

- MolSysViewer now exposes `view.apply_system_edit(new_molsys,
  atom_index_map=None, ...)` as the public low-level reconciliation primitive.
- Compatibility methods such as `view.remove(...)` and `view.add(...)` still
  exist, but internally route through that primitive.
- `view.addons.molsysmt.basic.remove(...)`,
  `view.addons.molsysmt.basic.add(...)`,
  `view.addons.molsysmt.basic.set(...)`, and
  `view.addons.molsysmt.basic.append_structures(...)` are no longer conceptual
  Tier-A aliases: they are addon-owned operations that call MolSysMT and then
  ask MolSysViewer to reconcile through `apply_system_edit(...)`.

Consequences for the addon:

- "Remove the waters" should become
  `view.addons.molsysmt.basic.remove(selection='molecule_type=="water"')` in the
  target 1.0-facing API.
- Existing core methods remain a transition/compatibility surface while the
  wider MolSysViewer proposal (`move_molecular_editing_to_molsysmt_addon.md`)
  decides how to deprecate `view.remove/add`, `molsysviewer.tools.basic`, and
  `view.whole` molecular edit delegations.
- The addon now exposes a `remove-selected-atoms` context action, including a
  selection-driven dynamic item. This is the target GUI route for atom removal;
  the older core context-menu action remains a compatibility path until the host
  migration is completed.
- Per-atom color overrides (`_atom_color_map`, set by
  `view.whole.set_color_by_values`) are remapped and replayed by the
  MolSysViewer reconciliation primitive after atom-index-changing edits. This
  matters for the addon because color overlays applied before a MolSysMT edit can
  survive the reconciliation path.

## Other problems

### Missing adapter layer

Scientific logic currently lives inside each panel's `handle_action(...)`.
This makes it hard to guarantee that panel actions, context actions, and future
Python APIs perform the same operation.

The addon needs an `adapters/` or equivalent service layer:

- panel code should call adapters;
- context actions should call the same adapters;
- the public `view.addons.molsysmt` namespace should call the same adapters;
- tests should validate adapters directly and then validate panel routing.

### Declared but missing contributions

Resolved for the MVP surface: the `AddonSpec` now keeps only implemented
contributions. MVP `context.*`, `workbench.*`, and `exports.*` entries resolve
to real modules, and phantom `shape_providers` were removed until a provider API
is genuinely needed. Post-MVP context/shape/export entries should be added back
only when their modules and tests exist.

### Tests are too shallow for integration confidence

The current tests validate useful bootstrap properties:

- `AddonSpec` contract
- host registration
- lifecycle metadata
- panel class resolution
- panel `on_mount(...)` state pushes
- no-system error paths

However, they do not yet validate enough real workflows:

- loading a MolSysMT system into a viewer and opening a panel;
- basic panel inspection from the actual viewer system;
- selection panel creating or highlighting a real selection;
- color panel applying values with correct element cardinality;
- contacts or topology links producing MolSysViewer shape messages;
- hydrogen-bond links across structures;
- PBC/build/mechanics operations using the right reconciliation route
  (`set_coordinates`, `view.add`, or `view.load(mode="replace")`) and keeping
  state synchronized;
- dependency-related failures for soft scientific backends;
- replay/export behavior after addon operations.

### State model — settled on `addon_states`

The panel widgets now use MolSysViewer's synchronized `addon_states` model for
small UI state snapshots. Python handlers call `AddonPanelWidget.set_state(...)`;
ESM panels hydrate from `model.get(...)` and subscribe to `change:<key>` events.
The previous one-way `push_state(...)` path is no longer used by this addon.

The state split is:

- durable UI preferences and form values can live in `addon_states`;
- scientific results and large arrays should live in Python runtime;
- current molecular system lives on the view, not in addon runtime;
- derived summaries are synchronized as compact `addon_states` snapshots.

### Public addon namespace — wired, and resolved as an active facade

`view.addons.molsysmt` is now wired through `AddonSpec.state_factory` (done in the
addon foundation; see the implementation plan). The remaining question — *what it
exposes* — is resolved in Decision #5 as an **active facade** mirroring the
MolSysMT module layout, with alias / viewer-aware / addon-native tiers.

TopoMT is the precedent for the state_factory *mechanism*: it declares
`state_factory=create_topomt_state`, so MolSysViewer creates a lazy per-view
namespace at `view.addons.topomt`, and its runtime helper prefers that public
namespace, falling back to `view._topomt_addon_runtime` only for legacy
compatibility and test doubles. MolSysMT uses the same mechanism.

Where MolSysMT goes **further** than TopoMT: TopoMT exposes its operations as
module-level functions (`molsysviewer_topomt.attach_topography(view, ...)`) and
keeps `view.addons.topomt` a passive state dataclass. MolSysMT instead makes
`view.addons.molsysmt` itself the **active** API (the facade), so:

- `view.addons.molsysmt` is the public per-view namespace *and* the operation
  surface;
- `view._molsysmt_addon_runtime` is a compatibility alias only;
- panels, context actions, and user code converge on the same facade methods;
- the facade delegates pure science to shared `adapters`, keeping viewer
  coordination (rendering, tags, index mapping) in the facade methods.

This changes the design emphasis. The problem is not that an addon must avoid
modifying the `view` API entirely. The problem is modifying it in an unordered
way. MolSysViewer already has a defined place for addon APIs:
`view.addons.<addon_name>`.

TopoMT also shows what this namespace should and should not hold. Its runtime
stores only session and bookkeeping state — the attached source `topography`,
the active feature/simplex selection, and a `render_groups` map that records the
tags of every layer it drew — so it can clean up and reason about what it
produced. It deliberately does *not* keep a mutated copy of the molecular
system. MolSysMT should treat its namespace the same way: cached results, UI
state, and shape/tag bookkeeping, while the molecular system stays resolved from
the view. As a convenience, TopoMT additionally sets a plain domain attribute
(`view.topography`) so users can reach the attached object directly; that is
acceptable as sugar, but the managed `view.addons.<name>` namespace — not the
loose attribute — is the contract.

### Packaging and dependency cycle

`molsysmt` currently depends on `molsysviewer`, and `molsysviewer` depends on
`molsysmt`. The addon also lives inside the `molsysmt` repository and imports
MolSysViewer classes.

This cycle is confirmed at the code level, not just hypothetically:

- `molsysmt/pyproject.toml` lists `molsysviewer` in its dependencies.
- `molsysmt/basic/viewer/molsysviewer.py` does `from molsysviewer import
  new_view` inside MolSysMT core (this backs `msm.view()`), so the dependency is
  not confined to the addon subpackage.
- MolSysViewer in turn imports `molsysmt` at runtime to render systems
  (`to_form("molsysmt.ViewerJSON")`, `msm.get`, `msm.select`).

So the relationship is genuinely bidirectional and already load-bearing in both
directions. This may work in the local monorepo-style development environment,
but it is a distribution and import-order risk. The clean long-term shape may be:

- `molsysmt`: scientific library
- `molsysviewer`: viewer
- `molsysviewer-molsysmt`: integration package

If the integration stays inside the `molsysmt` distribution, imports must stay
very light and lazy. Heavy optional dependencies must never be imported at addon
module import time.

Two concrete techniques observed in TopoMT keep this safe and are worth adopting:

- Lazy addon construction. `molsysviewer_topomt` builds its `AddonSpec` and
  lifecycle only on demand: the package `__init__` and `addon.py` expose
  `addon`/`ADDON`/`lifecycle`/`get_addon` through module-level `__getattr__`, and
  every MolSysViewer or heavy import happens inside `get_addon()`,
  `get_lifecycle()`, and the action functions — never at import time. The current
  `molsysviewer_molsysmt/addon.py` does the opposite: it imports the spec classes
  at module top level and evaluates `addon = AddonSpec(...)` on import, which
  forces MolSysViewer to load as soon as the addon module is merely touched. This
  should be reworked to the lazy form.
- Capability-guarded spec/lifecycle fields. TopoMT wraps optional keyword
  arguments such as `AddonSpec.state_factory` and
  `AddonLifecycleSpec.on_active_selection_changed` with an
  `_accepts_keyword(...)` check, so the same addon keeps working against older
  MolSysViewer hosts that do not yet expose those fields. MolSysMT should use the
  same guard for any host feature it cannot assume is present.

## Useful existing references

Useful MolSysViewer references:

- `docs/content/developer/addons.md`
- `devguide/addon_panel_widget_contract.md`
- `molsysviewer/addon_templates/dummy_addon.py`
- `molsysviewer/addon_templates/minimal_elasnetmt.py`
- `molsysviewer/addons.py`
- `molsysviewer/viewer/panel_mode.py`
- `molsysviewer/js/src/ui/addons-panel.ts`
- `molsysviewer/js/src/managers/viewer-controller.ts`
- `SMONITOR_GUIDE.md` (SMonitor diagnostics/profiling, for soft-dependency and
  latency handling)

Useful MolSysMT references:

- `molsysviewer_molsysmt/addon.py`
- `molsysviewer_molsysmt/runtime.py`
- `molsysviewer_molsysmt/panels/`
- `devguide/molsysviewer_addon.md`
- `tests/molsysviewer_molsysmt/`
- `molsysmt/form/molsysviewer_MolSysView/`

The `molsysmt/form/molsysviewer_MolSysView/` adapter is especially important:
MolSysMT already knows how to treat a `MolSysView` as a molecular-system form.
The addon should reuse that relationship instead of inventing a parallel
system bridge.

The form implements, among others:

- `to_molsysmt_MolSys.py` — convert the view into a standalone MolSys;
- `get_structural_attributes.py`, `get_topological_attributes.py`,
  `get_mechanical_attributes.py` — attribute access straight from the view;
- `extract.py`, `append_structures.py`, `copy.py`, `attributes.py`,
  `has_attribute.py`, `is_form.py`.

In practice this means the MolSysMT verbs (`get`, `select`, `extract`,
`convert`, ...) already accept a `MolSysView` as input. This is the concrete
mechanism behind the "resolve the system from the view at action time"
recommendation in the Central problem section: the addon does not need to hold
or synchronize a separate MolSysMT object — it can pass the view directly.

The authoritative reference for the current addon structure is the MolSysViewer
developer documentation on the `feature/navigate-panel-redesign` branch
(`docs/content/developer/addons.md`) together with the `dummy_addon` and TopoMT
reference implementations, which the docs point to explicitly (state_factory,
subsections, lifecycle). The `molsysviewer_elasnetmt` package predates this
structure; it may be skimmed for ideas but is not the template.

Useful TopoMT reference:

- `../topomt/molsysviewer_topomt/`

The TopoMT addon is currently the strongest local example of an ordered
MolSysViewer addon integration. It includes real modules for addon spec,
runtime, integration functions, context actions, workbench sections, exports,
shape providers, panels, rendering adapters, and tests. In particular:

- `molsysviewer_topomt/addon.py` wires `state_factory` into `AddonSpec` behind a
  capability guard, and builds the spec and lifecycle lazily through
  `get_addon()` / `get_lifecycle()` so importing the package does not pull
  MolSysViewer in;
- `molsysviewer_topomt/runtime.py` creates `view.addons.topomt` through the
  factory and keeps the legacy `view._topomt_addon_runtime` alias pointing at the
  *same* object, with a fallback for test doubles that have no addons manager;
- `molsysviewer_topomt/integration.py` exposes programmatic operations such as
  `attach_topography(...)`, `attach_features(...)`, and
  `attach_dfnd_tetrahedra(...)`, registers the addon idempotently via
  `register_with_molsysviewer()` (`if not molsysviewer.addons.contains('topomt')`),
  and offers a top-level `new_view(...)` that builds a viewer from a domain
  object, enables the addon, and attaches state in one call — a strong precedent
  for a future MolSysMT `new_view`;
- the runtime's `render_groups`/`tags` bookkeeping gives it deterministic cleanup
  of exactly the shapes it drew;
- it carries an optional `on_active_selection_changed` lifecycle hook that turns
  the current atom selection into addon context-menu items (DFND simplices) — a
  pattern the MolSysMT select workflow may want;
- panel widgets call those shared integration functions instead of owning all
  domain behavior directly.

This is the pattern MolSysMT should emulate more closely than the current
prototype does.

## Known limits of this assessment

This assessment is based on the MolSysViewer addon host, the bundled addon
templates, the current `molsysviewer_molsysmt` package, and the existing
MolSysMT tests and form adapters.

The following items still need direct verification before implementation
decisions are final:

- (optional) `molsysviewer_elasnetmt` for additional ideas only — it predates
  the current addon structure, so it is a secondary reference, not the template;
- the current state of the MolSysViewer panel-navigation redesign branch when
  it is merged or stabilized;
- the final, stabilized API of the third-level panel subsection model
  (`AddonSectionSpec` with `meta={"panel": "<panel_id>"}`): the mechanism itself
  is already confirmed on the `feature/navigate-panel-redesign` branch, but its
  details may still shift before that branch merges;
- exact return shapes for each MolSysMT operation selected for the MVP,
  especially contacts, hydrogen bonds, physicochemical properties, and
  mechanics outputs;
- optional dependency behavior for operations that may require external
  backends or heavier scientific stacks;
- frontend state-sync ergonomics for complex panel forms using `addon_states`.

The document should therefore be read as an architecture and risk assessment,
not as a final implementation specification.

## Recommended MVP

The current ten-panel scope is too large for a first reliable milestone. The
addon's unique value is **MolSysMT analysis rendered or colored into the viewer**
(overlays), not system mutation — mutation (`remove`/`add`) is native to
MolSysViewer and only aliased (Tier A). So the MVP is analysis + overlay:

A practical MVP should focus on:

1. `system`
   - inspect the current viewer system;
   - display atom/group/chain/structure counts;
   - prove the source-of-truth bridge.

2. `select`
   - first slice implemented through `msm.select(...)`;
   - creates and activates a MolSysViewer persistent selection;
   - avoids coloring as the selection side effect.

3. `color`
   - first slice implemented for `charge`, `mass`, and `atomic_radius`;
   - validate element cardinality and units before calling
     `view.whole.set_color_by_values(...)`.

4. `structure` or `contacts`
   - first contacts slice implemented with explicit `output_type="sorted pairs"`
     and `output_indices="atom"`;
   - renders contact links through MolSysViewer shapes and tracks a cleanup tag.

Panels such as `pbc`, `build`, `molecular_mechanics`, and broader mutating
operations should come after the source-of-truth and adapter patterns are
stable. They mutate the molecular system, may require optional dependencies,
and can be expensive or surprising for users.

The navigation model should mirror MolSysMT's own public namespaces rather than
inventing GUI-only categories. The public panels are:

- `basic`
- `topology`
- `structure`
- `hbonds`
- `pbc`
- `physchem`
- `molecular_mechanics`
- `build`

`transform` should not be a root-level panel: centering, RMSD fitting, principal
axis alignment, wrapping, solvation, and related operations belong under their
real MolSysMT namespaces (`structure`, `pbc`, or `build`). A namespace panel can
still contain third-level subsections when it grows, but the first navigation
level should teach the user the MolSysMT API layout.

## Design risks to keep visible

Some issues are not simple missing code; they are design choices that affect
the public behavior of the addon:

- Source of truth: the addon must not silently diverge from the molecular
  system currently loaded in the viewer.
- Reproducibility: every GUI action should have a Python-callable equivalent.
- User intent: operations that mutate or replace the current system need clear
  semantics and possibly confirmation.
- Performance: expensive calculations should not block the panel without
  progress, cancellation, or at least clear error reporting.
- Diagnostics: operations that depend on optional scientific backends should
  report structured failures through the ecosystem diagnostics layer, not raw
  Python tracebacks in the panel. SMonitor should be used for backend import
  failures, calculation errors, and latency-sensitive operations where it adds
  traceability.
- Units and cardinality: values passed to viewer coloring or shape APIs must
  match the target element level and unit expectations.
- Cleanup: addon-created shapes, tags, regions, and colors need predictable
  names and removal/reset behavior. TopoMT's `render_groups` bookkeeping — it
  records the tags of every layer it draws, keyed by kind and tag prefix, so it
  can clear precisely what it produced — is a concrete precedent to follow.
- Packaging: importing the addon must stay light, even if individual actions
  later import heavier MolSysMT functionality.

## Decisions still needed

1. Should the addon continue to live inside the `molsysmt` distribution, or
   should it become a separate `molsysviewer-molsysmt` integration package?

2. Should the runtime store `molecular_system`, or should adapters always read
   the current system from the view? (Given the `molsysviewer_MolSysView` form,
   a third and likely-preferred option is to hold nothing and pass the view
   itself to the MolSysMT verbs.)

3. Which panels are in the 1.0 scope?

4. Which declared contributions should be implemented now, and which should be
   removed from the `AddonSpec` until they are real?

5. What should `view.addons.molsysmt` expose? **Resolved (direction).** An
   **active facade** mirroring the MolSysMT module layout (`.basic`,
   `.structure`, …). `basic` owns live-view molecular edit semantics by calling
   MolSysMT and then MolSysViewer's reconciliation primitive
   (`apply_system_edit(...)`). `.show` / `.overlays` covers addon-native
   compute-and-render flows with no MolSysMT analog. Only entries that add value
   over a bare `msm.verb(view)` belong there. Fine placement settles with usage.

6. What is the error policy for operations requiring optional scientific
   backends? **Answered for the MVP.**

   MVP panels use `molsysviewer_molsysmt.diagnostics.panel_error_state(...)`:
   optional dependency failures produce a compact user-facing message, compute
   failures are reduced to a single line, and SMonitor receives a best-effort
   diagnostic with addon/panel/action context. Post-MVP panels should adopt the
   same helper as they are migrated.

7. Which operations should mutate the current viewer, and which should produce
   a new view or require confirmation? **Largely answered:** MolSysMT owns the
   molecular edit semantics; MolSysViewer owns reconciliation. The addon now
   implements `basic.remove/add/set/append_structures` over MolSysMT plus
   `view.apply_system_edit(...)` while core view mutators remain compatibility
   methods during the transition.

8. How should addon-created tags and layers be named and cleaned?

9. Which panel state should be synchronized through `addon_states`, and which
   should remain Python-only runtime state?
   **Resolved: adopted.** Panels synchronize compact UI state through
   `addon_states`; runtime keeps caches, tags, and scientific results.

10. Should MolSysMT map the active viewer selection to addon-specific context
    actions through an `on_active_selection_changed` lifecycle hook (as TopoMT
    does for DFND simplices), or keep selection handling entirely inside panels?
    **Resolved: adopted.** The hook is registered behind a capability guard and,
    when atoms are selected, offers an "expand to whole residues" context item.
    It also motivated a public MolSysViewer primitive `view.active_selection.set(...)`
    so the addon sets the active selection through a public API rather than viewer
    internals.

11. Should the full feature catalog be represented as root-level panels, or
    should most tools be grouped as third-level subsections under a few parent
    panels? The current panel-navigation redesign makes the grouped model
    available and probably preferable.

## Work ahead

> **Note:** the phased implementation this outline anticipated is **complete** —
> the addon is built and tested (facade, adapters, panels with subtabs,
> diagnostics, packaging, mutation reconciliation, and the selection hook). The
> steps below are kept as the original analysis-level view; they no longer track
> pending work.

The next technical phase should be:

1. Study the current addon reference for the new structure: the MolSysViewer
   developer docs on the `feature/navigate-panel-redesign` branch
   (`docs/content/developer/addons.md`) plus the `dummy_addon` and TopoMT
   reference implementations. Treat `molsysviewer_elasnetmt` as an optional
   secondary read only.

2. Define a small system-access helper. In most cases this can be a thin
   wrapper that simply passes the `MolSysView` to the MolSysMT verbs through the
   `molsysviewer_MolSysView` form, only materializing a standalone MolSys (via
   `to_molsysmt_MolSys`) when an operation genuinely needs one.

3. Create an adapter layer for the MVP operations.

4. Introduce `state_factory` and design `view.addons.molsysmt`.

   The TopoMT pattern suggests implementing this early, not late: the public
   namespace is the place where panel actions, context actions, and Python user
   calls can converge.

5. Reduce the `AddonSpec` to implemented contributions, or implement the
   missing `context`, `workbench`, `shapes`, and `exports` modules.
   **MVP done**: context/workbench/export entries are implemented and phantom
   shape providers are removed.

6. Redesign the panel layout around a small number of parent panels, using
   targeted `AddonSectionSpec` subsections where appropriate.

7. Define SMonitor-backed diagnostics for optional backend failures and
   expensive operations, then make panels translate those failures into compact
   user-facing error states. **Resolved** via `diagnostics.py` and the migrated
   namespace panels.

8. Rework tests so at least one flow starts from a real loaded viewer and then
   exercises the panel or adapter.

9. Add the packaging entry point once the import path is stable. MolSysViewer's
   current discovery implementation supports entry points that resolve to a
   module exposing `addon`, `ADDON`, or `get_addon()`. Use the module form for
   this addon so discovery preserves both the `AddonSpec` and module lifecycle:

```toml
[project.entry-points."molsysviewer.addons"]
molsysmt = "molsysviewer_molsysmt"
```

10. Expand from the MVP only after the core bridge is reliable.

## Current status

This assessment started from the original broad prototype. That prototype was a
useful sketch: it identified the major MolSysMT capabilities that could be
exposed in MolSysViewer, and it already used many real host APIs.

The implementation has since moved past the central architectural problems
identified here:

- `runtime.molecular_system` was removed; the active view is the source of truth.
- `view.addons.molsysmt` is the public per-view facade.
- Panels, context actions, and scripted calls share adapters.
- Phantom spec contributions were removed or implemented.
- The exposed panel set now mirrors MolSysMT namespaces:
  `basic`, `topology`, `structure`, `hbonds`, `pbc`, `physchem`,
  `molecular_mechanics`, and `build`.
- Focused addon tests pass (`tests/molsysviewer_molsysmt/`: 106 passed).
- A backend smoke on real demo viewers passed (16 ok, 0 failed).
- A Playwright visual smoke confirmed Add-ons navigation and panel rendering in
  standalone HTML with no JavaScript console errors.

The remaining validation gap is manual live-widget testing in Jupyter/Qt, where
button clicks can exercise the Python backend. Static standalone HTML is useful
for frontend rendering/navigation only.
