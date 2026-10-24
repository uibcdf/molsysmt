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
copy/conversion/preflight, composition/identity queries, read-only comparison,
all eleven current topology readers, eighteen structure calculations and sync controls
now have source receiving, while other editing families, panels and broad coverage
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


## Composition and comparison receiving — 2026-10-23

The basic slice receives `contains`, `is_composed_of` and
`compare(redefine_indices=False)`, with the second system explicit. The native
forced topology-rebuild branch mutates both inputs and stays unreceived; reject
it before effects, not as a hidden reader call. Native query cache behavior,
separate scopes, result types, errors and lifetime remain unchanged.

The compare alias is re-scoped from provider-owned AliasTable declarations
before local defaults are forwarded. This protects the native historical alias
without accepting a user-written canonical/alias collision. The bounded guard
is `tests/molsysviewer_molsysmt/test_predicate_tools.py`, including actual native
calls, deferred data reads, independent reference scopes, empty/closed views,
negative inputs and preservation of both input topologies on rejected rebuilding.

The [dated predicate receipt](../../devtools/data/molsysviewer_tools_predicate_receiving_20261023.json)
records the per-function modes/effects, native source hashes and executed results:
33 predicate/comparison cases, the complete 157-case addon/packaging/route regression,
all seven guide Python blocks and unchanged executable course Module 14 cells.
It also retains the prior source-pair pandas failures and experimental Qt scope.
Native structural comparison emits UnitStrippedWarning; observed parity remains
intact and the warning is not silently suppressed by the addon. Forced two-input
rebuild, broader namespaces and panels remain separate receiving work.


The native structural-comparison quantity warning is now separately reported in
uibcdf/molsysmt#435, at the maintainer's request. It reproduces without Viewer;
observed parity is preserved and no wrong scientific result is demonstrated.
Keep the fix in the native comparison/unit owner rather than adding a filter
or alternate algorithm to this addon.


## Identity and explicit collection receiving — 2026-10-23

Receive bound get_form, is_a_molecular_system and where_is_attribute, plus the
explicit-input are_multiple_molecular_systems utility. Do not guess a single
primary slot for a collection classifier. Native input inspection is preserved;
there is no promise of I/O-free classification. It remains usable before loading a
system, but requires a live owning view and caller-stable inputs rather than
implicit edit locking. Identity readers retain serialized current-target access.
Native live owner references and fallback policies remain unchanged.

The three intentionally undigested native helpers stay untouched. Their facade
adds a keyword-only addon digestion control without forwarding an unsupported
scientific parameter; ordinary where_is_attribute forwarding remains native.
The bounded guard is `tests/molsysviewer_molsysmt/test_identity_tools.py`.

The [dated identity receipt](../../devtools/data/molsysviewer_tools_identity_receiving_20261023.json)
records all four binding/digestion dispositions, 28 focused cases, 239 applicable
addon/packaging/dependency/devguide checks and all eight guide examples. Module 04
only gains availability prose; its executable cells and outputs are unchanged.
The source checks preserved the concurrent native namespace/documentation work;
they are not an exact clean full-provider or installed-candidate claim.


## First topology namespace receiving — 2026-10-23

The source adds an explicit topology namespace for graph, covalent block/path
and dihedral-quartet readers. It reuses the same private current-target delegate
as basic, keeping serialized reads, ownership, cached methods and pending data
semantics. Graph cuts remain analytical; no molecular edit or graphical result
is implied. Hypothetical label arrays and ragged lists/sets remain native.

Native skip arguments are forwarded only where declared. Path/quartet controls
belong to the addon boundary and are not injected into scientific kwargs.
Native optional request limitations remain visible instead of being converted
to fabricated success. Other topology functions need their own receiving.

The [dated topology receipt](../../devtools/data/molsysviewer_tools_topology_receiving_20261023.json)
records 32 focused cases, the complete 271-case applicable regression and nine
executed guide blocks. Source/wheel/sdist metadata includes the new topology
module (14 addon Python files); this is not installed-artifact qualification.

Using the owning AST inventory over provider 2d5fbb7d5 updates the export-name
count from the earlier 267 paths to 271 across the same 21 tracked scopes. Added
paths are basic/root compose_atom_maps, build.project_atom_names and
build.merge_nonpolar_hydrogens. They remain pending adaptation with their own
binding/effect review. The earlier resolved AST/signature ledger is retained as
its dated snapshot; this name-only delta does not qualify all new functions or
untracked native class/form-specific iterator APIs. The receipt lists all basic
and topology exports as received, conditional or pending rather than silently
omitting them.


## Eleven topology exports received in source — 2026-10-23

The explicit topology namespace now also wraps get_rings, get_rigid_fragments,
get_rotatable_bonds, get_substructure_matches, get_atom_correspondences,
get_sequence_alignment and get_sequence_identity. All eleven baseline exports
have current-primary binding, native signatures/defaults/returns and serialized
reads. No new host runtime, unrestricted proxy, automatic molecular preparation,
result attachment or scene update is introduced. Optional engines remain native.

The [completion receipt](../../devtools/data/molsysviewer_tools_topology_completion_20261023.json)
records 39 focused cases, 310 applicable regression cases, eleven guide examples,
37 passing docstring examples and Ruff checks. Module 13 gains narrative only;
its code cells and outputs remain unchanged. The prior 40012474771 smoke was
cancelled during main advancement, not a passing test result. The new exact-head
hosted smoke is still required; these working-source results are not a clean
solver-installed artifact pair.

Native identity on capped pentalanine reveals a scientific group/sequence-axis
mismatch, filed with maintainer authorization as uibcdf/molsysmt#439. The addon
preserves native behavior, documents the limitation and demonstrates explicit
amino-acid selections; it does not implement a competing formula. Reference
inputs remain explicit/caller-stable, search limits retain native scope, and
insufficient chemistry raises rather than being silently prepared. Hypothetical
cuts and correspondences are scientific outputs, not edits or scene objects.

This completes the reviewed topology mirror only. The broader source ledger,
other modules, general edits, lazy/support utilities, panels and installed
compatibility remain pending; #421 and uibcdf/molsysviewer#264 stay partial.


## Six structure calculations received — 2026-10-23

The first explicit structure namespace receives distances, vectors, centers,
radius of gyration, angles and dihedrals with native signatures/options/results.
It reuses the host's serialized reader, resolves the current primary system per
call and keeps an auxiliary system and selectors caller-owned. No coordinate
edit, automatic preparation, result attachment, measurement creation or scene
projection is introduced. Missing native dihedral skip_digestion is handled by
an addon-only keyword, never injected into scientific named flags.

The [source receipt](../../devtools/data/molsysviewer_tools_structure_receiving_20261023.json)
records 54 focused cases, the one complete applicable regression, fourteen guide
examples and sixteen passing native-docstring examples. Packaging metadata guards
now include all fifteen addon Python files. Module 16 gains narrative only; all
existing executable cells/outputs and protected course topics remain unchanged.
Ruff and local guide checks pass. These are source checks, not an installed
artifact pair, optional GPU qualification or general memory bound.

Independent coordinate references protect supported distance/vector and weighted
center/radius routes. Native CPU/PBC/output/angle behavior is also parity-tested.
Native forced calculations reveal two scientific defects, filed with maintainer
authorization: uibcdf/molsysmt#440 (radius physical scale in alternate length
units) and #441 (second distance population discarded). Affected-route parity
is explicitly not a scientific pass; the addon neither silently switches mode
nor overrides units/formulas. Their native reports retain independent bundled
reproductions and required guard outcomes.

Owning AST namespace discovery accounts for all current structure exports;
only these six are received. Other calculations, transformations, support/lazy
utilities and graphical panels remain pending. #421 and uibcdf/molsysviewer#264
stay partial. Prior topology CI 40014551589 passes on provider c4b71b206;
new exact-head CI is still needed for this structure delivery.


## Four distance-independent structure readers — 2026-10-23

The maintainer requires waiting for the MolSysMT development team on #441.
No scientific distance fix, alternative algorithm or hidden heavy-mode routing
is introduced here. Min/max/contact/neighbor wrappers remain pending. Reviewed
raw/minimum RMSD, principal axes and least-squares planes use independent direct
paths with numeric/plain-property selectors and are now explicitly received.
Rich selectors and optional engines retain their own native dependency limits.

The [source receipt](../../devtools/data/molsysviewer_tools_structure_comparison_receiving_20261023.json)
records 36 focused cases and one complete applicable regression, seventeen
executed guide blocks, twenty-six native-docstring examples and Ruff checks.
NumPy norms, Kabsch/SVD, weighted covariance and plane residuals protect actual
values, while lifecycle, pending reads, source/reference preservation and native
errors have integration receiving. Module 16 gains narrative only; existing
code/output and protected transformation/RMSD topics remain unchanged. Packaging
inventory remains fifteen addon Python sources; no host runtime or protocol changes.

A separate native RMSF forced-unit defect was reproduced without Viewer and
filed with maintainer authorization as uibcdf/molsysmt#442. RMSF remains unreceived;
the scientific team owns its correction. Prior #440/#441 affected routes retain
their explicit limits. The owning AST inventory now accounts for ten received
and eighteen pending structure exports, not a complete scientific toolbox.

Previous six-reader structure smoke 40016357086 passes on provider 8ebb1b4d5.
That evidence is retained under its scope; new exact-head receiving remains
pending for these four readers. The overall addon and Viewer receiving remain
partial, with other namespaces, mutations, graphical panels and clean installed
compatibility unfinished. No freeze, tag or release is authorized by this work.


## Native fixes received and three relation readers — 2026-10-24

The native fixes for #439/#440/#441/#442 are closed and now have bound receiving.
Source bae6d0101 repairs distance endpoints; 1123eeb7d repairs observable units and
sequence source groups, with the keyword-only native flag qualified at bc2142831.
The provider already updated the bound identity flag. This delivery adds no
scientific correction or hidden routing/unit change.

New explicit structure wrappers cover get_maximum_distances, get_contacts and
get_rmsf with native signatures/results and the current primary system implicit.
The [source receipt](../../devtools/data/molsysviewer_tools_relations_receiving_20261024.json)
records 47 focused cases, a single 535-case applicable regression, eighteen guide
blocks and 74 native-context docstring examples. Independent coordinate/variance,
threshold and argmax/index references protect physical values and source domains.
Ruff and developer-guide checks pass. The source/wheel/sdist inventory remains
fifteen addon Python files; Modules 13/16 gain current receiving prose only,
preserving executable cells/outputs. Earlier receipts remain historical evidence.

Native minimum second-center weighting and neighbor second-system forwarding
still fail independent reproductions. With explicit authorization, they are
reported as uibcdf/molsysmt#444 and #445; those wrappers remain absent pending
scientific-owner fixes. The maintainer explicitly requested a pytest contract
matrix for get_distances/get_neighbors/get_minimum_distances/get_maximum_distances
in both issue comments, including independent numeric/index oracles and critical
parameter/path combinations. This bounded receiving does not claim to complete
that native family review. The structure inventory accounts for thirteen received
and fifteen pending exports; overall #421 and uibcdf/molsysviewer#264 remain partial.

Provider CI smoke 40123084475 passes on bc2142831 for the repaired earlier readers.
New exact-head CI remains pending for this delivery. Optional engines/GPU,
universal RAM bounds, general edits, panels and installed artifact qualification
retain their separate scopes. No freeze, tag, Release or package publication.


## Local minimum and neighbor receiving — 2026-10-24

The maintainer authorizes receiving the provider working tree before its owner
commit. Explicit get_minimum_distances and get_neighbors wrappers preserve the
native signatures after primary binding, including native skip_digestion. The
neighbor wrapper re-scopes the native criterion-admission contract before
forwarding defaults; absent criteria stay absent and explicit incompatible calls
still fail. No scientific formula, weight substitution or fallback is added.

The local receiving record under uibcdf/molsysmt#421 retains provider base
3502232d802ee2927f6b6f5d19f0ae045777ecb5, host base f9a87cb55f9041cffab415fa3b3ddaded54c647a,
file/extension SHA-256 values and original JUnit digests. The source is unchanged
during the 1001-case applicable regression: all pass without errors or skips.
It includes 424 cases from the native family matrix and the 89-case bound
relation file. Nineteen guide blocks and 74 native-context docstring examples
pass, as do Ruff and the sixteen-file packaging inventory. The addon receiving
paragraph in Course Module 16 changes narrative only; the scientific team owns
its independent course changes.

Independent physical-value/index references cover separate endpoint weights,
translated auxiliary systems, repeated structures, units and supported sparse
outputs. View state, analyses, pending-edit status, lifetime and replacement
binding remain guarded. Structure now has fifteen received and thirteen pending
exports; other namespaces, task panels and installed qualification remain partial.
Provider commit/CI and the owner's closure of uibcdf/molsysmt#444 and
uibcdf/molsysmt#445 remain separate. No tag, package, dependency-floor change,
release candidate freeze or public publication is implied.


After this stable regression, the scientific team updated the five native public
function files while extending their documentation. Those later file hashes are
recorded separately; the earlier 1001-case result is not automatically transferred
to changed bytes. The updated documentation passes 19 guide blocks and 90
native-context docstring examples. Final owner-commit/CI reconciliation remains
pending. Host reporting/link guards pass 276 cases and both guide/index checks
pass.


## Structural-analysis source receiving — 2026-10-24

The provider working tree adds get_symmetry_corrected_rmsd,
get_secondary_structure and principal_component_analysis through the existing
serialized primary reader. Native signatures, explicit references, chemical
states, map/constraint scope and execution choices remain intact. The native
secondary-structure helper has no skip flag; its addon-only keyword is not
forwarded. The other native flags retain their ordinary semantics. No host
runtime, wire protocol, coordinate edit or result attachment is introduced.

The provider receipt under uibcdf/molsysmt#421 records 1099 passing
applicable regression cases and 44 focused real-view cases, zero failures/errors/
skips, plus 22 guide blocks and 103 native-context docstring examples. Original
JUnit digests, exact source hashes and source copies are retained. The watched
scientific and addon sources stay unchanged during this regression. Only the
generated version module changed when the owner committed those scientific
corrections; result version strings retain their initial-import provenance. Native/packaging/lifecycle
checks and Ruff pass; this does not qualify clean solver-installed artifacts.

Independent weighted covariance reconstruction and pose geometry over explicitly
declared maps protect values and units; MDTraj codes and actual group/structure
correspondence protect the DSSP integration. Tests retain saved analyses, scene
state, pending updates and cached reader binding after replacement. Discovery
does not import the optional engines. Numerical degeneracy, dense PCA memory,
engine prerequisites and experimental symmetry scope stay explicit.

Native PCA's documented list weights reproduce a Rust type failure independently
of Viewer. The authorized owner report is uibcdf/molsysmt#448. The received CPU
routes use default or float64 ndarray weights, with no addon normalization or
scientific workaround. Eighteen structure readers/calculations are now received;
ten coordinate-changing exports remain pending. The course addon paragraph gains
only current receiving prose; other provider course changes are separately owned.
Overall uibcdf/molsysviewer#264 / uibcdf/molsysmt#421 remain partial, and local
source receiving does not authorize publication or imply completed exact-head CI.


The native scientific owner subsequently committed 5710cc0cff1f3f468823699104e51e6fe029c3b2 and closed
uibcdf/molsysmt#444 and uibcdf/molsysmt#445. This reconciles the earlier local
receiving without rewriting its original hash-scoped evidence. The pending PCA
weight-container defect stays under uibcdf/molsysmt#448. Addon-head CI remains
separate from the native commit and the local applicable regression.
