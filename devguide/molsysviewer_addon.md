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
calculations and retained-axis translation, proper rotation, plane reflection, least-RMSD fitting/alignment, explicit centering and single-structure displacement under `view.addons.molsysmt`. Other scientific namespaces, edit families and graphical
task panels remain pending. Old root entry points and retired adapter files remain
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
