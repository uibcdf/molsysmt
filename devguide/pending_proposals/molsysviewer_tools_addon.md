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
lifetime and new discovery/packaging route; editing, panels and broad coverage
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

The Viewer receiving draft proposes `get_sync_status` and `sync_view` as facade
integration controls. These names are proposals, not current APIs. The draft
defines pending/failed/uncertain state, completed-result access after failed
synchronization, composed maps, stale-index protection and lifecycle. Review
the exact public protocol before mutating wrappers; do not call private Viewer
methods as a substitute for an admitted integration boundary.

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
