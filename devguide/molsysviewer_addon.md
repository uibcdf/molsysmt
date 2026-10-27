# Native MolSysViewer integration

**Role:** normative provider/consumer boundary
**Decisions:** legacy retirement under uibcdf/molsysmt#354 /
uibcdf/molsysviewer#186; redesigned tools under uibcdf/molsysmt#421 /
uibcdf/molsysviewer#264

MolSysMT supplies the native molecular-system, scientific calculation and H5MSM
backend used by MolSysViewer. The source now ships a redesigned
`molsysviewer_molsysmt` integration, discovered through the new
`molsysmt-tools = molsysviewer_molsysmt.tools` entry point on a compatible host.
Its experimental facade provides native `basic` queries/independent outputs,
retained-axis removal and geometry setting, root basic aliases, synchronization
controls, eleven current `topology` analysis readers, eighteen `structure`
calculations and retained-axis translation, proper rotation, plane reflection, least-RMSD fitting/alignment, explicit centering and single-structure displacement and principal-axis alignment and both dihedral editors under `view.addons.molsysmt`. Ten `pbc` box queries/factories are also explicit: only has_pbc binds the primary;
other inputs remain caller-owned. Repaired native orthogonal defaults are received.
Three `pbc` coordinate editors also have source receiving, with repaired native
centered in-place ownership under uibcdf/molsysmt#467. Thirteen physchem tools
are source-received, including the repaired native syntax/element contracts
under uibcdf/molsysmt#470 and uibcdf/molsysmt#471. Collantes unit review remains
uibcdf/molsysmt#473. The additional conformational SASA wrapper brings source
exposure to fourteen tools, with bounded CPU receiving. Native area-unit
context and explicit periodic controls are corrected under uibcdf/molsysmt#478
and uibcdf/molsysmt#479; own-image screening and general SASA accuracy are not
qualified by these controlled fixtures.
Two detached chemistry reports bring source exposure to sixteen tools, with
explicit single-structure/state scopes and native readiness external syntax
repaired under uibcdf/molsysmt#480; independent unequal-cardinality persistence
is repaired under uibcdf/molsysmt#481. Two aromatic participant/flag
readers brought physchem exposure to eighteen of thirty reviewed exports.
Three feature readers bring exposure to 21 tools on the qualified 31-export
baseline. Native 5681f5e78 adds secondary-structure propensities: the inspected
inventory at that source is 32. The two reference readers now bring the facade
to 23 tools. The bound molecular-descriptor readers bring the facade to 25 of the reviewed
34 inspected exports, with nine pending. Their separate receiving does not relabel older
source gates. The SMARTS repair is received under
#488; native reference-metadata ownership is repaired under #490 and its guard is
included in the new receiving tier. Native graph selector/scope repairs are received
under uibcdf/molsysmt#482 / #483; source evidence and remaining limits are
recorded in the dated section below.
Other scientific namespaces, edit families and graphical task panels remain pending. Old root entry points and retired adapter files remain
unsupported; source support is not installed-package qualification. Domain addons
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

Migrate calls to retired addon editing/rendering APIs to native Viewer
operations where provided, or to public `msm.basic`, `msm.build`,
`msm.structure`, `msm.topology`, `msm.pbc`, `msm.physchem` and
`msm.interactions` tools. The redesigned facade deliberately reuses the `view.addons.molsysmt` name
without restoring those retired methods. Do not silently rewrite legacy
serialized UI/session state. Viewer owns scene/session migration.

The removed adapters wrapped existing public tools; their panel state and
rendering projection were UI-specific, not another scientific engine. Their
source and tests remain in Git history. The
[archived architecture](archive/assessments/molsysviewer_addon_before_retirement_20261009.md)
records the old surface without presenting it as current behavior.

## Packaging and evidence

Current-source wheels, source distributions and installed-runtime checks must
include the reviewed new tools sources/entry point and reject legacy addon
files and declarations. The installed runtime probe exercises automatic discovery
and a bound scientific read against native MolSysMT on a compatible host. Native Rust/resource/form metadata
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

## Tools addon implementation in progress

The maintainer has accepted a redesigned provider-owned tools addon under
uibcdf/molsysmt#421, coordinated with uibcdf/molsysviewer#264. The
[implementation record](pending_proposals/molsysviewer_tools_addon.md) owns
the source ledger, expert scientific API mirror and task-oriented panels.
Preserve native mutation/return semantics; qualified bound-system edits will
synchronize by default, while independent results require explicit adoption.
Provider documentation will explain capabilities and use; Viewer documentation
owns general management, creation and catalogue links.

The first source delivery has real read-tool parity/lifecycle and packaging
guards. See the [user reference](../docs/content/user/tools/molsysviewer_tools.md).
Read/extract/copy/conversion/preflight and retained-axis remove/geometry-set
routes have source receiving. Broader effect coverage, panels and exact installed
qualification remain pending under the implementation issue.
The withdrawn observer request uibcdf/molsysmt#413 remains closed.


## Development metadata receiving

Automatic discovery consumes installed distribution entry points. A source
checkout can also contain ignored local `molsysmt.egg-info` generated before the
new entry point existed; Python metadata discovery may prefer it to a correct
editable installation in site-packages. Inspect the selected distribution's
public `entry_points` before changing the host or registering modules manually.
If that local metadata is stale, regenerate it from this checkout with its
configured setuptools backend:

```bash
python -c 'from setuptools import setup; setup(script_args=["egg_info"])'
```

Use the selected development interpreter. This refreshes generated metadata,
not a scientific implementation, public package, dependency floor or host
allowlist. Restart the importing process and verify ordinary discovery from
both checkout working directories. The initial receiving exercise reproduced
this shadowing and then ran both user-guide code blocks plus the bound extraction
without explicit addon registration. These are development-source checks, not
clean installed-artifact qualification.


## Managed retained-axis removal

The source facade admits `basic.remove` with native scientific options/defaults
and a keyword-only `update_view=True`. Independent native outputs remain caller
owned; `in_place=True` edits the actual bound MolSys and retains native None.
The preparation adapter uses the provider's own selection/index validation and
native candidate-publication contract, supplying authoritative retained maps to
the generic Viewer coordinator. No second scientific removal engine exists.
Atomic native rejection is qualified only while the same state dictionary remains;
uncertain writes need explicit recovery. The receiver rejects empty in-place axes
before science; independent native empty results retain their native behavior.

`get_sync_status` returns detached integration metadata and `sync_view` retries
projection without repeating science. Deferred removals compose maps; scene
indices remain unavailable until reconciliation. Native readers are serialized
with managed writes but read pending scientific results. Raw external writes and
returned live references remain outside automatic synchronization.

Source guards are `tests/molsysviewer_molsysmt/test_remove_tools.py` and the
existing read/packaging guards, received against the coordinated Viewer host
under uibcdf/molsysviewer#264. Broader namespace/effect qualification and graphical
task panels remain pending under uibcdf/molsysmt#421. This does not qualify any
published package pair or authorize a release.


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


## Geometry-only basic.set receiving

Source admits the coordinate/box routes of `basic.set` with native parameters,
None return and keyword-only update_view. The addon reuses the native ArgDigest
attribute domain; integration rejects unreceived attributes and axis changes
before writes. Native unit/selector tools own input interpretation and native
setters own per-structure invalidation. Analyses on untouched structures and
old snapshots survive. No automatic calculation or coordinate broadcasting is
introduced. The current host synchronizes through a scene rebuild, not a
guaranteed incremental transfer.

The host executor's explicit rejection_check token reader covers nested protected
geometry and analysis snapshots. It may certify an unchanged rejection without
declaring a multi-attribute call atomic; changed/uncertain state instead requires
explicit recovery. Hosts without that keyword reject before executing science.
Guard: `tests/molsysviewer_molsysmt/test_set_tools.py`; broader attribute/effect
receiving remains open under uibcdf/molsysmt#421 and uibcdf/molsysviewer#264.


## Independent copies, conversion and preflight

The bound facade exposes native `basic.copy`, `basic.convert` and
`basic.get_conversion_report`, including root aliases and native signatures after
binding the primary system. They use the coordinator's serialized reader rather
than managed editing: independent results are not adopted and files are explicit
Python-host outputs. Pending scientific data can be read without projecting them
or changing synchronization status. Native converter caches/ownership, including
full-axis live results for `copy_if_all=False`, remain native and unobserved.

Converter-specific **kwargs are validated by the native converter domain after
native target-form normalization. The addon does not duplicate the provider's
format/dependency registry or interpret filenames as browser downloads. A report
retains native audited scopes/exhaustiveness, strict rejection and failures.
Target lists do not imply atomic multi-file writes. H5MSM receiving uses actual
round trips with named analyses and nonconsecutive/repeated structures; optional
engines/formats retain their own qualification, not a blanket addon guarantee.


## Composition predicates and comparison

The source facade adds bound `basic.contains`, `basic.is_composed_of` and the
non-mutating `basic.compare` route. Only the primary MolSys is implicit; the
second comparison system remains explicit, with independent selections and
structure scopes. They use the serialized reader, retain native condition and
result/error semantics, and do not project pending edits or attach analyses.
Caller-owned auxiliary systems must remain stable during a call; the host does
not provide a cross-view transaction or automatic reference locking.

The historical compare argument alias is re-scoped from the provider's declared
ArgDigest tables before wrapper defaults are forwarded. This avoids treating a
forwarded default as an explicit user choice. A user supplying both alias and
canonical name, even an explicit canonical None, still gets the native collision
error. No independent alias vocabulary or value normalizer is introduced.

`compare(redefine_indices=True)` rebuilds topology in both native inputs and is
not admitted by the reader route. It fails before writes, including trusted
calls. Receive its primary/auxiliary effects and reconciliation separately;
experimental status does not excuse silently forwarding that mutation.


Native structural comparison can currently emit UnitStrippedWarning during
implicit quantity conversion (uibcdf/molsysmt#435). Preserve the provider outcome;
do not introduce a downstream filter or comparison algorithm. The report is a
native usability/unit-boundary finding, not a demonstrated scientific mismatch.


## Identity readers and an explicit collection utility

The source facade receives bound `get_form`, `is_a_molecular_system` and
`where_is_attribute`. They resolve the actual current MolSys and use the
serialized native reader. The returned attribute item retains native ownership,
including a live reference to the bound MolSys; no defensive copy or external
write observer is introduced.

`are_multiple_molecular_systems(molecular_systems)` keeps its explicit collection
input. It is not a bound-primary operation: the addon neither inserts a system
nor combines/adopts sources. It can run before loading a system, while still
checking the owning view's lifetime. Inputs remain caller-owned/stable and do not
acquire edit locks. A one-item valid container keeps the native True result;
this is not a source-composition/load-mode decision.

The three native identification/classification helpers deliberately have no
ArgDigest escape hatch. Their addon boundary supplies keyword-only
skip_digestion, does not forward it, and leaves the native function undecorated.
`where_is_attribute` retains its ordinary native signature minus the primary
input. This explicit exception avoids recursive form digestion and honors the
addon public-boundary controls without weakening scientific validation.


## Stored-topology analysis readers

The first topology namespace receives get_bondgraph, get_covalent_blocks,
get_covalent_paths and get_dihedral_quartets with current-target binding and
native outputs. Basic and topology share one private read-delegation owner;
all reviewed functions still have explicit scientific signatures and names.
No arbitrary scientific module proxy is exposed. Root aliases stay limited to
actual provider root aliases, not every topology function.

Graph cuts return hypothetical blocks and never remove source bonds. Quartet
blocks retain native ragged lists/sets. Selection/state/output contracts and
derived caches remain native; no extra preparation, trajectory copy, analysis
attachment or scene projection is added. Source get_bondgraph/get_covalent_blocks
have declared native skip flags; path/quartet wrappers add a keyword-only addon
flag without passing it into undeclared scientific **kwargs. Native validation
of those public operations remains active.


## Chemical-graph and sequence receiving — 2026-10-23

All eleven topology exports at the reviewed baseline have explicit primary-bound
wrappers. The seven additional readers are get_rings, get_rigid_fragments,
get_rotatable_bonds, get_substructure_matches, get_atom_correspondences,
get_sequence_alignment and get_sequence_identity. They reuse the serialized
reader and never prepare missing chemistry, transform coordinates, attach results
or update the scene. The caller chooses native chemical assumptions, states,
search policies, match/block limits, patterns, constraints and optional engines.
No chemistry assignments or scientific interpretation are duplicated in the addon.

Source bond indices in explicit rigid cuts remain distinct from atom pairs in
covalent-block cuts. Native sparse membership, empty shape, source-index and
query-order contracts remain intact. Search bounds retain their actual native
scope and errors; no partial answer is substituted. RDKit/Biopython imports and
dependency checks remain at their native runtime boundaries.

Correspondence and sequence references remain explicit, caller-stable inputs.
A native None correspondence reference retains its self-reference behavior.
There is no auxiliary-view lock or implicit coordinate fit/adoption. Sequence
prettyprint retains native stdout/None behavior. Current get_sequence_identity
declares a keyword-only native skip flag, forwarded by the bound method without
changing historical positional slots. Native contributing-group mapping under
uibcdf/molsysmt#439 is repaired and received. Earlier source limitations remain
in dated receipts; the addon never implemented a competing identity formula.


## Initial geometric structure readers — 2026-10-23

The explicit structure namespace receives get_distances, get_vectors, get_center,
get_radius_of_gyration, get_angles and get_dihedral_angles. These reuse the existing
current-primary serialized reader, preserving scientific selectors, physical
quantities, weights, PBC, output metadata and supported execution choices.
Auxiliary molecular_system_2 inputs, selectors and weights remain explicit and
caller-stable. No auxiliary-view locks or atom/structure pairing guesses are added.

Centers are returned coordinates, not centering edits; geometry results are not
scene measurements or attached analyses. Repeated/nonconsecutive structure choices
and native tuple/dictionary/list outputs remain native. Dihedral named flags are
not repurposed for addon controls: the added keyword-only skip_digestion is not
forwarded to the native helper, which lacks a declared flag. Native validation
still runs. Other native escape hatches remain explicit native parameters.

Native heavy endpoint/unit fixes under uibcdf/molsysmt#440/#441/#442 are now
received from their scientific owner, including independent physical references
and explicit nm/angstrom/pm contexts. Earlier parity-only limits remain in their
dated receipts. No addon unit/formula or routing correction is introduced.
Optional GPU/alternate engines, universal memory bounds and coordinate-changing
operations need separate receiving; no new host runtime/API is needed.


## Independent structural comparison and fitting readers — 2026-10-23

The source also receives get_rmsd, get_least_rmsd, get_principal_axes and
get_least_squares_plane through the existing serialized reader. They preserve
native signatures, return quantities/arrays/dictionaries and reference inputs.
Raw RMSD does not fit coordinates; minimum RMSD optimizes a temporary comparison
without transforming either input. References stay caller-stable, with native
selection/reference-index defaults, not an auxiliary-view transaction. The native
get_rmsd signature lacks a skip parameter; its addon-only keyword is never forwarded.

Axes retain native numeric moments, ascending eigenvalues, row basis and
sign/degenerate-subspace semantics. Plane results retain sparse memberships,
source structure order, typed empties and native quantity/normal fields. Fitting
a plane does not create a shape, certify chemistry or unwrap periodic groups.
No source/scene edit, automatic attachment or new host runtime follows.

These direct calculations and numeric/property selectors retain native
execution dependencies; rich selectors/optional engines have their own routes.
The earlier wait for the MolSysMT team on uibcdf/molsysmt#441 is satisfied by its
native repair and new receiving. RMSF is also received after the native #442
unit fix. Minimum/neighbor wrappers now have authorized local receiving of the
provider changes under uibcdf/molsysmt#444 and uibcdf/molsysmt#445. Their provider
commit and issue closure remain separate from this working-tree evidence.
No addon alternative or hidden routing change substitutes for scientific fixes.


## Repaired observables and relation readers — 2026-10-24

The source receives the native fixes from bae6d0101 and 1123eeb7d through
bc2142831, including the native keyword-only sequence flag. Existing get_distances,
radius and identity readers gain independent regression coverage; new explicit
get_maximum_distances, get_contacts and get_rmsf wrappers use the same serialized
primary reader. Maxima retain native local endpoint positions/reduction semantics;
its extra skip_digestion keyword is addon-only. Contacts retain threshold units,
cell-list/dense choices and boolean/pair outputs. RMSF returns fluctuations in
the supplied coordinate frame, with no hidden alignment or coordinate wrapping.

All calls return science without edits, scene measurements, color scales or
analysis attachment. Secondary inputs, when native signatures admit them, remain
explicit and caller-stable. Native units, errors and resource limits apply.
No host runtime, protocol, scientific algorithm or published dependency floor
is changed by this receiving. This earlier relation receipt covered thirteen functions. The local
minimum/neighbor receipt brought the mirror to fifteen functions; the later
analysis receipt brings the current total to eighteen, with ten edits pending.

The scientific team owns #444 (independent second-center weights) and #445
(neighbor second-system forwarding). The maintainer explicitly requests native
pytest coverage of the distance/neighbor/minimum/maximum contract family, using
independent numeric/index oracles and cases spanning sources, structures, weights,
PBC, units, execution modes, representations and errors. These two new wrappers
have local receiving of those provider corrections; no guessed route or argument
substitution is used. Original source-only versus installed-package boundaries
remain intact.


## Local minimum and neighbor receiving — 2026-10-24

The maintainer explicitly accepts receiving the provider working tree before its
commit. Both wrappers preserve native signatures after binding only the primary
system, including native skip_digestion. Minimum endpoints keep separate weights
and local reduction/pair positions. Neighbors preserve the auxiliary system,
its structure correspondence, count/cutoff choices and supported sparse outputs.
The addon re-scopes the native argument-admission declaration and omits only
empty criterion defaults during delegation; caller-supplied incompatible
criteria still fail at admission. No scientific formula or fallback is added.

Tests exercise actual views, NumPy reference geometry, physical units, unequal
populations, repeated structures, weighted centers, CSR/atom pairs, errors,
pending edits, replacement/close and scene/analysis preservation. The source
inventory now has sixteen addon Python files, including the criterion contract.
The receipt records its original working-tree hashes. The owning scientific
fixes are now committed as 5710cc0cff1f3f468823699104e51e6fe029c3b2 and
uibcdf/molsysmt#444 / uibcdf/molsysmt#445 are closed. Addon exact-head CI remains
separate; no installed artifact, dependency floor or publication is qualified.


## Structural-analysis receiving — 2026-10-24

get_symmetry_corrected_rmsd, get_secondary_structure and
principal_component_analysis use the existing serialized current-primary reader.
All native parameters remain explicit after primary binding, including reference
systems, chemical states, constraints and execution choices. Secondary structure
has only an addon keyword-only skip flag because its native signature has none;
the other native skip controls are forwarded. Discovery remains lazy for MDTraj
and RDKit. This slice receives eighteen calculation exports. Translation below
brings the current total to nineteen of twenty-eight reviewed structure tools;
nine other coordinate-changing operations remain pending.

Receive actual DSSP group/structure correspondence and codes, NumPy weighted
covariance/eigenvalue properties and direct positional geometry over explicit
chemical maps. Retain native result ownership, quantities, search scope,
attribution and cache consistency. No analysis attaches automatically or creates
scene content. No preparation, alignment, molecular edit, default engine change
or whole-trajectory copy is added by the addon.

PCA's weight normalization/validation repair under uibcdf/molsysmt#448 is
received from 306e91dda, with independent covariance, squared-unit and input
preservation checks across supported containers/dtypes. The native owner supplies
this normalization; no addon conversion is introduced. Optional GPU and other
unexecuted routes retain their own qualification. Source receiving does not
freeze versions, change published floors or qualify an installed artifact.


## Native translation receiving — 2026-10-24

The explicit translate wrapper preserves the native scientific signature and
in_place=False default, adding only keyword-only update_view=True. Independent
outputs use the serialized reader and are not adopted. In-place calls use the
existing managed-edit coordinator, retaining axis/source identity and native
return. No new Viewer runtime, message or generic transaction layer is needed.

The family preflight resolves native selections/structure scope and rejects
active native edit sessions; it computes no displacement or alternative science.
One native translate call owns units, broadcasting and publication. The receiver
uses the protected geometry/interaction identity token already qualified by
basic.set. Native clean rejection preserves prior state; evidence of publication
before failure enters uncertain state. Changed scope composes with deferred
removal/set operations, while native invalidation preserves unaffected analyses.
Sync retry rebuilds the scene without replaying translation or retaining an
unrequested full scientific snapshot. Source now exposes nineteen structure
tools: eighteen readers/calculations and one coordinate editor.

Center remains absent under uibcdf/molsysmt#451 after a standalone partial-scope
target/return reproduction. Its scientific owner must resolve that contract;
the addon does not silently repair populations, coordinates or return values.


## Proper rotation and plane reflection receiving — 2026-10-24

Explicit structure.rotate and structure.flip reuse the existing retained-axis
geometry receiver and scientific-edit coordinator. The public native operation
executes once; the addon provides no geometry, matrix validation, normalization
or broadcasting. Native independent/in-place returns and update_view semantics
match translation. Flip adds an addon-only keyword skip_digestion because its
native callable has no declared flag; ordinary native validation remains active.

Receiving covers proper matrix stacks and an actual SciPy Rotation, explicit
unit plane normals, physical rotation centers/plane points, repeated axes and
unit contexts. Cartesian rotation/plane references, inverse/double-reflection
and distance invariants check scientific values independently. Real views retain
selection/region/shape/source/navigation identity; mixed deferred edits and actual
transport interruption protect synchronization without repeated science. Scene
recovery is distinct from native partial writes and supplies no rollback.

Native flip has two independently reproduced limitations: vector=None rejects
before its implementation's fallback, and nonunit normals are not normalized,
so vector [2,0,0] changes distances instead of producing the same reflection as
[1,0,0]. A zero vector silently produces no change. Only explicit-unit-normal
reflection is qualified; these routes remain native-owner work, not addon fixes.
The runtime help and owning user guide disclose these limits. Source now exposes
twenty-one structure tools: eighteen calculations and three coordinate editors;
seven reviewed coordinate-changing exports, including center under uibcdf/molsysmt#451, remain
pending. No new host capability, dependency floor or package qualification is
implied.


## Native rigid fitting and sequence alignment — 2026-10-24

Explicit structure.least_rmsd_fit and structure.least_rmsd_align preserve native
parameters/defaults/results, including independent output conversion for fit,
CPU precision controls and caller-owned references. In-place calls reuse the
retained-axis geometry coordinator, with update_view controlling projection only.
There is no new scientific algorithm, correspondence heuristic, reference
substitution, all-trajectory recovery copy or host runtime capability.

Fit selection_fit/reference_selection_fit define corresponding anchors, whereas
selection defines the moved population. Sequence alignment derives anchors and
moves complete selected components; the geometry preflight checks participating
scope presence rather than claiming the anchors are the full moved population.
Native setters own exact edited-structure interaction invalidation. Only the
primary view is serialized; caller-owned references must remain stable and their
views are never implicitly synchronized.

Receiving uses independent Cartesian poses and distinct/mixed-unit references,
repeated/nonconsecutive structure scopes, partial moved populations and actual
multi-component views. Native independent forms, scene identities, pending mixed
edits, lifetime/replacement and real transport interruption are received. CPU
scope is explicit; forwarding optional GPU controls is not qualification of them.
Native scientific interruptions after a partial publication remain uncertain;
projection retry never repeats fitting.

The native default None reference of least_rmsd_align fails even though self
reference is documented (uibcdf/molsysmt#452). Explicit references, including an
explicit self reference, remain the received route; no addon workaround changes
the default. Native alignment also interprets numeric atom-selection indices as
group indices (uibcdf/molsysmt#453); only MolSysMT expression selections are qualified here. The addon
neither converts indices to expressions nor redefines scientific correspondence.
Center remains unreceived under uibcdf/molsysmt#451, and earlier
native reflection limits remain visible. Source now provides twenty-three
structure tools: eighteen calculations and five coordinate editors; five other
reviewed coordinate-changing exports and the broader addon remain pending.


## Native centering contract resolved — 2026-10-24

The scientific owner resolved uibcdf/molsysmt#451 in 5814dc534 with the
maintainer-approved explicit source/destination redesign. Native center now
uses selection as its moving population, source_center_selection as a contained
source-center population (defaulting to selection), and mutually exclusive
initial target_center_selection or physical target_coordinates destinations.
Its in-place return is consistently None; old keyword names are retired before
1.0. Tests and executed tutorials/course modules protect the new contract.

Earlier dated partial-reference/return findings above describe the historical
blocker. They no longer describe current native behavior. Addon receiving
remains pending under uibcdf/molsysmt#421: this correction does not introduce a
center wrapper, host synchronization contract or installed-package evidence.


## Native sequence-alignment repairs — 2026-10-24

uibcdf/molsysmt#452 and uibcdf/molsysmt#453 now resolve the original input
reference before selection, and distinguish atomic populations from original
sequence-group positions. Numeric/Boolean selections use each source atom
axis. Identically aligned group pairs retain unique selected atom-name
correspondences even when atom order differs. Arbitrary ordered atom pairs
remain the least_rmsd_fit contract. Complete selected query components move.

The native CPU matrix protects original reference structure snapshots, units,
precision, query/reference ownership, unselected components/structures and
interaction invalidation. Real-view fitting tests receive omitted/None/self
references and atomic masks in both independent and managed in-place calls.
The admission path lets native alignment own its nonempty population contract
instead of reparsing its mask through generic select; it forwards arguments
unchanged and computes no scientific correspondence. Earlier dated limitations
above are historical. No installed package or optional GPU qualification is
implied by this source receiving.


## Explicit centering received — 2026-10-24

The bound structure.center mirrors the new native moving/source/destination
signature and preserves source containment, weights, physical units, initial
target snapshots, retired-name rejection and independent/in-place returns.
It delegates to native center through the existing retained-axis geometry
coordinator, adding keyword-only update_view only. No alternate centering,
reference correction, periodic preparation, molecular snapshot or host runtime
capability is introduced.

Receiving includes weighted and default source centers, overlapping/disjoint and
contained initial targets, point/per-structure destinations, repeated atom and
structure indices, standard-unit contexts and native mass weights. Independent
NumPy means, translations and pair vectors protect geometry and ownership; real
views protect native edited-structure interaction invalidation, retained scene
identities, deferred mixed edits and synchronization retry without science replay.
A scientific pipeline interruption after publication becomes uncertain.

The scientific fix in 5814dc534 remains accepted. At the maintainer's explicit
request uibcdf/molsysmt#451 was reopened only to supply its missing final closure
comment; the archived scientific evidence is retained. This administrative state
is separate from the bound center implementation under uibcdf/molsysmt#421 /
uibcdf/molsysviewer#264. The facade now exposes twenty-four structure tools:
eighteen calculations and six coordinate editors. Four other reviewed geometry
editors, other scientific namespaces, graphical task panels and installed
qualification remain pending. Native alignment repairs under uibcdf/molsysmt#452 / uibcdf/molsysmt#453
are separately integrated by their owner in a38c00d19; centering receiving does
not absorb or reimplement those edits.


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

### Native displacement repair — 2026-10-25

The scientific owner repairs uibcdf/molsysmt#456 and uibcdf/molsysmt#457.
Finite nonzero directions are normalized with scale-safe arithmetic. Coincident
automatic centers, nonfinite centers/distance and unsupported structure or
direction cardinalities reject before coordinate writes. An explicit offset
is composed into one target point and delegated to `structure.center`; there
is no intermediate center-only publication. Single-structure scientific
semantics, source containment, units and native output ownership are preserved.

The native and real-view guards now assert unchanged coordinates, boxes,
interaction coverage and scene/synchronization state for these rejections.
The addon contains no scientific workaround. Normal successful coordinate
setters invalidate only the edited structure. Generic partial backend failures
and display synchronization failures retain their separate uncertainty/retry
contracts. The source receipts above remain historical; these repairs do not
qualify installed packages or a broader multi-structure route. The final
administrative closure comment for uibcdf/molsysmt#451 is also restored.


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


### Native reflection repair — 2026-10-25

The scientific owner repairs the default/normal defects under
uibcdf/molsysmt#460. None selects the existing z-normal convention. The native
argument boundary normalizes finite nonzero plane normals using the shared
scale-safe helper; generic vector digestion remains unchanged for other callers.
One finite physical point applies to all selected structures. Unsupported point
stacks and undefined normals reject before writes. The existing Rust kernel
still owns reflection; no addon formula or provider dependency is added.

Independent plane matrices, distance invariance, inverse reflection and signed
volume guard native MolSys/Structures across physical unit policies. Real-view
receiving includes default and scaled normals, rejected invalid planes and
preserved synchronization/interaction state. Earlier explicit-unit-only receipts
remain dated evidence. The repaired current contract does not imply installed
package qualification or stability of unrelated scientific profiles.


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

## Periodic-box utilities received in source — 2026-10-26

The explicit `pbc` namespace exposes ten queries/factories. Only `has_pbc`
consumes the current primary through the managed reader. Nine utilities retain
explicit quantities, work before system loading, require an open owning view
and acquire no molecular edit locks for their caller-owned inputs. They return
native scientific values without box assignment, adoption or scene updates.
The two volume utilities lack native skip parameters; their addon-only flags
never bypass native public validation. Native row-vector geometry, units,
rounding and mean-angle shape labels remain unchanged. The declared
`get_box_from_lengths_and_angles(..., box_angles=None)` default rejects in the
native public boundary and remains unqualified; explicit angles are received.
Coordinate editors wrap_to_pbc/wrap_to_mic/unwrap remain pending. The dated
[source receipt](../devtools/data/molsysviewer_tools_pbc_receiving_20261026.json)
records independent metric references, rejection/lifecycle receiving and the
separate source/package qualification scope. No host runtime change is needed.

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
[the repair receipt](../devtools/data/dihedral_edit_repair_20261026.json).
The native limitations are repaired; this is bounded source qualification, not
unconditional scientific coverage or an installed release-pair qualification.

Local receiving completes 1,171 scoped addon/native-PBC/packaging cases in
371.30 seconds with no failures/errors/skips. All 94 focused cases, four PBC
guide blocks and twelve inherited PBC docstring examples pass. Scientific/addon
sources and the frozen existing backend remain unchanged during that run.
The dated [PBC-edit receipt](../devtools/data/molsysviewer_tools_pbc_edits_receiving_20261026.json) records exact tested baseline, source hashes,
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
[physchem receipt](../devtools/data/molsysviewer_tools_physchem_properties_receiving_20261026.json) records source hashes, the exact 7/30 inventory,
23 pending exports, independent references versus parity and both native audits.
Post-run additions concern report/index/documentation only; committed-head CI is
still separate and pending at this snapshot. No host runtime change is needed.


The physchem producer 2b777e554 now passes all six original source CI controls,
including 1,576 native and 1,137 addon cases in smoke 40413404006. This supersedes
the local receipt's pending-CI state. The [provider record](pending_proposals/molsysviewer_tools_addon.md)
retains terminal evidence, source hashes and native/installed limits.


## Additional reference descriptors and native PBC receiving — 2026-10-26

Six explicit physchem wrappers add both ProtOr helpers, get_surface_area,
get_volume, get_area_buried and get_buried_fraction. Thirteen of the 30 reviewed
exports are now exposed; 17 remain pending. Native containers, definitions,
atom/group axes and no-assignment behavior remain unchanged. get_volume has
only an addon-owned keyword skip_digestion because the native helper lacks it;
get_area_buried gains no invented syntax argument. Native tables are not a
conformational SASA/volume calculation. Collantes unit qualification remains
explicitly uncertain under uibcdf/molsysmt#473; no guessed conversion is added.

The native repair d7c82e92f also restores orthogonal omitted/None box angles
and centered in-place wrapping ownership under uibcdf/molsysmt#465 and
uibcdf/molsysmt#467. The addon removes its temporary prewrite rejection; native
science still owns all coordinate calculations/publication. The 24 centered
receiver cases use independent weighted-center/lattice references, native
parity, nm/angstrom/pm, repeated/nonconsecutive structures, skip controls,
retained owners, exact interaction coverage and deferred synchronization.
The 67 new property cases pass on the isolated committed baseline. Full scoped
regression and committed-head CI remain separate pending gates at this point.


The single scoped local regression records 1,726 passes and ten failures from
one temporary get_transmembrane_tendency forwarding error introduced while
expanding the namespace. That call is corrected; all 329 cases in the four
affected files then pass. No second clean full local run is claimed. The
[dated receipt](../devtools/data/molsysviewer_tools_physchem_tables_receiving_20261026.json)
preserves both outcomes, source hashes and the pre-fix diagnostic. Five PBC
guide blocks, 33 native docstring examples and the new property guide block
execute. All code cells/outputs in the four property-course paths are preserved.
The final committed-source addon CI remains the whole-tier post-fix gate.


## Descriptor source CI and native query repair receiving — 2026-10-26

Producer 3c2dfcf651e2b6a8505cd7d88b38686811079f4a completes all six original
source controls. Smoke 40418549676/job 121906860117 passes 1,576 native and 1,230
addon cases with no failures/errors/skips. Ruff 40418549659, dependency
40418549584, developer guide 40418549611, suite policy 40418550369 and Conda
governance 40418550276 pass. GH Run Receptor confirms terminal success.
Original log `/tmp/msm-addon-3c2dfcf6-tables-smoke.log` has SHA-256
`f103d16bd6de793eb21fe1a50b5a067bae62b40af54e128da445e9fdc5cd269c`. This is the whole-addon post-fix gate; it does not relabel
the first failing local regression as a clean run.

The subsequent native query repair 825a66d39 under uibcdf/molsysmt#470 and
uibcdf/molsysmt#471 is received separately. All 627 targeted addon/native
contract cases pass in 183.33 seconds, with no failures/errors/skips; 40 inherited
property docstring examples pass. Receiver tests now require successful alternate
syntax against intended resolved atom/group populations, rather than accepting
the former native rejection. Unsupported fixed levels reject before interpreting
an invalid selector, with both ordinary and trusted flags. Obsolete current
help/guide warnings are removed. Raw table unit review uibcdf/molsysmt#473,
other tool families and installed qualification remain separate. The new
`molsysviewer_tools_physchem_query_repairs_receiving_20261026.json` receipt in
devtools/data records source hashes and scope. Final committed-head CI follows.


## Exact-source fixed-ref qualification completed — 2026-10-26

Producer 77657b030ac0e0a7858e6a3db70628e93b5c0c8c completes source qualification. Five original
controls pass on that exact SHA: Ruff 40420418943, dependency 40420418946,
developer guide 40420419175, suite policy 40420419530 and Conda governance
40420419490. Original main smoke 40420419017 and later composed main smoke
40420849878 remain cancelled by legitimate concurrent main-branch commits;
neither is counted as a passing test result.

Exactly one replacement [smoke 40421689803](https://github.com/uibcdf/molsysmt/actions/runs/40421689803)
runs on fixed source ref qualification/viewer-tools-77657b0, independently of
main concurrency. GitHub run/ref metadata both resolve to 77657b030ac0e0a7858e6a3db70628e93b5c0c8c.
Job 121917427555 passes 2,011 native and 1,246 addon cases with no
failures/errors/skips. GH Run Receptor confirms terminal success. Original log
`/tmp/msm-addon-77657b03-fixed-smoke.log` has SHA-256
`12494e500201f3875ba486e89f62dd04ae99447eb461dfbf7fd7f6f742973b25`. The reference stays fixed as a source-CI record; it is
not a release tag, artifact producer, promotion or package qualification.

This supersedes the pending-CI state of the query-repair receipt, without
rewriting its snapshot or the earlier full-local-run failure. The thirteen
physchem paths and received native PBC/query repairs have completed this source
gate. Native unit review uibcdf/molsysmt#473, the other seventeen physchem
exports, panels and installed compatibility remain separate. Later owner
I/O, fixture and course commits retain their own qualification; this record
does not label every later main revision green. Both 1.0 publications stay paused.


## Conformational SASA source receiving — 2026-10-26

An explicit `physchem.get_sasa` wrapper adds the fourteenth of 30 reviewed
physchem exports, leaving sixteen pending. It forwards every native scientific
parameter/default and the declared digestion flag through the serialized reader,
without scene effects, preparation or result adoption. All primary atoms remain
occluders; requested elements filter outputs. No Viewer runtime change is needed.

Scientific qualification remains bounded: native CPU in the nm length context,
MDTraj CPU with nm/angstrom/pm contexts, native hierarchy sums and selection axes,
analytical sphere truth, and the actual different engine boundary conditions.
Native-engine non-nm area correctness is unresolved under uibcdf/molsysmt#478;
implicit engine-periodic semantics are tracked under uibcdf/molsysmt#479.
The addon does not compensate for either. GPU and installed-artifact receiving
remain separate, and both 1.0 publications stay paused.

Local receiving passes 56 SASA cases, then one applicable regression of 1,414
cases with zero failures/errors/skips and stable native/addon source/backend
hashes. The 1,250 warnings remain in the receipt/log, including legacy H5MSM
fixtures and existing diagnostic/third-party cases. All 36 guide blocks and
40 inherited native-context doctests pass. The [source receipt](../devtools/data/molsysviewer_tools_sasa_receiving_20261026.json)
retains the corrected pending-export test mistake and initial wrong-import-route
example attempt; neither is hidden or counted as a product defect.
Exact-producer CI is pending; earlier thirteen-tool receipts are unchanged.


## SASA source gate completed — 2026-10-26

Producer 9442e0df20a659b9d8fa6c9a8a6bc0d115a074fc passes all six source
controls: dependency 40427400706, Conda governance 40427401058, Ruff 40427400528,
suite policy 40427400994, guide integrity 40427400665 and
[smoke 40427400657](https://github.com/uibcdf/molsysmt/actions/runs/40427400657).
Smoke passes 2,011 native and 1,302 addon cases, zero failures/errors/skips.
This closes the preceding pending source-CI status at the original bounded SASA
contract; it does not resolve #478/#479 or qualify new native fixes, GPU or
installed artifacts. The source log has SHA-256
e60208c15f7d5028c07aacca383e9efea4f21458521f7d0660cbc664e97cdf72.

## Detached stored-chemistry reports — 2026-10-26

Explicit bound `physchem.get_hydrogen_inventory` and `get_chemical_readiness`
wrappers add two of the reviewed exports: source exposure is 16/30, with
fourteen pending. Both reuse the serialized reader and current resident primary,
forward native scientific parameters/results and introduce no scene or chemical
preparation effect. A distinct single structure must be requested on trajectories;
no visible-frame substitution or implicit first-state resolution is introduced.

Receiving covers native coverage/issues, int64 unknown H counts, indexed/virtual
separation, selected parents with external H neighbors, incident/crossing bonds,
typed empties, explicit and ambiguous/unassociated states, detached result edits,
nonfinite-coordinate reporting, unit metadata, pending/replacement/close behavior
and preserved molecular/interaction/scene domains. Reference-state external readiness syntax is repaired under uibcdf/molsysmt#480;
the bound reader now forwards its positive native contract without scientific
selector compensation. The report labels never certify valence or protonation.

Local receiving passes 66 report cases, plus 61 focused SASA cases on native
repair d8bda65ec. One joint regression passes 1,760 cases with zero failures,
errors or skips, stable native/addon/backend hashes and 1,325 retained warnings.
The existing GPU-selector compatibility tests execute CPU fallback; they are not
GPU qualification. All 37 guide blocks and 53 inherited examples pass. The
[source receipt](../devtools/data/molsysviewer_tools_chemical_audits_receiving_20261026.json) retains the initial native #480 failure, corrected
reference-test input, exact parent, environment, source hashes and prior CI.
The final producer d0563c61ddf70ef62e08f4676c1fe4ba1b11a15b passes all six
source controls. [Smoke 40430386606](https://github.com/uibcdf/molsysmt/actions/runs/40430386606)
passes 2,033 native and 1,373 addon cases, zero failures/errors/skips; suite policy
40430387125, Conda governance 40430387183, guide integrity 40430386488, dependency
40430386549 and Ruff 40430386451 also pass. The [terminal CI receipt](../devtools/data/molsysviewer_tools_chemical_audits_source_ci_20261026.json)
preserves the exact source, job/step identity and original-log SHA-256
174f60a533e5685f87cb98cc82ee0fbb6749d6620654255f39f8dcd3328e7b41. This supersedes the pending-CI state in the immutable local receiving
snapshot; #480 and other remaining tools keep their own scope. No host runtime,
dependency floor, installed qualification or paused publication changes.

## Default-reference selector repair — 2026-10-26

Native uibcdf/molsysmt#480 now preserves a reference-state request when
resolving external selections. Positive native/complementary/H5MSM and bound
reader guards cover the intended population, typed empty matches and read-only
state. A declared reference at index 1 remains distinct from a structure's
associated state 0. Explicit and structure-associated requests retain the
common selector's restrictions. No downstream selector translation is added.

The owning resolution and local qualification are
[recorded in #480](https://github.com/uibcdf/molsysmt/issues/480).
Unequal structure/state population persistence exposed a separate writer issue,
uibcdf/molsysmt#481; the selection repair does not fix that storage defect.


## Aromatic participant and flag readers — 2026-10-26

Explicit `physchem.get_aromatic_rings` and `get_aromaticity` wrappers bring
source exposure to 18/30 reviewed physchem exports; twelve remain pending.
Both bind only the current resident primary through the serialized reader and
forward every native scientific parameter/default and digestion flag. No host
runtime or molecular/scene preparation is introduced.

Stored participants require declared complete aromatic chemistry and whole ring
selections, retaining sparse sorted memberships, fused/perimeter and tied-basis
limits, explicit completeness evidence and the cyclic block bound. Perception
uses the explicit optional RDKit model, returns detached flags with native
attribution, filters internal bonds after full-graph evaluation and never
assigns results to the source. These are chemical reports, not geometric
interactions or per-structure occurrences.

Native repairs f234396bb46e384e1d3b30b369de9798aafbf91c close
uibcdf/molsysmt#482 and uibcdf/molsysmt#483: default-reference external syntax
is retained and explicit resident ring structure indices are validated. Explicit
and structure-associated state syntax still obeys the native selector's
restrictions. Readiness #480 is received from f27406cd6, and c4b7abacd preserves
explicit H5MSM maps across unequal populations. No consumer compensation is
introduced. Installed MDTraj symbolic-comparison compatibility is separately
tracked under uibcdf/molsysmt#484; aliases and numeric selections are not silently
substituted. Compact collection-count presentation is pytest-receptor#46; pytest
exit status remains authoritative.

One frozen applicable regression passed 1,935 cases on 35ef8f5f plus the initial
51 aromatic cases, before incoming native repairs. The f234396bb follow-up passed
363 cases, including the expanded 93-case aromatic addon file. After receiving
8cf8b0107, the changed-area follow-up passed 910 cases with no failures, errors
or skips (143 legacy H5MSM warnings). All 38 guide blocks and 65 inherited
native-context examples also passed. These are sequential source observations,
not three independent full-suite gates. The compiled backend was retained,
not rebuilt; installed-artifact qualification is separate.

The current native surface-area reader now returns a standardized quantity from
the provisional Collantes Å² convention. The addon preserves that quantity;
original-paper units, normalization and values remain unverified under
uibcdf/molsysmt#473. Table lookup is not conformational SASA.

The [source receipt](../devtools/data/molsysviewer_tools_aromatic_receiving_20261026.json) preserves inputs, test phases, fixture corrections
and evidence limits. Final exact-source CI is pending at receipt creation.
Source exposure does not qualify every model, missing optional provider,
installed artifact, GUI or release. Both 1.0 publications remain paused.


### Aromatic readers: exact-source CI received — 2026-10-26

Producer `eeaf1cab8e9a1ea24113cc131da39a5f834a8217` completes all six source controls.
[Smoke 40438923814](https://github.com/uibcdf/molsysmt/actions/runs/40438923814)
passes 2,117 native and 1,467 addon cases with zero failures,
errors or skips. Dependency 40438923826, Ruff 40438923843, guide integrity
40438923895, suite policy 40438924145 and Conda governance 40438924176 also pass.
The [terminal source receipt](../devtools/data/molsysviewer_tools_aromatic_source_ci_20261026.json) retains source/job/step identity and the
original log SHA-256 `7d2855acf0d26894597ee420c46aade0df316bc25c5cc772d49d49fdeb9e9094`. It supersedes the pending hosted state in the
immutable local receiving receipt; its sequential local phases stay unchanged.
The named native/third-party limits, remaining twelve reviewed physchem paths,
GUI and installed qualification retain their own scope. No publication changes.


## Formal-charge centers and chemical feature sites — 2026-10-26

Three explicit physchem mirrors add get_charge_centers, get_hydrophobic_sites
and get_halogen_bond_sites. They bind the current resident primary through the
serialized reader, retain exact native scientific signatures/defaults and
results, and do not assign chemistry, prepare molecules, synchronize managed
edits or create scene objects. The native inventory has grown to 31 exports
with af8264049's bulkiness addition; 21 are now exposed and ten, including
bulkiness, remain pending in this facade.

Known small declared graphs check whole sparse charge-center memberships,
distinct geometry references and elementary-charge quantities, typed
hydrophobic atoms, and ordered halogen donor/reference pairs. Selection cannot
cut a compound charge center; SMARTS output filtering retains only selected
atoms or complete pairs after full-source recognition. Explicit completeness
assumptions record evidence without repairs; unknown chemistry and exceeded
match caps reject even with empty output. These are bounded chemical-feature
contracts, not universal classifications or geometric interactions.

Native default-reference external syntax is received for charge centers and
MDTraj comparison parsing uses the actual imported PyParsing 3.3.2. The installed
environment also has stale 3.3.3 distribution metadata, so its metadata alone
must not be reported as the executed parser or a clean package qualification.
The SMARTS selection branch originally lost the reference request; native
uibcdf/molsysmt#488 repairs the shared-boundary delegation. Positive default/None
reference and nonzero-reference receiving now passes for all three feature tools.
The initial reopen of #482 was restored to its qualified aromatic/ring scope to preserve the immutable archive.
Explicit and structure-associated SMARTS syntax retains its native restrictions;
the facade supplies no selector or state rewrite.

The frozen pre-repair snapshot passes 62 focused cases and its one 2,812-case
applicable regression, with unchanged source/backend hashes. The provider repair
then passes 390 targeted checks, including the expanded 81-case feature-reader
file. These are distinct source observations, not two full-suite gates. The
39 guide blocks / 83 inherited native-context examples pass; final exact-source
CI is recorded after final integration. The received native repair is fixed at
`c64e3599c2b772320b8bb4ec5e1842d3f997a63b`; all four tested native files match
that commit byte for byte. The [source receipt](../devtools/data/molsysviewer_tools_feature_sites_receiving_20261026.json)
retains the initial failures, sequential test phases, provenance and exclusions.
This scope does not qualify all chemistry, optional-provider absence, installed artifacts, graphical panels,
benchmarks or release candidates. Both 1.0 publications remain paused.


### Feature readers: exact-source CI received — 2026-10-26

Producer `02671792f3b90de654b467683a8d394118dc4ccb` completes all six source controls.
[Fixed-ref smoke 40446657873](https://github.com/uibcdf/molsysmt/actions/runs/40446657873)
passes 2,293 native and 1,548 addon cases with zero failures,
errors or skips. This includes the native SMARTS reference guard and the expanded
81-case consumer feature file. Dependency 40445094701, Ruff 40445094654, guide
integrity 40445094707, suite policy 40445095033 and Conda governance 40445095086
also pass. The [terminal CI receipt](../devtools/data/molsysviewer_tools_feature_sites_source_ci_20261026.json) retains exact source/job/step
identity and original-log SHA-256 `7d2c3ee12b8bbd4ebff4a00214cac570eb3b145509e9d7208b73a2d3eef014e5`. This supersedes the pending hosted
state in the immutable local receipt without changing its sequential evidence.
Original main smoke 40445094772 remains cancelled; one manual recovery uses
`receiving/physchem-sites-02671792f` at the same SHA, isolating the source gate
from concurrent main pushes. The original cancellation is retained in the receipt.
Native mutable reference metadata remains tracked under uibcdf/molsysmt#490;
these passing cases do not qualify arbitrary mutation of returned references.
At this producer ten native paths remain unwrapped. Subsequent native 5681f5e78
adds secondary-structure propensities: the inspected inventory is now 32, with
21 wrappers and eleven pending tools. The newer export is not qualified by this
older source gate. GUI and installed qualification remain pending; no host
runtime, package floor or paused-publication change is introduced.


### Reference-metadata repair received locally — 2026-10-26

Native #490 is resolved in `6eebcd4ec30e8ed3fbb76ea6e36cbfca5f326c9f`. An isolated snapshot
matching that committed source passes 172 targeted cases (native reference
ownership plus the existing feature/table consumers), zero failures/errors/skips,
with 77 legacy H5MSM warnings. A bound-reader check mutates one hydrophobic
reference and confirms a later same-reader result and a halogen result retain
independent canonical 2.2.2 references and the scene stays unchanged. The native
guard also covers nested metadata and evaluated-empty results. The provider
detaches small references; the addon adds no copy or scientific transformation.

The [local receiving receipt](../devtools/data/molsysviewer_tools_reference_metadata_receiving_20261026.json) retains source-file digests, JUnit digest
and the executed bound-reader observations. This removes the metadata ownership
limit when using that received source, without retroactively changing producer
02671792f or its hosted evidence. No second full regression, new hosted gate,
installed artifact or release qualification is claimed. Current native exports
remain 32; 21 wrappers and eleven pending functions retain their separate scope.


## Bulkiness and secondary-structure reference scales — 2026-10-26

Two explicit physchem readers add get_bulkiness and
get_secondary_structure_propensity. The first reviewed 32-export baseline has 23 wrappers. Native 97a8dc08c then
adds TPSA, making the inspected inventory 33 with ten pending addon functions. These group-name lookups retain native
scientific signatures, the required propensity category, validation, output
containers/units and optional attribution. The primary is resolved at call time;
no scene color, assignment, preparation, averaging, category inference or
synchronization is added.

Bulkiness remains a standardized reference area quantity, with later published
Å² interpretation and native original-derivation evidence limits. Levitt weighted
ratios remain dimensionless float64 arrays rather than probabilities or observed
secondary-structure assignments. Group-only scope, ordered/repeated/scalar/empty
axes and strict unknown/modified/cap/placeholder-name errors are retained. The
wrapper never filters terminal caps silently or invents sums and normalization.
Rich selectors retain their own coordinate requirements; the lookup itself
requires group names, not a structure axis or geometric calculation.

All 119 focused consumer cases and the one frozen 3,144-case applicable
regression pass on 39bb09715 plus these readers, with zero failures/errors/skips
and unchanged source/backend hashes. All 40 guide blocks and 90 inherited
native-context examples pass. Initial test expectations used the wrong exception
base and miscounted the bundled ACE–ALA–NME demo; those were corrected without
runtime changes. An authored guide block contained accidental patch prefixes;
these were removed before successful compilation/execution. The source receipt
preserves these attempts rather than treating them as provider defects.

Exact-source hosted CI remains pending at local receiving. Broader optional-
provider absence, installed compatibility, performance and universal scientific
validity remain separate. Native metadata #490 remains repaired and received;
its guard is now explicitly included in the bounded CI tier. Other scientific
families, the GUI and both paused publications retain their own scope.


The scientific owner subsequently publishes the group-free molecule query/builder
repair cd00cd40a and TPSA 97a8dc08c. A 596-case focused follow-up on that incoming
composition passes, zero failures/errors/skips, retaining the two scale signatures
and contracts; no second full regression is claimed. The group-free native guard
is included in the bounded CI tier. TPSA remains unreceived by the addon; a new
native export does not automatically expand its facade or qualify that science.


### Reference scales: exact-source hosted receiving completed — 2026-10-26

All six applicable source gates pass for efc9b94f37bbad8af251b58f81bbb17db029793f.
Smoke [40453242375](https://github.com/uibcdf/molsysmt/actions/runs/40453242375)
passes 2,576 native and 1,666 addon cases on Linux/Python 3.14, zero failures or
errors. Two native and one addon attribution tests are skipped because optional
Ackredit is absent. Local receiving executes them; it does not turn hosted skips
into passes. Dependency, Ruff, guide integrity, suite policy and Conda governance
all pass on this same source. The [terminal receipt](../devtools/data/molsysviewer_tools_reference_scales_source_ci_20261026.json) preserves official job/step
identities, exact Viewer deaba4cbea source, log and receptor-bundle file digests,
counts, optional omissions and remaining scope. It supersedes the earlier local
receipt's pending hosted state without changing that immutable observation.

The evidence-only closeout does not expand the 23-tool facade or receive TPSA,
optional-provider absence, graphical tasks, installed artifacts, performance or
another platform. Both 1.0 publications remain paused. No runtime change is made
by this receipt; no duplicate heavy smoke is needed for this evidence-only commit.


## Molecular TPSA receiving — 2026-10-27

The explicit get_tpsa reader extends the experimental physchem facade to 24 of
33 inspected exports. Nine tools remain unreceived. It binds only current
view.molsys and delegates unchanged native parameters, digestion and results.
Native molecule order/repetitions/scalar/empty axes, complete covalent boundaries,
explicit state and nonconsecutive structure context, squared area units and the
N/O versus N/O/S/P choice remain visible. The optional detached report preserves
source maps, method, software and provenance; no fragment capping, chemistry or
hydrogen preparation, aggregation, color, adoption or scene sync is introduced.
TPSA is distinct from geometric SASA and permeability prediction.

Two native defects were independently reproduced without Viewer and filed with
maintainer authorization: #494 duplicates molecule rows when adding groups to
an existing molecule inventory; #495 fails group-free MDTraj selection with
NAType. These are owner repairs, not consumer translation or hierarchy patches.
The receiving uses valid group-free sources, numeric/native expressions, exact
rejection parity for the external-syntax limit, and bundled caffeine explicitly
read through RDKit with declared H inventory. Native SDF records without the
required CTAB H evidence remain rejected rather than silently inferred.

All 53 directed consumer cases and the one frozen 3,294-case applicable
regression pass on c905d8ac7 plus this wrapper, zero failures/errors/skips. Source
and retained ABI3 backend hashes are unchanged during the regression. All 41
bound-guide blocks and 94 inherited native-context doctests pass. The source
receipt retains the initial builder/MDTraj findings and the corrected SDF input
expectation; these do not justify a scientific transformation in the consumer.
The records for #494/#495 remain open with owner acceptance criteria.

Exact-source hosted CI is pending at local receiving. Uncommitted native work on
molecular descriptors is explicitly preserved and not included in this source
qualification. The code does not receive either native repair, optional-provider
absence, GUI, installed artifacts, universal model accuracy or another platform.
Both 1.0 publications remain paused.


### TPSA terminal source receiving and incoming refactor — 2026-10-27

All six applicable source gates pass for producer f55d7c2f7. The single fixed-ref
smoke [40549539065](https://github.com/uibcdf/molsysmt/actions/runs/40549539065)
passes 2,645 native / 1,718 addon cases; three native and two addon attribution
cases are skipped because optional Ackredit is absent. Our automatic main smoke
40549383525 was intentionally cancelled during setup, preserving its non-pass
status while the canonical gate runs on receiving/tpsa-f55d7c2f7. No tag, release
candidate or package is created. The [terminal source receipt](../devtools/data/molsysviewer_tools_tpsa_source_ci_20261027.json)
preserves official source/ref/job/step identity, controls, original cancellation,
counts, skip evidence and complete log/receptor-bundle digests.

The native owner subsequently commits 4e2e18ce7, moving TPSA internals into a
shared molecular-descriptor helper and adding get_lipophilicity. The TPSA wrapper
remains unchanged. A clean incoming-source snapshot passes 158 directed native
and consumer cases, zero failures/errors/skips, plus 41 guide blocks and 94
inherited examples. This is focused receiving, not a second full regression.
Owner smoke [40549946055](https://github.com/uibcdf/molsysmt/actions/runs/40549946055)
also passes 2,645 native / 1,718 addon cases with the same five optional Ackredit
omissions; Ruff, guide integrity, suite policy and Conda governance pass on this
same incoming source. The unchanged dependency declarations/pins retain their
prior applicable f55d7c2f7 check; no separate 4e2e18ce7 dependency workflow ran.
The [incoming receiving receipt](../devtools/data/molsysviewer_tools_tpsa_refactor_receiving_20261027.json)
keeps both phases distinct. The original 3,294-case regression stays attached to
its older c905d8ac7-plus-wrapper source.

The inspected native inventory is now 34, with 24 addon functions and ten pending,
including lipophilicity. Its new scientific model is not adapted or qualified by
this TPSA receiving. Native #494/#495 remain owner repairs, with no consumer
hierarchy/selector workaround. Actual optional-provider absence, GUI, installed
artifacts, universal model accuracy, performance and other platforms remain
separate. Both 1.0 publications stay paused. This evidence-only closeout changes
no runtime and reuses the exact completed source gates.

### TPSA native contribution extension — 2026-10-27

Native uibcdf/molsysmt#497 adds atom/group/component/chain/entity/system
contribution outputs while preserving the molecule default. The existing bound
reader delegates these levels without a new control or scene update. Consumer
guards now test all seven valid levels and retain unsupported bond-level
rejection. Reports distinguish output `element_*` maps from evaluated molecular
contexts; H attribution and scalar system selections follow native semantics.
This does not receive the separate lipophilicity reader or claim installed-pair
qualification. The general native membership prerequisite is uibcdf/molsysmt#498.


## Bound lipophilicity and complete-context contributions — 2026-10-27

The explicit get_lipophilicity wrapper extends the physchem facade to 25 of the
34 reviewed native exports; nine remain unreceived. Both molecular descriptor
readers receive the contribution contract of native 010c489aa. Science remains
in the native owner: exact parameters, digestion, element/structure/state scope,
source indices and result containers are forwarded with current view.molsys
implicit. No scientific algorithm or source preparation is added to the addon.

TPSA preserves squared area units and N/O versus N/O/S/P. Lipophilicity preserves
dimensionless float64 arrays or system scalars, negative contributions, declared
charged sites and the limits of physical logP/logD interpretation. Atom, group,
component, molecule, chain, entity and system outputs retain source order,
repetitions, empty axes and explicit aggregation. Element output maps remain
separate from complete evaluated parent contexts. Indexed H retains its own row;
nonindexed H is attributed to its retained attachment atom. Partial output never
recalculates a cut molecular fragment or changes the source atom/H inventory.

All 122 directed consumer cases pass, including independently fixed reference
rows, reversed declared group/chain membership, repeated/empty/scalar outputs,
positive external syntax with explicit hierarchy, state/frame ambiguity,
H-presentation conservation, actual charged and bundled caffeine graphs,
independent nested provenance, pending reads/replacement/lifetime and real
optional Ackredit. All 43 bound-guide blocks and 98 inherited native-context
examples pass. These are bounded contract/parity/reference checks, not universal
predictive accuracy or installed-package qualification.

The one frozen 3,589-case applicable regression passes with zero failures,
errors or skips. Runtime source and the retained ABI3 backend remain unchanged
during that run. The recorded 1,499 warnings retain their original categories,
including legacy H5MSM and controlled GPU/invalid-input observations.
No new native defect is reported by this slice. Native #494/#495 keep their
separate owner receiving; the addon adds no selector/hierarchy workaround.

Exact-source hosted CI still requires integration. GUI tasks, optional-provider
absence, performance, other platforms, artifacts and both paused 1.0 publications
retain separate scope. Source support is not installed-package qualification.

### Native group-free hierarchy repairs — 2026-10-27

Owner repairs uibcdf/molsysmt#494/#495 preserve inherited source molecules during
group insertion and allow MDTraj selections through external-only placeholders.
The bound TPSA reader retains exact native delegation and requires actual selector
success in its receiving guard, with source hierarchy and scene state unchanged.
Metadata selector limits follow the native adapter; no consumer translation or
source repair is added. The subsequent uibcdf/molsysmt#499 owner repair aligns atom growth across
all populated states and converts its retained guard to an ordinary passing test.
New assignments stay unknown/partial; this does not add a Viewer atom-editing
operation or automatic scene adoption.


### Bounded native-plus-addon scientific smoke budget

The development `ci-smoke.yaml` job has a finite 25-minute maximum. Its scope
includes environment/toolchain setup, native build, native scientific guards,
the bound MolSysViewer scientific tier and cleanup. Keep those selected tiers
when adjusting operational budget; do not remove tests to manufacture green CI.
This ceiling is a bounded operational choice, not a guaranteed runtime across
all runners. GitHub timeout/cancellation remains a non-success conclusion even
when completed pytest output is positive. Preserve the official run, annotations
and original outputs, then qualify a corrected source through an actual complete
run. The measured 15-minute exhaustion and accepted adjustment are tracked by
uibcdf/molsysmt#501; fixture migration is the separate uibcdf/molsysmt#500.

### Descriptor CI closeout — 2026-10-27

Corrected source 4ad988584 passes fixed-ref smoke 40575948453: 2,847 native
passes / four optional Ackredit skips / one strict #499 xfail, and 1,845 bound
passes / three optional Ackredit skips. All five other applicable source controls
pass. #500 fixture migration and #501 bounded-budget adjustment are resolved.
Original timeout/failure conclusions remain preserved. #499's later owner
repair ab165135e passes 80 directed native builder cases in separate receiving;
it is not retroactively included in the earlier hosted source or its counts.
See `devtools/data/molsysviewer_tools_descriptor_ci_closeout_20261027.json`.
