---
summary: Implement a bound MolSysMT tools addon with a scientific API mirror.
issue: uibcdf/molsysmt#421
status: partial
opened: 2026-10-22
closed:
verification: inspected
area: [api, molsysviewer, addons]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bound MolSysMT tools addon for MolSysViewer

**Reported:** 2026-10-22, explicit maintainer direction after reconsidering the
visual-core/scientific-tools boundary with MolSysViewer.
**Status:** partial implementation: six source-qualified `basic` queries, bound
lifetime and new discovery/packaging route; retained-axis removal, geometry setting,
copy/conversion/preflight and sync controls now have source receiving, while other
editing families, panels and broad coverage
remain pending. The maintainer authorizes the Viewer development effort to
implement the owning integration here.

## What

Provide a broad expert facade mirroring scientific module/function paths under
`view.addons.molsysmt`, bound to the actual current `view.molsys`. Design task
panels over that API for nonprogrammers. Keep general molecular preparation and
editing in this addon; Viewer retains visual scene owners and qualified visual
convenience calculations. Coordinate Viewer receiving through
uibcdf/molsysviewer#264.

## How

Selected source baseline: `fe5036c1f4c145ec2eecf1627e80eb70fc995618`.
The [source ledger](../../devtools/data/molsysviewer_tools_addon_source_inventory.json)
uses the provider's own `validate_api_stability.py::discover_exports` over its
tracked scopes, with AST resolution of exported definitions and fixed-source
hashes. It records 267 exports: 190 function paths (including aliases), 34 class
paths, 11 data paths, 31 module paths and one external namespace. It verifies
203 source files. These are source-discovery counts, not implemented wrappers,
unique algorithms or scientific qualification. No scientific imports/calls were
performed to construct the ledger.

Preserve native names, defaults, returns, options, units, validation and
scientific provenance. Bind only the primary system slot; additional systems,
reference systems, filenames and factory inputs remain explicit. Collection
operations need their own ordered-input contract. The historical 169-export
inventory in Viewer remains an earlier source snapshot, not the current facade
specification.

Preserve `in_place`, including `basic.remove`'s current default `False`.
Independent native results do not replace the view. Admitted edits of the bound
system synchronize by default; a qualified `update_view=False` defers only visual
synchronization. No collision with `update_view` exists in the ledger's AST
parameter names; runtime/decorator options still require receiving.

`get_sync_status` and `sync_view` are source-received facade integration
controls for the admitted removal and geometry-setting routes. The host owns
pending/failed/uncertain state, completed-result access after failed
synchronization, composed maps, stale-index protection and lifecycle. Broader
mutations still need their own effect receiving; private Viewer methods do not
substitute for an admitted integration boundary.

## Why

The retired addon had only four basic editing functions, an empty structure
namespace and compute/render routes now owned by visual core domains. It is not
the complete, discoverable scientific mirror requested by the maintainer.
Reverting its retirement would also evade current packaging/discovery guards.
The new addon is a different implementation premise.

## What is measured and what is assumed

The ledger records AST signatures/default expressions, source documentation,
decorators, provider stability and binding candidates. Explicit parameter names
suggest a binding slot; they do not establish scientific effect or safe mutation.
Every entry is marked pending adaptation and unqualified. Optional engine
behavior, native runtime returns and decorator overrides need executed parity.
No time or memory target is inferred from these counts.

Untracked namespace contents, native class methods, factories and infrastructure
still require explicit exposure/exception decisions. Do not claim whole-package
completion solely because the stability registry's tracked exports are listed.

## What was refuted

The general observer request uibcdf/molsysmt#413 remains withdrawn and closed.
The addon coordinates its own calls; raw arrays and direct external calls are
not automatically observed. Restoring the previous `show`/`overlays` API would
duplicate current scene owners. Forcing `in_place=True` in expert wrappers would
violate native semantics; GUI actions can choose explicit arguments for their
declared edit. A full-system copy on every call is not a required safety model.

## Scope and exclusions

Implement the facade, provider-owned panels, registration/spec and qualified
packaging. Normal MolSysMT import remains independent of Viewer/browser; optional
engines remain lazy. Provider docs own capabilities, expert API and graphical
usage, methods, examples and limits, including the course. Viewer docs own addon
management, creation and catalogue links. No new detector, universal observer,
general Undo, scientific stability promotion or public release follows from this
issue. The native backend dependency floor remains unchanged by this source pass.

## Acceptance criteria

Complete per-symbol binding/effect/mapping/return/engine dispositions before
calling the facade complete. Pending ledger entries cannot count as coverage.
Use real systems to test native parity, independent and in-place branches,
nonconsecutive/repeated structures, units, references, rejection/partial writes,
scientific validity, pending synchronization and recovery without repeated
science. Qualify cached handles across loads, panel disable versus headless
access, closed views, two views and stale completion with Viewer.

Then qualify task panels through real Jupyter/popup actions, update API/user/course
docs and replace legacy-absence package guards with positive compatibility tests
for the new integration. Installed qualification and release authorization remain
separate from source receiving.

## Dependencies and risks

Viewer receiving uibcdf/molsysviewer#264 owns general structure correspondence,
safe synchronization and host/lifecycle changes. No current host capability is
assumed from a marker or version guess. Tool-specific provider gaps discovered
later need separate owned reports. Avoid silent configuration changes, raw
mutable alias observation promises and default full-trajectory copies.

## Provenance

Source-only inspection on 2026-10-22 using the development environment
`molsyssuite@uibcdf_3.14`. The ledger names exact provider and Viewer checkpoints,
source hashes and its limits. The provider stability registry remains the
authority for native API stability; no addon stability is inferred from it.

## First read-tool delivery

The provider-owned `molsysviewer_molsysmt` package now supplies `basic.get`,
`select`, `info`, `get_attributes`, `has_attribute` and `get_label`, plus their
root aliases. The explicit allowlist does not proxy unreviewed mutators.
Signatures/defaults and help use native contracts with the primary input bound;
scientific arguments are validated by the original public scientific call.
The facade's ArgDigest configuration validates integration controls and delegates
scientific domains, without forcing trusted digestion bypasses.

New entry-point metadata uses `molsysviewer_molsysmt.tools`. Root package import
is independent of Viewer, factories are lazy, cached methods follow replacement,
panel deactivation preserves Python access, and closed/empty views fail clearly.
Read wrappers add no trajectory copy or scene commands; native scientific cache
behavior remains unchanged. `tests/molsysviewer_molsysmt/test_read_tools.py` uses
real bundled viewers and metadata discovery. Older hosts have an explicit
compatibility skip for these tests; that is not addon qualification.

One shared packaging contract requires the eight reviewed source files and new
entry point across sdist/wheel/installed probes. Retired routes/files retain
negative guards. These are structural checks, supplemented by the installed
probe's real automatic-discovery/native-read parity; they do not by themselves
qualify an artifact. Editable development metadata refresh is not a clean solver
installation or a preserved release. The original source ledger remains fixed
historical input and does not certify these new wrappers.

The initial bounded checks pass 46 read/packaging cases (including all 16
real read-tool tests), plus the retained historical packaging selector after
its guard name was preserved. Viewer receives the host changes in
`60659082596eb055054da99364715b5cef7f3767`; routine source callers and the full
workflow default now pin that source instead of the legacy-refusing `66ea54e4`.
Runtime dependency floors and explicit candidate inputs remain unchanged.
The consumer's full local core run retains the existing box-fixture failure
uibcdf/molsysviewer#263; no global green or exact installed qualification is
claimed. Both documentation builds complete, with unrelated provider warnings
retained. Native course code cells/outputs are unchanged; the integration note
links the new provider-owned guide.

The Viewer formatting-only follow-up is `7449675aa8407e94136357f11da1256188e46183`
(AST identical to the tested host logic). Routine/full-default source pins now
use that head; explicit release-candidate inputs remain authoritative. The
separate false-positive documentation dependency guard was reported as
uibcdf/molsysmt#427, without adding a guessed external package.


## Independent extraction and retained structure receiving

The facade additionally supplies `basic.extract` and its root alias, preserving
the native signature/defaults, target forms, output-file argument and
`copy_if_all` policy. Independent results are not adopted; unrestricted native
live-reference behavior is not converted into a copy or automatic observation.
The same source parity suite now exercises repeated/nonconsecutive structures,
independent coordinates/topology, native errors and unchanged scene state.

Viewer receiving under uibcdf/molsysviewer#264 now admits a retained
`structure_index_map` for live molecular adoption, shared with independent
View extraction. That boundary does not yet qualify managed mutation, deferred
synchronization or failed-rebuild recovery. This phase adds no mutator or task
panel and does not alter the published compatibility floor.


The two user-guide Python blocks execute sequentially with real automatic
entry-point discovery after refreshing a stale, ignored local egg-info that
shadowed the already-correct editable distribution. Automatic discovery and
bound extraction also pass from the Viewer checkout. The metadata diagnosis
and conditional refresh procedure belong to the maintained integration guide;
no manual registration or host lookup exception is introduced.


## Managed retained-axis edit receiving

The first writer is native `basic.remove`, with the provider's False default,
independent outputs, true in-place mutation, native None return and authoritative
retained atom/structure maps. `update_view=False` defers only scene projection;
`get_sync_status` and `sync_view` expose the shared host state/retry route.
Provider preparation reuses owned native validators and publication contracts;
Viewer owns map composition, stale-index gates, scene metadata checkpoint/retry
and explicit replacement recovery. Empty in-place axes are rejected before
execution by the initial receiver; independent outputs preserve native behavior.

The source receiving guard is `tests/molsysviewer_molsysmt/test_remove_tools.py`,
using actual demos and native operations. A fault-injecting real widget interrupts
projection after science, checking retry without a second removal or double
remapping and preservation of handle identities. The generic coordinate/uncertain
and locking cases also exercise actual native setters. No scientific success is
mocked. Ordinary read/extract guards remain applicable. Installed artifact
qualification, wider effects and task panels are not implied by these results.


Source receiving checkpoint: Viewer `9da52e5500c9f8637e2f6f76eea0eb81ce783882`. Routine smoke/docs/full-fallback
source routes now pin that managed-edit receiver; explicit candidate inputs retain
precedence. Local receiving passes 17 remove/control cases, 20 read/extract cases,
30 packaging guards and all three guide Python blocks in
`molsyssuite@uibcdf_3.14`. Viewer retains its once-run full-suite result (3,266 pass,
21 skips, two subsequently corrected inventory/TypeScript failures), focused
corrections and the real Chromium receiving evidence under uibcdf/molsysviewer#264.
These are working-source checks, not a frozen installed pair. Hosted exact-source
CI remains to be inspected after this delivery; no runtime dependency floor,
package, tag or release is changed.


## Coordinates and box source receiving — 2026-10-23

`basic.set` now has an explicit partial effect inventory: coordinates and box,
retained nonempty axes, native scientific signature/None return, and update_view.
Other attribute names remain valid native names but their effects are unreceived;
keyword typos are rejected through the shared native ArgDigest attribute domain.
Provider-owned preflight normalizes units/selectors and checks the integration's
retained dimensions before native execution. No second molecular authority exists.

Nested writes are received through the host's explicit rejection_check token
reader, so an older host rejects before science rather than silently ignoring a
plan option. Tests cover native parity, nonconsecutive/repeated structures,
coverage/snapshots (also actual Buch results), deferred removal plus geometry,
invalid requests, partial-write uncertainty and connector interruption/retry.
The visual synchronization currently rebuilds the scene: bounded or incremental
trajectory transfer is not established by this receiver. Broad attributes,
other namespaces, task panels and installed pair qualification remain pending.

The geometry source delivery receives Viewer
`deaba4cbea43015859544b1b393ecbe02dd2ee19`. Routine source pins and smoke
preflight now require its explicit rejection token argument, and smoke runs
the read, remove and set guards. Local source checks pass 23 setter cases,
37 existing addon cases, 30 packaging guards and all four guide Python blocks
in `molsyssuite@uibcdf_3.14`. Viewer reports 3,278 core passes with 21 skips,
eight coordinator cases and real Chromium coordinate/box receiving. The source
receipt is owned under uibcdf/molsysviewer#264. Course Module 06 availability
prose is updated; its executable cells and outputs are unchanged. New hosted
checks and exact installed-pair qualification remain pending.


## Independent conversion receiving — 2026-10-23

The next basic slice adds native copy, conversion and conversion preflight through
serialized reader calls. Independent molecular results are returned without
adoption; full native sharing remains available through converter options.
Explicit filenames identify Python-host files. Reports/strict behavior and
optional dependencies stay provider-owned; no format-completeness or multi-file
atomicity promise is added. The bounded guard is
`tests/molsysviewer_molsysmt/test_conversion_tools.py`, including real H5MSM with
named sparse analyses, reordered/repeated structures, preserved destination
bytes on preflight, independent ownership, pending reads and lifetime/errors.

The [dated conversion receipt](../../devtools/data/molsysviewer_tools_conversion_receiving_20261023.json)
records the per-function binding/effects and bounded results: 122 addon/packaging/route
checks, three final file-route/option cases (one overlapping), all six guide Python
blocks and 3,278 Viewer core passes with 21 skips. The host token fixture is now
received against both current provider source and cached public 0.23.0 runtime.
It observes edited values instead of assuming either native storage implementation.
New hosted source gates and exact installed qualification remain pending.
