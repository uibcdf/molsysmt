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
controls, eleven current `topology` analysis readers and ten `structure`
calculations under `view.addons.molsysmt`. Other scientific namespaces, edit families and graphical
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
prettyprint retains native stdout/None behavior. get_sequence_identity lacks a
declared native skip flag: its addon keyword controls only addon digestion.
Native sequence/group-axis mismatch uibcdf/molsysmt#439 remains visible; source
parity is not certification of that scientific result or a wrapper formula fix.


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

Known heavy-mode defects uibcdf/molsysmt#440/#441 are preserved and visibly
reported, not silently corrected by changing routing, units or formulas. Native
parity for those affected routes does not qualify numerical correctness. Source
examples explicitly choose eager mode for affected small-system calculations;
that is not a large-system memory guarantee. Optional GPU/alternate engines,
remaining structure exports and coordinate-changing operations need separate
receiving. No new host runtime, public API or frontend transport is needed here.


## Independent structural comparison and fitting readers — 2026-10-23

The source also receives get_rmsd, get_least_rmsd, get_principal_axes and
get_least_squares_plane through the existing serialized reader. They preserve
native signatures, return quantities/arrays/dictionaries and reference inputs.
Raw RMSD does not fit coordinates; minimum RMSD optimizes a temporary comparison
without transforming either input. References stay caller-stable, with native
selection/reference-index defaults, not an auxiliary-view transaction. Its
missing native skip parameter is handled by an addon-only keyword, never forwarded.

Axes retain native numeric moments, ascending eigenvalues, row basis and
sign/degenerate-subspace semantics. Plane results retain sparse memberships,
source structure order, typed empties and native quantity/normal fields. Fitting
a plane does not create a shape, certify chemistry or unwrap periodic groups.
No source/scene edit, automatic attachment or new host runtime follows.

The reviewed direct calculations and numeric/property selectors avoid the
get_distances path affected by uibcdf/molsysmt#441. General rich selectors and
optional engines retain their own dependencies. The maintainer requires waiting
for the MolSysMT scientific team to fix #441; min/max/contact/neighbor wrappers
remain pending, with no addon alternative or hidden routing correction. RMSF
also remains unreceived after native forced-unit issue uibcdf/molsysmt#442.
Other scientific corrections remain with their owning team.
