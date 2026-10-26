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
all eleven current topology readers, eighteen structure calculations, native translation/rotation/reflection/fitting/centering/displacement/principal-axis alignment/dihedral editing, ten PBC queries/factories, three periodic coordinate editors, seven physchem property readers and sync controls
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


## Translation and PCA weight repair received — 2026-10-24

The explicit structure.translate wrapper preserves native defaults and returns,
including independent in_place=False output. In-place calls add only keyword-only
update_view=True over the existing coordinator. Family preflight resolves retained
target/selection/structure scope and active-edit exclusion; native science owns
displacement, broadcasting and publication. Independent results are not adopted.
No host runtime, protocol, alternate scientific calculation or full scientific
recovery snapshot is added.

Targeted receiving passes 35 translation cases and 79 structural-analysis cases.
The one applicable 1274-case regression records 1268 passes and six failures from
the obsolete assertion that translate must be absent. The expected public
inventory was updated; all 89 cases in the two affected files pass, including
all six original failures. The full local suite was not repeated. Original
JUnit digests and source snapshots distinguish the initial run and focused
correction; they are not mislabeled as a single green full-suite run. Runtime
scientific/addon files remain fixed during that initial run; only the generated
version module changes. Ruff and 23 guide blocks/105 native-context docstring
examples pass. Exact-head hosted CI remains a separate gate.

Independent displacement and weighted covariance references guard physical
values/units, source ownership, repeated/nonconsecutive axes and repaired PCA
containers/dtypes from 306e91dda (uibcdf/molsysmt#448). Native setter invalidation
preserves unaffected named-analysis coverage. Tests retain scene handles, source
records and navigation, compose pending geometry/removal, and exercise real
transport failure after science with synchronization-only retry. Possible partial
publication becomes uncertain rather than implying rollback or repeat execution.

The authorized native report uibcdf/molsysmt#451 records center's partial-reference
target and in-place return inconsistency without Viewer. Center remains absent;
its scientific owner decides the supported population contract. Source now
provides eighteen structural readers/calculations plus one native coordinate
editor; nine coordinate-changing exports and the broader addon remain partial
under uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. No package, public floor,
version freeze or release is implied.


## Rotation and reflection received — 2026-10-24

Explicit structure.rotate and structure.flip wrappers mirror native scientific
parameters, independent in_place=False outputs and in-place None returns. The
existing retained-axis coordinator owns synchronization; no Viewer runtime,
protocol or scientific normalization is added. Flip's keyword-only
skip_digestion controls addon validation only, because the native callable has
no declared flag. Native public validation remains active.

Independent Cartesian quarter-turn/plane references and inverse/involution and
distance invariants receive proper rotations and explicit-unit-normal reflections.
Matrix lists, strided/read-only per-structure stacks, per-atom stacks and actual
SciPy Rotation objects retain native behavior. nm/angstrom/pm contexts, repeated
and nonconsecutive atom/structure axes, untouched boxes and exact edited-structure
interaction invalidation are exercised with real bundled views. Deferred mixed
rotation/translation/removal/reflection retains scene handles, selections, source
accounting and navigation. A real transport interruption after completed science
is recovered by synchronization without executing the transformation twice.

The focused transform file passes 93 cases. The single applicable regression
passes all 733 cases, with zero failures/errors/skips. Scientific/addon source
hashes remain fixed during the regression; only the generated version module
changes. Ruff check/format and 24 guide blocks/110 native-context docstring
examples pass. Original JUnit digests, scope and before/after source snapshots
are retained in the provider's rotation receiving record. Host reporting/link
checks pass 280 cases. Exact committed-head CI remains a separate pending gate.

Native flip independently rejects vector=None before its implementation fallback;
nonunit vectors are not normalized and change distances, while a zero vector is
accepted as a no-op. This receiving certifies only explicit unit normals and
retains the defects visibly in runtime help and owning documentation. The addon
supplies no hidden alternate formula. Center stays absent pending
uibcdf/molsysmt#451. Twenty-one structure tools are now available in source:
eighteen calculations and three coordinate editors; seven reviewed edits and
the broader API/panels remain partial under uibcdf/molsysmt#421 and
uibcdf/molsysviewer#264. This does not qualify installed artifacts or authorize
any tag, release or public promotion.


## Native rigid fitting and sequence alignment received — 2026-10-24

Explicit structure.least_rmsd_fit and structure.least_rmsd_align preserve native
scientific signatures, independent defaults/results and in-place None returns.
Only keyword-only update_view is added over the existing geometry coordinator.
Fit anchors and moved populations remain distinct; sequence-derived alignment
moves whole selected components. Caller-owned references remain stable inputs,
without locking or synchronizing another view. Independent outputs and conversion
stay in Python; native setters own exact edited-structure analysis invalidation.
No alternate correspondence, fitting, periodic reimaging or host runtime is added.

Independent Cartesian poses protect physical values, partial and whole-component
movement, reference indices and mixed-unit native reference forms. Repeated and
nonconsecutive structures, native CPU precision, cached facade/replacement,
source/scene identities, pending mixed edits and actual transport failure are
received. Synchronization-only retry preserves coordinate storage; an exception
after a real scientific publication enters uncertain state instead of rollback
or repeated science.

The final focused file passes 49 cases. The single 956-case applicable regression
records 952 passes and four failures from a historical assertion that
least_rmsd_fit must still be absent. Only that inventory expectation was corrected;
all 85 cases in the two affected files then pass, explicitly including all four
original failing nodes. The full local suite was not repeated or relabeled green.
Initial fixture corrections and the native numeric-selection reproduction retain
separate original JUnits in the provider's fitting receiving record.

Concurrent native center/get_center and related scientific/documentation work was
present in the local tree. Watched hashes record center.py and generated version
changes during regression; bound-addon/fitting-test sources remain fixed. The
run is scoped working-tree evidence, not one clean immutable native head. Other
native edits and shared-page hunks are excluded from this integration. Exact
committed-head hosted CI remains a separate gate. Ruff and 25 guide blocks/114
native-context docstring examples pass; host reporting/link checks pass 280 cases.

The authorized native reports uibcdf/molsysmt#452 and uibcdf/molsysmt#453 record
None-reference failure and numeric atom/group-index confusion in least_rmsd_align.
Its received route uses explicit references and MolSysMT expression selections;
no silent reference replacement or index-to-expression rewrite is introduced.
Native least_rmsd_fit's implicit self-reference is received separately. Optional
GPU forwarding is not GPU qualification. Earlier reflection limits and the
unreceived center under uibcdf/molsysmt#451 remain separate. The source facade now
exposes twenty-three structure tools: eighteen calculations and five coordinate
editors, with five other reviewed edits and broader coverage/panels pending under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. No installed package qualification,
public floor, tag, release, version freeze or promotion is implied.


## Native centering contract resolved — 2026-10-24

uibcdf/molsysmt#451 is resolved in 5814dc534. The new native source/destination
contract is documented in the [current addon guide](../molsysviewer_addon.md).
Earlier findings above are historical. Receiving the new center contract in
the addon remains pending under uibcdf/molsysmt#421; no wrapper is added here.


## Native sequence-alignment repairs — 2026-10-24

uibcdf/molsysmt#452 and uibcdf/molsysmt#453 are corrected in working source.
The [current addon guide](../molsysviewer_addon.md) owns the updated atomic-axis,
original self-reference and paired-name contracts. Real-view tests receive the
same native behavior without an addon reference or correspondence workaround.
Earlier dated restrictions above remain historical; final source publication
and artifact qualification are distinct evidence.


## Explicit native centering received — 2026-10-24

The bound structure.center mirrors the new native moving/source/initial-target
contract, with source containment, source-only weights, physical destination
units, repeated-scope rules and retired-name rejection. Keyword-only update_view
is the only addition. Native computation, independent default/output ownership,
in-place None returns and edited-structure interaction invalidation remain in
MolSysMT. The existing coordinator retains scene identities and composes pending
edits; no centroid calculation, periodic preparation, molecular snapshot or host
runtime is introduced.

Sixty-eight focused cases pass on real bundled views. The single applicable
regression runs in an isolated checkout based on
99cb83107, applying only the centering reception: **1007 passed**, no failures,
errors or skips, and no watched source changes during execution. Import-origin
assertions confirm isolated Python sources; the existing in-environment native
Rust extension is reused and its path/digest recorded. This is source evidence,
not a new solver installation or compiled-artifact qualification.

Independent weighted/geometric means, coordinate displacements and rigid pair
vectors cover units, defaults, mass weights, repeated atoms and structures,
point/per-structure destinations and overlapping/disjoint/contained initial
targets. Tests distinguish an initial destination snapshot from a final-center
constraint, retain untouched coordinates/box and native named-analysis scope,
exercise real transport interruption, and reject invalid populations/targets
without publication. Deferred center/removal/translation retains scene/source
identities and navigation; synchronization never repeats the science. A real
native publication followed by a pipeline exception becomes uncertain.

Ruff check/format passes six Python files. Twenty-six guide blocks and 120
native-context docstring examples pass. Host reporting/link checks pass 280
cases. Original JUnits, import origins and source snapshots are retained in the
provider's centering receiving record. The native owner separately integrates
alignment repairs in a38c00d19; their scientific/admission/docs changes are
preserved when applying this reception. Exact integrated-head CI remains a
separate gate, and the full local regression is not repeated.

At the maintainer's explicit request uibcdf/molsysmt#451 was reopened with the
missing closure-traceability appreciation; its scientific fix in 5814dc534 and
archived evidence remain accepted. Reopening does not block this addon work or
reopen its numerical diagnosis. Native uibcdf/molsysmt#454 documents the separate
executed course-preparation correction. The facade now has twenty-four structure
tools: eighteen calculations and six coordinate editors, with four reviewed
geometry editors and broader namespaces/task panels still pending under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. No public floor, version freeze,
release, package reconstruction or promotion is implied.


## Single-structure move_away receiving — 2026-10-25

The explicit structure.move_away wrapper mirrors the native signature/defaults
with only keyword-only update_view=True added. The primary MolSys is implicit;
reference systems/populations, source/reference weights and structure scopes
remain explicit native inputs. Eighteen calculations and seven coordinate editors
are now exposed (25 structure tools); align_principal_axes, set_dihedral_angles
and shift_dihedral_angles remain pending. Exposure is not qualification of every
native input or package route.

Positive receiving is limited to single-structure nondegenerate displacement.
Automatic direction adds distance along the existing center separation. Explicit
direction uses native normalization and initial-reference centering before
translation; its source population must be contained in the moving atoms.
Only the primary view is serialized; external references remain caller-owned.
No periodic preparation, alternative geometry or automatic detector is added.
Independent outputs retain native ownership; admitted in-place operations retain
None, selected-structure invalidation, deferred projection, scene identity/maps
and synchronization retry without scientific replay.

Native-only reproduction on fc2936bf9 finds two owner defects now reported with
maintainer authorization: uibcdf/molsysmt#456 publishes NaNs for coincident centers
or zero directions, including an all-default call; uibcdf/molsysmt#457 can reject
explicit multi-structure input after partial centering publication. Those routes
remain unqualified, not silently corrected in the addon. Their native reports
require scientific guards. Detected partial publication enters uncertain state;
no automatic rollback or replay is promised.

Guard: tests/molsysviewer_molsysmt/test_structure_move_away_tools.py exercises
weighted centers, units under non-default policies, both direction modes,
external/self references, independent/in-place returns, native clean rejection,
scene maps and delayed/failed projection without scientific replay. Its original
focused run passes 38 cases. Broader regression and exact integrated-head CI are
recorded separately; no installed qualification, new public floor or release.


### Completed local displacement qualification — 2026-10-25

The focused guard passes 38 cases. Local regression covers 1061 distinct cases
without a full-suite rerun: the first campaign passed 964, then was interrupted
(exit 2) in a documentary matplotlib Qt plt.show loop inherited from DISPLAY=:0.
The remaining 97 previously unexecuted cases pass with MPLBACKEND=Agg (exit 0).
Both original JUnits are preserved; this is composite evidence, not a single green
run. Scientific/addon source hashes and the compiled backend remain unchanged;
the developer packaging tests regenerate ignored molsysmt/_version.py metadata.
All 27 addon-guide blocks and 125 native-context doctests pass; Viewer
reporting/link guards pass 280 cases. Ruff and provider guide/index validation
pass. MolSysMT's source receipt is
`devtools/data/molsysviewer_tools_move_away_receiving_20261025.json`.
It retains JUnit digests, source/import origins, the native-only reproductions
and actual uncertain-state receiving of #457; sync_view refuses to bless the
partial write. These are not live Qt/window rendering observations.

The independently owned ArgDigest receiving commit 9135cee1fd29f8591d29d802562c34cc27c44353
is preserved as integration parent; its source tests/docs are not bundled as our
changes. Hosted exact-head qualification remains pending at this checkpoint.
No installed compatibility or release is asserted; #456/#457 require the
scientific owner's repair.

### Native direction and preflight repair — 2026-10-25

The subsequent scientific repair of uibcdf/molsysmt#456 / uibcdf/molsysmt#457
supersedes the failing-input restriction above. Undefined directions and
unsupported axes now reject before coordinate publication; the explicit route
delegates its final destination directly to `center`. Native and bound guards
protect no-write rejection and preserved interaction/scene state. Historical
receipts are unchanged. The maintained current contract is in
[the addon guide](../molsysviewer_addon.md#native-displacement-repair--2026-10-25).
No multi-structure support, installed-package qualification or publication is
inferred from the repair.


## Bound principal-axis alignment — 2026-10-25

structure.align_principal_axes receives the native scientific parameters and
native independent/in-place defaults and returns. Only keyword-only
skip_digestion and update_view are added. The former is addon-only because the
native function declares no digestion bypass; the latter controls projection,
not science or adoption. Both ordinary validation/diagnostics and the existing
retained-axis coordinator are reused; no host runtime extension is needed.

The native fitting population is independent of the atoms moved. Target axes
are right-handed orthonormal rows; geometric/inertial definitions, weights,
arbitrary eigenvector signs, degeneracy rejection and optional centering remain
scientific-owner behavior. No periodic reconstruction or box rotation is added.
The structure namespace exposes 26 tools: eighteen calculations and eight
coordinate editors. Only set_dihedral_angles and shift_dihedral_angles remain
pending among the reviewed structure exports; other namespaces and GUI panels
are separate work.

Guard: tests/molsysviewer_molsysmt/test_structure_axes_tools.py. Independent
weighted covariance/eigenvalue checks exercise both definitions, target bases,
centering, non-default units, repeated/nonconsecutive structures, rigid distances
and signed volumes. Native-parity checks cover disjoint fitting atoms; real
view tests cover interaction invalidation, defaults/returns, clean rejections,
managed scene maps, lifetime and synchronization retry without scientific replay.
This source receiving also includes owner repair e6677e4c6 of
uibcdf/molsysmt#456 / uibcdf/molsysmt#457 and its native/real-view guards. It
introduces no new detector or scientific workaround, installed qualification,
public floor, tag or release. Full applicable local and exact-head hosted
results are recorded separately.


### Native reflection correction — 2026-10-25

The scientific owner corrects uibcdf/molsysmt#460: the default z plane and finite
nonzero scaled normals now share the native reflection contract. Undefined
normals and invalid plane points reject before writes. The facade forwards these
inputs without its own geometry. Earlier unit-normal receiving receipts remain
historical; the [current addon guide](../molsysviewer_addon.md) records the repair.
No installed qualification or public floor changes.


### Completed local principal-axis qualification — 2026-10-25

The focused guard passes 73 cases plus two separately selected disjoint-fitting
cases. A single executed regression on fixed source 7b1604ec3 plus the owned
alignment patch passes 1299 cases, zero failures/errors/skips, in 272.85 seconds.
Scientific/addon source hashes do not change during execution. Generated ignored
version metadata is recorded separately; the existing Rust binary matches the
initial shared-checkout observation. No fresh backend build is claimed.
All 28 guide blocks and 138 native-context doctests pass; Viewer reporting/link
guards pass 280 cases. Ruff and isolated guide/index validation pass.

Source receipt: `devtools/data/molsysviewer_tools_axes_receiving_20261025.json`
in MolSysMT. It retains original JUnit digests, source/import origins, unit audits,
and the two failed runner preflights (no tests executed), rather than presenting
those attempts as passing campaigns. Documentary tests use MPLBACKEND=Agg, with
no claim of live Qt/window observation. Native #456/#457 guards are received;
concurrent scientific reflection work under uibcdf/molsysmt#460 is excluded from
this isolated local campaign and preserved in the shared checkout. Integrated
source identity and exact-head hosted CI follow separately. No release follows.


## Native dihedral editors received with scientific limits — 2026-10-25

Explicit set_dihedral_angles and shift_dihedral_angles wrappers preserve native
scientific arguments/defaults/returns with the current MolSys implicit. Both
add keyword-only update_view; only the setter needs addon-only skip_digestion,
because it has no native bypass. The shifter retains its native declared flag.
The retained-axis receiver uses atom/structure counts for possible publication,
without inventing a selection or recomputing molecular graph cuts. Native
quartets, blocks, angular units, periodic kernels and selected-scope invalidation
remain owned by the scientific tools. No torsion formula or workaround is added.

All 28 function exports of the reviewed structure namespace are now explicitly
exposed (18 calculations, ten coordinate editors). This does not certify every
input, backend or published package. The focused guard
 tests/molsysviewer_molsysmt/test_structure_dihedral_tools.py passes 61 cases:
independent NumPy quaternion/torsion checks, multi-quartet and repeated structures,
angular/length policies, native broadcasting, explicit setter blocks, orthogonal
and triclinic periodic images, missing boxes, clean rejection, native ownership,
scene maps/lifetime and sync-only transport recovery. Full local and exact-head
hosted scopes follow separately.

Native-only reproduction at e568a6269 shows that nonfinite angles can publish
nonfinite coordinates and that shift_dihedral_angles ignores explicit blocks.
Those routes are unqualified; native science must be repaired by its owner,
without an addon correction. The maintainer has been offered two owning reports;
reporting authorization is pending at this checkpoint. Broader namespaces,
task panels, installed compatibility, floors and releases remain separate.


### Completed local torsion qualification — 2026-10-25

The focused real-view guard passes 61 cases. One executed full applicable
regression on fixed bb6283ce7 plus the owned torsion patch passes 1469 cases,
zero failures/errors/skips, in 281.87 seconds. Scientific/addon source hashes and
the existing compiled backend do not change during execution. Generated version
metadata is recorded separately. All 29 guide blocks and 146 native-context
doctests pass; Viewer reporting/link guards pass 280 cases. Ruff and isolated
guide/index validation pass. Documentary plots use MPLBACKEND=Agg; this is not
live Qt/window qualification.

MolSysMT's source receipt is
`devtools/data/molsysviewer_tools_dihedrals_receiving_20261025.json`.
It retains original JUnit digests, source/backend hashes, native-only reproductions,
periodic-image quaternion checks and the status of the offered provider reports.
NaN reproduction is confirmed in both editors and copy/in-place modes. Explicit
blocks are ignored by native shifting. Those limitations remain unqualified;
reporting authorization is pending, not assumed. No molecular/scientific
workaround is introduced. Exact integrated-head source CI follows separately;
source exposure, scientific qualification and installed/public availability remain
separate claims. No release, tag or dependency-floor change follows.


### Native torsion reports filed — 2026-10-26

The maintainer-directed continuation authorizes the two prepared reports.
Duplicate checks find no equivalent open or closed issue. uibcdf/molsysmt#461
tracks explicit blocks ignored by native shift_dihedral_angles;
uibcdf/molsysmt#462 tracks NaN angular edits publishing nonfinite coordinates in
both native editors and both output modes. The native scientific source hashes
still match the original receiving audit. Their reports require owning pytest
guards; no scientific correction is added to the addon. The previous dated
pending-authorization notes retain their historical scope. Full scientific
receiving of those routes waits for provider repair and new evidence.

## Periodic-box utilities receiving — 2026-10-26

Ten explicit `pbc` wrappers extend the expert hierarchy without root aliases or
scientific substitutions. has_pbc reads the current primary, including pending
scientific box changes; the nine matrix/length/angle utilities preserve explicit
caller-owned inputs and can run before molecular loading. Factories do not
assign boxes or adopt outputs. Native first-structure/mean-angle semantics,
unit policy and rounding are visible in help and the owning user guide. The
native default-angle boundary rejects None and remains unqualified; its report
was offered to the maintainer and is pending authorization. Coordinate editors
remain a separate effect-receiving block. See the dated
[receipt](../../devtools/data/molsysviewer_tools_pbc_receiving_20261026.json)
for executed evidence and exact scientific source hashes. No dependency floor,
package candidate, scientific implementation or host runtime changes.

Local PBC receiving passes 33 focused tests and one 1,077-case scoped addon,
native PBC and packaging regression, with no failures/errors/skips and no
scientific/addon source or compiled-backend change during that run. All 31 user
guide blocks and 158 inherited native docstring examples pass. Ruff, devguide,
indexes, diff and the single CI pytest-command checks pass. The Biophysics PBC
notebook itself fails before computation on its absent H5MSM demo key; the other
three PBC course modules were reviewed, not rerun through remote solvation.
Owning reports remain offered/pending authorization. The local checkpoint precedes exact committed-head CI, whose terminal evidence
is recorded below; neither qualifies installed package artifacts.

### Exact-source PBC CI completed — 2026-10-26

Provider 9061e21494a1f50c1b4f5126edc4e938dbb0b2c2 passes all six original
controls. [Smoke 40386788168](https://github.com/uibcdf/molsysmt/actions/runs/40386788168),
job 121797066424, passes 1,258 native cases and 924 addon cases (including all
33 new PBC cases), with no failures/errors/skips. Dependency 40386787152,
Ruff 40386787130, guide integrity 40386787075, suite policy 40386788769 and
Conda governance 40386789041 also pass. GH Run Receptor agrees with GitHub's
terminal success. Original log `/tmp/msm-addon-9061e214-pbc-smoke.log` has
SHA-256 `e5d076fbd4752f89261148c8a93251d21df8f538d861d73cf67d43b1e42fdd10`. The dated local JSON receipt retains
its pre-CI checkpoint; this terminal evidence supersedes its pending-CI status.
The workflow uses its recorded routine host source, and no host runtime or
installed artifact qualification is introduced. Other PBC editors, native
repairs, broad namespaces, graphical panels and package compatibility remain
separate; both 1.0 publications remain paused.

### PBC reports authorized and filed — 2026-10-26

The maintainer authorizes the prepared reports: uibcdf/molsysmt#465 owns the
rejected default box angles and uibcdf/molsysmt#466 owns the PBC course's
absent membrane demo. Both reproduce independently of Viewer, have current
queue records and require native pytest guards. The addon retains explicit
angle forwarding; no scientific repair or tutorial scenario substitution is
introduced here. This supersedes earlier pending-authorization notes.

## Managed periodic coordinate editors — 2026-10-26

The explicit pbc namespace now also exposes wrap_to_pbc, wrap_to_mic and unwrap,
completing all thirteen reviewed function names. This is exposure plus bounded
receiving, not unconditional scientific or package qualification. A reusable
private receiver resolves only admitted module/name pairs and defaults existing
structure calls to their original module. It retains axes and native returns,
serializes in-place writes, defers projection when requested and retries failed
scene reconciliation without replaying science. Native setters own exact
interaction coverage invalidation. No alternative geometry algorithm is added.

Native centered wrapping with in_place=True writes a detached copy under
uibcdf/molsysmt#467; that combination is explicitly rejected before effects.
Independent centered outputs and uncentered in-place wrapping are received.
The 94 focused cases compare direct lattice/temporal references, units,
nonconsecutive/repeated axes, native parity and input/result ownership, covalent
reconstruction, rejection, scene identity, batching and synchronization retry.
Broader isolated regression, examples and exact-head CI remain separate gates.
The native-only audit and hashes are retained in the dated PBC-edit receipt.


## Native torsion mutation boundaries repaired — 2026-10-26

The native provider repairs under uibcdf/molsysmt#461 and uibcdf/molsysmt#462
supersede the two reported torsion limitations at the earlier source checkpoint.
Set/shift reject nonfinite edit requests before coordinate publication, retain
the existing read-only undefined-angle semantics, and validate angular broadcast
axes and explicit block/index requests before Rust. The shifter now forwards
its explicit block pool. A private selected-coordinate buffer and a finite
result check protect input ownership before the common coordinate setter.
No replacement torsion algorithm or preparation step is added to the addon.

The native guard tests a two-component synthetic system, independent Rodrigues
rotations and circular angles, selected/repeated structures, explicit/automatic
block populations, pm/nm and degree/radian policies, periodic lattice images,
invalid requests, degenerate geometry, topology retention and named interaction
coverage. The receiver guard now exercises explicit blocks in both editors and
nonfinite rejections while preserving the scene and synchronization state.
The final scope and source hashes are retained in
[the repair receipt](../../devtools/data/dihedral_edit_repair_20261026.json).
The native limitations are repaired; this is bounded source qualification, not
unconditional scientific coverage or an installed release-pair qualification.

Local receiving completes 1,171 scoped addon/native-PBC/packaging cases in
371.30 seconds with no failures/errors/skips. All 94 focused cases, four PBC
guide blocks and twelve inherited PBC docstring examples pass. Scientific/addon
sources and the frozen existing backend remain unchanged during that run.
The dated [PBC-edit receipt](../../devtools/data/molsysviewer_tools_pbc_edits_receiving_20261026.json) records exact tested baseline, source hashes,
raw native #467 controls and evidence limits. This local snapshot excludes
concurrent native torsion repairs; integrated exact-head CI remains separate.

After the owning torsion repair 6f6ed6bf1 is committed, an additional targeted
198-case PBC/dihedral receiver run passes. The help text now reflects native
nonfinite rejection and honored explicit block pools instead of describing
those source defects as still present. The PBC scientific hashes remain equal
to the frozen regression baseline. This integrated receiving is recorded
separately in the receipt; terminal committed-head CI is recorded below.

## Integrated PBC/dihedral source CI completed — 2026-10-26

Producer 4590545fd2c843f5823a717d33ebe7ba459cce2e passes all six original
controls. [Smoke 40408393902](https://github.com/uibcdf/molsysmt/actions/runs/40408393902),
job 121871993740, passes 1,576 native and 1,028 addon cases with no failures,
errors or skips. Dependency 40408393948, Ruff 40408393648, guide integrity
40408393764, suite policy 40408394283 and Conda governance 40408394299 pass.
GH Run Receptor confirms GitHub terminal success. Original log
`/tmp/msm-addon-4590545f-pbc-edits-smoke.log` has SHA-256
`1259ef82c610582f174a5ec91cec1dc6f9ec3ad84453025129e4c37a2cd30cb4`. The committed local JSON receipt retains its
pre-CI snapshot; this terminal source evidence supersedes its pending-CI status.

The composition includes owning torsion repair 6f6ed6bf1 and all thirteen PBC
wrappers, with the #467 centered-in-place integration limit preserved. Native
box default #465 and course fixture #466 remain separate. The workflow retains
its exact routine Viewer source pin; no host runtime, dependency floor,
installed artifact or release qualification is introduced by this source CI.
Viewer's historical-public-backend pandas gap and experimental Qt remain
separately tracked. Both 1.0 publications remain paused.


## First physchem property slice — 2026-10-26

Seven of the 30 reviewed physchem exports now have explicit bound source wrappers:
get_mass, get_charge, get_atomic_radius, get_electronegativity,
get_hydrophobicity, get_polarity and get_transmembrane_tendency. They use the
existing serialized primary reader and add no host runtime or scene operation.
Signatures/defaults, skip_digestion, native units/containers and explicit
scientific definitions remain native. Additional physchem families and the GUI
remain pending; this slice does not complete the module or installed receiving.

The tests distinguish independently checked elemental constants, hierarchy sums
and diverse amino-acid reference values from native parity across the 15
hydrophobicity tables, both polarity scales and both transmembrane definitions.
They also cover selection ordering, repetition, empty populations, source/scene
and interaction retention, replacement/lifetime, pending reads and explicit
OpenMM charge on a single-structure capped peptide. Native mass on bound MolSys
with OpenMM remains unsupported; multi-frame periodic conversion is not silently
reduced to one structure. Neither table charge nor ProtOr radius prepares
molecular chemistry or assigns a model to the source.

Native selector propagation is separately reported in uibcdf/molsysmt#470:
charge, radius, electronegativity and hydrophobicity drop the declared alternative
syntax. The addon forwards and preserves the native result/error without a
translator. MolSysMT expressions and explicit numeric selections are received.
Validation counts and exact source provenance are recorded after the scoped run;
no package, publication or dependency-floor qualification is implied.

Element-level clarification is separately owned by uibcdf/molsysmt#471. Current
receiving uses atom scope for atomic tables and group scope for group scales;
it does not certify ignored unsupported levels as deliberate aggregation.

Local qualification passes 109 focused cases and one frozen 1,272-case scoped
regression in 356.98 seconds, with no failures/errors/skips. All audited Python
sources and the existing backend remain unchanged, and live scientific/addon
sources match the snapshot. The new user-guide example executes. The
[physchem receipt](../../devtools/data/molsysviewer_tools_physchem_properties_receiving_20261026.json) records source hashes, the exact 7/30 inventory,
23 pending exports, independent references versus parity and both native audits.
Post-run additions concern report/index/documentation only; committed-head CI is
still separate and pending at this snapshot. No host runtime change is needed.


## Physchem source CI completed — 2026-10-26

Producer 2b777e554e7b382453ba0e2752fe726406f2dcab passes all six original
controls. [Smoke 40413404006](https://github.com/uibcdf/molsysmt/actions/runs/40413404006),
job 121889543344, passes 1,576 native and 1,137 addon cases with no failures,
errors or skips. Ruff 40413403765, dependency 40413403966, developer guide
40413403822, suite policy 40413404345 and Conda governance 40413404537 pass.
GH Run Receptor confirms terminal success. Original log
`/tmp/msm-addon-2b777e55-physchem-smoke.log` has SHA-256
`64a00b665449213d4daf86a79122c8b3683310ced10b64cac452c57ebc058983`.

This supersedes the pending-CI status in the immutable local physchem receipt;
it does not relabel local source evidence as installed qualification. Native
uibcdf/molsysmt#470 and uibcdf/molsysmt#471 remain open limitations. The 23
remaining physchem exports, panels, installed artifacts, dependency floors and
both 1.0 publications retain their separate scope. Concurrent native periodic
repairs are not part of this exact producer. No host runtime change is needed.
