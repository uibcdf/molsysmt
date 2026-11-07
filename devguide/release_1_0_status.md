# MolSysMT 1.0 Execution Status

**Role:** operational status ledger
**Last updated:** 2026-11-07
**Plan:** [MolSysMT 1.0 Execution Plan](pending_proposals/release_1_0_execution_plan.md)
**Release checklist:** [Release Gate](release_gate.md)

## Purpose

This is the single current answer to:

- what is complete;
- what is in progress;
- what remains pending;
- what is blocked or deliberately deferred;
- what evidence permits the next stage to start.

The execution plan defines scope, order, weights, and exit criteria. Detailed
bug reports and proposals define individual contracts. This ledger records only
current execution state and evidence; it must not duplicate or redefine those
contracts.

## Current correction checkpoint — 2026-11-07

The bound-tool source, #602 native/expert rotation constructor and
#632/#633/#634/#637 corrections are delivered on main in `684a5b0cb`;
archived records are published in `2499dc53b`. Independent complete GitHub API
trees match all 141 changed source paths and all changed archive paths. All
five issues are verified closed as completed. The
[delivery record](../devtools/data/rotation_source_delivery_602_632_633_634_637_20261107.json)
keeps publication/board evidence separate from local receiving.

The [receiving receipt](../devtools/data/axis_angle_and_transform_receiving_602_633_634_637_20261107.json)
records 7,764 integrated passes, 76 minimum-provider passes, 107 scientific
passes across 68 nodes, five executed notebooks and 14 passing fast gates.
Counts overlap. Original failures, the development-only ineligible scientific
certificate and six HTML underline warnings remain retained. Four human-owned
API stubs are unchanged.

#638 is delivered on main in `c4202c634`, with all 22 changed paths
independently matched and the issue verified closed. The
[delivery receipt](../devtools/data/xyz_coordinate_representation_delivery_638_20261107.json)
records source/board acceptance; [receiving](../devtools/data/xyz_coordinate_representation_receiving_638_20261107.json)
retains the passing controls, original failures and that stage's board snapshot.

#636 is delivered in public checkpoint `6d9f8b07a`, implementation
`970cf51b7`; all ten changed paths match the public tree and the issue is
verified closed. The [delivery receipt](../devtools/data/scientific_source_correspondence_delivery_636_20261107.json)
keeps source/board verification separate from the 23 runner controls and
107 actual molecular cases/68 nodes in its [receiving](../devtools/data/scientific_source_correspondence_receiving_636_20261107.json).
The latter pass `--require-clean` on the clean development commit; narrow
scientific/source eligibility does not select a release candidate. The complete
board now has 570 issues, 98 open, through #638; audit-related closures are **26**.

Next: receive published PR head
`42f5ed3bc` and #635's endpoint guards on its actual newer Viewer. The current
results qualify exact Viewer `25061d9e9` only. Remaining #421 graphical,
Jupyter/navigation, installed and human acceptance and #524 public-host/clean
installed closure stay open. Audit progress remains **40%**, with **26 verified
audit-related closures**. No new candidate, tag, Release, promotion or remote
matrix is selected.

## Audit execution and next correction — 2026-11-06

The [robustness audit and action plan](pre_1_0_robustness_audit_20261106.md)
owns the current six-phase work sequence and weighted progress estimate under
#334. Phases 1 and 2 are published and their seven owner issues are closed:
#618/#616 in `19d6d55c1`, and #605/#607/#606/#608/#619 in `3eb720444`.
The [PBC delivery receipt](../devtools/data/pre_1_0_robustness_phase2_delivery_20261106.json)
independently verifies all 27 checked blobs and five closed PBC issues. Accepted
plan progress is **40%**, not a release-readiness percentage.

Current phase-three source `f60e25b7edad28f035429563fd8b46f4d93395f2` corrects
#613 configuration writer/restoration races. Local receiving passes 4,438
integrated cases, 32 controlled-source floor/docstring cases, 500 documentation
cases and 97 scientific cases; these scopes overlap. The
[receipt](../devtools/data/configuration_serialization_receiving_613_20261106.json)
retains exact source/backend identity, original failures, warnings and limits.
It implements the existing process-global serialization contract; outside
observers, direct assignments and overlapping async contexts are not isolated.
Public checkpoint `1b1cc42e0` independently matches all 12 checked implementation/
receipt/report blobs, and #613 is verified closed. Its
[delivery record](../devtools/data/configuration_serialization_delivery_613_20261106.json)
keeps that separate acceptance and the remaining phase-three scope.

The #620 precision correction is locally qualified in `cb07e54af`, with supported
single-coordinate publication retained and effective float64 CPU arithmetic
diagnosed explicitly. Partial #524 source `44fd0acf0` declares the Jinja2 renderer
needed by default `info()`. Joint receiving passes 4,592 cases, documentation/
public doctests 599, and registered scientific execution 97 across 64 nodes.
Profiles overlap. The [precision receipt](../devtools/data/native_precision_receiving_620_20261106.json)
and [renderer receipt](../devtools/data/runtime_renderer_receiving_524_20261106.json)
retain exact source/backend identities and original failures. Public checkpoint
`8d466268c` independently matches all 43 checked source/record blobs, and #620 is
verified closed as completed. The [delivery receipt](../devtools/data/precision_renderer_delivery_620_20261106.json)
records that separate receiving. All fourteen final fast gates pass; no new
remote workflow is dispatched.

Next, continue the remaining #524 provider/restriction review. Actual public
Viewer floor/acquisition and clean installed closure remain due; do not infer
them from source pins or extra-rich development environments. Phase 3 has no
completed credit yet. #613 smoke 42314744961 at `60ded0f7c` now succeeds, as do
the previously recorded PBC checks. Those are ordinary source checks, not a
release matrix. Working commits use `[skip ci]` and pushes are batched under the
maintainer's renewed direction; remote qualification stays with agreed checkpoints.
Preserve the #616/#613 consumer reports on PR #543 integration rather than
reintroducing duplicate pending records.

The subsequent #524 support-floor review now receives five required published
providers: 581 consumer cases pass with 14 explicit optional ArgDigest-study
omissions, and 133 additional parser/preparation/doctest cases pass without
omissions. Existing floors are retained. Placement source `4f8b03364` removes
redundant deprecated Pandas sorting and uses ChemicalStates normalization.
The same broader review discovers #621's missed phase-two MIC caller; source
`2804f7954` restores the periodic fixed-state H boundary. Combined exact-Pandas-
3.1.0 receiving passes 965, documentation 543 and scientific execution 97 cases;
profiles overlap. See the [support-floor receipt](../devtools/data/runtime_support_floor_receiving_524_20261106.json)
and [#621 receipt](../devtools/data/periodic_fixed_state_hydrogens_receiving_621_20261106.json).
Public checkpoint `ad6b71e97` matches all 14 checked source/record blobs, and
#621 is independently verified closed as completed. The [delivery receipt](../devtools/data/support_preparation_delivery_621_20261106.json)
retains the separate public receiving and fresh complete board snapshot:
553 issues, 97 open, and unchanged PR #543. #524 remains partial for optional-
provider/NumPy restrictions, actual Viewer acquisition and installed closure.
No new remote CI or release is selected; progress remains 40%.

Optional MDTraj review also reproduces #622: a full-length invalid atom subset
could return the complete native Topology. Source `35a0457f0` validates its atom
domain before that shortcut, without changing attribute-query repetition or
structure order. Final receiving passes 1,971 source/documentation cases without
omissions. The [owning record](archive/resolved_bugs/topology_extraction_accepts_invalid_atom_subsets_as_the_complete_source.md)
and [receipt](../devtools/data/topology_extraction_receiving_622_20261106.json)
retain original failures, protected-source checks and limits. Public delivery
and board closure follow. This adds no audit weight; #524 optional-floor,
NumPy, Viewer and clean installed qualification remain active.

Checkpoint `b206781ed` is now independently verified against all twelve changed
public blobs, and #622 is verified closed as completed. Its
[delivery receipt](../devtools/data/topology_extraction_delivery_622_20261106.json)
retains the source/board evidence. All fourteen fast gates pass. No new remote
workflow is dispatched; progress remains 40% and #524 is the next active work.

The subsequent #524/#623 source block is qualified locally. #623 source
`0ea1e04d7` preserves MDTraj subset charges/labels and dense hierarchy indices;
partial #524 `962b2c68e` declares the metadata-preserving optional minimum,
generalizes optional-provider contract auditing and removes the unsupported
NumPy-major ceiling while retaining the real ABI guard. Final actual MDTraj
1.11.0 and 1.11.2 profiles each pass 1,191 cases; the route/provider/workflow/
documentation profile passes 654, and nine directed minimum-provider cases pass
on Python 3.12. Scopes overlap. The paired parser population profile preserves
the 3.3.3 exclusion (28 failures there; all 72 pass on 3.3.2). Source receipts are
[subset receiving](../devtools/data/mdtraj_subset_receiving_623_20261106.json) and
[optional-runtime receiving](../devtools/data/optional_runtime_receiving_524_20261106.json).
Public delivery/closure follow. #524 remains partial for the other optional
providers and actual Viewer/installed closure; accepted audit progress stays 40%.

Public checkpoint `f5c909e75` independently matches all 32 checked blobs;
#623 is verified closed. The
[delivery receipt](../devtools/data/optional_runtime_delivery_623_20261106.json)
records fourteen passing fast gates, whole-tree Ruff receiving and the verified
MolSysSuite #137 source handoff. Its graph refresh remains owned follow-up.
A complete board refresh finds new #624, an explicitly unprioritized collection
capability proposal, and the unchanged PR #543. No new demonstrated bug changes
the current #524 work order. Accepted progress remains 40%; no publication or
remote full-matrix evidence is inferred from this source checkpoint.

The OpenMM follow-up selects optional >=8.2.0 in `3325cda95`, with the
minimum API grounded in formal-charge export. Actual public 8.2.0/Python 3.12
and 8.6.1/Python 3.14 each pass 2,098 selected provider cases without omissions.
It also fixes #625's PDBFixer availability boundaries (`80590ef76`) and #626's
OpenMM copy/subset chemistry and topology-only structure dispatch (`207d054cb`).
The [receipt](../devtools/data/openmm_runtime_receiving_524_20261106.json)
retains initial failures, native exits, actual artifacts/origins, ordinary bridge
receiving and preserved notebook content. Source publication and board closeout
follow. Remaining PDBFixer/optional-provider, Viewer and clean installed work
keep #524 partial and accepted audit progress at 40%; no new candidate is selected.

Public OpenMM checkpoint `4d1d5949a` now independently matches all 24
checked blobs; #625/#626 are closed as completed. The
[delivery record](../devtools/data/openmm_runtime_delivery_625_626_20261106.json)
retains the complete 558-issue board checkpoint (98 open), unchanged PR #543,
and separate source/installed evidence boundaries. Fourteen fast gates pass.
The audit has 14 closed owner/supplemental issues and stays at accepted 40%.
Continue PDBFixer and remaining optional-provider work under partial #524.

Optional PDBFixer >=1.11 is also locally qualified in `fac0d8706`: the
minimum/public-support and newer profiles each pass 172 selected cases, with
1.10's incomplete-cap counterexample retained. Runtime/docs separation
`0a06a01c2` removes unsupported OpenMMTools acquisition and preserves Plotly's
documentation route. Its 625 registry/route/docs cases and 14 fast gates pass.
See the [receipt](../devtools/data/pdbfixer_runtime_receiving_524_20261106.json)
for native exits, original DNS/harness failures, origins and scientific scope.
Public delivery follows; #524 remains partial for other optional APIs and actual
Viewer/installed closure. Accepted audit progress remains 40%.

RDKit source `883e4e45a` selects optional >=2024.3.4 from the consumed
coordinate/CIP API. The paired public-provider profiles each pass 541 and omit
one conditional negative-string case, with positive CCO parsing independently
covered. Source `13b82905c` fixes #627's duplicate-VAL reference fixtures;
production parsing and scientific score assertions are unchanged. See the
[receipt](../devtools/data/rdkit_runtime_receiving_524_627_20261106.json).
Public receiving/627 closeout follow. The parallel review admits #628/#629 as
reproduced existing-operation data loss: MDAnalysis copy/subset metadata/forces,
and ParmEd native export coordinates/charges/IDs. Their owning repairs and paired
consumer receiving are now complete as recorded below. Audit progress stays
40%; 14 issues are already closed and no replacement candidate is selected.

PDBFixer checkpoint `dd60ee7d6` independently matches all 16 public files and
the central #137 notice body is verified. The
[delivery record](../devtools/data/pdbfixer_runtime_delivery_524_20261106.json)
records the requested graph refresh without claiming owner-side completion.

The #628 repair `f81ba2025` passes 155 cases on each actual public MDAnalysis
2.8/Python 3.12 and 2.10/Python 3.14 profile. #629 source `e270eda9b` passes 185
on each actual public ParmEd 4.3.1/Python 3.12 and 3.14 profile. Both have zero
omissions. Optional floors are aligned in `33a702bfa`. Shared conversion/docs
receiving passes 1,271 and scientific execution 97 cases/64 nodes, no omissions;
counts overlap. Source/public delivery still precedes actual issue closeout.
The [MDAnalysis receipt](../devtools/data/mdanalysis_runtime_receiving_524_628_20261106.json),
[ParmEd receipt](../devtools/data/parmed_runtime_receiving_524_629_20261106.json)
and [scientific record](../devtools/data/runtime_provider_scientific_receiving_524_20261106.json)
retain original failures, provider origins and development-only limits. Remaining
optional work is OpenFF, Biopython, NGLView and PyTraj plus the actual host and
clean installed closure; #524 stays partial and accepted progress remains 40%.

Public checkpoint `82bfa1c82` independently matches all 58 changed blobs.
#627/#628/#629 are verified closed as completed: 17 audit-related issues are
closed. The complete board has 561 issues, 98 open, and the unchanged PR #543
head `8ab2f5474`. Fourteen fast gates pass. See the
[delivery receipt](../devtools/data/runtime_provider_delivery_627_629_20261106.json).
Accepted progress remains 40%; #524 is still partial.

The next optional-provider checkpoint is locally advancing: Biopython minimum
1.80 and newer 1.86 each pass 385 selected cases, zero omissions, using public
alignment-row access instead of a private method. OpenFF's existing declared
minima are retained after both actual profiles pass 86. PyTraj's supported
AmberTools acquisition, native engine paths, diagnostics and strengthened route
audit pass 146; disabled pip routes and bundle identity remain distinct from
version floors. These counts overlap with other selections.

New #630/#631 NGLView defects are admitted under the same correctness block.
Source `e5d1dd0f8` locally fixes #630's internal-keyword leak; its public minimum
receiving passes 95. #631's synthetic two-widget reproduction proves that an
independent widget's initial PDB is included in HTML; its explicit state-closure
correction is being qualified. No unrelated trajectory-buffer inclusion is
claimed. Both source delivery and actual board closure remain due; 17 issues
are already closed and accepted progress stays 40%. The remaining OpenFF route
metadata review, exact host and clean installed closure remain explicit exits.

Four human autosummary edits remain outside the commits. The final optional-provider block
is source-qualified in `d850f6cc1`/`5cd744ebf`, with #630 `e5d1dd0f8` and #631
`fae9ab557`: Biopython pairs 385 each, OpenFF pairs 199 each, NGLView pairs 104
each, all without omissions. Joint receiving passes 798, scientific execution
97/64 nodes and fast gates 14/14; scopes overlap. HTML compilation passes with
four retained existing title-underline warnings and protected human edits
unchanged. The
[remaining-provider receipt](../devtools/data/remaining_optional_runtime_receiving_524_20261106.json)
and [NGLView receipt](../devtools/data/nglview_runtime_receiving_524_630_631_20261106.json)
retain attempts and limits. Public delivery and #630/#631 closeout follow.
The compatible public Viewer floor and clean installed closure keep #524
partial and accepted progress at 40%; this source block selects no release.

Candidate selection and the publication pause remain unchanged; exact-platform, installed Viewer,
graphical and release gates are still due. The earlier fifteen-issue campaign
retains its original completed evidence below.

Final optional-provider delivery is public as `7e61fcc5c`, with all 39 checked
blobs independently matched. #630/#631 are verified closed: **19 audit-related
issues closed**, accepted plan progress **40%**. Complete board acquisition has
563 issues, 98 open and unchanged PR #543. The
[delivery receipt](../devtools/data/remaining_optional_runtime_delivery_630_631_20261106.json)
records the verified central #137 notice and requested graph refresh. #524's
source review is delivered; actual compatible public-host/clean installed
closure remains separate.

The next actionable source route is isolated reconciliation of #543/#421 with
the corrected owner and published Viewer `25061d9e`. The Viewer #314 record
reports source/Jupyter R4/browser-core receiving but remains partial. Preserve
its pending hosted/installed/human exits, the current archived owner fixes and
the sibling checkout's unrelated edits. The audit packet's phase-four entry
records the finite comparison/test route. No new host pin, source merge,
release candidate or remote workflow is selected by this read-only review.

## Maintainer-ordered resolution goal — 2026-11-06

The maintainer explicitly authorizes resolution in this order:
**#304 → #593 → #428 → #544 → #572 → #576 → #557 → #594 → #595 → #596 → #597 → #598 → #599 → #600 → #601**.
The last three were explicitly added by the maintainer after the board review;
the active objective now contains fifteen issues. Their addition preserves the
previous twelve-item order and does not authorize premature closure of #304.
Keep the entire objective; do not substitute a narrow passing subcase for issue
closure. Prior post-freeze scheduling of listed work does not block this explicit
instruction. Tags, Releases, promotions and provider-repository code edits keep
their existing authorization boundaries.

**Completed native/provider criteria: all fifteen ordered issues, through #601.**
No further implementation remains within this bounded goal. The final #600/#601
source checkpoint is published together; their board closure is performed in that
order only after independent public-source verification. The #557 source-permutation controls also identified supplemental
[#617](archive/resolved_bugs/entry_mmcif_conversion_retains_a_retired_topology_component_flag_and_blocks_perm.md):
the mmCIF converter wrote a retired Topology component flag. The one-line
producer correction passes 137 adapter/permutation cases, preserving strict
extension refusal. This is a prerequisite correction, not an expansion of the
fifteen-item goal. The accepted fifteen-issue order above is unchanged.
The #557 generic CCD factory and exact-name correspondence are implemented in
d419e6fc2, with 421 affected cases, 101 public-provider-floor cases and
2 doctests passing. The [owning closeout](archive/resolved_proposals/ccd_component_chemical_templates.md)
and [source receipt](../devtools/data/ccd_template_receiving_557_20261106.json)
retain experimental/scientific limits, original provider versions, exact source
bytes/maps and deposited MK1/BTN pose controls. The new offline course example
is executed without rewriting historical cells. The #428 installed producer
bd40d7059 is independently received. Actual installed #428 receiving passes 2,542 consumer
and 83 scientific cases with no omissions; 248 integrated guards for the four
latest closures pass locally. See the
[installed receipt](../devtools/data/argdigest_installed_receiving_428_20261106.json)
and [joint closeout receipt](../devtools/data/ordered_feature_closeout_428_544_572_576_20261106.json).
Main 34b8c09e2 smoke 42267238580 passes, as do its four other applicable
hosted checks. Earlier #428 receiving failures remain in their archive; the
new #557 checkpoint retains its own source/local gates and CI evidence.

The #594–#598 implementation was already incorporated by ab789897b; current
owner closeout verifies 259 serial classifier/addon/doctest cases, 242 affected
conversion/comparison cases, 51 serial catalogue/conversion cases and 83 serial
NGL/widget cases, all without failures or omissions. Counts overlap. The new NMR
guard in cddc3f3a6 independently checks every deposited coordinate across 38
structures and normalized source labels. See the
[bounded bug receipt](../devtools/data/ordered_bug_closeout_594_598_20261106.json).
Runtime comparison semantics, unsupported naming defaults, immutable catalogues
and production widget serialization are preserved. #557 smoke 42271829370
was later cancelled after the next main checkpoint; its workflow declares
branch-scoped cancel-in-progress. Latest checkpoint 882b65b9c has four passing
administrative workflows and successful smoke 42273763066. No cancelled run is
counted as a pass. The
[source handoff to DockingMT](https://github.com/uibcdf/dockingmt/issues/49#issuecomment-6692452871)
records public usage and leaves consumer/scientific acceptance separate.

The #599 prepared-PDBQT projection is implemented in fe36aa3ff and
464158e5c with **396 affected tests/doctests** and **84 cases at all five public
provider floors** passing. It preserves non-coordinate prepared fields and tree
meaning under explicit complete atom/structure correspondence, with declared
REMARK removal, actual payload hashes, partial-reference semantics and atomic
one-model file output. Full Module 10 executes; its previous cells/outputs remain
unchanged. See the [owning closeout](archive/resolved_proposals/prepared_pdbqt_conformation_projection.md)
and [receiving receipt](../devtools/data/prepared_pdbqt_projection_receiving_599_20261106.json).
The preserved earlier #304 full run 42205436569 now concludes successfully at
56b37c983; it does not qualify this new projection checkpoint. Current source
publication/CI is recorded separately. The final two criteria are recorded below.

The #600 model-label correction in 68fc09224 retains exact deposited string IDs
on the unchanged numeric model/coordinate axis, including repeated selections,
explicit missing-data handling and separate incompatible-model results. **925 affected
cases**, **38 provider-floor cases** and one additional real NMR coordinate/label
control pass; documentation HTML has no warnings. See the
[owning closeout](archive/resolved_bugs/mmcif_native_conversion_drops_deposited_model_labels_despite_declared_structure_.md)
and [receiving receipt](../devtools/data/mmcif_model_labels_receiving_600_20261106.json).
The final shared #600/#601 source checkpoint retains that implementation order.
The preceding main 40bb54d05 delivers #599, with all five applicable workflows
passing, including smoke 42283798590. The new checkpoint has separate CI evidence.

The #601 correction in 711717828 preserves operational adapter-load causes through
public form detection and argument validation. DepDigest retains ownership of
loading/cache/retry; unsupported input and incompatible axes remain distinct.
**774 boundary/digestion cases**, **1,397 offline conversion/PDBQT cases**,
**8 separate live-network conversion cases** and **68 public-provider-floor
cases** pass. Profiles overlap. The original sandbox-DNS/incomplete run and old
exception expectation are retained rather than counted as passes. All fourteen
fast gates pass, and updated documentation compiles without warnings. See the
[owning closeout](archive/resolved_bugs/adapter_load_causes_are_lost_in_molecular_system_validation.md)
and [receiving receipt](../devtools/data/adapter_load_causes_receiving_601_20261106.json).

Feature closure does not qualify the complete version matrix, a future Viewer
candidate, its canvas/sessions, or the sixteen-cell installed release pair under
#334. Native force/assessment facades still need consumer receiving under #421 /
uibcdf/molsysviewer#264. The default-info Jinja2 declaration remains tracked in
#524. No tag, release, registry upload or promotion is authorized by these closures.

The #304 native profile has qualified explicit reader policy,
exact standard/curated modified-group references, observed-H parent consensus,
optional pinned H-name alternatives, naming-scoped ACE/NME/NHE/NH2 references
and bounded same-chain peptide candidates. PDB file/text/handler routes receive
an explicit naming declaration before classification/inference. CIF/BCIF native
conversion honors disabled inference and retains declared edges. Deposited PDB
records have typed location, endpoint, alternate/symmetry and conflict evidence.
All of these remain bounded connectivity operations, without chemistry-complete
or default-engine-change claims. See the
[owning record](archive/resolved_proposals/native_pdb_bond_inference_with_explicit_policy.md).

The final policy-boundary receiving makes existing exclusions explicit in the
application report: retain stored disulfide and coordination edges, infer no
additional ones, and disable geometry for groups without an exact template.
Its selected unsupported group indices are typed historical evidence. Fifty-four
new controls qualify close/competing sulfur sites, contradictory/unresolved
SSBOND, water/ligand/metal proximity, all four curated modified groups, source
immutability, selection and H5MSM history. The completed affected selection passes
227 cases, the four-published-provider-floor selection 55, and documentation
1,091 (overlapping selections); the aggregate fast gate passes 14/14 checks.
An earlier accidentally selected network-only
case was interrupted; that command is not passing gate evidence. The final
selection excludes that one network case explicitly. Both original PDB native
graph, atom-axis and coordinate digests remain unchanged, with fresh H5MSM
round trips and OpenMM imports blocked.

Original 181L/1IEP differences are explained by exact-name versus H-name-alias
policy (25 pairs) and noncontiguous group interpretation (one native-only pair).
The retained 45-process benchmark covers both originals plus three analytic
workloads up to 10,240 atoms and 15 H5MSM round trips. Native conversion is slower
in those measurements; the larger-workload RAM/storage cost remains explicit.
No new faster/lighter claim follows from the policy metadata.

The exact-source gate for #304 is now
[42205436569](https://github.com/uibcdf/molsysmt/actions/runs/42205436569),
on **56b37c983253e8f93cda6333703df2b3a626a238** with controlled Viewer
42234de839ed047016f8f241ea5eb717cfeb07be. All four Linux Python 3.11–3.14
cells and macOS Python 3.11/3.12/3.13 report success; macOS Python 3.14 is
still running. The six previously successful full-suite artifacts have been
independently received and their archive digests, JUnit and receptor evidence
checked. The additional macOS 3.11 artifact still needs independent receiving.
Each Linux suite records
29,253 passes and zero failures/errors. Its 118 JUnit skips comprise 117 item
skips plus one collection-skipped module; the receptor retains the separate
executed-item accounting. All 83 registered scientific cases and 432 directed
connectivity cases execute successfully per cell. Three additional optional
Ackredit controls are skipped for genuine dependency absence in each hosted
cell and pass separately with the published provider payloads locally.
Each received macOS suite has 29,252 passes, zero failures/errors and one additional
Linux-only test skip, retained explicitly rather than equating platform counts.
The [partial receiving receipt](../devtools/data/native_pdb_full_source_receiving_304_20261106.json)
retains exact artifact identities/digests and omissions. These are source checks,
not a complete matrix, installed pair or release qualification. This new gate
does not alter the earlier frozen PR candidate or erase its failed gate.

**Feature #304 is resolved at owner integration.** Its issue acceptance is
covered by the retained graph/policy/provenance/benchmark evidence. The earlier
decision to wait for the entire version matrix before closing this feature was
broader than that acceptance; the last active macOS lane and the additional
artifact receiving remain mandatory version qualification, with the exact running
source/ref preserved. The disulfide/unsupported-group
policies are now explicit and contract-tested; this does not promise automatic
oxidation-state matching, arbitrary-ligand preparation or metal-coordination
inference. No complete-matrix, installed-pair or release claim follows from closing
the implemented bounded feature.
New DockingMT proposal **#599** requests prepared-PDBQT conformation projection
for rescoring. Separately reported **#600** records missing mmCIF model-label
delivery; selected geometry remains available, and the connectivity correction
does not claim to fix that label contract. PeptideMT's **#601** requests preserving
adapter-load causes through form discovery and molecular-system validation.
These are explicitly included at the end of the expanded objective, with their
own implementation and acceptance work still pending.

The later **#602** requests a public axis-angle matrix constructor for Viewer.
It was read at this checkpoint and remains a separate incoming proposal; it was
not among the three additions explicitly identified when the maintainer expanded
this objective to fifteen. No automatic queue expansion or implementation is
claimed for later arrivals.

The next board checkpoint also reads **#603–#607**. These are incoming reports,
not additions to the maintainer's fifteen-item objective:

- **#603:** rejected-operation diagnostics lost by addon refresh; the contributor
  plans a fix in PR #543. That later source still needs owner receiving.
- **#604:** bounded positional RMSD/clustering requested by DockingMT. Its own
  proposal explicitly does not enlarge the frozen initial release gates.
- **#605:** box factories reportedly admit degenerate/nonfinite periodic cells.
- **#606:** temporal unwrap reportedly reuses the first cell classification after
  later cells become triclinic.
- **#607:** wrapping reportedly treats rotated orthogonal row bases as Cartesian
  diagonal cells.

The three new PBC reports contain consumer reproductions against main ed09f6453;
they are not independently reproduced in this PDB receiving checkpoint. Native
triage and correction/qualification are required before treating the affected
periodic families as ready for 1.0. The current PDB inference's nonperiodic
controls do not qualify those routes. Preserve the active ordered work and these
additional release obligations; do not silently mark them completed or deferred.

The integrated correction for **#593** is contract-tested while #304's
version-matrix source remains frozen. The course consumes independent repair outputs,
uses supported caps/quartets/torsion tools, requires a declared candidate pose
and binds the example mechanics request after atom edits. Its 12 new controls,
existing interface/minimizer regressions and documentation pass 1,118 cases;
22 overlapping published-provider-floor cases also pass, without omissions.
The 2BEG full biological route remains an explicit outline, with no invented
outputs or readiness claim. These satisfy the issue's explicit bounded-workflow
acceptance; documented closeout is complete after #304. See the
[owning record](archive/resolved_bugs/alzheimer_capstone_preparation_uses_unsupported_builder_keywords_and_drops_indep.md).

Public **ArgDigest 0.17.1** receiving for **#428** is complete:
2,542 native/digestion/query/diagnostics cases, all 83 registered scientific
cases and 14/14 fast gates pass. A 123-case overlapping constructor/ownership/
diagnostics selection also passes with SMonitor 0.16.0. Exact public payloads
are verified; the existing interpreter and other recorded development providers
are reused. `native_constructor`, global ownership policy and dependency floors
stay unchanged. The
[owning record](archive/resolved_proposals/argdigest_0_17_receiving.md)
retains the deliberate deferral of production ownership adoption. The subsequent
clean installed producer bd40d7059 passes 2,542 consumer and 83 scientific cases
in 42259461880 with verified archive/wheel/source bytes and actual public imports.
That actual installed evidence completes #428; the earlier source profile alone
did not close it. The final release-pair and #524 runtime-declaration gap remain.

Integrated owner source for **#544** pins all four active native build/upload,
ABI3 experiment and promotion calls to reviewed Conda provider v2.3.0
87c70b1443d5f22d738ee3ddf812bdbe0152f6c2. The other parsed workflow semantics
are unchanged. Its 54 local packaging/route controls, 29 offline provider cases,
exact already-called policy/publication checkers and dependency audit pass.
No package or registry mutation is executed. The
[owning record](archive/resolved_proposals/conda_provider_v2_3_owner_adoption.md)
retains the exact input/source evidence and completed ordered owner adoption.

Integrated source for **#572**, implemented at 993967a0f361d70cba5f7e5c7c246b0000734550,
supplies complete-environment native forces,
explicit structure axes, selection order/masks, magnitudes and application units.
One model context consumes bounded native/H5MSM coordinate blocks; an explicit
System can use a structures-only file without reconstructed chemistry. The
shared OpenMM converter also applies switching and explicit dispersion choices.
The affected 2,005-case selection, 77 published-support-floor controls and 583
documentation/doctest checks pass; the nine-cell tutorial executes with its plot
and 14/14 fast gates pass. Detailed source digests and execution limits belong to the
[owning record](archive/resolved_proposals/native_molsys_force_reader_for_bound_consumers.md).
The User Guide, Cookbook and course distinguish provider capability from addon
exposure. The native provider issue is resolved in order; no Viewer runtime is
changed and no release-pair qualification follows from these local checks.

Integrated owner source for **#576**, implemented at 5c13fcd85f03a5db956f7854686f5493789820d4,
supplies read-only
`build.assess_protonation` and a public `build.ProtonationAssessment` result.
Detached coverage retains every group's actual naming/reference context and
canonical bidirectional positional maps. Single-use application consumes the
same decision without repeating reference queries, rejects stale inventory,
chemistry and axes, and stages the complete native subset before publication.
Independent no-ops are real copies; all supported independent inputs return
native MolSys. Native/modular assessment avoids coordinate payloads, while
application retains ordinary resident candidate costs and analysis remapping.
The 1,717-case affected selection, 260 published-support-floor controls and 631
documentation/doctest/final-assessment checks pass without omissions; selections
overlap. All ten tutorial code cells execute, the fast gate passes 14/14, and
repository-wide Ruff lint/format checks pass. The
[owning record](archive/resolved_proposals/protonation_removal_correspondence_for_bound_consumers.md)
retains exact receipts, ownership/scientific limits and corrected validation
fixtures. The native provider issue is resolved in order. Managed addon admission
and final installed release-pair qualification remain separate. The frozen #304
version matrix retains its original source and outstanding qualification under
#334; it is not replaced by the bounded installed #428 receiving.

The subsequent board checkpoint reads **#608–#610**, again without expanding
the fifteen-item objective. #608 reports application-unit-dependent origin
snapping and extends the unresolved native PBC qualification obligations above;
it is not independently reproduced in this course receiving. #609 belongs to
later PR #543 Jupyter presentation-acknowledgement receiving, outside frozen
56b37c983. #610 asks for the supported XYZ/coordinate-delivery composition for
DockingMT; direct public quantity assignment is exercised here on bounded native
systems with both ranks and nm/pm policy, without claiming the consumer E4 run
or its exact older provider source has been received.

The next incoming report, **#611**, requests a measured finite smoke-budget
increase for the later PR's enlarged native/addon selection. Its cited run
42210639321 timed out at 25 minutes after the native tier completed; the addon
terminal result is absent. That PR contribution and its next exact-source
smoke need owner receiving. It does not change the active fifteen-item goal
or certify a new source gate here. At this board checkpoint PR #543 is at
**699fc69be57ac0e89f9bced3fd4f39139ccabf38**; this later source remains
outside the frozen receiving inputs 282e8337e and 56b37c983.

The next inspected incoming **#612** records a conflict between a multi-model
alternate-location fixture and the already accepted stable-ID preflight. Its
reported source is native main ed09f6453 and later PR source 699fc69be; it does
not establish that the safety guard should be removed. The frozen #304 input
keeps its own test inventory and exact gate. This distinct follow-up needs owner
receiving without weakening atomicity or round-trip coverage. PR #543 has since
advanced to **4f1710c5e66f7c9d5e9065fc82a7bd602824e611**, outside both frozen
receiving inputs. This incoming review does not silently expand the fifteen
maintainer-ordered issues.

The next source-preparation checkpoint reads **#613–#616** without expanding the
ordered objective. #613 reports overlapping global configuration contexts leaking
GPU policy; its deterministic consumer reproduction requires owner receiving and
does not establish GPU numerical failure. #614 concerns the Jupyter popup
navigation fixture's real current/selectable Add-ons identity. #615 preserves an
intermittent first-canvas initialization timeout whose cause remains unknown;
a later passing diagnostic does not resolve it. #616 reports native append
rejecting otherwise compatible H5MSM-recovered chemical inventories because
component string storage dtypes differ. The latter needs owner qualification
while retaining rejection of actual chemical differences. None is independently
reproduced or repaired by the #576 assessment controls. The open PR #543 is now
at **b18d5d82366808e8c170295f6fe483ffb58094bc**, outside the frozen receiving
inputs; its later additions and fixes still need owner review and exact-source
evidence. These incoming reports remain explicit release follow-up obligations,
not source qualification supplied by the active #304 matrix.

Other listed issues remain pending in the stated order; #594–#598 already have
source repairs in the separate PR candidate but their closeout belongs at the
end of this goal. Do not implement them again or close them out of order.

PR #543 receiving candidate **282e8337e04c14003622c19a359b7cd35d2b5e4b** stays
frozen on its published branch. Its exact full source gate is
[42171874158](https://github.com/uibcdf/molsysmt/actions/runs/42171874158), with
Viewer 42234de839ed047016f8f241ea5eb717cfeb07be. At the latest verified inspection,
the controlled wheel succeeds and all eight Linux/macOS cells have now failed
at the full-suite step. The
independently inspected Linux Python 3.14 and macOS Python 3.11/3.14 job logs
identify the stale converter-argument table; its
regenerated correction belongs to the ordered-work branch, not the frozen CI
input. No green full matrix or main integration is claimed. Ordered work uses
a separate branch/worktree and the existing development environment. PR #543
had advanced to 1e7a4273b905ca020815658f23ba645d40817226 at the earlier
receiving inspection; its still-later head is recorded above and remains
outside this frozen receiving candidate. Only the explicitly inspected logs
support the stated failure diagnosis; the other final failures are not silently
assigned the same cause.
The ordered branch published 62a5bb62d as an
intermediate source/backup handoff with local tests, source hashes and explicit
partial #304 scope. That checkpoint includes the cap and early PDB-context extensions; the subsequent
policy-boundary receiving is retained separately. The published checkpoint uses
the authorized deferred-CI marker to avoid another incomplete full matrix while
the issue's remaining methods are implemented. This does not clear the skipped
commit backlog, replace the frozen run's failures or qualify a release; finish
the complete work block through an unskipped/manual exact-head gate.

## PR #543 owner receiving and full-suite failures — 2026-11-05

**Owner receiving is in progress, not merged.** The isolated combination of
main `ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6` and submitted PR head
`1c88e785b4327350ad586d437a569eff1a2c5c9a` passes the 4,491-case addon suite,
52 tooling/dependency/documentation-boundary cases, 202 published-support-floor
cases, six additional #583/#584 consumer guards in both source/floor profiles,
and the real Jupyter removal/layout/popups guard. Suites overlap; these are
local source observations. Original main repairs and course executable evidence
are preserved. The duplicate incoming #583/#584 pending reports are reconciled
against their resolved owner records, without reopening them.

Existing PR full run **42153312659** has four failed Linux jobs and queued
macOS jobs at inspection. Linux Python 3.11–3.14 each records the same 33 failing
cases across seven modules; these are real failures, not a pending-only gate.
Owner fixes are tracked separately by **#594** (public export import identity),
**#595** (mmCIF inequality/comparison consumer), **#596** (initial GRO source
context), **#597** (generated-catalogue fixture isolation) and **#598** (test-owned
NGL widget graph cleanup). Current primary occupancy/stable-label contracts
remain strict; stale fidelity expectations are corrected rather than weakening
native validation. Related local selections pass 146 conversion, 72 serial
CCD/conversion and 83 serial NGL cases. The combined local selection passes **4,944 cases**, and 215 directed cases
pass with published support floors. Four edited-reader doctests and 1,077
documentation/reporting cases pass. These selections overlap. No mandatory
full hosted gate is claimed passed.

During receiving the PR advanced to
**`f7b305b3a126109aff5909e857ea7c53981486e8`**, adding independent GUI result
views and changing its controlled Viewer to
**`42234de839ed047016f8f241ea5eb717cfeb07be`**. That fixed delta needs separate
owner review and receiving; preceding measurements do not qualify it. Preserve
other teams' dirty worktrees and use isolated exact source snapshots. The
shared development environment still has optional dependency closure conflicts
under #524 (including Praxis/PyUnitWizard); it is not an installed-pair gate.

Next: complete combined-candidate review and exact required source gates, then
return to **#593**'s distinct course-preparation contract and **#334**.
**#587/#590/#591 remain pending owner integration.** No tag, Release, promotion
or new release matrix is authorized or launched by these source checks.

## Expanded PR owner reproduction — 2026-11-05

The frozen f7b305b3a / Viewer 42234de8 delta now passes **95** directed
System/native/tooling controls, **53** published-support-floor cases and **510**
documentation-boundary cases. Both actual-Jupyter guards pass (**2 cases**,
112.9 s): removal/layout/popups and seven independent-result checks covering
ordered extraction, repeated presentation destination changes, copy, detached
Studio, Python recovery and result lifetime after source closure. Private server
settings are removed and only test-owned browser/server resources are stopped.
The [owner receipt](../devtools/data/owner_pr543_result_views_receiving_20261105.json)
records this separately from contributor claims and the earlier input.
The complete addon selection on the combined new tree passes **4,507 cases**
in 325.7 s (four workers, Pytest Receptor). Final Ruff, formatting, dependency
contract and developer-guide checks also pass.

The obsolete run 42153312659 cannot qualify the candidate: its four completed
Linux jobs fail and its source is superseded. Cancellation of its remaining
queued jobs was requested to avoid redundant CI; this is not a successful gate.
Final combined-source full qualification and main integration remain pending.

## Independent addon result Views — 2026-11-05

**Contributor receiving record:** the following measurements were supplied by
the PR. Owner reproduction of this expanded fixed source is pending; the
preceding owner section identifies its separately received scope.

PR #543 now includes System / Extract subset and Copy system, using Viewer
`42234de839ed047016f8f241ea5eb717cfeb07be` through exact controlled-source pins.
The expert wrappers retain native molecular returns; the GUI prepares an
independent View and explicitly presents it below the notebook or in a window.
Changing destination reuses the same View, including from detached Studio.
Fullscreen delivery is explained rather than falsely described as visible.
Python can recover the result by handle. Native science and source remain
unchanged; leaving an unpresented result releases it.

Receiving on native ed09f6453 passes 128 addon System/mechanics cases and 180
read-tool/native #583/#584 controls, in overlapping scopes. The published Viewer
source passes the seven-step actual-Jupyter result scenario; the existing
six-step removal/popups control remains separately passing. Native offscreen
Qt ownership is separate from postponed human visible Qt qualification. All
157 incoming course notebooks preserve code, outputs and metadata. Current
evidence is in
[the receiving receipt](../devtools/data/molsysviewer_tools_result_views_receiving_20261105.json).
Owner review/integration, hosted exact-head CI and installed qualification remain
pending. Both 1.0 publications remain paused. No native algorithm is authored
by this GUI addition, and no tag, Release or promotion is authorized.

## Course geometric interface observable — 2026-11-05

**#589 is source-corrected.** The Alzheimer capstone uses explicit partner atom
populations and existing extraction/SASA tools to calculate fixed-coordinate
total SASA loss and its separately named half-area convention. The dry union
and isolated partners use identical radii/probe/sampling and Cartesian geometry.
H-bond counts use the same geometry and state a distance criterion rather than
energetic stabilization. Rose/Janin descriptors are distinguished from geometric
measurements in Foundations, Toolbox, Cookbook and course. No runtime API,
algorithm, dependency, unit policy, compiled kernel or schema changes.

Receiving passes **749 related tests**, **22 published-support-floor cases**
and **569 documentation/doctest cases**, including ten new actual-cell guards.
Suites overlap. Independent carbon-sphere, separated/periodic-cell, background
occluder, noncanonical-unit and source-preservation controls bound the science.
The complete seven-cell SASA tutorial executes in **11.2 s**, retaining original
examples. No synthetic output is published under biological project labels.
See the [owning record](archive/resolved_bugs/alzheimer_final_project_uses_a_reference_descriptor_as_a_geometric_interface_are.md)
and [receipt](../devtools/data/course_interface_sasa_receiving_589_20261105.json).

**New #593** owns the capstone's unsupported builder keywords, discarded
independent repair outputs and unqualified complete preparation. The course
labels that route as an outline; closing the surface-observable defect does not
qualify a simulation-ready model, pose or biological effect. Retain this separate
correctness item before claiming complete course execution. Next work returns
to PR **#543** receiving (#587/#590/#591), observed head
`1c88e785b4327350ad586d437a569eff1a2c5c9a`; it is not merged or qualified here.
The checkpoint board refresh found no other new native bug. The prior
#583/#584 head now has five successful routine hosted controls; this remains
separate from nightly, installed/platform and release qualification under #334.
No tag, Release, promotion or new release matrix is launched.

## Mechanical reader flags — 2026-11-05

**#584 is source-corrected.** Sixteen scalar mechanics readers now use the
existing shared Boolean query contract. True reads, False omits, absent settings
return None and stored Boolean settings remain data. Basic reads across MolSys,
MolecularMechanics and MolecularMechanicsDict agree; native MolSys reads reuse
the same value contract. Physical setter/converter branches and #581 constraint
translation retain their meaning. No new defaults, engine execution, signature,
dependency, attribution event or schema is introduced by a read.

Receiving passes **1,193 affected tests**, **313 published-support-floor cases**,
**23 setter/conversion cases** and **569 documentation/doctest cases**, including
152 new public query cases. Suites overlap. See the
[owning record](archive/resolved_bugs/basic_get_constraints_reader_flag_is_rejected.md)
and [receipt](../devtools/data/mechanical_query_flags_receiving_584_20261105.json).
All three edited notebooks preserve executable evidence. The shared private
helper's chemical-state consumers remain covered by the broader run.

The checkpoint board refresh found no new native correctness report ahead of
the existing queue. Continue with **#589**, then PR **#543** receiving (latest
head observed `1c88e785b4327350ad586d437a569eff1a2c5c9a`), including #587/#590/#591.
The PR is not merged or qualified by these native fixes. #582 and #592 remain
separate design/capability proposals. Batch #583/#584 into one unskipped hosted
checkpoint; installed/platform and release evidence remains separate under #334.
No tag, Release, promotion or new release matrix is launched.

## Shared OpenMM scientific attribution — 2026-11-05

**#583 is source-corrected.** Implicit-model construction and OpenMM solvation
with native ion replacement now reuse canonical software metadata for the actual
producer version. Separate captures retain each operation's context, OBC paper
and nested ion-replacement uses without disabling conflict detection. Optional
tracking absence/failure preserves completed science and detached provenance.
No force field, coordinate algorithm, public signature or schema changes.

Receiving passes **1,232 affected tests**, **54 published-support-floor cases**
and **569 documentation/doctest cases**, including six real-engine guards.
Suites overlap. The three edited notebooks preserve all executable evidence.
See the [owning record](archive/resolved_bugs/openmm_metadata_conflicts_between_implicit_models_and_solvation.md)
and [receipt](../devtools/data/openmm_attribution_receiving_583_20261105.json).
Continue with **#584**, then **#589**; PR #543 receiving retains #587/#590/#591.
Hosted controls, installed/platform and release gates remain separate under
#334. This does not qualify the complete preparation/dynamics protocol or launch
a tag, Release, promotion or new release matrix.

## Existing-engine minimization ownership — 2026-11-05

**#588 is source-corrected.** Independent requests involving live OpenMM
Context/Simulation inputs, including explicit output forms/files and composites,
first use the public source-copy contract. Those copies remain unsupported and
now raise before optimization or source-state changes. No snapshot rebuild,
rollback or platform/model fallback is introduced. Native MolSys modes and
explicit engine in-place editing retain their behavior; no new in-place rollback
promise is made. Public signatures/defaults and physical models are unchanged.

Receiving passes **1,847 affected tests**, **318 published-support-floor cases**,
**569 documentation/doctest cases** and the executed seven-cell tutorial. Suites
overlap. Twenty new engine/snapshot cases preserve State/System/Integrator and
same-live-context checkpoint bytes on rejection, prove no optimizer invocation,
cover explicit/file/composite outputs, retain intentional in-place behavior and
clarify partial State snapshots. CPU native controls and actual Reference engine
execution are included; GPU/cross-machine copying is not qualified. Checkpoints
and serialized snapshots are test-only, with no product snapshot cache.

See the [owning record](archive/resolved_bugs/independent_minimization_mutates_an_existing_engine_context_before_copy_failure.md)
and [receipt](../devtools/data/engine_minimization_ownership_receiving_588_20261105.json).
Docstrings, Foundations, Toolbox, Cookbook, five course lessons and three OpenMM
form pages agree with the actual copy boundary. Nine prose-only notebooks retain
all original executable evidence. **#592** owns a future faithful runtime/State
copy contract in the existing adapters; it does not block this safety correction
or claim a new cloning capability.

Continue with **#583/#584**, then **#589**. The checkpoint board refresh also
retains **#590/#591**, real-Jupyter addon outcome/CSS defects assigned to PR #543
receiving, alongside **#587**. No native physics workaround is requested for those
UI boundaries. Hosted runner, installed/platform and release evidence remain
separate under #334. No tag, Release, promotion or new release matrix is launched.

## Course minimization ownership — 2026-11-05

**#562 is source-corrected.** All four Module 43 notebooks and Alzheimer Module
54 retain the independent minimizer result used by subsequent steps. Unsupported
tolerance keywords are removed. The optimizer runtime, public signature and
engine defaults are unchanged; native independent/in-place ownership and units
are documented consistently. Scientific prose now distinguishes local L-BFGS
optimization from equilibrium, a nearest/global minimum or binding stability.

The recovered, collected minimizer test includes four real CPU/Reference native
mode controls and five tests executing the actual course call statements on a
bounded model. Forgotten/unused results cannot satisfy genuine coordinate-change
and energy-decrease assertions. Receiving passes **259 mechanics/digester tests**,
**29 published-support-floor cases**, **569 documentation/doctest cases**, the
focused ten-case run and the executed five-cell Toolbox tutorial. Suites overlap.
Full network/ligand/membrane preparations remain unqualified; no course outputs
are fabricated for sources that previously had none.

See the [owning record](archive/resolved_bugs/course_minimization_discards_independent_results.md)
and [receipt](../devtools/data/course_minimization_receiving_562_20261105.json).
Foundations, Toolbox, Cookbook and course are aligned; Cookbook executable
payloads and original course execution payloads are preserved.

**New native defect #588:** existing Context/Simulation default independent
requests minimize the source before failing on their unsupported copy route.
Both forms are reproduced; explicit engine in-place operation succeeds. This is
not fixed or waived by the native course correction. **#589** separately tracks
the final project's reference-descriptor/interface-area misuse. Continue with
#588 and #583/#584, then the remaining course observable and PR #543 receiving;
#587 remains the separate board-pagination report. No new scientific capability,
dependency floor, compiled code or schema is introduced. Publish an unskipped
checkpoint and inspect its controls; installed/platform and release gates remain
separate under #334, without tags or publication here.

## Nonbonded partition shape and source ownership — 2026-11-05

**#561 is source-corrected.** Flat/flat atom sets yield a scalar; partitioned
inputs yield ordered rows from selection and columns from selection_2, including
singleton axes. Typed empty entries, repeated partitions and overlaps within
one axis are supported. Across-axis overlap and ambiguous partitioned internal
requests receive explicit native diagnostics. The optimized evaluator is
retained; its inverse map records every membership.

A temporary engine System uses the existing public copy route and preserves
source parameters, force groups and coordinates. Current context box vectors
are retained. Standard nonbonded forces are isolated from other force groups;
missing/multiple standard forces are rejected. The SMonitor catalog now shows
conflict reasons and the unsupported method, using existing codes/classes.
Public signatures/defaults, unit policy and dependency floors remain unchanged.

Receiving: **1,818 affected tests**, **326 published-support-floor cases**,
**569 documentation/doctest controls**, the final function doctest and the
executed eight-cell tutorial. The 36-case function module includes scalar-cell
parity, nesting/order, repeats, empty/invalid sets, unit policy, source ownership
and a bounded current-cell cutoff control. This does not qualify arbitrary
periodic/custom models or turn interaction energy into binding free energy.

See the [owning record](archive/resolved_bugs/nonbonded_mixed_partitions_overwrite_first_selection.md)
and [receipt](../devtools/data/nonbonded_partitions_receiving_561_20261105.json).
Foundations, Toolbox, Cookbook and both relevant course modules are aligned;
three prose-only notebooks retain original executable evidence. The tutorial's
protein matrix is bounded to selected groups, with full lists an explicit
larger request. An order-sensitive test previously confused lazy unit-library
loading with policy mutation; it now checks policy and actual units separately.

Next: **#562**, then incoming **#583/#584** and PR #543 expansion receiving.
The board refresh also receives **#587**, a board-reconciliation pagination
defect; offline devguide checks here do not claim complete board agreement.
Publish an unskipped source checkpoint and inspect its own controls; hosted
runner execution, installed/platform artifacts and release qualification remain
separate under #334. No tag, Release, promotion or release matrix is launched.

## Engine-owned execution platform selection — 2026-11-05

**#559 is source-corrected.** General mechanics validation accepts a nonempty
platform name without an engine whitelist. The OpenMM adapter resolves exact
registered names and installed plugins through a shared Context/Simulation
selector. Invalid names, known absent registrations, missing engines and device
initialization failures remain distinct; failed requests do not change platform.
Existing engine contexts retain their actual platform. Public signatures and
defaults, physical models and quantity result formats are unchanged.

Receiving passes **1,784 affected tests**, **293 published-support-floor cases**
and **570 documentation/governance/doctest cases**, plus the executed four-cell
platform tutorial. Twenty focused controls cover actual Reference construction,
CPU/Reference energy/unit parity for vacuum and both OBC variants, metadata and
failure categories, source preservation and existing-context identity. GPU
hardware is not qualified. The largest observed small-fixture energy difference
is 0.000030386 kJ/mol. Full Ruff check/format and native dependency/doc guards pass.

See the [owning record](archive/resolved_bugs/mechanical_platform_validation_rejects_reference_and_opencl.md)
and [receipt](../devtools/data/platform_receiving_559_20261105.json).
Five other edited notebooks retain original executable cells, outputs and
metadata. No new runtime dependency/floor, scientific method/credit, compiled
kernel or H5MSM schema. Next: **#561**, **#562**, then PR #543 expansion
receiving. #582 retains the broader engine-neutral effective-recipe proposal.
The board refresh also identifies native defects #583 (conflicting OpenMM
attribution metadata) and #584 (Boolean constraints reader), plus separate
interoperability study proposals #585/#586. They are not covered by #559.
Publish an unskipped checkpoint and inspect its own hosted controls; missing
runner execution remains pending under #334. Installed/platform and release
qualification remain separately required; no tag or release is created here.

## Explicit implicit-solvent variants and physical policies — 2026-11-05

**#580 and #581 are source-corrected.** Mechanics keeps physical model names
independent of the engine. OBC1 and OBC2 now select their actual standard model
XMLs in the OpenMM adapter for the seven existing AMBER fields. Native mechanics
stores solute/solvent settings, not engine classes or resources. Shared conversion
uses explicit keywords, then supported stored settings, then defaults, and
validates newly read source values. Default HBonds remains; requested none,
all-bond and hydrogen-angle policies are now translated faithfully.

The actual unconstrained OBC1 conversion passes the pinned upstream 22-atom
force reference at its original tolerance (max error 0.024869 kJ/mol/nm).
Both variants agree with direct engine recipes and differ numerically from
each other. No new independent Amber run or general physical-accuracy claim
is made. Optional Ackredit records the scientific method, actual engine/version
and contextual model/resources after successful construction only.

Receiving passes **1,817 affected tests**, **234 published-support-floor cases**
and **570 documentation/governance/doctest cases**, plus the executed ten-cell
tutorial. User Guide, native mechanics, course and docstrings are aligned;
Cookbook/course code and outputs are preserved. See the
[#580 record](archive/resolved_bugs/amber14_obc1_conversion_omits_implicit_solvent_force.md),
[#581 record](archive/resolved_bugs/openmm_system_conversion_ignores_the_requested_constraint_policy.md)
and [receipt](../devtools/data/implicit_solvent_receiving_580_581_20261105.json).

Broader effective-recipe/capability reporting and unsupported stored tuning
are tracked separately in [#582](pending_proposals/expose_effective_engine_neutral_mechanics_recipes_and_unsupported_stored_control.md).
No public OpenMM-shaped mechanics API or new backend placeholder is introduced.
No dependency floor, compiled kernel or H5MSM schema changes. Next native reports
remain **#559**, **#561**, **#562**, then PR #543 expansion receiving; the new
proposal has no automatic release deferral or additional initial-1.0 gate.
Publish an unskipped checkpoint and inspect its own hosted controls; missing
runner execution remains pending under #334. Local results do not replace
installed/platform or exact release qualification. No tag or release is created.

## Force-field resource ownership — 2026-11-05

**#560 is source-corrected.** `get_engine_forcefield()` returns an independent
ordered list of XML/leaprc names on every valid call. Caller edits cannot mutate
the registry, other results or later parameterizations. All 71 registry entries,
resource ordering and implicit-solvent precedence are retained. The existing
public signature is unchanged; ArgDigest and SMonitor now cover the public
metadata boundary. Engine installation and actual physical configuration remain
separate from metadata lookup.

Receiving passes **984 affected tests**, **169 published-support-floor cases**
and **569 documentation/governance/doctest controls**, plus the executed
seven-cell tutorial. The real OpenMM control preserves particle/constraint and
per-force payloads after caller-local edits. See the
[owning record](archive/resolved_bugs/forcefield_resource_results_alias_registry_lists.md)
and [receipt](../devtools/data/forcefield_resources_receiving_560_20261105.json).
The Cookbook and Module 20 retain original executable cells and outputs.
No resource definitions, dependency floors, compiled kernels or H5MSM schema change.

The scientific review found **#580**: AMBER14/OBC1 conversion accepts the label
but creates no implicit-solvent force. Its
[record](archive/resolved_bugs/amber14_obc1_conversion_omits_implicit_solvent_force.md)
keeps the physical evidence separate from metadata ownership and makes no
unmeasured energy claim. Review this silent model mismatch next, before the
remaining **#559**, **#561** and **#562** native mechanics reports and final
PR #543 expansion receiving. #572/#576 remain separate capability work.

#578 is already closed and published in `ea4086c7297a7ecf1757648ebd3c5bd44e440c7f`;
its five routine checks were still queued when inspected through GH Run Receptor.
Publish this block without a skip marker and inspect its own hosted checks;
missing execution remains pending under #334. Local source evidence does not
replace installed/platform or release qualification. No new tag, Release,
promotion or release matrix is launched.

## Empty visualization input contract — 2026-11-05

**#578 is source-corrected.** Ordinary `msm.view()` and explicit None create an
empty Python workspace with either registered backend. Only this exact public
caller gains the None exception. Shared axis validation rejects expressions or
nonempty indices without a source before construction; all/None/flat empty axes
are admitted. No zero-atom MolSys is synthesized. Loaded inputs retain their
existing extraction/backend requirements, including rejection of unsupported
empty loaded selections rather than replacing their source with None.

The MolSysViewer adapter gains its explicit DepDigest guard; invalid viewer types
retain native diagnostics. Backend selection, static-HTML behavior and the
public signature remain unchanged. The corrected Foundations matrix lists only
the two actual dispatch routes; explicit viewer=None reads configuration, while
omitting viewer retains its MolSysViewer default.

Receiving passes **273 affected tests**, **66 published-support-floor cases**
and **569 documentation/governance/doctest cases**. Real empty widgets are closed
after inspection; no browser rendering or session evidence is claimed. Three
edited notebooks retain all original executable cells, outputs and metadata.
See the [owning record](archive/resolved_bugs/basic_view_rejects_default_empty_input.md)
and [receipt](../devtools/data/empty_view_receiving_578_20261105.json). No new
dependency floor, scientific method/credit, compiled kernel or file-format schema.

Queue review observes no newer issue than the now-resolved #579, with PR #543
still at `94548b434f5d673f6fcfc6c97db9d83601a5b4b7`. Next: **#560** (mutable
force-field registry results), then **#559**, **#561** and **#562**, before final
expansion receiving. #572/#576 remain separate capability work. Finish this
block with an unskipped published head and inspect its own hosted controls;
missing hosted evidence remains pending under #334 until runners execute.
Installed/platform and release qualification remain separately required.

## Solvation identifier preservation — 2026-11-05

**#574 and #579 are source-corrected.** OpenMM solvation no longer interprets
source atom/group labels as integer indices. Native output preserves retained
labels, duplicates and missing values, and allocates labels only for generated
sites. Existing native ion maps handle removal of original waters; source counts
are retained in their solvation context. Finalization uses native tools before
the requested output conversion. Noncanonical provider traversal fails before
construction rather than producing an ambiguous positional correspondence.

The related **#579** fix belongs to the shared `get()` normalizer: pandas.NA,
numeric NaN and None remain missing, while actual '<NA>', 'None', 'nan' and empty
string labels remain literal. Universal and native queries reuse that boundary;
solvation uses public get/set without a second missing-ID interpreter.

Receiving passes **3,273 affected tests**, **167 published-support-floor tests**
and **585 documentation/governance/doctest controls**. The five edited lessons
retain every original executable cell, output and notebook metadata. See the
[#574 record](archive/resolved_bugs/openmm_solvate_rejects_nonnumeric_atom_ids.md),
[#579 record](archive/resolved_bugs/get_stringifies_nullable_ids.md) and
[shared receipt](../devtools/data/source_identifier_receiving_574_579_20261105.json)
for commands, source hashes, corrected draft assumptions and boundaries.
No public signature, dependency floor, compiled kernel, H5MSM schema or new
scientific credit changes. This is source evidence, not release qualification.

Queue review observes PR #543 at
`94548b434f5d673f6fcfc6c97db9d83601a5b4b7`. Next is **#578** (empty-view
default), followed by remaining native correctness issues #559–#562 and expansion
receiving; #572/#576 remain capability work. The preceding source checkpoint's
hosted controls were queued at the last inspection. Finish this work block with
an unskipped published head and inspect its own controls; missing routine hosted
evidence remains pending under #334 until runners execute, with installed and
release gates separately required. No extra release matrix or promotion is
launched by this metadata correction.

## Native ion replacement and explicit solvation counts — 2026-11-05

**#575 is source-corrected.** New experimental `build.add_ions` replaces complete
waters with one of nine monovalent species, using existing sparse Rust-backed
periodic neighbor queries. Counts, charge-dependent neutralization and additional
salt pairs have separate documented semantics. PCG64 seeds, bounded failure,
producer versions, attribution and composable source/output atom maps are retained
in ChemicalStates preparation history and H5MSM 0.5. No new dependency, compiled
kernel or file-format revision was needed. This prepares geometry, without
equilibration or invented force-field parameters.

OpenMM explicit counts and seeded requests construct water first, then delegate
to the native operation; mixed neutralization uses the original force-field
charge. Unseeded defaults keep OpenMM's ordinary provider route. Native solvation
delegates placement while explicitly retaining its legacy pH-7 source-charge
approximation. PDBFixer rejects explicit counts or a seed before construction;
its ordinary default route remains supported and tested. See the
[owning record](archive/resolved_bugs/openmm_solvate_ignores_explicit_ion_counts.md)
for the precise bounds and corrected findings.

Receiving passes **212 affected tests**, **77 published-floor tests**, **156
native-owner tests**, **601 documentation/governance tests** and **2 doctests**.
The new tutorial's five code cells and the added course/cookbook examples execute.
Finite analytical charge and lattice-image controls support a deliberately
**partial** scientific-evidence declaration, not an equilibrium or optimal-packing
claim. The [receipt](../devtools/data/ion_replacement_receiving_575_20261105.json)
retains exact commands, source hashes, failed drafts and limits.

The prior main smoke **42118274443 passes**. The new source delivery still needs
routine hosted inspection; none of this replaces exact-candidate installed,
platform or release qualification. Queue review observes new **#578** (empty-view
default) and PR #543 at `c0149a2d6147380046768b9211cf11b7b63ebeda`. Continue with
**#574** (OpenMM labels), then #578 and expansion receiving; #576/#572 remain
explicit capability work. No tag, Release or package promotion is authorized here.

## Water-box geometry receiving — 2026-11-05

**#564 is source-corrected.** `build.make_water_box` uses the row-vector
fractional transform and both half-open bounds, preserving complete O-H-H
reference waters. The reported cell now contains **207 waters, zero oxygen sites
outside**, rather than 266/111. The orthogonal control retains 268 waters. An
independent scalar enumeration verifies complete reference-lattice membership;
checking output bounds alone would not detect missing valid candidates.

The factory reuses shared PBC validation before reference loading and honors its
existing output `form` through public conversion. Native storage remains nm
under nondefault presentation policies. Empty populations have explicit shapes;
no charges, force field, exact density or equilibration are inferred. The
[archived record](archive/resolved_bugs/water_box_clips_triclinic_cells_in_the_wrong_fractional_coordinates.md)
and [receipt](../devtools/data/water_box_receiving_564_20261105.json) retain the
failed fixture drafts, baseline, analytical controls, source identities and limits.

Receiving passes **773 affected cases**, **23 published-floor cases**, **586
documentation/owner-invalidation cases** and the native doctest. The complete
eight-code-cell tutorial executes in 7.4 s; three other edited notebooks preserve
all code, outputs and metadata. The touched Structures page also removes a stale
sentence contradicting the implemented #285 public-setter notification boundary.
No signature, dependency floor, file schema or compiled kernel changes.

Queue review observes no newer open issue than #576 and PR #543 head
ac1f6dbad9ce3b29751dfd0a33e5df596e5dbae0. The prior main smoke 42114952994
is in progress, not yet passing evidence. Next: **#575** explicit OpenMM ion-count
semantics, then **#574** atom/group labels; #576 and #572 remain capability work.
The new native source checkpoint still needs its own routine hosted inspection;
installed/platform/release qualification and expansion admission stay separate.

## Mutation selection receiving — 2026-11-05

**#568 is source-corrected.** Mutation selectors now resolve on source
atoms before either engine; all mutation specifications intersect the enabled
groups. Literal IDs, duplicate-target checks and independent no-op copies share
one resolver. Native heavy repair stays within target groups; legacy whole-system
hydrogen completion and PDBFixer repair remain explicit. Optional-provider ID
ambiguity is rejected before mutation. This does not expand coordinate-placement
coverage or admit the expert addon expansion.

Final mutation receiving passes **100 tests**, including the all-target H
completion correction; published support floors pass **73 controls**. The earlier
expanded selection passes 493 cases, documentation/API-registry receiving passes
593, and the native doctest passes. The nine-code-cell tutorial executes in 12.3 s. Four actual course
mutation blocks execute against local systems; complete network-backed lessons
are not claimed. The broader selection passes **1,478 tests** before the final H-policy
correction; the unchanged-path reuse and final focused receiving are explicit. The
[receiving receipt](../devtools/data/mutation_selection_receiving_568_577_20261105.json)
retains commands, failures, source hashes and scope. The
[#568 record](archive/resolved_bugs/mutate_selection_masks_mix_syntax_and_atom_group_axes.md)
and [#577 record](archive/resolved_bugs/live_build_tests_access_pdb_downloads_during_offline_selection.md)
are archived with their executable guards.

The first broader run has 1,475 passes, two failures and seven setup errors.
Eight cases are unmarked live downloads, now separately owned by #577 with an
exact real-pytest selection guard. The other is a stale reinsertion expectation:
restored CIF occupancy is correctly reported as dropped when H are appended.
The strengthened assertion checks source occupancy and output policy explicitly.

Prior smoke 42095546341 on ccff2557f failed before tests because the intentional
#504 signature extension was undeclared. Its narrow declaration is now recorded
with #568's keyword-only skip flag. Historical failure remains visible; the
validator is unchanged. Hosted/installed qualification is separate from local
source receiving.

The board review observes PR #543 at b285d7fb8a4bcf2fb852c8ce3899d7158063a202.
Incoming #574 (solvation ID labels) and #575 (ignored explicit OpenMM ion counts)
are reported native defects awaiting triage; #576 requests public protonation
removal correspondence for managed consumers. Next: #564's triclinic water-box
correction; triage #575/#574 before expanding
preparation capabilities. #576, #572 and the naming #549 receiving remain owned
work, without inventing another initial-1.0 detector requirement.

## Per-structure solvation predicate — 2026-11-05

**#504 is source-corrected.** `build.is_solvated` now accepts keyword-only
`structure_indices='all'`, retaining source order/repetitions. It preserves Python
bool for one selected structure and returns a Boolean vector for multiple/empty
selections, with no implicit ensemble aggregation. The existing addon mirror and
its help delegate the same contract. Native inputs need only inventory and box
metadata; foreign-file loading retains its existing adapter costs.

The criterion remains global water density above 15 waters/nm³. Independent unit
controls exposed a floating-point equality difference between nm and angstrom/pm
representations; the explicit eight-epsilon relative equality tolerance fixes
that numerical boundary without a physical density margin. Absent waters/box
produce false per selected structure; unknown inventory and unusable volumes
have native diagnostics. This is not a solvent-completeness/equilibration claim.

Receiving passes **796 affected tests**, **41 published-floor native cases**,
**544 documentation controls** and the native doctest. The full tutorial executes
13 code cells; the existing course/Cookbook executable content is preserved. The
[#504 archived record](archive/resolved_bugs/is_solvated_fails_for_multiple_structures.md)
and [receipt](../devtools/data/solvation_predicate_receiving_504_20261105.json)
retain failures, corrected test assumptions, source identities and scope. No
compiled kernel or dependency floor changes. Hosted and installed/release
qualification remain separate.

The checkpoint review finds no newer open issue than #572 and observes expansion
PR #543 at 10ef88c907aa6a1bef83c76efee7f1beffbddcdf. That observation is not its
admission or acknowledgement of the native naming handoff. The next independent
corrections are #568 mutation selection/syntax, then #564 triclinic water boxes;
#549 D6/D7 continues when the expansion owner is ready.

## CIF observations and assembly receiving — 2026-11-05

**#556 and #563 are source-corrected.** CIF/BinaryCIF and compressed imports
retain primary occupancy, explicit missing values and model-local alternate
observations. Source coordinates, B factors and model indices follow the same
canonical atom map. Explicit per-group chemistry remains separate between models.
Both direct occupancy and B-factor getters honor ordered/repeated structure
indices. Native sorted conversion extraction and direct-query atom order remain
distinct documented contracts. The
[#556 record](archive/resolved_bugs/cif_conversion_drops_primary_occupancy.md)
retains the independent literal controls and limits.

PR #566 is owner-reviewed and merged as fcf76b755, preserving its exact
3635c90ac contributor head and history. Its full required source run 41952069798
passes all eight Linux/macOS × Python 3.11–3.14 lanes. Repeated assembly rows now
retain every operation in source order and preserve individual chain scopes;
heterogeneous construction remains explicitly unsupported. The
[#563 record](archive/resolved_bugs/mmcif_assembly_generator_rows_overwrite.md)
distinguishes that source matrix from later combined-main receiving.

Broader affected receiving passes **5,376 tests**. Following the final B-factor
forwarding correction, **2,481 current-source tests**, **34 published-floor
cases**, **551 documentation controls** and **two doctest items** pass. The
Cookbook occupancy block executes; seven notebook executable payloads, outputs
and metadata are unchanged. The shared
[receiving receipt](../devtools/data/mmcif_observations_receiving_556_563_20261105.json)
records exact hashes, failures, selection and reuse boundaries; these overlapping
runs are not added together or presented as a full installed/release matrix.

The broad initial attempt is retained as interrupted (exit 2), with five
name-resolution/download failures in eight unmarked live PDB-ID conversion tests.
#573 fixes that classification in 522d58067; offline selection now excludes all
eight while network collection retains them. #565's assembly-specific marker
correction is received through #566. Existing online assertions remain unchanged;
local collection is not live-provider execution.

The prior main 532d0362 smoke (42082100392) is now successful, independently of
this new reader checkpoint. The periodic board review observes PR #543 head
04b9fbbda4654516c01d6c34e9c19ad17c1be0fb and the new #572 force-input proposal.
The naming handoff still awaits coordinated #543 receiving; the force proposal
belongs with the mechanics contract review, without inventing an initial-1.0 gate.

## Incoming alternate-site corrections — 2026-11-05

The checkpoint review of recent open issues identifies three new related
correctness reports, #569/#570/#571. Their native repair now selects the actual
maximum, preserves chosen primary occupancy/B-factor coherence and preflights
the whole selected request before writing. Invalid later sites preserve source
geometry, IDs, optional observations and analysis identities. Sparse planning
keeps the normal mutable-backend failure limit explicit. Native optional-field
setters also reuse proper ArgDigest value validation and avoid materializing
coordinates when creating observation storage.

Local receiving passes **4,639 affected tests**, **50 published-floor cases**,
**533 documentation controls** and the resolver doctest without omissions. The
tutorial executes eight cells; course/Cookbook executable content is preserved.
The [#571 owning record](archive/resolved_bugs/invalid_alternate_location_requests_partially_modify_earlier_structures.md)
retains the shared receiving and links the specific #569/#570 guards. These are
source corrections; hosted and installed/release evidence retain separate scope.

The previous naming source d3650cc09735ccfc7bf02d35ca4e0a746f83f96f now passes
all seven applicable routine push workflows: smoke 42074491673, dependency
42074491697, data 42074491651, Ruff 42074491781, devguide 42074491689,
suite policy 42074492404 and publication governance 42074492306. GH Run
Receptor's public 1.3.0 payload reports terminal smoke success. This is not the
full source/platform matrix or admission of PR #543. The #549 handoff is
published in that PR; the follow-up review observes head 04b9fbbda4654516c01d6c34e9c19ad17c1be0fb,
pending coordinated adaptation and receiving.

### Revised bounded work order

Revisit incoming issues/PRs at meaningful phase checkpoints, as requested by
the maintainer; keep the active work and its handoffs visible. The review of the
latest fifty updated open reports preserves this route after #569–#571:

1. Receive #543's naming mirrors and complete #549 D6/D7 when its owner is ready;
   independent native bug fixes continue meanwhile.
2. Continue #568's mutation selection/syntax, then #564's triclinic water-box
   correctness. #504 is received in the solvation-predicate checkpoint above.
3. Receive #559–#562 engine/platform/registry/partition/doc failures. Review the
   new #572 native-force input proposal with the same mechanics contracts;
   decide environment, selection and units before implementing that route.
4. Keep #567's comparable performance and third-party gate semantics owned
   before using those measurements as qualification. Network classification
   #565/#573 is corrected in the reader checkpoint above.
5. Keep #557's public CCD template proposal, #558 generation evidence and older
   explicit scientific studies in their owned queues; they are not silently
   promoted to initial-1.0 gates by the incoming review.

No new detector, release tag or installed artifact is admitted by this triage.

## Group-name public cutover — 2026-11-05

**Native D6 delivered locally under #549; expansion receiving remains open.**
The sole scalar code entry is now `element.group.get_1_letter_code_from_name`.
The former amino-acid implementation/export is removed; historical values use
explicit legacy context. User/API migration routes remain available, the
canonical tutorial preserves the original alphabet example, and exact group
stability/tier inventories retain Experimental status. Existing addon conversion
and preflight signatures now mirror native from_naming_scheme without source,
scene or scientific reinterpretation in the wrapper.

Local receiving passes **9,062 native tests**, **2,699 addon/integration
controls**, **270 published-floor cases**, **548 documentation controls** and
**three doctest items**, without omissions. The tutorial executes ten cells;
course executable content is unchanged. The
[owning record](pending_bugs/reconcile_legacy_amino_acid_name_mappings_with_native_protonation_labels.md#d6-native-public-cutover-and-addon-receiving--2026-11-05)
retains failures/corrections, source hashes and PR #543's required wrapper,
signature, discovery and manifest handoff. This checkpoint does not admit that
expansion or complete D7/installed-release qualification; #549 stays active.

## Group-name fidelity receiving — 2026-11-05

**D5 complete locally under #549.** Conversion/preflight now reports selected
stored or prospective naming declarations that a target cannot retain. The
public preflight accepts `from_naming_scheme`; strict mode refuses detected loss
before target writes. Unknown context remains unknown on foreign rereading.

Named-analysis omission and selected evaluated-coverage invalidation from a newly
added declaration are explicit losses, including evaluated-empty structures.
Matching declarations and irrelevant coverage remain unchanged. Partial-system
preflight inspects only available domains. Native/dictionary/H5MSM round trips,
reordering, independent snapshots, state maps and named observations are covered.

Final local receiving passes **4,651 tests**, **236 provider-floor cases**,
**514 documentation controls** and **three doctest items**. The small tutorial
executes nine cells; larger tutorial/course executable payloads stay unchanged.
The owning record distinguishes failed fixtures, real missing-domain bugs and
final runtime evidence. D6 old scalar/addon cutover and D7 final acceptance remain
open; no installed artifact or release is qualified by these local checks.

## Group-name producer receiving — 2026-11-05

**D4 complete locally within #549's bounded scope.** Peptide construction now
reads exact source labels/context, checks explicit overrides and declares its
known Amber output vocabulary before native transport. The shared reference layer
recognizes checked historical and construction H layouts. Native H addition no
longer duplicates HID beta hydrogens or Amber ACE methyl hydrogens merely because
reference names differ; group declarations do not force atom naming.
Coverage retains candidate ambiguity and records each candidate's actual source.

Local receiving passes **3,000 affected tests**, **221 provider-floor cases**,
two additional input/preflight guards, 514 documentation controls and three
doctest items. The final cap-attribution follow-up passes 62 producer/resource
tests with current providers and the same 62 with published floors. Two revised
tutorials execute 18 cells; course executable payload is retained. The owning
record keeps failed-process evidence, corrected test premises and scientific
limits. D5 fidelity, D6 old scalar/addon cutover and D7 final acceptance remain
open. No installed artifact or release qualification is implied.

## Group-name scheme design accepted — 2026-11-04

**Local D4 chemical-reference receiving:** Atom/H expectations, bounded native
preparation, chemical coverage and reference-bond candidates now consume stored
group conventions without substituting sequence parents. The eight reviewed
Amber states use only raw catalogue variants matching bundled reference heavy
connectivity and H inventories. Named-state terminal completion, unavailable
placement layouts and external naming adapters remain unassessed or explicitly
unsupported. Raw readers preserve undeclared contextual labels/source edges and
omit automatic inference for those groups. Exact bond-pair parity with PyTraj is
retained after declaring the fixture's Amber context.

Final local receiving passes **2,945 affected tests**, **333 tests with published
support-library floors**, **514 documentation controls** and **four doctest
items**. Ten tutorials execute all 57 code cells. The owning #549 record retains
initial failures, negative controls, reference provenance and remaining limits.
Broader producer audit, D5 fidelity, D6 old-path/addon cutover and D7 final receiving
remain open; this block does not qualify an installed artifact or release.

**Local D4 reference-name and recognition receiving:** Parent reporting,
amino-acid recognition, per-group type inference and native non-standard-group
reports now share the bounded naming resolver. Raw readers preserve ambiguous
labels as unknown; scalar queries require context. Inference preserves stable
molecule membership and copies no topology for an all-group query. Nullable
initial group labels/types preserve missingness instead of creating literal
`"nan"` strings. Published-provider floor receiving passes 419 cases; five revised
tutorials execute. Final current-provider receiving passes 7,460 tests; 514
documentation controls and three doctest items pass. The wider run's 19 missing-type
failures are corrected and revalidated, with their failed evidence retained.
Exact chemical preparation, conversion fidelity and the old scalar
one-letter/addon cutover remain open under #549. Detailed receiving,
negative controls and remaining boundaries belong to the owning record.

**Local D4 sequence-consumer receiving:** Identity and direct three-to-one-letter
conversion share the native naming authority, retaining stored conventions and
original group positions. Native queries copy no domains; all/index dictionary
and H5MSM identity reads use topology only. Alignment/identity have selected-engine
Biopython guards and completed-work attribution. The new support-library probes
find ArgDigest's already resolved #17 in the old minimum: `argdigest>=0.14.0` is
now the justified public floor, verified as a public main-label archive and aligned
across maintained routes under #524. No host bypass fork is introduced.

The four published-provider probe passes 363 cases and normal development
receiving passes 384, with current pytest diagnostics kept enabled. The owning
record retains the old-minimum failure, the separate harness limitation and
the remaining recognition/preparation, fidelity and cutover work.

Extended receiving passes 5,221 cases; 521 documentation/command controls and
four doctest items pass. The small naming tutorial executes eight code cells.
Warnings, intentional offline selection and retained failing controls are recorded
under #549. No installed-package or release qualification follows from these
local checks.

The unchanged shared environment separately fails `pip check` on optional
AmberTools-related extras (pdb2pqr absence and older NumPy/Biopython constraints).
#524 records this remaining environment-closure limitation; the naming work
neither repairs those packages nor qualifies the whole installed workspace.

**Local D4 source-keyword receiving:** `convert` and native one-letter adapters
now accept keyword-only `from_naming_scheme`. Known selected declarations must
agree; native queries leave the source untouched and copy no molecular domain.
Native molecular outputs retain added context independently, with coordinated
interaction invalidation. Selection maps, dictionary/H5MSM transport, FASTA
record boundaries and one-letter text envelopes are covered. The owning record
separates this delivery from remaining recognition/preparation/alignment work,
the D5 fidelity audit and D6 old-path/addon cutover. No push or hosted gate is
claimed for this local block.

Final receiving passes 344 focal cases with public ArgDigest 0.13.0 and Ackredit
0.9.0, including 87 new source-keyword cases. Supporting default-route receiving
passes 2,396 cases; documentation controls pass 513 and all four doctest items
pass. The updated small tutorial executes successfully. The owning record
retains original failures, their corrections, warning counts and exact scope;
these results do not qualify an installed package or complete platform matrix.

**Local D3 and initial D4 receiving:** The scheme-aware group-level letter
helper and private resolver are implemented. The maintainer admits `sequence`
after primary CCD inspection confirms additional XAA/XLE collisions. Its appended
code preserves old three-profile wire meaning. Explicit peptide templates now
declare Amber, canonical sequence construction declares its alphabet, and native
sequence projection uses group context across native/dictionary/H5MSM routes.
Names, bonds and absent coordinates are retained. The final floor selection
passes 229 cases; a separate sequence/FASTA/template selection passes 341.
Independent 229-case receiving also passes with public Ackredit 0.9.0 and
ArgDigest 0.13.0 in the existing development environment; it does not qualify
an installed MolSysMT artifact or its complete dependency closure.
The owning record retains the extended run's one obsolete schema assertion and
the successful targeted correction, plus documentation/attribution evidence.

D0–D3 are complete locally. D4's source keyword is received in the next local
block below; its remaining consumer audit and D6's coordinated old-path/addon
retirement are next. The old standalone
amino-acid parent helper is not fixed by the new entry point. No push, remote CI,
installed package, tag or complete issue qualification is claimed here.

**Local D2 receiving:** Native group-aligned naming declarations and versioned
transport are now implemented and contract-tested. TopologyDict 0.3 carries the
registry/codes; H5MSM root 0.5 uses topology layer 4. Known/unknown mixed groups,
copies, selection, addition, builder growth and staged interaction invalidation
are covered. The extended receiving run passes 2,602 cases; final boundary/floor
receiving passes 138 cases with public ArgDigest 0.13.0, including seventy new
naming guards. The owning record distinguishes finality and warnings. Changes
remain local pending a meaningful combined publication checkpoint.

D0–D2 were complete at that checkpoint; D3 is received locally above.
The original GLH/HID/HIE interpretation/conversion bug remains open. This storage
block is not scientific profile validation, hosted CI or package qualification.

The maintainer accepts #549's explicit source-scheme design and requests a public
comparison of supported schemes and their differences. The
[owning plan](pending_bugs/reconcile_legacy_amino_acid_name_mappings_with_native_protonation_labels.md#accepted-design--2026-11-04)
records group-aligned Topology ownership, default ambiguity refusal, source
argument spelling, helper relocation and native/H5MSM/dictionary preservation.
The conceptual User Guide page distinguishes the delivered scheme-aware helper
and native sequence routes from the remaining legacy consumers.

The source study confirms real CCD/Amber collisions and native template sequence
failures. The earlier documentation-only checkpoint changed no runtime table,
public signature or file schema. D0/D1 were complete; D2's typed storage/schema contract
is received locally above. This accepted correction precedes #504 and #543 receiving.

The six applicable routine workflows for source 5f3af9374 all pass, including
[CI smoke 41878036717](https://github.com/uibcdf/molsysmt/actions/runs/41878036717).
This completes #554's pending hosted checkpoint, not full-matrix or installed
qualification. The earlier #548 smoke 41874330460 also passes; no failed producer
is relabelled or new package published.

## Native reference-map validation — 2026-11-04

[#554](archive/resolved_bugs/reference_bond_index_maps_are_not_consistently_validated.md)
adds a scoped ArgDigest registry at all seven reference-bond entry points.
Malformed values/lengths fail before reference reads with SMonitor argument,
caller and expected/actual fields. Maps are flat unit-free/unmasked nonnegative
int64-range integers; repeated indices remain allowed. Scalar compatibility,
all seven public signatures and three executed notebook payloads are preserved.
Generic molecular selection digesters, chemical reference data and optional
dependency declarations are unchanged.

The final group suite passes 627 cases, including 186 new guards, with the exact
verified public ArgDigest 0.13.0 py_1 payload and no omissions. Supporting runs
pass 659 argument/build/native-query cases, 197 CIF/guard cases and 572
documentation/doctest cases. The owner record distinguishes their finality,
warnings, original 28-case failing control and corrected ATP test expectation.
All 246 docstrings, notebook/signature checks, fast gates and Ruff are included
in final local receiving. This is source receiving, not an installed-package or
full platform qualification. Hosted routine CI follows publication separately.

Next: #549's legacy name/protonation-context study, then #504's multi-structure
contract and PR #543 receiving. The new validation does not select a chemical
state or add an addon coercion; unchanged signatures permit current wrappers to
delegate the new native diagnostics without a calling-convention change.

## Audit recorded and reference-help correction received — 2026-11-04

The maintainer-requested audit and resumption route are recorded in
e62557952, with the original scientific certificate retained unchanged. This
documentation checkpoint does not select a release candidate or qualify new
runtime behavior.

Source correction 1f462976d is integrated and published on main; #548 is closed
with its guard and archive record. The new
[#555 assessment request](pending_proposals/read_only_geometry_and_steric_plausibility_assessment.md)
has an inspected owner disposition: post-freeze contract/method study, retaining
read-only per-check results and no implied molecular repair. No scientific
assessment implementation or additional release gate is introduced by triage.

[#548](archive/resolved_bugs/reference_bond_pairs_documented_as_atom_names.md)
corrects the four remaining group reference-bond docstrings and aligns the User
Guide, recipe and Module 03 with the seven-helper index contract. All 342
contract/container cases, 572 documentation/doctest cases and 99 additional
existing group cases pass with zero omissions. The separate 246-function
docstring validator, all fourteen fast gates and whole-tree Ruff pass. The
owning record retains warnings, original failing controls and receiving scope.
AST and notebook comparisons establish unchanged executable bodies/signatures
and unchanged notebook code/output/metadata. No runtime or chemical-table fix is
claimed by this documentation correction. Routine hosted CI on the integrated
head remains a separate checkpoint.

[#554](archive/resolved_bugs/reference_bond_index_maps_are_not_consistently_validated.md)
retains the independently reproduced malformed-map defect and is the next native
correction. Its report is now recorded; no validation fix is included with #548.
Then continue #549's naming-context study and #504's multi-structure contract
before receiving #543 against the corrected native source. All subsequent
dependency, scientific-provenance and installed-client decisions retain their
owners in the route below. The four unrelated API-stub edits remain excluded.

## Resumption route after the library audit — 2026-11-04

**Role:** current work ordering following the maintainer-requested
[dated audit](archive/assessments/library_engineering_and_scientific_audit_20261104.md).
The audit's broader evaluation ideas are planning inputs, not newly admitted
1.0 features. The [scope admission rule](release_1_0_scope.md#admission-rule)
and exact-candidate gates remain authoritative. This section orders subsequent
work; it does not report that any step has been completed.

### Observed starting point

- Main is `93d29bf23e2c54f238f7ada984a4b23420b4b3b0`. Its five routine
  workflows pass, including smoke 41854905816: 5,210 native passes/16 optional
  omissions and 2,658 addon passes/four optional omissions. This later routine
  evidence completes the follow-up requested in the metadata checkpoint below;
  it is not a new full-matrix qualification.
- The audit, its addendum and original scientific execution certificate are
  prepared locally and linked from this guide. Their documentation/index checks
  pass. They are not yet committed or published. Four pre-existing generated API
  stub edits remain outside the audit and stabilization changes.
- #548 is prepared on isolated branch `dev/template-bond-contracts-548`, based
  on main above. Its 342 contract cases, 572 documentation/doctest cases and
  246-function docstring validation pass. Its local report predates the last
  documentation result and needs reconciliation before closure. The final diff,
  notebook preservation and applicable receiving checks are still due.
- GitHub inspection on this date finds one open PR, #543, published head
  `3889ad75ab8def7ad20ac5dcee1fe7bd28bc9466`. It conflicts with main and its
  recorded full matrix fails. Contributor results and earlier review do not
  qualify a new combined candidate. A later local integration commit is visible
  in the contributor worktree; it is not the published PR head or accepted owner
  evidence.
- New [#555](https://github.com/uibcdf/molsysmt/issues/555), requested by
  DockingMT, proposes read-only geometry/steric plausibility assessment. It
  explicitly describes a capability request, not a reproduced numerical defect
  or an initial-1.0 gate. No assessment method is selected or implemented here.

### Ordered work and exit conditions

| Order | Work | Exit condition before proceeding |
| --- | --- | --- |
| 0 | Preserve and publish the audit as its own documentation checkpoint; triage #555 against existing tools and the scope rule. | The dated assessment is durably recorded without staging unrelated API stubs. #555 has an explicit owner/scope disposition; any later feature work remains separately scheduled. |
| 1 | Finish [#548](https://github.com/uibcdf/molsysmt/issues/548), resuming the prepared patch. | Review the four docstrings, all seven helper contracts, User Guide/course changes and literal output guards; verify executable bodies/signatures/reference data are unchanged and notebook code/outputs/metadata are preserved. Reconcile completed evidence, run applicable remaining checks, integrate and close with its addressable guard. |
| 2 | Repair [#554](https://github.com/uibcdf/molsysmt/issues/554) at the native argument boundary. | Decide aligned-map length, scalar compatibility, boolean/negative/duplicate/empty cases first. ArgDigest enforces the chosen contract with existing SMonitor diagnostics. Invalid maps fail deliberately; valid family semantics and caller inputs are preserved. Coordinate signature/skip changes with #543 rather than adding addon coercion. |
| 3 | Resolve [#549](https://github.com/uibcdf/molsysmt/issues/549) through a bounded naming-context study and correction. | Establish the meaning of legacy names versus explicit native protonation labels; audit GLH/HID/HIE and relevant collisions from pinned primary sources. Name/sequence/template controls agree under the declared context, without implicitly changing chemical states. Escalate a required public context decision before broadening APIs. |
| 4 | Repair [#504](https://github.com/uibcdf/molsysmt/issues/504), then reconcile remaining scientific and presentation defects. | Define the multi-structure solvation-predicate result/selection contract before implementation; do not guess first/any/all reduction. Guard thresholds, mixed structures, absent prerequisites and units. Correct the README's moved graph-tool example. For #473/#475, either establish reference semantics or record an explicit release disposition with visible uncertainty; no guessed units or false scientific closure. |
| 5 | Receive [PR #543](https://github.com/uibcdf/molsysmt/pull/543) against the resulting native main under #421. | Review the actual published revision, reconcile conflicts, retain supported/attribute/element/build namespaces and the single guarded smoke command, and verify detached preparation plus source/scene preservation. Qualify the exact combined candidate with all applicable PR gates before integration. Failed old matrices remain historical; source exposure counts are regenerated, not assumed. |
| 6 | Complete dependency/publisher decisions under [#524](https://github.com/uibcdf/molsysmt/issues/524), [#428](https://github.com/uibcdf/molsysmt/issues/428) and [#544](https://github.com/uibcdf/molsysmt/issues/544). | Ground remaining optional/sibling floors in consumed APIs; coordinate a genuinely published compatible Viewer floor. Retain ArgDigest ownership deferral unless a concrete need justifies adoption. Review the Conda action's immutable pin without changing the native publication profile or publishing files. Run the dependency-route and publisher-contract checks. |
| 7 | Return to exact-candidate source and installed-client qualification under #334, #250 and #254. | Select compatible source/artifact identities with Viewer, execute required source/native/scientific/documentation and installed-pair gates, verify client workflows, and close owning items only with their required evidence. Tags, package publication, promotion and archival retain their separate authorization. |

This is the default order, not a claim that every step is a hard dependency on
its predecessor. Provider-floor research and #555 contract triage can proceed
while a hosted gate runs. A scientific source-access limitation must receive an
explicit disposition rather than causing indefinite table changes or blocking
unrelated work. Fresh demonstrated regressions can change priority under the
existing admission rule.

### Validation and scope discipline

Use the audit immediately to strengthen review: independent expected outcomes,
nondefault units, index remapping, immutable caller data and failure publication
where relevant. Reuse completed tests only while their source and scope remain
applicable. Run targeted receiving for each correction, then the mandatory exact
candidate gates; neither repeated full suites after every prose change nor
passing a small selection qualifies the eventual package.

Broader corpus expansion, readiness presentation, detector sensitivity,
universal mutation tracking, streaming append, caching (#553), conformer/state
enumeration and hydrogen/environment refinement remain separately owned future
work unless explicitly admitted. Do not restart the completed ChemicalStates
source refactor or the merged #538/#540 receiving merely because the audit lists
opportunities. No implementation, issue closure, consumer notice or publication
was performed by writing this route.

## Metadata integration and native array repair — 2026-11-04

PR #538/#540 are admitted on exact candidate
fbb09782c3f66735762bd4a507314db692927f97 after all ten applicable workflows pass.
The eight-cell full source matrix passes 25,114 cases per Linux cell and 25,113
per macOS cell, with respectively 102 and 103 recorded omissions. All eight
registered scientific evidence executions pass 79 cases without omissions.
Native wheels pass four-target/Python 3.11--3.14 compatibility, NumPy floors,
source-distribution round trip and the four Linux installed-public checks.
The [addon owner record](pending_proposals/molsysviewer_tools_addon.md) and
[terminal receipt](../devtools/data/molsysviewer_tools_metadata_gate_receiving_20261104.json)
retain exact source, jobs, hashes and scope. The 155/244 source-path inventory
is not a count of independently validated scientific algorithms or installed
Conda release-pair qualification. Earlier failed producers remain failed.

[#550](archive/resolved_bugs/template_bond_helpers_reject_numpy_atom_names.md)
repairs the documented NumPy name-array routes for three reference bond helper
families without changing their data or valid list outputs. Its separate
receiving merge aa1527bc2 combines that native repair with the frozen metadata
candidate and passes 2,938 group/addon/inventory cases and 568 documentation/
doctest cases without omissions, plus all 14 fast gates and Ruff. Its warning
counts and bounded parity remain explicit in the owning record. The metadata
hosted gates do not qualify this later repair as a new full source matrix.

The first routine smoke on 776ed2fc2 (41853652640) fails before pytest at
the separate default-fidelity validator: three updated reference-helper
docstrings omit an explicit default=None declaration. A docstring-only follow-up
adds those declarations without changing executable ASTs, signatures or guards;
the separate validator is now included in local receiving. The failed run is
not relabelled as passing; the new head needs its own routine CI.

Next: follow the updated
[post-audit resumption route](#resumption-route-after-the-library-audit--2026-11-04),
starting with the prepared #548 documentation patch. It incorporates the new
#554 validation defect and the remaining #504 contract decision before updated
PR #543 receiving, retaining both metadata namespaces and current native repairs. Provider/runtime
floors (#524/#428), #504's solvation policy and final installed delivery retain
their separate owner boundaries. Future reference-database caching is tracked
in #553 without entering this stabilization patch. #421 and #334 remain open;
no release, tag, package upload or promotion is performed by this integration.

## Post-integration stabilization review — 2026-11-03

The live-board review found 89 open issues, including 12 labelled bugs, before
the new checkout-budget report #536. This is a dated inventory observation, not
a live count or a requirement to implement every extension before 1.0.
The release-scope admission rule remains unchanged.

The completed #531 typed-component preservation fix and #532 explicit dictionary
domain-composition fix are published on main. Their archived owner reports
identify exact source CI, tests and remaining installed/consumer boundaries.
The later documentation-only checkpoint 27c6bd3c0b4adfc1b7c3b635b9f30bcf6ffa0cab
retains their qualified runtime/test bytes. Its devguide job exhausted five minutes
in full-history checkout on two attempts before running a validator; #536 owns
that separate recovery rather than relabelling either attempt successful.

Completed bounded work (owner records retain detailed evidence):

| Issue | Verified state and next boundary |
| --- | --- |
| [#533](archive/resolved_bugs/rust_vector_export_missing_from_reviewed_manifest.md) | Fix source 2797c5425f5735568422325928520ae591c3676a admits the existing vector kernel and adds real-module drift guards. Fifty-five focused tests and real noneditable Linux/Python 3.14 installed-extension validation pass with exactly 102 exports. Hosted native-source guards pass on d8ea626a0ab6dbd976d0e04ad9299019e4ae0a42. The diagnostic wheel is unpublished; it does not establish the Viewer installed matrix or a new public floor. |
| [#520](archive/resolved_bugs/append_structures_named_analyses_partial_state.md) | The transactional runtime introduced by #255 already repairs the original append publication order. Forty-five combined public regressions cover successes, source selection, rejections, late preparation failure and H5MSM persistence. The combined append/state/analysis selection passes 68 cases; hosted native-source qualification passes on d8ea626a0ab6dbd976d0e04ad9299019e4ae0a42. No runtime rewrite was needed. |
| [#536](archive/resolved_bugs/devguide_ci_times_out_during_full_history_checkout.md) | The full-history devguide job has a bounded 15-minute budget while retaining ancestry, archive restoration, integrity validators and API baseline checks. Run 41687790369 passes on d8ea626a0ab6dbd976d0e04ad9299019e4ae0a42. The successful 209-second checkout is below the former budget; this is recovery evidence, not a measured speed improvement. |
| [#515](archive/resolved_bugs/weekly_full_suite_has_seven_repeated_failures.md) | The #255 corrections already repair the historical seven-case weekly backlog. A fresh audit verifies every original node executed and passed in each of the eight official full-matrix artifacts for de7ffad2aef18ff3bccd184133dc69e081cb506e; 310 affected-module cases also pass locally on 13f72af2c9630bf768e03b59e2c973d5c6def4f4. Original failures/cancellations and optional omissions remain recorded. No new runtime patch or later-source full-matrix claim is made. |
| [#503](archive/resolved_bugs/cip_result_reference_authors_are_shared_with_later_calculations.md) | CIP result references now own their nested author lists. Two positive/empty mutation controls fail before the correction and pass afterwards; 119 CIP/SDF/fixed-hydrogen/history/Ackredit cases pass without skips. Scientific labels and source data are unchanged. This scoped local closure does not claim routine hosted or installed-candidate qualification. |
| [#534](archive/resolved_bugs/stable_inventory_marked_as_bond_dependent.md) | Stable molecule/entity inventory no longer requests bond inference. The independent 320-case requirement matrix and four real PDB planning controls pass locally and in exact-source hosted native receiving. Graph and state-local source prerequisites remain intact. |
| [#535](archive/resolved_bugs/attribute_alias_initialization_depends_on_import_order.md) | Shared plain declarations remove the consumer bootstrap cycle. Nine unprimed subprocess orders preserve aliases, collision/unknown-keyword errors, native reads and the original registry-builder entry point. Hosted source receiving passes without omitting those controls; no ArgDigest patch or consumer preload is needed. |

The combined local selection for this work passes **2,818 tests**, zero failures
or omissions, exit 0, with 719 disclosed warnings; all 14 fast gates pass.
This is Linux source evidence in the existing Python 3.14.7 environment. It is
not a fresh full matrix, clean dependency closure, public package or release.
Owner records hold commands, raw evidence references and final lifecycle state.

The exact-source hosted checkpoint **d8ea626a0ab6dbd976d0e04ad9299019e4ae0a42**
passes all six applicable workflows. [CI smoke 41687790382](https://github.com/uibcdf/molsysmt/actions/runs/41687790382)
records **4,184 native passes / 16 optional skips** and **2,449 bound-Viewer
passes / four optional skips**, each exit 0. Linux/Python 3.14 uses Pandas 3.1.0
and Viewer ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352. The native omissions are
14 unavailable Ackredit checks plus unyt and astropy; addon omissions are four
Ackredit checks. The tiers retain 590 and 1,539 warnings. These source smoke
results do not replace the zero-skip scientific gate or installed-pair matrix.

The #534/#535 follow-up passes **3,866 local cases** without skips, the 14 fast
gates, public doctests, Ruff and signatures. Exact source
**839709e4adeb754adbb5a9eea0a5eb2fa21d795c**, which also contains #503, passes
[routine CI 41698204284](https://github.com/uibcdf/molsysmt/actions/runs/41698204284):
**4,530 native passes / 16 optional skips** and **2,449 addon passes / four
optional skips**, each exit 0. No new attribute/bootstrap guard is skipped.
The tiers retain 590 and 1,539 warnings. The Conda manifest records Python
3.14.10, NumPy 2.5.4 and Pandas 3.1.0; Viewer stays ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352.
Ackredit accounts for 14 native and four addon omissions, with one native unyt
and astropy omission each. All five applicable source workflows pass: smoke
41698204284, devguide 41698204237, Ruff 41698204479, suite policy 41698205147 and
publication governance 41698205100. This is not a full-matrix, installed-pair or
release claim. The older 13f72af2c scientific job remains cancelled without
executed steps.

### Benchmark and site-scope closeout — 2026-11-03

[#539](archive/resolved_bugs/benchmark_reference_h5_conversion_fails_in_ci.md)
passes the complete exact-source audit 41706735371 on 3920346fb: three reference
controls and 21 compared paths meet the unchanged 15% threshold. Runtime origins
and the actual Conda interpreter are recorded; no installed-package claim follows.

[#509](archive/resolved_bugs/hbond_site_structure_bounds_differ_between_resident_and_h5msm.md)
is repaired in the shared source-axis/chemical-context and H5MSM reader boundaries.
Combined native/addon receiving passes 1,279 tests without skips/failures; the
518 documentation/doctest controls and 14 fast gates also pass. The owner record
retains warning counts, original failing guards, requested-row memory controls,
nondefault units and source/scene preservation. This is local source receiving,
not a full hosted matrix or installed-pair qualification.

### New board and PR review — 2026-11-03

**Gate follow-up, 2026-11-04:** refreshed metadata source 4ea80278f passes all
native-wheel/installed-public smoke jobs in 41755220512, plus smoke, performance
and administrative checks. Full matrix 41755216514 still fails in all eight
cells on the same two legacy private donor-digester assertions. Their test-only
alignment is owned by
[#552](archive/resolved_bugs/legacy_donor_digester_tests_retain_obsolete_selector_and_list_expectations.md):
127 focal and 1,141 broader cases pass, with eight new public rejection cases
and unchanged production code. Both generic guards now join native smoke.
Preserve the frozen r2 identity and qualify a new exact candidate before merging
the metadata extensions. Passing native jobs do not replace the failed full suite.

Corrected source merge f2d59d5b3 on `dev/review-tools-537-540-r3` retains main
d9255c85c and both PR heads. Runtime/addon/Rust/build inputs match frozen r2;
136 focal guards, the live 155/244 inventory and all 14 fast gates pass. The
[new receipt](../devtools/data/molsysviewer_tools_corrected_guard_candidate_20261104.json)
keeps prior results separate. Its applicable hosted gates remain due before
integration; source equivalence is not a substitute for their execution.

The refreshed board contains 87 open issues and two open PRs before the two
metadata closeouts above. New incoming work is #537, PR #538, #539 and PR #540. These
counts are a dated snapshot, not a live generated inventory.

Current receiving and next admitted defect/contribution reviews:

1. **[#542](archive/resolved_bugs/pi_pi_h5msm_calculations_materialize_structures_during_graph_only_preparation.md):**
   resolved on main dbdbc9bfe. Frozen combined candidate a24b14f3d passes source
   smoke 41730351587 (4,810 native passes / 16 optional skips and 2,658 addon
   passes / four optional skips) and performance audit 41730356380. The original
   bounded-read guards execute successfully; the old failures remain historical.
   This defect no longer blocks the metadata contributions' remaining gates.
2. **[#537](archive/resolved_bugs/sdist_directory_entries_mistaken_for_addon_files.md)
   and PRs #538/#540:** the native TarInfo directory correction is received
   separately from PR #538, with four red/green guards and an unchanged real
   59,061,773-byte archive. All 98 packaging controls pass. The four supported
   reports and seven attribute metadata tools remain unmerged. Reconcile their
   inventories, retain newer guards and qualify
   the combined integration. Candidate a24b14f3d retains both PR ancestries,
   passes 2,687 local tests without omissions and the corrected hosted smoke.
   All eight full-matrix lanes now pass. Rust workflow 41730347088 remains a
   terminal failure: its four installed-public smoke jobs rejected generated
   addon bytecode. The original wheel contains no caches; the installed-only
   inventory correction and real pip-install/adversarial guards are resolved under
   [#551](archive/resolved_bugs/installed_addon_inventory_rejects_installer_generated_bytecode.md).
   All 94 packaging controls and a Linux/Python 3.14 public runtime reproduction
   pass with the original wheel and patched validator. That local prefix inherits
   development dependencies. It does not reclassify the original workflow or
   qualify the next integrated candidate's complete installed/platform matrix.
   The [addon owner record](pending_proposals/molsysviewer_tools_addon.md) holds scope.
   Refreshed source merge 33c4171da on `dev/review-tools-537-540-r2` retains both
   PR heads and main 73dedbbae, including #537/#551. Its 664 selected
   native/metadata/package cases, 572 documentation/doctest cases, actual source
   archive and all 14 fast gates pass locally. The live inventory is 155/244.
   This newer candidate still needs its own exact-source hosted gates before
   integration; the first candidate and its receipts remain unchanged.
3. **[#511](archive/resolved_bugs/classic_hbond_precomputed_donors_have_inconsistent_shapes.md)
   and [#516](archive/resolved_bugs/aromatic_detectors_reject_reference_mdtraj_selection.md):**
   resolved with supplied donor-anchor/pair validation and reference-aware aromatic
   selection. Final local receiving passes 2,021 source/bound-addon tests and 569
   documentation/doctest cases without skips. Scientific criteria, sparse-output
   restrictions and explicit-state external-selector limits are preserved. These
   later corrections are separate from the frozen metadata candidate a24b14f3d.
   #509's site/state/structure controls and #542's eager-read guards remain green.
4. **[#541](archive/resolved_bugs/setuptools_minimum_for_pep639_license_metadata.md):**
   resolved with Setuptools >=77.0.3 across source, both Conda hosts and five
   explicit tool environments. Exact 76.1.0 rejects the existing metadata; exact
   77.0.3 and current 84.0.0 build native artifacts with matching license metadata
   and original notices. Five local artifact identities and 62 packaging tests
   are recorded. The #537 general sdist inventory failure and clean installed/
   platform release qualification remain separate; public files are unchanged.
5. **#504:** choose and document multi-structure solvation output/aggregation;
   choosing first/any/all silently is not an acceptable numerical repair.
6. **[#523](archive/resolved_bugs/legacy_h5msm_structure_index_route.md):**
   resolved with metadata-only legacy 0.3/0.4 file/handler index getters.
   Requested order/repetitions, bounds, empty/None semantics, source units and
   handle ownership are guarded. All 1,390 H5MSM/index and 566 documentation/
   doctest cases pass without omissions. H5MSM 0.5 retains its separate reader
   boundary; no installed qualification is inferred.
   **[#524](pending_proposals/runtime_dependency_api_floors.md)** is partial:
   five core floors are aligned after exact provider API/ABI probes on Python
   3.11 with NumPy 1.26.0 and 2.4.6. Pandas 3.1 source receiving passes 1,886
   tests after removing deprecated summary-table inplace drops; nine final
   strict summary guards and 31 default-provider checks pass. Viewer public
   acquisition/floor, sibling/optional-provider review and the NumPy ABI-bound
   disposition remain due before publication. No installed qualification is implied.
7. **PR #543:** incoming element-utility and current-system addon contribution,
   latest reviewed intake head b41810c26c36984a68781e7706f3e933e8589c66. Its reported local tests are
   contributor evidence, not owner receiving. It excludes #538/#540; reconcile
   shared inventories, API exports, documentation and guarded smoke arguments
   only in a separately identified integration after review. Its hosted checks
   are queued; it does not extend frozen candidate a24b14f3d's qualification.
8. **[#547](archive/resolved_bugs/terminal_cap_end_labels_are_inverted.md),
   [#545](archive/resolved_bugs/canonical_amino_acid_codes_are_unreachable.md),
   [#546](archive/resolved_bugs/standard_name_examples_expect_bare_none_output.md):**
   resolved in the owner source. Cap resources now name the protected peptide
   end, with a coordinated bond-candidate consumer and generator-path correction.
   Canonical XLE/J and XAA/X are reachable; existing variant outputs are preserved.
   Exactly the standard-name print/example guard is received from PR #543;
   remaining addon changes are unmerged. Broader receiving passes 430 cases,
   final focal guards 77 and documentation/doctests 570, all without omissions.
9. **[#549](pending_bugs/reconcile_legacy_amino_acid_name_mappings_with_native_protonation_labels.md):**
   newly observed mismatch between legacy label lookup and explicit native
   protonation names. GLH resolves to Q/GLN; HID/HIE are absent from the one-letter
   route, while the native template inventory supplies those state labels.
   Keep this as an open stabilization review; #545 does not settle naming dialects.
   Incoming **#548/#550** separately report template-helper index-return
   documentation and documented NumPy atom-name arrays failing at list.index.
   They need bounded native triage; #547 does not resolve those contracts.

The Collantes ISA/ECI primary-reference questions **#473/#475** remain open;
quantity wrappers and source parity do not settle scientific dimensions or
aggregation. ArgDigest public-artifact receiving (#428), attribution adoption
(#292) and final native-domain/Viewer delivery (#254/#421/#334) retain their
existing owner boundaries. Old umbrella issues are not closed merely because
their titles describe partly implemented work.

Additional profiles and expansions such as #519/#521 and the #447/#375/#323
remainders are not selected by this defect-repair batch. Existing protected
upstream compatibility/performance follow-ups (#403/#486/#530) and course
content-contract debt (#512) remain separately scheduled. No new method,
dependency floor, tag, Release, package upload or promotion is authorized or
performed by this review. The proposed next pre-1.0 checkpoint remains a future
exact-candidate decision; historical 0.23.0/0.24.0 artifacts are not relabelled.

## Authorized ChemicalStates main integration — 2026-11-02

The maintainer authorizes integrating the completed #255 development branch
into main after its source closeout. This supersedes the earlier no-merge
boundary for this integration only. The integration combines main
183ff252b4b3005438e4d7a5335c5564ab558661 with source-delivery checkpoint
cc7c6e36c6e5d57515b7fa3e2d1bb33f026528f3, retaining the archived report and
the newer shared guides. Runtime and test bytes remain those qualified at
de7ffad2aef18ff3bccd184133dc69e081cb506e.

Routine smoke, full-suite fallback, weekly, benchmark and documentation source
routes now select the compatible Viewer ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352
used by that qualification. Manual candidate input remains explicit. The
integration checks cover the combined documents, API transition, source-route
contracts and real native/addon smoke workflows; post-push CI is checked
separately. The routine Viewer manifest is updated with its workflow consumers,
and the already implemented keyword-only OpenMM get_missing_bonds control from
#527 receives its specific signature-transition record. Runtime code is unchanged.

The combined tree passes the native smoke selection (4,049 cases), the complete
bound-Viewer addon selection (2,453 cases) and 73 route/API/OpenMM controls,
each with zero failures and skips. Canonical Pytest Receptor evidence is
finalized, session-complete and integrity-valid and agrees with JUnit. Native
and addon selections retain 492 and 1,533 visible warnings respectively. All
14 fast gates, Ruff and the signature-transition check against pre-integration
main pass. These are integration-source checks, not a fresh full matrix or
installed-package qualification; the unchanged runtime retains its separately
identified complete local/eight-cell evidence below.

No package version, public dependency minimum, tag or Release is created by this
integration. Final installed-candidate work remains #254/#334.

## Chemical-domain source closeout — 2026-11-02

The #255 source refactor is complete on `dev/chemical-states-separation-255`.
Exact runtime/test source `de7ffad2aef18ff3bccd184133dc69e081cb506e` passes the
complete local selection (23,774 passed/two disclosed skips), all eight complete
Linux/macOS Python 3.11–3.14 cells and 79/79 registered scientific cases without
skips in each cell. The [archived execution record](archive/resolved_proposals/retire_topology_bonds_after_1_0_in_favor_of_chemicalstates.md)
owns detailed counts, omissions, guards, measured limits and original failures.
The [core specification](CORE_SPECIFICATION.md) and
[migration guide](chemical_states_migration.md) own current behavior.

Source handoffs/review requests exist in all five client repositories. Their
teams finish adoption and qualification; draft/unapplied work is not called
integrated. No main merge or release is performed. Next-stage main integration,
new candidate construction, exact installed-pair/platform qualification and
public availability remain separate under #254/#334 and client owners. Historical
0.23.0/0.24.0 artifact receipts do not qualify this refactored source. Future
MDTraj batch-performance recovery is tracked post-1.0 in #530.

## Chemical-domain migration started on an isolated branch — 2026-10-29

The [#255 execution receipt](archive/resolved_proposals/retire_topology_bonds_after_1_0_in_favor_of_chemicalstates.md)
records advance notices, initial target tests, the private storage extraction,
scoped passing regressions and the still-failing future targets. Runtime work
stays on `dev/chemical-states-separation-255`; main receives documentation only.
Neither the public native/functional cutover nor new dictionary/topology schemas
are delivered. Receiving clients and final candidate qualification remain open;
the tracker owns detailed completion state and exact evidence.

## Chemical-domain separation plan recorded — 2026-10-28

The maintainer accepts the pre-1.0 architectural direction and requests a written
plan before refactoring. The [#255 phase tracker](archive/resolved_proposals/retire_topology_bonds_after_1_0_in_favor_of_chemicalstates.md)
now records the native, functional, form/lifecycle, persistence and consumer
migration, its acceptance matrix and the unresolved engineering preflight items.
The planning document is delivered; runtime implementation, migrated tests,
consumer receiving and candidate qualification are not started by this work.
The tracker is the sole detailed checklist; do not duplicate its completion
state in this release ledger.

Chains stay in Topology. Bonds/components and the nine listed graph tools have
ChemicalStates/chemical_states as their accepted target. #447 implementation
follows this migration. Existing #254 delivery evidence remains valid for its
original sources; final #254/#334 candidate qualification must use the resulting
new sources and actual artifacts. No new release/package is claimed or authorized.

## Current source follow-up — 2026-10-27

TPSA/lipophilicity contribution outputs are source-resolved under #497 and native
atom-membership order/missing-parent behavior under #498. The subsequent #494/#495
owner repairs preserve inherited molecules when adding groups and support MDTraj
selection of group-free sources through target-only hierarchy. Local tests and
executed documentation do not replace candidate/platform/installed-pair gates.

The subsequent #499 source correction coordinates atom growth across every
chemical state, retaining original evidence and marking new chemistry unknown/partial.
Its former strict expected-failure guard now passes normally; group-free compiled
molecule metadata remains aligned. This is local source qualification, not a new
release waiver. Existing source-versus-artifact identities and the publication
pause below remain unchanged.

The #181 DCD/XTC execution slice now selects 206 of 606 declared conversion
edges, with 400 explicit debt entries. The #502 repair preserves whole-file copy
ownership and adds the standard output_filename keyword without removing the
legacy positional alias. Unsupported subset-file serialization refuses before
writes; selected native/H5MSM coordinates remain supported. The
[execution record](pending_proposals/execute_every_declared_conversion_edge_in_the_test_suite_not_only_audit_it_stati.md#dcdxtc-coordinate-execution-extension--2026-10-27)
records the local 485-case regression and final 38-case receiving scope. This
source evidence does not replace candidate/platform/installed-pair gates.

The prior #499 exact-source smoke run
[40576737384](https://github.com/uibcdf/molsysmt/actions/runs/40576737384) has now
finished officially with success on ab165135ee4ba48595ecfda70861458ef9aaaa4d.
It does not qualify the subsequent conversion-source changes above.

The bounded #144 documentation follow-up removes ten topology directive-parse
warnings and both unknown directives. Forced full-site builds on the recorded
source move from 737 to 725 warnings, with zero errors; remaining debt stays
explicit and nonblocking. A later joint-head build with the addon prose update records 726 warnings
(one additional accepted course-header warning), still with zero errors.
Real-source rendering/negative controls and raw notebook
schema checks pass. Scientific code and saved notebook outputs are unchanged;
one new course-cell ID is repaired separately. See the
[documentation record](archive/resolved_bugs/sphinx_warning_baseline_and_api_reference_debt.md#bounded-directive-rendering-and-cell-id-repair--2026-10-27).

The next #144 markup-only slice removes the full inline-title parse-warning
family: 261 corrected directives in 161 source documents. The forced full-site
checkpoint has 465 warnings and zero errors; 509 schema/rendering controls pass.
All scientific code, saved outputs and other notebook payloads are unchanged.
No suppression or source exclusion is added. The
[family receipt](../devtools/data/documentation_dropdown_family_repair_20261027.json)
retains source differences and preservation proof. Remaining header/reference
debt stays partial and supplies no new release qualification.

The following #144 reference/rendering slice moves a fresh forced full-site
baseline from 465 to 456 warnings, with zero errors. Real-source rendering and
schema checks pass 519 cases; focused API/doctests pass 15. It repairs highlighting,
reference destinations, existing attribution and list markup, plus four newly
introduced cell-ID/schema mismatches while preserving all notebook contents.
The original parent navigation anchor and executable Python ASTs are preserved.
The [reference receipt](../devtools/data/documentation_reference_repair_20261027.json)
records the scope and remaining 435 header, 17 orphan-page and four internal-link
warnings. No warning is suppressed and #144 remains partial.

The #144 publication-boundary pass connects five public API pages and retains
twelve contributor/template/prototype documents in Git outside the published
site. Source-discovery guards protect every User Guide/API page, all 156 course
modules and manifested public pages; stale manifest paths are repaired. All
554 documentation checks pass. A clean-output full-site build has 433 warnings,
all from heading policy, and zero errors; the 17 orphan and four reference
warnings are gone. Two template-only header warnings leave the site with the
template. Public notebook content and package source remain unchanged. The
[navigation receipt](../devtools/data/documentation_navigation_repair_20261027.json)
separates publication scope from warning suppression. #144 remains partial.

The final #144 pass normalizes the maintainer-approved course heading hierarchy,
repairs the six other skipped levels and gives the home page one semantic title
with scoped presentation. Heading-marker changes preserve all code/results and
other notebook values; the 101 normalized public articles retain equivalent HTML
apart from section-close/horizontal-rule delimiter placement. A latent duplicate
Basic/Element tutorial label is separated, preserving the Basic API anchor.
All 565 documentation regressions pass, and both 12-worker and serial strict
full-site builds produce zero warnings and errors. The existing publication
workflow rejects warnings through executed -W option tests. #144 is source-resolved;
the [heading receipt](../devtools/data/documentation_heading_repair_20261027.json)
retains the evidence and browser-check limitation. Missing module-specific course
contracts are deferred independently under #512. These source checks neither
publish documentation nor qualify a release or installed pair under #334.

## Current source stabilization — 2026-10-26

Default-reference readiness selection is source-resolved under
[uibcdf/molsysmt#480](https://github.com/uibcdf/molsysmt/issues/480). Its additional
state controls exposed an independent H5MSM association defect, now source-resolved
under [uibcdf/molsysmt#481](https://github.com/uibcdf/molsysmt/issues/481). The
[association resolution](archive/resolved_bugs/h5msm_writes_an_unreadable_identity_association_when_structure_and_chemical_stat.md)
records guarded unequal structure/state populations and unchanged strict reading.
This changes neither the H5MSM version nor the paused artifact identities.

Collantes physical interpretation remains open under #473/#475; the scientific
registry now explicitly classifies get_charge as partial instead of extending
its bounded physical_pH7/OpenMM evidence to unverified ECI dimensions and sums.
The current-source SDF declaration refusal remains a bounded profile limitation
under #215. Local source regression and documentation checks do not replace the
new exact-candidate platform, scientific-evidence and installed-pair gates under
#334. Publication remains paused as recorded below.

The subsequent native ring/chemical-selector repairs under #482/#483 preserve
reference requests and validate source structure scopes. Under the maintainer's
new #473 decision, ISA now returns standardized PyUnitWizard area quantities from
a provisional angstrom² table convention; original-paper verification stays open.
#475 retains ECI dimension/additivity review, and #485 records a separate external
observable exploration. These source contracts require applicable new candidate
qualification; they do not change the publication pause or prior artifact evidence.

The #484 compatibility correction excludes PyParsing 3.3.3 in optional/source
test solve routes without raising MDTraj's global floor or removing Python
3.11 support. The existing development runtime now uses validated PyParsing
3.3.2; this is source/development evidence, not a new installed release pair.

The first #485 reader, experimental `physchem.get_bulkiness`, is implemented
under #487 with unit-aware reference values, strict unsupported-group diagnostics
and optional attribution. Evidence remains partial for the original derivation;
this source addition requires applicable new candidate qualification and does
not change the publication pause.

The #488 follow-up extends the shared reference-preserving selection boundary
to SMARTS and its site-reader clients. Default/None external selectors now work
without changing explicit/associated-state restrictions or scientific matching.
Local regression evidence does not replace new exact-candidate qualification.

## Release coordination paused — 2026-10-08

On 2026-10-20 the maintainer extends the publication postponement by a couple
of days while awaiting MolSysViewer and authorizes a bounded issue/improvement
window. The selected #206 extension adds optional keyword-only masks to info,
with the independent duplicate-intersection correctness repair #389 discovered
through its guards. The
[summary-mask record](archive/resolved_proposals/info_selection_masks.md),
[selection-defect record](archive/resolved_bugs/repeated_selection_or_mask_indices_can_introduce_atoms_outside_their_intersectio.md)
and [receipt](../devtools/data/info_mask_qualification_20261020.json) retain
1,075 passing basic/native cases, five passing doctests, fourteen fast gates
and executed/rendered new documentation sections. Source changes need later
candidate qualification; the following frozen files/refs and pause are preserved.

The Viewer owner relays an explicit maintainer decision to postpone both
MolSysMT 1.0 and MolSysViewer 1.0 while a Viewer design/use question is discussed.
The qualified **MolSysMT 1.0.0 build 0 / MolSysViewer 0.24.1 build 1** pair below
is preserved as evidence, but is no longer selected for immediate public
publication. No replacement Viewer version, source SHA or artifact is agreed.

Keep all existing refs, original files and qualification outcomes unchanged.
Do not move/delete refs, rebuild files, repeat matrices or close #250/#254 as
final-candidate acceptance during this pause. No tag, GitHub Release, public
promotion or Zenodo publication is authorized. No MolSysMT implementation change
has been requested for the new Viewer question. First discuss that question;
then agree new candidate identities and the affected qualification scope.

On 2026-10-09 the maintainer authorizes repairing newly reported DockingMT
correctness defects **#352, then #353** while the Viewer discussion continues.
This is bounded stabilization of existing public merge/add behavior, not a
resumption of publication or a new capability. Keep the qualified pair below
unchanged as evidence of its original bytes. Runtime fixes on main require
replacement candidate selection and applicable qualification before release;
they do not inherit the original producer's exact-commit results.

The bounded corrections are now source-validated: #352 preserves prepared
mechanics on the selected combined atom axis; #353 preserves declared chain
IDs/names independently of chain-index offsets. The combined composition and
hierarchy selection passes 151 tests and the add/native doctests pass 2 tests.
The original 1,483-atom PDBQT reproduction preserves charges/types and all
output chain fields. Records:
[mechanics merge](archive/resolved_bugs/prepared_mechanics_merge_loses_atom_axis.md)
and [chain labels](archive/resolved_bugs/native_add_drops_declared_chain_ids.md).
These corrections do not change the paused candidate selection above.

The maintainer next selects #390, #348, #188 and #120, in order. #390 now
preserves explicit atom stereo declarations from chemical templates, with strict
correspondence admission unchanged. Its [handoff record](archive/resolved_proposals/chemical_template_stereo_handoff.md)
retains 238 passing affected cases, nine focused cases including H5MSM/history,
two doctests and counterfactual failures under the old reader. #348 is also source-validated: state-aware induced connectivity and general
spatial selection delegation pass 1,249 affected cases, with executed guide/course
examples. Its [connectivity record](archive/resolved_proposals/selected_state_connectivity.md)
retains the contract and evidence. #188 now adds programmatic supported-report outputs with 80 passing contract/
registry cases, four doctests and executed/rendered documentation; its
[introspection record](archive/resolved_proposals/supported_forms_and_info_return_only_styled_tables_with_no_programmatic_result.md)
retains the exact scope. #120 now supplies bounded native representations;
its [inspection record](archive/resolved_proposals/native_object_representations.md)
retains 1,159 passing native/interaction cases, 17 doctests, 88 integrated guards
for all four issues and executed/rendered examples. All four selected issues
are source-validated. On 2026-10-21 the maintainer begins the prior #128 study,
expanding it from MolSys/Topology/Structures to relevant native domains and
representations used by suite clients. The [native-query study](pending_proposals/native_query_shortcuts.md)
records existing access paths, baseline methodology and the proposed shared
validated core. The maintainer subsequently authorizes the resident implementation: six native
types now share validated get/info and direct explicit-index acquisition, with
the current specialized queries retained. See the [native contract](native_queries.md).
This resident source phase passes 2,285 affected regression cases, seven shared
method doctests and 34 adjacent count doctests, with executed/rendered guide
and course examples. Broader dictionary/file work is not claimed complete.
The builder validation bypass discovered during this inventory is tracked
separately in [#391's record](archive/resolved_bugs/builder_shortcuts_bypass_argument_validation.md).
The shared scalar-output delta passes 373 affected get/info/native cases.
Dated paired resident benchmarks (32 to 100,000 atoms, eight structures) record
native count-query gains around twofold and more modest info gains; they do
not certify disk access, cold startup or complete client throughput.
#128 remains partial for its separately scoped representation/file follow-up;
#391 and the discovered [nullable count defect](archive/resolved_bugs/selected_hierarchy_counts_follow_missing_parents.md)
are source-resolved. #113 still awaits its separate prior design study;
#121 has subsequently entered implementation and measured native-copy acceptance.
The subsequent #128 dictionary phase reads stored atom counts, indices and
already normalized ID/name/type strings without native reconstruction, including
combined selected queries. Other/defaulted fields and complete info summaries
retain their converters. It passes 397 affected regression cases, 36 adapter
doctests and the fourteen fast gates, with executed guide/course examples.
The dated dictionary benchmark records 32-atom counts at 0.36--0.45 ms
versus 339--355 ms with the same public reconstruction control, and selected
three-position labels around 1.5 ms at 100,000 atoms. The #128 study retains
fixture, source/environment provenance and limitations; full summaries, memory
peaks and disk throughput are not covered by those timings.
The subsequently discovered dictionary schema discrepancies are source-resolved
under [#393](archive/resolved_bugs/native_dictionary_guides_describe_fields_outside_their_implemented_0_1_schemas.md),
with guarded real-payload tables and executable examples. The related
[#394 scalar transport repair](archive/resolved_bugs/native_declarative_dictionaries_retain_numpy_scalars_that_break_json_and_yaml_se.md)
normalizes NumPy numbers in Topology/MolSys/Builder record writers. Together they
pass 304 affected cases and 21 converter doctests; no format or public signature
changes. The subsequently authorized
[#395 structure-observable correction](archive/resolved_bugs/structures_constructor_rejects_per_structure_temperature_quantities_accepted_by_.md)
now admits aligned temperature/potential-energy/kinetic-energy series in native
construction and append, preserving scalar simulation-setting semantics. It
passes 1,276 affected cases, ten method doctests, executed guide/course examples
and fourteen fast gates. H5MSM/StructuresDict and nondefault-unit round trips
are covered; no storage schema, public signature or artifact identity changes.
The subsequent #121 source work implements protected native geometry copies,
whole-MolSys ownership boundaries and bounded H5MSM geometry transfers. The
[native-copy record](archive/resolved_proposals/native_copy_protocol.md) and
[benchmark guide](benchmarking/native_copy.md) retain the dated measurements and
limitations. #121 now defines the resident copy/ownership boundary, with controlled edit
publication, explicit table/slot/resource limits, the additional workload
campaign and a passing TopoMT source copy route. Cross-client adoption remains
under uibcdf/molsyssuite#122; #405 tracks broader observable storage after 1.0.
Installed-release qualification remains separate under #334.
The independent [#396 assembly repair](archive/resolved_bugs/validated_native_bioassembly_operations_cannot_round_trip_through_h5msm_0_5.md)
aligns validated native operations with the existing H5MSM 0.5 codec, including
chain scopes and translation units. It does not change the file schema.
The subsequent [#401 selected-structure repair](archive/resolved_bugs/make_bioassembly_ignores_requested_structure_indices.md)
applies assembly operations to the requested structures in their supplied order,
including repetitions, while preserving structure labels and times. Direct file
inputs use resident native construction; default structure 0 is unchanged.
These changes remain outside the frozen historical artifact identities and
require applicable qualification when replacement candidates are selected.

## H5MSM handler boundary and local suite checkpoint — 2026-10-22

The bounded diagnostic improvement #411 identifies H5MSM 0.5 requested as
`molsysmt.H5MSMFileHandler` before materializing its domains. The direct
constructor explains the same supported 0.3/0.4 boundary and recovery paths;
resident 0.5 loading and legacy handler support remain covered. Its
[record](archive/resolved_proposals/h5msm_handler_version_boundary.md) retains 45 passing
focused cases, the convert doctest, 247 validated public docstrings, executed
course/tutorial notebooks, rendered pages and 14 passing fast gates.
This adds no 0.5 file-backed reader; that separate capability remains outside
this diagnostic improvement.

The maintainer-authorized complete local run uses the current development
environment, Linux x86_64/Python 3.14.7 and 12 workers:

```bash
python -m pytest --receptor=llm -n 12
```

The first complete run records **15,046 passed, 13 failed, two skipped** in
459.36 seconds. One guard needed the new #411 message; the other findings are
tracked separately: chemical fixtures declaring coverage before state append
(#414), a retired form-copy spy (#415), generated ViewerJSON keyword-union
drift (#416), and a helper-import false positive (#417). Their repairs retain
scientific/transactionality checks and add positive/negative import controls.
The combined affected selection passes 138 cases. The second complete run
passes **15,066 cases with two skips**, exit 0, in **416.96 seconds**, with
1,726 warnings in 52 groups. The skips are CuPy when unavailable and the
without-RDKit SMILES fallback when RDKit is installed. The seven additional
cases exercise the corrected import guard. The first run remains recorded
as failed; no deselection was introduced. Records:
[chemical fixtures](archive/resolved_bugs/chemical_preparation_fixture_coverage.md),
[projection guard](archive/resolved_bugs/coordinate_projection_guard_observes_retired_copy.md),
[argument catalog](archive/resolved_bugs/converter_argument_catalog_viewer_selectors.md),
[import guard](archive/resolved_bugs/converter_import_guard_helper_false_positive.md).
Production source is baseline
`70103677841fba359c7e1ca9b092d04d41e5807e` plus the #411/#414–#417 changes recorded here.
Relevant runtime versions are NumPy 2.4.6, h5py 3.16.0, pytest 9.1.1 and
pytest-xdist 3.8.0; Pytest Receptor is `1.2.1+22.g00a31c4`. This uses existing
editable development dependencies, not an isolated installed candidate.
Viewer source is `d96b073f23247e25cd42c95af545b6d20e7fa982`, with 23 dirty
paths observed and preserved. No independent Viewer qualification is inferred.

A formatting-only follow-up corrects the initial push's Ruff and suite-policy
format checks. Both affected test-module ASTs are verified identical before
and after formatting, retaining the complete local suite results above.
Repository-wide `ruff check .` and `ruff format --check .` pass.

### Remaining route to 1.0

The consumer has withdrawn the general observer/notification request under
uibcdf/molsysmt#413 after reviewing explicit reconciliation. Its
[withdrawal record](archive/resolved_proposals/viewer_controlled_edit_notifications_withdrawn.md)
retains the consumer decision and boundaries: direct Python edits require explicit
Viewer reconciliation; future tools integration can coordinate its own edits and
scene update. No new generic provider deliverable remains under #413. Viewer-side
reconciliation and the redesigned tools add-on are not certified as implemented.
The publication pause remains in effect.

1. Reconcile the remaining result/domain acceptance under #250 and #254
   with Viewer feedback. Existing source guards and historical packages are
   evidence for their tested scope, not acceptance of a newly selected pair.
2. Under #334, after the design decision, select immutable replacement source
   and artifact identities; qualify the applicable exact-candidate scientific,
   full platform/interpreter and installed-pair gates and public documentation.
   This local single-environment run cannot replace those gates.
3. Obtain final publication approval. Preserve the earlier qualified package
   pair, refs and artifacts throughout the current pause.

#382 retains separately scoped startup/platform/installed qualification;
#128 retains its dictionary/file follow-up. Broader documentation debt #144,
newer-MKL requalification #403 and the explicit post-1.0 native-copy/mutation/
client-workflow improvements #405/#407/#408 remain tracked. Their existence
is not an instruction to reopen general feature development before 1.0.

## Removal ownership correction — 2026-10-22

The reporting Viewer requirement #406 is source-resolved in the
[removal record](archive/resolved_bugs/remove_ignores_in_place_and_ownership.md).
`msm.remove` now defaults to False, preserving established return-new calls and
making no-op candidates independent. Explicit True updates supported native
targets after preparation and returns None. Attached domains, unsupported mutation
and ambiguous disk destinations are rejected. Named analyses follow extraction;
historical snapshots remain intact. The intentional default correction is recorded
for clients before replacing any installed candidate.

The associated [#410 converter repair](archive/resolved_bugs/molsys_dict_conversion_ignores_selections.md)
preserves requested dictionary axes by reusing dictionary extraction. Two stale
ownership/chemical-coverage guards are corrected under
[#409](archive/resolved_bugs/complementary_conversion_guard_requires_shared_owner.md).
The [#412 allocation guard](archive/resolved_bugs/allocation_guard_rejects_lower_peak.md)
keeps its ceilings while distinguishing growth from reduction and per-edit work
from initialization. The final focused selection passes 125 cases; the removal
record preserves the broader 5,478 passing cases and its one subsequently repaired
guard failure without claiming an all-green broad run. Eleven doctest examples,
two executed notebooks, recipe/dictionary examples and scoped HTML rendering pass.
These are source checks, not a new installed pair or a publication decision.

The separate H5MSM 0.5 handler-capability/diagnostic proposal #411 remains open;
legacy handlers intentionally support 0.3/0.4. Its initial native-0.5-support claim
was disproved and corrected. It does not introduce a 1.0 file-backed-reader gate.
The publication pause and all historical artifact/ref identities remain intact.

## Additional source stabilization and acceptance review — 2026-10-13

The maintainer authorizes the next bounded sequence: repair the six invalid
notebook schemas under #144, resume #382 after its provider correction is
admitted, and review the final acceptance conditions for #250/#254/#334.
This does not resume publication or select replacement artifact identities.

Source changes after the retained 2026-10-10 delta inventory have their own
records and must be included when replacement-candidate scope is agreed:

| Work | Source evidence and affected qualification |
|---|---|
| #310/#387: declared-state atom correspondences and symmetry-corrected pose RMSD, including anchors and caller-supplied maps | [Chemical correspondence/RMSD record](archive/resolved_proposals/chemically_constrained_pose_rmsd.md) and [explicit-map extension](archive/resolved_proposals/support_anchored_and_caller_supplied_chemical_correspondences_for_pose_rmsd.md) own scientific criteria, optional-engine boundaries, attribution and regression evidence. These source tools are not included merely by retaining the old installed pair. |
| #385: native gzip PDB input | [Input-adapter record](archive/resolved_proposals/read_gzip_pdb_inputs_through_native_parser.md) owns real-fixture parity, selection, integrity and handler-lifecycle evidence. Experimental Tier 3 and eager input-only scope remain explicit. Exact form rosters now include the adapter. |
| #386: obsolete pandas composition keywords | [Composition record](archive/resolved_bugs/topology_composition_emits_obsolete_pandas_copy_warnings.md) owns separately executed pandas 2/3 controls for connectivity, chemical-state values and independent output storage. |
| #144: six notebook-schema repairs | [Active documentation record](archive/resolved_bugs/sphinx_warning_baseline_and_api_reference_debt.md#bounded-notebook-schema-repair--2026-10-13) and [receipt](../devtools/data/notebook_schema_repair_20261013.json) preserve every JSON value except schema minor and cell IDs. Six guards fail before repair; 11 schema/executor checks pass afterward. A focused six-page HTML build retains stored outputs without schema errors; it does not certify the whole site or re-execute examples. |

For #382, DepDigest 0.15.1 is publicly admitted and uibcdf/depdigest#39 is closed.
The maintainer's provider-team handoff has led to adoption of DeclaredRegistry
with adapter inspection, requiring >=0.15.1 across the audited installation
surfaces and pinning its exact public source. The
[consumer adoption record](pending_proposals/first_conversion_triggers_full_form_registry_loading.md#admitted-provider-consumer-adoption--2026-10-13)
and [receipt](../devtools/data/form_registry_adoption_20261013.json) retain
fresh-interpreter sentinel, override/removal, failure/retry, concurrent-read and
legacy-loader molecular parity controls. The final local Python 3.14 suite passes
14,067 cases with two omissions and no failures, using twelve workers and
pytest-receptor; twelve bounded cases each also pass on existing 3.12/3.13
environments. Local 3.11 runtime qualification is not executed. Exact installed
and platform/Python admission remain part of #334; #382 stays partial for that
remaining scope rather than blocked on the provider. No frozen bytes or refs move.

The first full-suite run also reproduces four CRD+PSF refusals and a stale PDB
download-spelling assertion with the original loader modules. The classifier
defect is repaired under [#388](archive/resolved_bugs/crd_coordinate_metadata_is_misclassified_as_a_second_primary_topology.md)
by retaining the CRD metadata pipe and explicitly declaring its topology partial.
The PDB guard now expects the existing canonical lowercase spelling while
retaining all 304-atom/38-structure truth. Ninety nearby cases and the final full
suite pass. This is bounded stabilization, not a new molecular protocol.

An additional #144 source checkpoint repairs three broken API-to-tutorial links
and the alternate-location tutorial's plural API roles. The
[active record](archive/resolved_bugs/sphinx_warning_baseline_and_api_reference_debt.md#bounded-api-to-tutorial-link-repair--2026-10-13)
and [receipt](../devtools/data/api_tutorial_links_repair_20261013.json) retain
three failing-before/passing-after HTML-link guards, 29 passing API rendering
cases, three passing module doctests and preservation of notebook code/outputs.
All 246 current explicit API autodoc declarations resolve in the local inventory;
the older import-warning counts are historical. This is bounded link repair,
not a warning-clean full site or a replacement installed candidate.

The 2026-10-14 #144 checkpoint additionally repairs Core-to-Foundations and
renamed-module navigation. The
[active record](archive/resolved_bugs/sphinx_warning_baseline_and_api_reference_debt.md#bounded-common-core-navigation-repair--2026-10-14)
and [receipt](../devtools/data/course_navigation_repair_20261014.json) retain
37 passing course/API/schema controls, an HTML guard for twenty Foundations
links and nineteen sequential destinations, and a replay rejecting 37 original
reference warnings. Only Markdown sources change in twenty Core notebooks and
the template; all executable content and stored results are preserved. This
checkpoint leaves the broader documentation debt and publication pause intact.

Reviewing the published acceptance reconciliations and closure criteria for
[interaction organization](pending_proposals/organize_interaction_detection_by_family_before_1_0.md#acceptance-criteria)
and [ChemicalStates ownership](pending_proposals/promote_chemical_states_to_a_native_molsys_domain.md#acceptance-criteria)
confirms that #250/#254 retain final-candidate obligations under #334. Their
existing implementation/published-pair evidence remains distinct from a future
candidate. Do not close them during the publication pause. The October 10 path
counts are historical and do not describe the newly changed head; refresh the
delta inventory when candidate coordination resumes. No new build, matrix, tag,
Release or promotion runs in this checkpoint.

## Renewed pre-1.0 issue review — 2026-10-10

The maintainer requests a substantive review including post-1.0 issues, rather
than using their milestones alone to exclude possible stabilization work.
That review reproduces two current public-boundary defects, now admitted to the
1.0 queue: [MolSys shortcut validation](archive/resolved_bugs/native_molsys_shortcuts_bypass_argument_validation.md)
(#377) and [MolSys mechanical-type setting](archive/resolved_bugs/molsys_atom_ff_type_setter_missing.md)
(#376, received concurrently from DockingMT). The review admitted these defects;
subsequent source repairs are recorded below.

The #374 runtime bridge/generated-output cleanup and #368 broken regeneration
scripts have received bounded repairs recorded below. #374's remaining native
scope has now been verified on Linux as recorded in the native checkpoint below.
New scientific models,
native dispatch redesign and wider format coverage remain separate proposals.
This overrides the earlier board-review observation of only three open provider
1.0 issues; it does not change frozen identities or resume publication.

## Eager bridge and Simulation export repairs — 2026-10-10

Two runtime bridges under #374 now retire managed PDB scratch on success and
write/read/extraction failure; returned data remain usable and removal errors
propagate. At this checkpoint #374 stayed partial because generated output
failure custody and loaded temporal-library lifetime were pending. The former
is repaired in the generated-output checkpoint below. The real-engine test found
and repaired #379: Simulation PDB export selects one current box and explicitly
converts its units before updating a copied topology. Source topology, current
pose, caller paths and nm/angstrom session policies are protected by the
[export regression](archive/resolved_bugs/simulation_pdb_export_passes_a_structure_axis_box_to_openmm.md).
The combined lifecycle/export selection passes **13 tests**, and three strict
API rendering guards pass. The #368 regeneration-script repair is recorded below.
None of this resumes frozen-pair publication or qualifies newer source as an
installed candidate.

## Chemical database generation repair — 2026-10-10

#368 now has four inert CLI entry points sharing the existing real mmCIF parser
and a private maintenance owner. Explicit CCD/RTP/JSON inputs produce the current
reader schemas, sorted files and input/output hash manifests. Malformed inputs
and nonempty output directories fail before writing. The
[record](archive/resolved_bugs/legacy_chemical_database_generators_import_a_nonexistent_ciffilehandler.md)
and maintained [workflow](chemical_group_database_generation.md) document scope.
**39 focused tests** pass with Python 3.14 and twelve workers, including existing
reader delivery, byte reproducibility and a real curated MSE component. No
distributed databases are regenerated. Validation separately finds #380: two MET
supplements and their bundled variants contain an undeclared OXT endpoint; the
new generator rejects that inconsistent source until its chemistry is reviewed.
The prior source head `889b3b4fe0ddac4a24105b49a58d3321e8708045` passes all five
ordinary hosted checks. At the repair's original head `4393d9fdc`, five checks
pass but smoke `38041410267` fails before tests: its AST guard treats two retired
unexported script helpers as public. Follow-up `59b6da08a` records their retirement
with two exact file/symbol waivers; comparison against the pre-repair head passes
without changing guard discovery. Frozen-candidate identities and the publication
pause remain unchanged.

## MET reference-data repair — 2026-10-10

#380 now has a reviewed source correction and a bounded generator revision. The
two 19-atom MET variants match AmberClassic's N-terminal peptide connectivity;
their undeclared C–OXT edges are removed. The other four variants, atom inventories,
group membership and all other bucket files are preserved. A generated receipt
records input/output and generator source hashes. The
[record](archive/resolved_bugs/amino_acid_met_supplements_reference_an_undeclared_oxt_atom.md)
explains the scientific reference and the
[maintenance route](chemical_group_database_generation.md#revising-an-existing-amino-acid-supplement)
reproduces the correction from its original inputs. Source/generator/reader tests
pass **72 cases** with Python 3.14 and twelve workers. Both bundled supplements
can now be supplied to CCD generation. This is a reference-data correction, not
an installed-package qualification or resumption of publication.

## Generated output lifecycle repair — 2026-10-10

The MET/source checkpoint `514a48de35b12716d75525090e1b5846efaa66c0`
passes all six ordinary hosted checks: CI smoke `38042286888`, Ruff,
data freshness, developer-guide integrity, MolSysSuite policy and Conda
publication governance. This remains source evidence.

#374 now protects caller destinations during RCSB download failure and PDB-ID/
AlphaFold conversion failure. Each operation owns staging through its preparation
before publishing the completed file. PDB-text and UniProt FASTA writers retire
failed automatically generated outputs, retain explicit writer destinations and
preserve successful returned files. The
[record](archive/resolved_proposals/legacy_temporary_resource_lifecycle_exceptions.md#generated-output-custody--2026-10-10)
and [owner contract](temporary_resource_operations.md) document the writable-parent
requirement and publication/cleanup boundaries. At this checkpoint #374 remained
partial solely for its loaded temporal native-library probe; Windows evidence is
still required before a platform claim. The combined lifecycle selection passes
**86 tests** with Python 3.14 and twelve workers; seven doctest statements and
fourteen strict API renders pass. All fourteen fast gates and exact-base signature
comparison pass. Documentation code cells and saved outputs remain unchanged.
No release artifact or frozen reference
changes, and this does not qualify a replacement candidate or resume publication.

## Native-probe lifetime repair — 2026-10-10

The generated-output source checkpoint
`539633b77a4da51e9dd03c5edcd12c5658a4093a` passes all five applicable ordinary
hosted checks: CI smoke `38043644739`, Ruff, developer-guide integrity,
MolSysSuite policy and Conda publication governance.

#374's implementation is now complete. The parent owns the compiled temporal
probe directory and only a child loads its library. It reaps normal/failed exits,
kills and waits after interruption/communication failure, then retires owned
scratch before publishing JSON. Child HDF5 scratch stays inside that root. The
[resolution](archive/resolved_proposals/legacy_temporary_resource_lifecycle_exceptions.md#native-process-lifetime--2026-10-10)
and [owner contract](temporary_resource_operations.md) state the precise lifetime
and measurement limits. A complete old/current CLI comparison preserves JSON
keys and nine deterministic fields; timing values are not claimed as performance
parity or a new ranking. The Rust kernel stays unchanged.

Executed native evidence is Linux/Python 3.14.7/Rust 1.97.1. Windows/macOS native
guards have not executed and lifetime/platform-release qualification is not
claimed. All lifecycle guards pass **97 cases** in twelve workers with no skips;
the standalone module has eleven cases. Repository Ruff and all fourteen fast
gates pass. All earlier runtime fixes remain guarded. No installed artifact, frozen
reference, scientific method or publication state changes in this checkpoint.

## Native charge unit-boundary repair — 2026-10-10

The preceding source checkpoint `aedd5a76d195d10fc2c1fb9ac6d24c96cc751a28`
passes all five ordinary hosted checks: CI smoke `38044948696`, Ruff,
developer-guide integrity, MolSysSuite policy and Conda publication governance.

#381 is source contract-tested. Native assignment shares the existing scientific
calculation and attaches canonical elementary-charge values without requiring a
presentation standard. The quantity-returning getter still follows the active
charge standard and raises `NoStandardsError` when it is absent. Neither operation
changes caller configuration. The [resolution](archive/resolved_bugs/native_partial_charge_assignment_requires_a_presentation_standard.md)
records four reproduced failures before repair and **71 passing cases** afterward
with no skips, including both scientific providers, source immutability,
nonzero unitful totals, getter presentation, native lifecycle and public doctests.
Strict docstring checks and unchanged signature/decorator comparisons pass;
nine documentation code blocks execute and course outputs remain preserved.
The native owner contract and all relevant user/course guidance are updated.
This does not alter a frozen package or qualify a replacement release candidate.

## Released SMonitor source checkpoint — 2026-10-14

The public SMonitor 0.21.0 release is verified at
`066b69cad8896cdc126d5586fd53268af4ea6490`; the controlled source manifest now
selects that commit. It adds opt-in safe audience-specific metadata templates
and a bounded nonemitting identity bundle, and repairs event-buffer resizing and
handler delivery with warnings promoted to errors. Provider scope is recorded
in uibcdf/smonitor#39, uibcdf/smonitor#40, uibcdf/smonitor#41 and
uibcdf/smonitor#42. MolSysMT does not adopt the new opt-in APIs or change its
initialization, emission policy or public `smonitor>=0.16.0` floor.

The existing development interpreter has SMonitor 0.20.0 installed. This source
checkpoint prepends the sibling source root to `PYTHONPATH` for each validation
command and its subprocesses. The imported source is verified, and its runtime
has no Git diff against 0.21.0. Source metadata still says 0.19.0; it does not
identify the tested runtime. No auxiliary environment or installation is used.
The official guide at tag 0.21.0 is byte-identical to the current copy, including
its 0.20.0 source-version field, so it is retained without editing owner metadata.
Suite inventory is refreshed and sibling working states are preserved.

On Python 3.14.7, twelve-worker pytest-receptor validation passes **346 cases**
with no failures or omissions, and all **14 fast gates** pass. The
[receipt](../devtools/data/support_provider_releases_20261014.json) retains
runtime identity, JUnit digest, versions and scope. The previous full local
suite used 0.20.0; it is not claimed as full-suite evidence for 0.21.0. This is
focused source compatibility, not qualification of the installed 0.21.0 Conda
file or a new MolSysMT/Viewer pair. Release coordination under #334 stays paused.

## Released SMonitor source checkpoint — 2026-10-13

The public SMonitor 0.20.0 release is verified. The controlled source manifest now
pins `f6230af431a7fc185209fa44364c017d711cc2b7`, and `SMONITOR_GUIDE.md`
is synchronized byte-for-byte from that release's official guide. Provider
implementation and publication are tracked by uibcdf/smonitor#48 and
uibcdf/smonitor#50.

MolSysMT retains its existing initialization and diagnostic emission behavior.
It does not enable the new `bootstrap_policy=False` option. The public floor
remains `smonitor>=0.16.0`; using that new option would require >=0.20.0 and its
own receiving tests. The guide's >=0.19.0 application-policy preservation and
capture capabilities remain separate feature floors, not guarantees added to
MolSysMT's minimum by updating the controlled source.

On the shared Python 3.14.7 development environment, twelve-worker
pytest-receptor validation passes **346 diagnostic and form-integration cases**
in 11.75 seconds. The editable distribution metadata still reports 0.19.0, but
the imported runtime source has no diff against 0.20.0. The earlier 14,067-pass
full local suite recorded that exact runtime commit, so its evidence remains
applicable to this pin/guide update. No MolSysMT runtime files change.

The [source receipt](../devtools/data/support_provider_releases_20261013.json)
retains versions, scope and the earlier full-suite receipt. The dependency
contract audit and all 14 fast gates also pass. This is source
compatibility evidence; exact installed-file and platform/Python qualification
remain separate under #334. Publication stays paused and frozen artifacts and
references remain unchanged.

## Form-registry startup investigation — 2026-10-10

#382 is reproduced and awaits the reusable provider capability requested as
uibcdf/depdigest#34. Existing metadata detection is lazy, but target validation
and first conversion dispatch still trigger full registry initialization.
The [analysis](pending_proposals/first_conversion_triggers_full_form_registry_loading.md)
and [raw receipt](../devtools/data/form_registry_startup_20261010.json) distinguish
instrumented validation from unprofiled cold/repeated/prepared public conversions
on identical bundled PDB bytes. Three tool guards pass. No runtime optimization,
provider release/admission or changed dependency floor is claimed. Current code,
frozen artifacts and the publication pause remain unchanged; this performance
proposal is not by itself a demonstrated functional release blocker.

## Native shortcut repair — 2026-10-10

#377 is source contract-tested: `MolSys.get`, `info` and `to_form` respect the
caller's digestion flag through their existing decorated providers. Valid aliases
and scalar selections are normalized; invalid options/attribute requests fail at
the public boundary. Signatures and explicit trusted calls are preserved.
The ordinary five applicable hosted checks on source
`ae0ad2404e5e1550cc5da791c67f0529d7377483` also pass (policy, governance,
Ruff, devguide integrity and CI smoke). The new guard and existing native MolSys
tests pass **27 cases**, with three
strict docstring render/example guards passing separately. User Guide and shared
course module 4 are updated. This repairs correctness without implementing #128's
separate dispatch redesign or resuming frozen-candidate publication.

## Mechanical type setter repair — 2026-10-10

#376 is now source contract-tested: public MolSys assignments reuse the owning
MolecularMechanics setter, preserve the complete atom axis on initial subset
edits, and clear typing attribution independently of charges. Full/subset/empty
and malformed edits on full and structures-only systems pass with the existing
AutoDock assignment tests (**39 passes**); a strict docstring render/example
guard passes separately. User Guide and shared course guidance are updated.
The frozen pair and publication pause remain unchanged. Applicable exact-source
and installed-artifact qualification will be required when new candidates are
selected under #334.

## Sequence and CRD stabilization — 2026-10-09

During the publication pause, #363/#364 repair existing advertised file-adapter
contracts: FASTA/PIR chain/entity positions, CRD metadata delivery, native string
IDs and selected conversion axes. The focused public adapter/regression/doctest
selection passes 93 cases; the delivery audit reports 60 remaining unreachable
attributes across three forms. Four strict documentation guards also pass,
including the retained Toolbox draft's invalid grid correction under #144.
Records: [sequence positions](archive/resolved_bugs/fasta_and_pir_declare_chain_and_entity_indices_without_delivery.md)
and [CRD metadata/subsets](archive/resolved_bugs/charmm_crd_metadata_delivery_and_native_ids_violate_adapter_contracts.md).

These bounded repairs do not close #139/#144, resume publication or qualify a
replacement candidate. The frozen pair, receipts and references remain unchanged;
new runtime sources require applicable candidate qualification when coordination
resumes. No heavy matrix or new molecular feature is introduced.

## Native Viewer integration reconciliation — 2026-10-09

Under #354 and uibcdf/molsysviewer#186, current source retires the separate
MolSysMT addon package and registration. Scientific APIs, MolSysView form
adapters, named interactions and H5MSM 0.5 remain native backend paths. The
[maintained integration/migration guide](molsysviewer_addon.md) owns this boundary;
the [resolution record](archive/resolved_proposals/retire_legacy_molsysviewer_addon.md)
owns scoped source tests. Future wheel/sdist/installed gates reject the obsolete
addon. Existing frozen artifacts, refs and original receipts stay unchanged.
MolSysViewer has independent local changes; no Viewer file was edited here and
no new installed pair/browser qualification was executed.

#348 and #350 explicitly request new state-aware connectivity and rejected
aromatic-candidate diagnostic capabilities, respectively, rather than fixes to
their documented current defaults. They are classified Post-1.0. The addon
reconciliation does not resume publication or add those capabilities to the freeze.

The additional #356 native addition defect is repaired: `Topology.add` and
`MolSys.add` accept their documented boolean `keep_ids` with digestion enabled.
The [native boundary record](archive/resolved_bugs/native_add_rejects_valid_keep_ids_flags_during_argument_digestion.md)
retains 115 focused passes and 3 doctest passes; invalid flag types remain
rejected before mutation. This does not change the artifact/publication pause.

#355 repairs the general selector's empty `bonded to` operand. Positive/negative
queries retain set semantics, and the hydrogen-free 3,983-atom 1TCD protein now
supports acceptor/donor role identification and a named, evaluated-empty Buch
analysis. The [selector record](archive/resolved_bugs/empty_bonded_to_operands_break_hbond_role_identification.md)
retains 213 selection/hbond regression passes, an H5MSM coverage round trip and
the exact Viewer Python source reproduction. No hydrogen reconstruction,
scientific-method change or new browser/installed candidate qualification is claimed.

#357 corrects the dihedral output documentation: the quantity follows the active
PyUnitWizard angle policy, and numerical consumers explicitly extract their
required unit. Computation and defaults are unchanged. The
[angle-policy record](archive/resolved_bugs/dihedral_documentation_ignores_active_angle_policy.md)
retains six dihedral regression/control passes and one public doctest pass.
Foundations, Toolbox, Cookbook and the unit-safety course describe the same
contract. This source correction does not resume artifact qualification or publication.

The maintainer's further issue audit resolves #22's historical hydrogen-bond
output question through the existing sparse `Interactions` contract, and #123's
CI-skipping request through the existing controlled direct-push/backlog route.
[Output reconciliation](archive/resolved_proposals/hbonds_output_format_question_is_answered.md)
retains 30 Buch/Luzard-Chandler passes;
[CI reconciliation](archive/resolved_proposals/ci_skip_option_is_implemented_and_governed.md)
retains 21 backlog/workflow passes and corrects stale policy wording.
#358 repairs the public box-geometry return-unit contract and three Sphinx
rendering errors, with
[analytical units and rendering evidence](archive/resolved_bugs/box_geometry_documentation_misstates_units_and_fails_rendering.md).
These bounded corrections do not close #250/#254/#334 or resume publication.

#359 repairs real Biopython sequence recognition and the declared group-index/name
queries. The [sequence boundary record](archive/resolved_bugs/biopython_sequence_forms_reject_real_objects_and_declared_groups.md)
retains 13 public-facade passes and four doctest passes, including repeated/empty
selections and missing sequence content. The delivery audit now reports 74
unreachable declarations across seven forms; #139 remains open for that debt.
These Tier 2 read-only corrections do not select or qualify a replacement candidate.

#360 repairs the sequence copy, full extraction and identity-conversion routes.
The [copy/conversion record](archive/resolved_bugs/biopython_sequence_copy_and_identity_conversion_fail.md)
retains thirteen failing pre-repair controls and fifteen passing public cases
plus two doctest passes after repair, including independent nested record
metadata. Ordered Seq subsets work; SeqRecord subsets remain explicitly
unsupported. This correction does not broaden the Tier 2 support guarantee or
resume artifact production or publication.

#361 repairs the NGLView public example and unknown-target rendering error,
with seven distinct guard/doctest/color passes and one executed Python 3.14
Toolbox notebook. [NGLView resolution](archive/resolved_bugs/nglview_color_example_uses_obsolete_apis_and_fails_rendering.md)
records explicit backend choice and value/selection alignment. Runtime color
calculations are unchanged; #144 retains the remaining documentation debt.

#362 restores source atom-index delivery for INPCRD, using the existing header
count without coordinate materialization. [INPCRD resolution](archive/resolved_bugs/inpcrd_declares_atom_indices_without_delivery.md)
retains six failing controls before repair, 28 passing adapter cases and one
doctest afterward. These bounded corrections preserve the frozen candidates
and publication pause; they do not inherit artifact qualification.

## Qualified pair preparation — 2026-10-08

**Frozen producer:** MolSysMT **1.0.0, ABI3 build 0**, source
`6dc80725ea506f977fb5e52dfd701c2227875fa5`, remote branch
`candidate/1.0.0-build0`. The initially selected Viewer **0.24.1, noarch build 0**,
source `66ea54e45ff3b9498e5f6f668c3d519888dca7b4`, is now withdrawn by its
owner as the final candidate. The replacement is **0.24.1, build 1**, source
`ae1fb995d6a38f2df6df206d2af26fbde1531f24`, verified remote branch
`candidate/0.24.1-build1`; its file/hash are independently inspected below and
prerequisite gates are now reviewed. GitHub comparison verifies nine changed files: three workflow defaults,
one existing guard and five developer-guide records. No molecular or runtime
source changes require rebuilding the MolSysMT artifacts. The
[frozen-candidate receipt](../devtools/data/release_1_0_frozen_candidate_20261008.json)
records verified refs, local results and dispatch identities. Main may advance
with receipts while this producer stays fixed.

The [clean scientific certificate](../devtools/data/release_1_0_scientific_6dc80725e_20261008.json)
passes 54/54 cases from 47 nodes with zero omissions. Thirty local route/workflow
guards, the fourteen fast gates and Ruff pass. A fresh local Sphinx HTML build
succeeds with 782 warnings and zero nonexistent toctree references; #144 retains
the general warning debt. This compilation does not execute notebooks or publish
gh-pages. An initial scientific attempt correctly rejected the dirty tree caused
by Sphinx rewriting three generated RST stubs, despite all cases passing. After
the build, those reviewed stubs were restored and the clean certificate above
was obtained. The receipt retains both outcomes; they are overlapping checks.

Conda producer [37757683710](https://github.com/uibcdf/molsysmt/actions/runs/37757683710)
completes successfully on all four native platforms. The
[staging handoff](../devtools/data/release_1_0_staging_handoff_20261008.json)
records all four filenames/builds/URLs/SHA-256 values. Downloaded bytes, registry
hashes and original producer receipts agree. Actual version/build/upload/evidence
steps execute successfully on every platform. ABI3 metadata, canonical
distribution version 1.0.0 and eight source files match the producer, with only
Windows CRLF normalization. All four hashes were delivered to Viewer through
`codex queue`. This is file inspection, not installed-pair qualification.

The initial eight-cell source campaign
[37757713370](https://github.com/uibcdf/molsysmt/actions/runs/37757713370) and
native wheels [37757715875](https://github.com/uibcdf/molsysmt/actions/runs/37757715875)
used the withdrawn Viewer source and terminate cancelled after explicit
cancellation to avoid completing qualification against a superseded counterpart.
Preserve their original outcomes/artifacts; they do not qualify the replacement.
Four original Linux scientific certificate ZIPs emitted before cancellation
are downloaded and digest-verified; no full-suite JUnit artifact was present
in that campaign's inventory. New source qualification
[37759578359](https://github.com/uibcdf/molsysmt/actions/runs/37759578359) and
native wheels [37759580359](https://github.com/uibcdf/molsysmt/actions/runs/37759580359)
are dispatched on the same MolSysMT producer with the replacement Viewer SHA
explicitly supplied. Native qualification completes successfully: thirty jobs
pass and the PR-only job is the expected skip. Native job records confirm Rust
format/lint/tests and all four controlled installed public-smoke steps actually
execute. GH Run Receptor independently confirms the terminal result. The
eight-cell source campaign completes successfully; all eight original scientific ZIPs
are downloaded and digest-verified against the clean producer, all 47 nodes
and 54 passing cases with zero omissions. All eight original full-suite JUnit
ZIP/payload hashes, skipped-case reasons and required executed-step records are
verified. Each Linux cell records 13,301 passes and 26 skips; each macOS cell
records 13,300 passes and 27 skips, with zero failures/errors throughout. Native
logs confirm 40 default `peptide_parity` deselections per cell, which JUnit does
not record. Skips concern optional Ackredit, Vina, CuPy, unyt and astropy,
an RDKit-dependent expectation, and one Linux-only test on macOS; they do not
waive the separate zero-skip scientific certificate. GH Run Receptor confirms
the successful terminal source campaign. Viewer's independent review of the
original artifacts adds confidence, not test counts.

After both owners' prerequisite review and agreement, MolSysMT launches the
single [installed-pair staging matrix 37783010701](https://github.com/uibcdf/molsysmt/actions/runs/37783010701)
on `candidate/1.0.0-build0`, the exact producer above: **MolSysMT 1.0.0 build 0 /
MolSysViewer 0.24.1 build 1**, four native platforms by Python 3.11–3.14.
The preflight finds no previous installed-pair dispatch on that SHA. This
campaign checks clean Conda installation, version/provenance, native code,
BCIF, PDB-text loading and Viewer resources, retaining explicit environments.
It completes successfully on **16/16 cells**. All sixteen original environment
ZIP digests and payload hashes are verified. Explicit staging URLs, exact builds
and MD5 agree with the previously SHA-256-verified original package bytes; each
platform uses one native artifact across its four Python minors. All 64 required
installation, validation and environment-retention steps execute successfully.
GH Run Receptor confirms seventeen successful jobs and sixteen artifacts.
Consumer-specific interaction, browser and session evidence retains its own
scope; this smoke matrix does not execute those tests in every cell or change
Windows' experimental portability classification. Final #250/#254 acceptance
and #334 publication review remain pending. No public tag, Release or main-label
promotion is performed.

The replacement Viewer file is `molsysviewer-0.24.1-py_1.tar.bz2`, SHA-256
`ab2d6c2a7f8c165c7dc626e277724dcddf06b211f34149de685d0839c1bfde94`,
from owner producer `37758700492`. Independent download and registry inspection
confirm 1,518,815 bytes, noarch build 1 and the staging-only label. The
[replacement receipt](../devtools/data/release_1_0_viewer_build1_staging_20261008.json)
retains its metadata. Independent GitHub inspection confirms successful
Viewer Windows `37759393730` and core-browser `37758593628` campaigns on the
exact replacement source. Their consumer-installed scope remains separate.

The Viewer owner subsequently reports **322/322** guards with zero failures/skips:
191 design, Interactions, nine-family, H5MSM, session, paging and residency cases,
plus 131 composite-loading, source-origin, box and Studio cases,
on Linux/Python 3.14.8 using the exact 1.0.0 build-0 / 0.24.1 build-1 files.
Imports originate only in `site-packages` and `pip check` passes. This updates an
existing environment from verified original files; it is **not** a clean
solver-created installation or the sixteen-cell qualification. These are
owner-reported results, not independently rerun by MolSysMT. The earlier
191-test selection is included in 322 and must not be counted again.

Viewer canonical staging CI
[37760422583](https://github.com/uibcdf/molsysviewer/actions/runs/37760422583)
identifies the replacement source and selected versions. Its required scientific
jobs complete successfully: all six execute their `Run tests` step and pass.
The Qt job fails in its experimental scope under uibcdf/molsysviewer#109;
do not report that campaign globally green. The native job records and GH Run
Receptor retain its global failure alongside the successful scientific scope.
The Viewer owner confirms readiness for the single installed-pair dispatch;
MolSysMT independently reviews these terminal outcomes before launching it.

The Viewer owner initially delivers `molsysviewer-0.24.1-py_0.tar.bz2` from producer
`37757179478`, SHA-256
`88ad5b7497bdfa06f16a7e9a47996edd633dd5f63534d38e0b9a0a418478ee58`.
Independent download and registry inspection confirm that hash, 1,515,134 bytes,
noarch build 0, Python 3.11–3.14 metadata and the staging-only label. The
[file receipt](../devtools/data/release_1_0_viewer_staging_20261008.json)
does not claim installed or consumer qualification. The owner later reports
2,880 local passes, 23 skips and one workflow-default failure: the source-pair
workflow still defaulted to 0.24.0 while its release plan selected 0.24.1.
This is an owner-reported preparation failure, not a demonstrated molecular
regression. Viewer preserves build 0 and its branch and prepares build 1 with
corrected defaults. Do not replace or publish those original bytes. Agree one
installed-pair dispatch after the replacement's prerequisite gates are reviewed.

The initial preparation under `uibcdf/molsysmt#334` updates release metadata
and the staged route for **MolSysMT 1.0.0, build 0**, based on main
`b9954fa5e4ba1af5956613308211b90a37880e5c`, delivered at `0a7cfdd8a`. That
checkpoint precedes the frozen producer above and does not identify an
available package or a published release. The
[preparation receipt](../devtools/data/release_1_0_candidate_preparation_20261008.json)
records its checks and remaining exact-candidate gates. The older qualification
below retains its original identities and does not qualify these new files.

Authorized coordination with the existing MolSysViewer team initially fixes its
candidate as **0.24.1, noarch build 0**, source
`66ea54e45ff3b9498e5f6f668c3d519888dca7b4`, with immutable branch
`candidate/0.24.1-build0`. Native GitHub inspection verifies that branch against
the delivered full SHA. This replaces its earlier source-only checkpoint
`0067a2c27c152a068655b8824f0d1c249a32d6b8` and includes the already closed
uibcdf/molsysviewer#149 and uibcdf/molsysviewer#177. The owner confirms the
experimental compatibility contract and delivers the independently inspected
staged file recorded above. The public 0.24.0 build-1 baseline remains
historical evidence. No installed-pair matrix is dispatched before both new
artifact identities are available and inspected.

The frozen MolSysMT source retains that initial audited routine Viewer pin and
source-gate fallback. Manual full/native qualification must supply the accepted
replacement SHA explicitly; review its diff before reusing any evidence or
changing the producer. MolSysMT freezes `candidate/1.0.0-build0` at the committed
source selecting these routes, preserves that producer as later receipts are
recorded, and builds the staged files under the existing construction/upload
authorization. Source/native execution and staged-file delivery remain separate
from the later installed-pair claim. The preparation checkpoint `0a7cfdd8a`
passes all six applicable hosted checks, including smoke; those checks used the
previous Viewer baseline and do not qualify this new source pair.

MolSysMT confirms continuity of the implemented Interactions consumption
contract: sparse roles and compound participants, analysis-version occurrence
indices, evaluated-empty coverage, explicit selections, bounded pages, units,
producer provenance, periodic images, named analyses and H5MSM 0.5 maps/remapping.
Standalone import association remains an explicit declaration. The
[API contract](interactions_api.md), [query semantics](interactions_query_semantics.md)
and symbol stability registry retain their current authority. `Interactions`,
`InteractionsDict`, detector families and the page boundary remain experimental;
1.0 metadata does not promote their stability. Page bounds apply to occurrence
and participant copies after query construction, not to universal memory usage.
Public setters invalidate coverage; raw-array edits require explicit invalidation.
No new functional provider blocker or detector requirement was reported.

The installed-pair workflow requires the operator to supply Viewer version and
build explicitly rather than silently selecting obsolete default coordinates.
Initial preparation checks pass: 17 release-tool/workflow tests with twelve
workers and pytest-receptor, 14/14 fast gates, full-package and changed-test
Ruff, changed-test formatting and citation consistency for 1.0.0. These checks
exercise the prepared working tree, not a frozen release artifact.
#250/#254 remain open for their final-candidate
obligations. #334 still requires exact source/native/scientific, documentation
and installed-consumer qualification followed by the separate publication
approval. No public 1.0 tag, Release or main-label promotion is authorized by
this preparation.

## Qualified pre-1.0 checkpoint — 2026-10-07

**Stabilization follow-up — 2026-10-08:** main commit
`eab7aeb79cc397f92a08081766f5c25792503ae8` publishes the #349 repair and
the archived #251/#252 resolutions; all three owning issues are verified closed.
The separate [scientific certificate](../devtools/data/pre_1_0_scientific_eab7aeb79_20261007.json)
passes 54/54 cases from 47 registered nodes with zero skips/errors/failures
on that clean source. Remote smoke `37734610812`, Ruff, dependency contract,
devguide, suite policy and Conda governance pass on the same source.

The completed [full matrix](https://github.com/uibcdf/molsysmt/actions/runs/37734711393)
and [native wheels](https://github.com/uibcdf/molsysmt/actions/runs/37734713996)
retain that exact source and the published Viewer SHA. The native campaign
concludes success: thirty jobs pass and the PR-only runtime job is the expected
skip. Rust controls, four platform builds, sixteen runtime cells, four NumPy
floor checks, four installed public smokes and the source round trip execute.
GH Run Receptor independently confirms that terminal conclusion. This is native
qualification of the recorded development source, not public-package delivery.
The full source matrix concludes success on all eight Linux/macOS arm64 ×
Python 3.11–3.14 combinations. GH Run Receptor independently confirms the
terminal result. Nine jobs succeed, including the controlled Viewer build;
the PR-only aggregate job is the expected skip for manual dispatch.

All eight original scientific certificate ZIPs have been downloaded and
checked against GitHub SHA-256
digests: each identifies this clean source, matches all 47 registered nodes and
passes 54 cases with zero skips/errors/failures. All eight full-suite cells
also have verified original JUnit artifacts and native job logs:

| Platform / Python versions | Passed per cell | Skipped per cell | Deselected per cell | Failures/errors |
| --- | ---: | ---: | ---: | ---: |
| Linux, Python 3.11–3.14 (four cells) | 13,301 | 26 | 40 | 0 |
| macOS arm64, Python 3.11–3.14 (four cells) | 13,300 | 27 | 40 | 0 |

The JUnit receipt retains every skipped node and reason: absent optional
Ackredit, Vina, CuPy, unyt and astropy, the installed-RDKit negative path and,
on macOS, one Linux-only test. The default peptide-parity exclusion accounts
for the forty deselected cases; these are recorded separately from JUnit.
Every cell's native job record confirms executed fast gates, scientific
evidence, Ruff, the full suite and JUnit retention. Original ZIPs and logs
remain in the task-owned `/tmp` directory recorded by the bounded receipt.
The documentation-only heads `b777029e2` and `4d6ace0d6` pass their applicable
smoke, devguide, suite-policy and Conda-governance checks. Runtime sources,
tests, workflows and packaging are unchanged from the qualified `eab7aeb79`.
These receipts qualify that development source, not a different final 1.0
commit or newly installed release artifacts.

No new package or release tag is published by this reconciliation. The central
receiving owner has accepted #237/#244 under uibcdf/molsyssuite#51 at
`3116b7d9f1fa9ba4d09b81a8f24a22b749805f9f`, frozen by `policy-v1.5.9`.
MolSysMT is `admitted` for the immutable public 0.23.0 / Viewer 0.24.0 pair;
its applicable support-library/developer-tool reviews are `adopted`. The
caller/badge and canonical guide are delivered at
`a04ec0fa3a947a7c959b7f56b09301bb37eceb90`. Both owning issues are closed and
their reports are archived with addressable guards. Exact native conformance
`37742928564` and devguide `37742932367` execute successfully on that delivery;
GH Run Receptor independently confirms their terminal conclusions, and native
steps confirm conformance, Ruff lint and formatting actually ran. The central
delivery receipt is retained under uibcdf/molsyssuite#51.
Final 1.0 candidate gates under #250/#254/#334 remain mandatory and are not
waived by either this closure or the earlier public pair.
The latest 2026-10-08 read-only board review now finds only three open 1.0
issues: #250, #254 and #334. #139/#144 retain their accepted post-1.0 debt boundaries;
they are not evidence that every declared form route or documentation warning
has been corrected.

**Issue reconciliation:** #349 is reproduced and repaired after the published
checkpoint. Its public PDB name/topology guard passes with Pandas 2.3.3 and
3.0.6; the [bounded receipt](../devtools/data/pre_1_0_issue_reconciliation_20261007.json)
retains the initial failures and compatibility outcomes. The original 0.23.0
files remain unchanged and do not contain this later repair.

The subsequent complete shared-environment Linux/Python 3.14 source suite passes
13,327 cases with two skips, no failures/errors and 1,766 warnings in 407.20 s,
using twelve workers and pytest-receptor. The two skips are absent CuPy and
the installed-RDKit negative-path branch; their nodes/reasons and JUnit digest
are retained in the bounded receipt. A separate acceptance selection passes
129 cases; counts overlap the full suite and must not be added. All 14 fast
gates, full-package Ruff, changed-file formatting and developer-guide/index
checks pass. This is editable working-source evidence with the existing native
extension and recorded sibling versions, not a new exact-installed release
campaign. The shared environment has unrelated AmberTools auxiliary dependency
conflicts; no clean `pip check` claim is made for that environment.

Explicit published consumer acceptance now exists under the closed
uibcdf/molsysviewer#114. #251/#252's delivered design/implementation reviews
are resolved with their normative contracts and guards. #250/#254 retain their
explicit exact-1.0 obligations. The central receiving decision above reconciles
#237/#244 with the independently verified public-pair evidence. Native
source/public execution and exact files retain their original identities;
administrative admission is separate from fresh 1.0 candidate qualification.

Current development routes now select the published Viewer producer
`1a4c97a58b68b69f3a836546c9e4ac6187c3efa2`. Original release/source/file receipts
retain their historical pins. #334 still owns final 1.0 candidate selection,
qualification and publication approval; no 1.0 candidate is selected here.

The selected pair is **MolSysMT 0.23.0 / MolSysViewer 0.24.0**, under the
feature freeze in `uibcdf/molsysmt#334`. The coordinated pre-1.0 publication
checkpoint is complete; the separate 1.0 stabilization review remains open.
This checkpoint prepares the next pre-1.0 release; it does not select 1.0.0.

MolSysMT's four native ABI3 **build-0** files are available in
**`uibcdf/label/staging`**, from source
`46ef28eb60a258aa77d82ff1bc39ee0d1591e3c9` and producer run
[37534744593](https://github.com/uibcdf/molsysmt/actions/runs/37534744593).
The [staging handoff receipt](../devtools/data/stabilization_023_staging_handoff_20261006.json)
owns filenames, build strings, SHA-256 values, source comparisons and validation
limits. MolSysViewer can declare **`molsysmt>=0.23.0`** for the coordinated
Interactions, H5MSM 0.5, loading and box capabilities. Experimental interaction
contracts retain their current classification.

For GitHub manual dispatch, the temporary remote branch
`candidate/0.23.0-build0` points exactly to that producer SHA. Use it as the
`ref` for `validate_conda_staging.yaml`; GitHub's dispatch endpoint requires a
branch or tag rather than the raw commit SHA. Keep this branch fixed until
installed-pair qualification and evidence verification are complete, then
remove it during candidate-reference cleanup. It is not a release tag.

Executed evidence includes 14/14 fast gates, 54 scientific cases with no skips,
26 basic doctests, 35 tests importing the actual staged Linux payload and the
successful native-wheel campaign (30 jobs plus one expected PR-only skip).
The local full suite retains its original failed restricted-network invocation
and the successful recovery of all 33 affected cases; it is not recorded as a
second complete green invocation. Details and limitations remain in the dated
checkpoints and handoff receipt below.

Source run [37534217132](https://github.com/uibcdf/molsysmt/actions/runs/37534217132)
has completed successfully in all eight cells, using the earlier controlled
Viewer source `5bb59c0e13045ee0aaf34cf336a3533d611197bf`. The definitive Viewer
candidate is now **0.24.0, build 1**, from
`1a4c97a58b68b69f3a836546c9e4ac6187c3efa2`:
`molsysviewer-0.24.0-py_1.tar.bz2`, SHA-256
`e31dfb114ab2e49f22b372992d0201455b91849f2631d0165b802069e13abeaa`.
Installed-pair run
[37541876875](https://github.com/uibcdf/molsysmt/actions/runs/37541876875)
passes **16/16 cells** on MolSysMT's original candidate. Receiving inspection
verified every required install, runtime, environment-record and retention step;
the Viewer receipt agrees with all four MolSysMT artifact digests.

Viewer's exact canonical source run
[37542642197](https://github.com/uibcdf/molsysviewer/actions/runs/37542642197)
and Windows launcher run
[37542333568](https://github.com/uibcdf/molsysviewer/actions/runs/37542333568)
are successful. The Viewer owner records 39 core browser suites and 25 notebooks
in its receiving receipt at documentation commit `3465e563`, under
`uibcdf/molsysviewer#93` and `uibcdf/molsysviewer#114`.

MolSysMT source run
[37577738386](https://github.com/uibcdf/molsysmt/actions/runs/37577738386)
has completed successfully from the fixed candidate branch with the **final
Viewer SHA**: **8/8 cells** pass. All eight downloaded scientific certificates
identify the original clean MolSysMT candidate and pass **54/54 cases** across
47 registered nodes, with zero scientific failures, errors or skips. The eight
JUnit reports each contain 13,323 cases and zero failures/errors: Linux has
13,297 passes and 26 skips per cell; macOS has 13,296 passes and 27 skips.
Recorded omissions cover optional Ackredit, Vina, CuPy, unyt and Astropy, the
installed-RDKit negative-path case, and a Linux-only test on macOS. This is the
workflow's declared test/doctest scope, not a claim that every optional backend
was exercised there. The additive `coordinated_publication_review` in the handoff
receipt retains every certificate/JUnit digest and the original observations.
The maintainer has authorized MolSysMT publication; its public package records
are now verified. Paired public installation and archival remain pending.

With the maintainer's final authorization on 2026-10-07, tag **0.23.0** and
[GitHub Release 0.23.0](https://github.com/uibcdf/molsysmt/releases/tag/0.23.0)
are published on the qualified source. The four original ABI3 build-0 files are
promoted to **`uibcdf/main`** without rebuilding. Downloaded promotion and
independent public-verification receipts agree with all original SHA-256 values
and verify each file's `main` label and solver-visible index. Successful runs:
linux-64 `37583470115`, linux-aarch64 `37583473201`, osx-arm64 `37583476153`,
win-64 `37583479224`. Their evidence and digests are retained in the receipt's
`publication_checkpoint`. MolSysViewer has received the public-provider handoff
through its existing session. Its build-1 publication is now complete, as
recorded in the coordinated checkpoint below.

The first Zenodo receipt, run `37583386427`, retains **`ingestion_pending`**.
Read-only reprobe `37583715416` now reports **`verified`** for the exact version,
repository and concept family, with version DOI **10.5281/zenodo.23205366**.
The archived source file is `uibcdf/molsysmt-0.23.0.zip` (153,784,473 bytes,
`md5:9e2aa4844c6b8ef030b92dcca6bc7bd3`). The receipt preserves both probes;
the public project-level concept DOI remains 10.5281/zenodo.1298752.
The paired 16-cell **public** installation matrix is now complete and verified,
as recorded below; both source-version archival records are also verified.

Hosted documentation run `37583385927` completes successfully on the release
source; this does not erase the previously recorded warning debt. Release Conda
route run `37583386011` now completes successfully in all four native jobs.
Its staged route skips rebuild/upload; the four separate promotion runs already
verified the original public files.

MolSysViewer [0.24.0](https://github.com/uibcdf/molsysviewer/releases/tag/0.24.0)
is public. Receiving checks resolve its tag to the original candidate
`1a4c97a58b68b69f3a836546c9e4ac6187c3efa2` and confirm successful promotion run
`37587274965`. The Viewer owner verifies the original build-1 digest,
`main` label, solver index and npm/CDN recovery run `37586395370`; publisher-only
recovery is owned by `uibcdf/molsysviewer#176`. Downloaded Zenodo receipt
`37587205154` reports **`verified`**, version DOI **10.5281/zenodo.23206053**,
source ZIP 24,560,894 bytes and `md5:7335fc5b63254d841ea0184aadfdce3f`.

Public installed-pair run
[37587631519](https://github.com/uibcdf/molsysmt/actions/runs/37587631519)
is dispatched **once** from `candidate/0.23.0-build0` on the exact MolSysMT
source, with MT 0.23.0/build 0, Viewer 0.24.0/build 1, Python 3.11–3.14,
all four platforms and `package_source=public`. It completes successfully in
**16/16 cells**, with all four required install/runtime/environment/retention
steps approved per cell. The provider downloaded all sixteen original ZIPs,
verified their GitHub SHA-256 digests and checked exact public URLs, build
filenames, Python minors and MD5/SHA-256 against original package bytes and
registry records. The receipt retains every ZIP/environment digest and the
installed identities. The Viewer owner independently verifies the same sixteen
environments and publishes its final receipt at
`fd8f499e5216df432fd5f52c67647983a935ce27`, under
`uibcdf/molsysviewer#93` and `uibcdf/molsysviewer#114`.

The additional native read-only verification run `37591619395` is queued at
this checkpoint. It will check the completed matrix without rerunning its
installations; retain its receipt after execution.
This closes the coordinated **0.23.0/0.24.0 pre-1.0 publication** checkpoint.
It does not declare 1.0, settle every experimental profile or close owning
acceptance issues without their required guard/normative reconciliation.

Use [Resume from here](#resume-from-here) for the remaining sequence. Earlier
dated observations preserve history; their pending statements do not supersede
this checkpoint.

## Scope freeze and next work — 2026-10-05

The maintainer has frozen feature scope at `d609187ae` under
`uibcdf/molsysmt#334`. The [normative scope decision](release_1_0_scope.md)
now owns admission, the finite S1–S6 stabilization queue and the preserved
post-1.0 issue inventory. Start there before taking another implementation
task. This is a scope decision, not release certification.

S1's fresh triage of #25/#30/#112 is complete in the checkpoint below. S2's
acceptance reconciliation and public validation completion are recorded below.
S3's current preparation profiles are qualified in the checkpoint below.
S4 public-claim reconciliation and S5 workflow/dependency progress are recorded
below. Obtain updated MolSysViewer feedback and complete the remaining executed
Python/provider evidence before freezing exact candidates. No additional chemistry or method
expansion is admitted implicitly. Viewer owns canvas/browser/Qt and session
presentation; its integration feedback is required, while other client
integrations remain outside the initial release gate.

The bounded native PDB policy/application is implemented through `7b51c240f`,
with its generated API view corrected in `d609187ae`. The #304 record retains
532 focused tests, the final boundary check, original-input comparisons,
storage/time observations and their limits. Broader H/terminal/group/disulfide
inference and performance qualification now remain post-1.0 in #304.
Current code may ship experimentally without implying complete receptor preparation.

Deferred individual observation editing, streaming/resumable H5MSM, specific
metal-coordination rules and longer water paths have separate owners
#335/#336/#337/#338. Compatible structure replacement, compaction, bounded
resident export and existing one/two-water methods are already implemented.

The historical 99% weighted campaign below is not a measure of current
stabilization effort. S1–S6 are not certified complete by this documentation
checkpoint; no new heavy suite, installed-candidate matrix or release artifact
is produced. Existing Python/policy obligations and exact-candidate gates remain.

## S1 stabilization checkpoint — 2026-10-05

- #30: GRO-to-MDTraj now reuses the existing native connectivity policy while
  retaining MDTraj's multi-structure coordinate/time/box reader. The original
  NGLView GRO is byte-identical to the bundled fixture. Its former 152 components
  become one under the native candidate rules. The
  [resolution record](archive/resolved_bugs/gro_mdtraj_connectivity_bypasses_native_inference.md)
  distinguishes route consistency from chemical validation.
- #112: no-site native PDB input already yields `None`; a new public PDB/MolSys/
  H5MSM guard protects it. Present sparse attributes keep empty maps and the
  requested structure axis. See the
  [absence record](archive/resolved_bugs/empty_alternate_locations_preserve_absence.md).
- #25: existing local names and source metadata remain supported. Verified
  database identity is a separate enrichment capability; the
  [remaining proposal](pending_proposals/local_molecule_names_and_external_enrichment.md)
  stays open in `Post-1.0`. Deferral is not a claim that enrichment is implemented.

The affected Python 3.14 suite passes 819 tests, including three converter
doctests, in 358.97 s. Ruff, dependency loading/routes, the 263-symbol API
registry, devguide, archive restoration, scientific-registry structure and the
maintained 156-module course validator pass. Notebook executable cells and
saved outputs were unchanged. This is scoped development evidence, not a
full release matrix or an installed-candidate check.

Sphinx HTML compilation passes in the existing Python 3.13 documentation
environment with 40 recorded warnings. The routine 3.14 environment lacks
documentation extensions; #237/S5 retains that qualification work. The legacy
`docs/content/course/devtools/validate_course.py` still diagnoses obsolete
section names; the normative route is `devtools/scripts/validate_course.py`.
It does not replace the maintained course gate or certify missing legacy headings.

On previous head `0efb14144`, remote runs 37366063932 and 37366064781 ended
with failure after GitHub could not acquire a hosted runner. Their jobs have
no runner and no executed steps; Conda governance passed. This is missing
remote evidence under #334, not a code-test failure or a gate waiver. Inspect
the applicable runs after the unskipped S1 checkpoint and recover any still
unexecuted controls before exact-candidate qualification.

S2's newer evidence follows. Keep S3–S6 within the frozen scope.

## S2 provider/consumer checkpoint — 2026-10-05

At clean provider `4d048a78d466728c2fa9a12befacc22182b71d23`, the Python 3.14
result/native/public-H5MSM selection passed 279 tests in 37.14 s. A separate
namespace/detector/codec/doctest selection passed 77 tests and failed one
sandbox network download; the exact failed 5XJH node then passed with network
access in 3.94 s. The
[dated artifact](../devtools/data/interactions_review_packet_20261005.json)
retains both outcomes, selected hashes, runtime versions and fixture hashes.

Local Viewer `eb14716f982be87f66ef8dea5218262bbabdad1d` completed four real
workloads and all nine-family/two-water-order scenarios. Ten initial/restored
structure projections match; five lifecycle analyses retain producer versions,
execution records and exported scene state through a session. Its three local
sandbox design files and Ackredit's nine edits were preserved. These checks
qualify Python data/protocol compatibility, not browser/Qt geometry, a clean
installed pair, large-system performance or the S6 matrix.

The [updated review packet](interactions_molsysviewer_review.md#s2-stabilization-review--2026-10-05)
maps #250/#251/#252/#254 acceptance to existing guards and prepares a message
for the maintainer to forward. No external message was sent. Explicit current
Viewer feedback, agreed combined-memory measurements and final candidate gates
remain open. These reports stay partial. Original class constructor/query/remap
methods needed review at this baseline; the subsequent checkpoint below clears
#252 criterion 2 with tested ArgDigest behavior, without granting an exception.

Stale active-proposal claims about missing remapping, H5MSM embedding and native
ownership are corrected. Historical experimental measurements are preserved;
#335/#336 continue to own the deferred editors and streaming/resumable writes.
No runtime API, scientific criterion, dependency or format was changed.

Remote governance, policy and devguide runs at this provider head succeeded;
Ruff 37369027830 and CI smoke 37369027887 later ended with run failure and
cancelled jobs 111961192306/111961193123. Both have no runner and no executed
steps; GitHub annotations report that no hosted runner acquired the job after
multiple attempts. This is infrastructure evidence, not failed lint/scientific
assertions. Missing execution remains #334 evidence to recover on the next
unskipped head before qualification, not a waiver. Next finish the bounded public class
validation review (now completed below); progress S3–S5 while obtaining Viewer feedback.

## S2 public validation completion — 2026-10-05

Provider `0959a0f7cf3ecf6352d0ed714afacf441563c8b6` completes ArgDigest for
construction, inspection, original/invalidated/recalculated queries, remapping
and standalone persistence. Integer counts and indices refuse booleans and
fractions before encoding; periodic vectors refuse overflow; typed evidence
decoding cannot truncate fractional codes. Record generators are preserved.
Original positional arguments/defaults remain; skip options are keyword-only
and reserved for already validated inputs. Stored cross-column/file invariants
remain active. No method, dependency or file-format extension was introduced.

The corrected broad selection passes 1,520 tests in 211.99 s. The final
source-block delegation guard passes 116 tests in 5.43 s; selections overlap.
The [dated artifact](../devtools/data/interactions_argument_validation_20261005.json)
retains initial failures, source phases, dependency versions and hashes. The
[owning report](archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md#s2-acceptance-reconciliation--2026-10-05)
records the remaining criteria. #252 is partial; criterion 2 now has a guard.

Ruff, formatting, dependencies, signature/API registries, docstrings, course and
devguide checks pass. Foundations, Toolbox, Cookbook and Module 04 are updated;
course executable cells and saved outputs remain unchanged. Sphinx HTML passes
with 27 warnings in the existing Python 3.13 documentation environment; #237/S5
still owns Python 3.14 documentation-tool qualification. Nine Cookbook and five
initial Toolbox blocks execute; later contextual snippets are not one standalone
script. This is scoped development evidence, not an installed/full release matrix.

At preceding documentation head `dcccc730e`, CI smoke 37371423746 passes.
Policy/devguide/Conda checks ended with no runner or executed steps (jobs
111969243288, 111969240011, 111969242582). The policy annotation confirms hosted
runner acquisition failure. Inspect the next unskipped head and recover missing
execution under #334 before qualification. The maintainer reports Codecov's
service problem resolved; coverage publication still requires evidence from its
next applicable executed gate.

Next: S3's existing preparation/SDF/PDBQT/native profiles; then S4 documentation
claims and S5 environment/dependency policy. Obtain current Viewer feedback in
parallel through the prepared maintainer-forwarded message. No new feature is
admitted and the 1.0 tag remains conditional on S6 exact-candidate gates.

## S3 preparation/form qualification — 2026-10-05

**Contract-tested current frozen profiles**, at provider
`fe0b813d7267f4c5a0728264094441e62c910e1b`: 1,094 preparation/form cases pass
in 380.42 s, without skips. A separate native pipeline, mapped-H reinsertion,
public H5MSM mechanics-exclusion and doctest selection passes 80 cases in
38.82 s, without skips. Runtime, tests and dependency inputs remain unchanged;
this checkpoint corrects explanations rather than extending chemistry.
The [dated artifact](../devtools/data/preparation_profiles_20261005.json)
records commands, source/fixture hashes, actual producer and dependency versions,
warnings and interpretation limits.

| Included contract | Executed evidence | Remaining boundary |
| --- | --- | --- |
| Native SDF graph/charge/isotope/coordination and explicit stereo | `tests/form/file_sdf/`, including the synthetic corpus and original 5X72 stereoisomers | Vina 1IEP valence overrides and versionless 1S63 SDF remain deliberate rejections, not malformed sources. No silent RDKit fallback or complete parser parity claim. |
| Prepared PDBQT file/string/native exchange | `tests/form/file_pdbqt/`, independent MDAnalysis reading and Vina parsing | Source serial IDs align reordered output; BRANCH evidence is partial connectivity. No implicit preparation, H merging or universal torsion policy. |
| Declared template transfer and scoped context | `tests/physchem/test_chemical_template*.py`, readiness/inventory and peptide-template guards | Explicit maps/states, conservative global completeness, retained pose and unknown checks; no template authentication or readiness certificate. |
| Fixed-state H and mapped reinsertion | `tests/build/add_missing_hydrogens/test_fixed_state.py`, `test_preparation_history.py`, and `tests/build/add_terminal_atoms/test_component_hydrogen_reinsertion.py` | Explicit RDKit, one declared state/structure, retained original atom coordinates/indices; generated H geometry is local, without environmental refinement. |
| Named charges, AutoDock types and torsion candidates | Charge/type assignment guards, `tests/topology/test_get_rotatable_bonds.py` and original Vina comparisons | Neutral-amine typing and aryl–nitrile/amide torsion differences remain explicit policy evidence; parameter assignment is not full force-field preparation. |
| Bounded native inference and PDB engine policy | Candidate/application guards and `tests/form/file_pdb/test_connectivity_policy.py` | Declared edges retain precedence; inferred orders stay unknown, coverage partial, history indexed to the operation and changed analyses invalidated. Broader chemistry stays #304. |
| History, units and conservative exclusions | Native/H5MSM history guards, non-default units, native protein/pH pipeline and public mechanics-rejection tests | H5MSM retains original chemical-preparation evidence, while nonempty MolecularMechanics is rejected before file creation; #256/0.6 owns its persistence. |

The normative conversion guide now reflects implemented completion/context and
historical report storage. The PDBQT recipe links implemented assignment/torsion
tools and states the H5MSM rejection; it is registered with its page contract.
The protein/pH pipeline distinguishes its supported templates from fixed-state
ligand H and no longer claims identical provider pKa rules or missing ACE/NME H
support. Common Core 12 already describes these contracts; no executable notebook
cell or saved output changed. The maintained 156-notebook course check passes.

All 96 adapters pass structural checks and the delivery ratchet; the existing
78 unreachable declarations remain #139 debt. Sphinx HTML passes incrementally
in Python 3.13.14 with 26 warnings, without a warning naming the changed PDBQT
recipe. This does not qualify Python 3.14 documentation tools. One NumPy size-change
RuntimeWarning occurred in the broad scientific run and did not recur in fresh
selected-provider imports; S5/#237 retains its origin/installed-ABI review. Other
warnings report legacy H5MSM, pandas/provider deprecations and declared metadata
loss/protonation policies; the artifact records counts rather than hiding them.

Published DockingMT #33 consumer evidence is inspected, including the initial
prepared-input slice and later readiness/charge/H/fragment migrations. It is
historical evidence, not a fresh consumer run on this provider. That integration
does not block this bounded S3 qualification or certify scoring/preparation.
#214/#215/#304 remain partial with their scheduled post-1.0 extensions.
No runtime defect is reproduced within these tested profiles.

S3's bounded local review is complete; S4's newer checkpoint follows. Continue
with S5 dependency/Python policy; keep current Viewer feedback and all S6 source,
installed-artifact, platform and publication requirements open. The preceding
head's policy, Conda governance and devguide runs pass; smoke/Ruff remain queued
at this observation. No full-suite backlog or release gate is waived.

## S4 public presentation checkpoint — 2026-10-05

The README now identifies MolSysMT as a core molecular-system library in
MolSysSuite, qualifies experimental capabilities where claimed, removes its
broken contributor link and replaces stale form counts/full-support wording
with the maintained route contract. Package/Conda metadata, landing and About
pages agree; the existing citation abstract already states this role. No API
stability or form classification was promoted (#186/#192).

The native hero's optional-engine absence guard found #339: native solvation
implicitly delegated water-template reading to OpenMM. The correction reads
without optional inference, uses the existing general native water bond tool
and rebuilds the semantic hierarchy. It qualifies all four existing models
with OpenMM/PDBFixer imports forbidden. No new chemistry is admitted by #334.

For #199, 47 legacy transparent export heads were refreshed using a template
from MolSysViewer's public exporter. All 49 bodies are byte-identical before/
after, retaining scenes, producer versions and runtime references. Six actual
Chromium iframe/screenshot checks of three representative heads match both
host themes. They qualify head/base-canvas behavior, not scientific scene
replay, Viewer interaction geometry or session restoration. The provider's
three sandbox files and four-commit behind state were preserved.

The [dated artifact](../devtools/data/public_presentation_20261005.json)
records 48 passing tests, zero skips, the solvation doctest, commands, runtime
versions and tested hashes. The [header artifact](../devtools/data/static_view_headers_20261005.json)
retains the producer, original/current/body hashes and browser measurements.
Negative controls reject unqualified claims, broken links, unrelated suite
mentions and inert/late/missing header corrections. Expected legacy H5MSM
warnings and TIP4P-EW virtual-site-name warnings remain explicit.

Ruff, dependency loading/contract, citation and the maintained 156-module
course validator pass. Homepage executable cells and stored outputs are
unchanged. Incremental Sphinx compilation passes in Python 3.13.14 with 17
warnings; #144/#237 retain documentation warning/environment qualification.
This is scoped development evidence, not installed/exact-candidate evidence.
At published source `a0d6fc896`, CI smoke, dependency contract, devguide and
Conda governance pass. Ruff 37379969985 and policy 37379970731 execute and
fail because four new tools/tests need formatting; the earlier focused local
lint check did not cover that second requirement. The follow-up formats those
four files, verifies identical Python ASTs and runs both complete Ruff checks.
Scientific runtime code and all scene bodies are unchanged. Inspect the new
unskipped head's controls before treating this remote checkpoint as complete.

Next: S5 dependency/Python review, current Viewer feedback and all S6 gates.
No release tag or GitHub Release has been published by this checkpoint.

## S5 dependency/Python checkpoint — 2026-10-06

- #245: dependency-route coherence and mutation guards pass; the proposal is
  [resolved](archive/resolved_proposals/audit_dependency_contracts_across_packaging_environments_and_ci.md).
  This certifies static contracts, not installed binary compatibility.
- #286: the actual automatic producer at `a8f567c82` has a complete processed
  Codecov report and numeric SVG. The badge is restored with scope in README.
  The [resolution](archive/resolved_proposals/restore_current_coverage_reporting.md)
  preserves its real 11 failures and 26 skips; reporting does not clear test debt.
  No scientific suite was launched solely for coverage.
- #237: routine routes select 3.14; full source qualification now has eight
  Linux/macOS arm64 × 3.11–3.14 cells. Weekly recovery retains all four Linux
  minors and recurring macOS arm64. Wheel runtime matrices include 3.14 with
  an available Python-specific NumPy wheel floor. The debt guard rejects an
  omitted minor and weekly artifacts do not collide. Hosted/installed evidence
  and central admission remain pending; the proposal remains partial.
- #244: current focused unit and argument contracts pass; #236 is already
  resolved and #155's optimization review stays post-1.0. The integrated full
  gate and exact installed closure remain required; no exception is manufactured.

The [scoped artifact](../devtools/data/stabilization_s5_20261006.json) retains
89 passing focused cases, expected legacy-file warnings, policy source, solver
limits, old full-suite failure nodes and Codecov/XML measures separately. All
14 fast gates and applicable Ruff checks pass. Fresh Python 3.14 docs compile
with 784 recorded warnings and no missing course toctree documents; #144 retains
the warning inventory. The docs extra supplies the actual configured extensions.
Homepage executable cells and saved outputs are unchanged.

The initial S5 head `5e4106433` passes remote contract, Ruff, policy, devguide
and Conda governance. Smoke `37422022941` creates the complete Python 3.14
environment but pip rejects the old DepDigest pin's `<3.14` metadata; subsequent
tests are skipped. #237 corrects the manifest to exact published DepDigest
0.13.0 and SMonitor 0.18.0 sources and verifies isolated installation; inspect
its corrected head separately. The original failure remains visible.

Corrected provider head `ce769ffb7dc803fa514e48667e2a3e77b56911f0` executes and
passes Python 3.14 smoke `37423046917`; its package installation, dependency
validation, form/docstring/Rust controls and actual test step all pass. Remote
Ruff `37423046945`, dependency contract `37423046946`, devguide `37423046920`,
policy `37423047391` and Conda governance `37423047467` also pass. The actual
released-provider selection passes 102 scoped cases and all 14 fast gates.
This settles the first routine installation defect, not full-matrix admission.

Fresh triage reproduces four stale catalogue expectations from the old full
producer. #340 adds actual pinned Vina PDBQT file/text detection routes and
explicit SDF/PDBQT supported-table entries; the independent census is retained.
The [resolution](archive/resolved_bugs/catalogue_guards_omit_the_admitted_sdf_and_pdbqt_forms.md)
and [artifact](../devtools/data/catalogue_guards_20261006.json) retain four
initial failures and 45 passing catalogue/real-PDBQT cases without skips.
Fresh triage of the seven remaining old failure nodes with Python 3.14,
pytest-receptor and twelve workers passes the missing-RDKit absence contract and
the converter-table guard. Five caller assertions still assume reconstruction
outside the native profile accepted in #322. #341 corrects the mutation/capping
coverage claims and tests without changing placement algorithms. Its
[resolution](archive/resolved_bugs/mutation_and_terminal_repair_claims_bypass_the_bounded_native_placement_contract.md)
and [receipt](../devtools/data/bounded_repair_callers_20261006.json) preserve the
initial five failures, 87 passing repair cases, two passing public doctests,
exact missing inventories and unchanged observed/source coordinates. All runs
use `--receptor=llm -n 12`. Warnings remain recorded. At `b1fc6b3a5`, actual
Python 3.14 smoke `37425890605` and the applicable remote Ruff, devguide, policy
and Conda-governance controls pass.

The complete local Python 3.14 source suite finishes with exit 1: 13,191 passed,
43 failed, 25 errors and 14 execution skips, in 1,225.59 s with 2,152 warnings.
JUnit additionally retains seven collection skips; these are not seven more
executed tests. DNS-blocked downloads contribute long retries. A network-enabled
retry of the 68 failed/error nodes passes 35 and retains 25 failures/eight errors
in 18.35 s. Missing ParMed, PyTraj and OpenFF explain the optional-provider routes;
MOL2 currently requires ParMed explicitly. This is not a green complete suite.
The [execution receipt](../devtools/data/stabilization_s5_execution_20261006.json)
preserves original outcomes, failed/skipped nodes, log/JUnit identities and scope.

#342 corrects a stale dependency guard that patches a removed private loader
alias; real filtering and missing-library diagnostics now execute with restored
configuration. #343 corrects supported pandas 3 missing-name/membership and
read-only NumPy-export behavior without changing chemical criteria. The same
271-case selection passes without skips on pandas 3.0.6 (17.90 s) and pandas
2.3.3 (18.57 s). The receipt distinguishes initial and intermediate failures;
warnings remain visible. These selections are scoped editable-source evidence.
See the [dependency-guard resolution](archive/resolved_bugs/dependency_architecture_guard_patches_a_removed_depdigest_loader_alias.md)
and [pandas resolution](archive/resolved_bugs/native_topology_operations_fail_under_pandas_3_missing_value_and_copy_semantics.md).

The completed shared development environment now supplies ParmEd 4.3.1,
PyTraj 3.0.0.dev0 through AmberTools 26.0, OpenFF Toolkit 0.19.0, unyt 3.1.0
and Astropy 8.0.1. At clean source `5e2721691`, the 75-selector recovery
passes 109 cases without skips. The complete Python 3.14.7 source suite then
passes 13,313 cases, with two skips, no failures/errors and 1,763 warnings,
in 473.85 s. Both use twelve workers and `--receptor=llm`; their overlapping
counts must not be added. The two skips concern the installed-RDKit SMILES
branch and absent optional CuPy. The separate registered scientific gate passes
all 54 cases from 47 nodes with zero skips and a clean-source certificate.
Its maintained runner deliberately executes serially.

Fresh shared-environment Sphinx compilation exits 0 with no missing course
toctree documents, 781 warning lines and five Docutils error lines. These
existing markup/reference defects remain accepted #144 debt; successful
compilation is not a warning/error-free claim. Notebook execution is disabled,
and generated formatting rewrites were restored.

The [shared-environment receipt](../devtools/data/stabilization_s5_shared_20261006.json)
retains actual versions, commands, hashes, skips, scientific certificate and
documentation errors. The released support providers are pinned, but Viewer
is an editable sibling undergoing concurrent changes; its imported version
and installed metadata differ. These results are development evidence, without
an immutable Viewer-candidate claim. Earlier failed runs remain recorded.
All 14 fast release checks pass after the evidence/documentation update.

S6 preparation then identifies #344: the wheel smoke's manual dependency list
omits required mmcif, and controlled PyUnitWizard 0.28.1 requires ArgDigest
0.14.0 while the old pin supplied 0.13.0. Earlier successful editable execution
does not establish a coherent installed closure. The
[correction report](archive/resolved_bugs/wheel_smoke_accepts_incomplete_runtime_dependencies.md)
and [preflight](../devtools/data/wheel_dependency_preflight_20261006.json)
retain four initial failures, 37 passing corrected guards and actual rejection
of the old closure. The published ArgDigest 0.14.0 pin and installed-metadata
checks address both gaps. At clean `865ff6ec6`, the corrected complete shared
suite passes 13,313 cases with two skips and no failures/errors (404.84 s),
and the separate scientific certificate passes all 54 cases without skips.
All four installed wheel public smokes resolve and validate the real required
closure; the 3.14 smoke installs mmcif 1.2.0 from the wheel metadata.

Wheel run [37438849560](https://github.com/uibcdf/molsysmt/actions/runs/37438849560)
has 29 successful jobs, one failure and one expected pull-request-only skip.
Four builds, sixteen current-NumPy runtime cells, four NumPy-floor cells, four
public smokes and the sdist round trip pass. The global result is **failure**
because Rust formatting rejects one import ordering; Clippy, Rust tests and
cargo-deny have not executed. The local format correction passes Rust 1.97.1,
but its exact-source wheel workflow must execute before qualifying this layer.
The [execution receipt](../devtools/data/wheel_execution_20261006.json) retains
actual artifact bytes/digests and all limits. Published Viewer 0.23.4 is the
fixed smoke baseline, not the final current integration candidate. No package
is published. This is stabilization within the frozen scope.

On corrected source `5bd893c85`, wheel run
[37441629705](https://github.com/uibcdf/molsysmt/actions/runs/37441629705)
concludes **success**: thirty jobs pass and the pull-request-only profile is
the expected skip. Format, Clippy, all 81 Rust native tests and cargo-deny
execute successfully. Four wheel builds, sixteen current-NumPy runtime cells,
four floor cells, four installed public smokes and the sdist round trip pass.
The [corrected receipt](../devtools/data/wheel_corrected_execution_20261006.json)
retains original producer/artifact identities and independently hashed bytes.
#344 is resolved with its dependency-closure regression guard.

Full source run [37441978743](https://github.com/uibcdf/molsysmt/actions/runs/37441978743)
uses the same exact MolSysMT source and Viewer baseline. All eight Linux/macOS
Python 3.11–3.14 cells pass their registered 54-case scientific certificate
without skips; their full suites are still executing at this checkpoint.

S5 is still partial for full-matrix/installed admission evidence. Next obtain
Viewer feedback, agree exact provider/Viewer candidates and execute the required
eight-cell source and installed wheel/Conda pair gates for S6.
No release tag or GitHub Release is published. Configured eight-cell matrices,
solver success, focused editable tests and an accepted badge are not S6 evidence.

## Reported-defect review — 2026-10-02

Legacy H5MSM unit reads now share explicit, validated metadata across queries,
conversion, iteration and migration; conflicting or missing units fail clearly
(uibcdf/molsysmt#240). Group-free native atom metadata returns None without
inventing residues (uibcdf/molsysmt#233). The root argument-validation instruction
uses the real arg_digest boundary (uibcdf/molsysmt#231).

Formal closure also records the already-merged Windows path correction,
explicit rejection of unsupported partial-charge snapshots, verified public
Conda resolution and mmCIF conversion, and the CI trigger/backlog contract
(uibcdf/molsysmt#241, #234, #195, #200, and #185). MolecularMechanics
persistence remains post-1.0 in H5MSM 0.6.

The observed scheduled run 37008569379 at 78981d6c1 executed all three
Linux Python 3.11–3.13 suites but failed three policy tests per cell. It
still installed Viewer source 7a1522662e30575caf580a9447e3e6d80b628e07.
Routine pins and the default full-candidate fallback now use the verified
public 0.23.4 source cf427942d0b08a1c5c60f262c6a6b33f248d6f8b
(uibcdf/molsysmt#293). The corrected public pair passes the policy guard;
this is not yet a new green hosted full matrix. Explicit candidate SHA inputs
remain mandatory for the actual 1.0 qualification decision.

General adapter-delivery debt (uibcdf/molsysmt#139), documentation build debt
(uibcdf/molsysmt#144), and older reports requiring fresh reproduction stay
open; this closure does not certify them or establish release readiness.

## Resume from here

Release advancement is paused by the maintainer decision relayed above. The
sequence below describes retained evidence and the former release route; do
not execute its publication/closure steps or new qualification campaigns until
the owners agree the new candidate direction after the Viewer discussion.

The [2026-10-10 source-delta review](pending_proposals/freeze_1_0_scope_and_complete_bounded_stabilization.md#source-delta-for-coordination-resumption--2026-10-10)
maps post-producer stabilization and addon retirement to existing guards and
remaining installed-consumer checks. It is preparation for resumption, not a
replacement candidate selection or executed qualification. The reviewed source
is explicit; later changes require a renewed delta review.

The [frozen scope](release_1_0_scope.md) governs admission. The published pre-1.0
pair is **MolSysMT 0.23.0 / MolSysViewer 0.24.0**; its files and executed evidence
are recorded in the current checkpoint above and the
[staging handoff receipt](../devtools/data/stabilization_023_staging_handoff_20261006.json).
Keep MolSysMT's original package producer and source SHA even when later commits
correct developer tooling or update this ledger.

1. Retain the completed publication evidence with the finite S1–S6 queue
   under `uibcdf/molsysmt#334`, and review the owning native/result acceptance
   issues. The 16/16 public pair, 8/8 final source matrix and verified Zenodo
   receipts are a completed pre-1.0 baseline, not automatic 1.0 sign-off.
2. Preserve the frozen MolSysMT producer `6dc80725ea506f977fb5e52dfd701c2227875fa5`
   and its four original 1.0.0 build-0 files. The selected Viewer counterpart is
   `ae1fb995d6a38f2df6df206d2af26fbde1531f24`, 0.24.1 build 1. Current candidate
   source/native qualification explicitly supplies this replacement SHA; the
   routine pins frozen with the producer still describe the initial Viewer
   source. Do not move refs or rebuild artifacts solely to change those pins.
   Historical source/native campaigns `37734711393` / `37734713996` remain
   pre-1.0 development evidence, not a 1.0-artifact claim.
3. Retain the completed central receiving response for #237/#244 under
   uibcdf/molsyssuite#51 and this delivery's administrative conformance. Version
   metadata, the staged route and both current artifact identities are recorded
   above. The exact eight-cell source campaign `37759578359`, native campaign
   `37759580359` and required Viewer prerequisites are reviewed. The sixteen-cell
   installed-pair staging campaign `37783010701` also passes; its original
   explicit environments and exact-file/runtime outcomes are verified and
   retained. Do not dispatch a duplicate. Reconcile consumer-specific interaction,
   browser and session evidence separately from the clean-install smoke scope.
   #250/#254 retain their final-candidate checks and #334 owns qualification and
   publication approval. Keep feature scope frozen; extensions retain their
   post-1.0 owners. A final-candidate failure returns its affected scope to
   stabilization rather than reopening feature development.
4. Preserve original package/ZIP/environment identities, the read-only matrix
   receipt and both version DOIs. Retire the temporary candidate branch after
   all reference-dependent verification and owner reconciliation are complete;
   the qualified tags remain fixed.

The public 0.22.4/0.23.4 pair and the
[Python 3.14 checkpoint](python_3_14_checkpoint.md) remain historical installation
and development evidence. They do not select the current producer, replace its
qualification or authorize publication.

The [interaction-detection namespace proposal](pending_proposals/organize_interaction_detection_by_family_before_1_0.md)
(`uibcdf/molsysmt#250`) has been accepted for the bounded pre-1.0 migration of
hydrogen-bond methods and disulfide-candidate detection. The bounded namespace,
detector migration and persistence routes are implemented in the staged
candidate. The published pre-1.0 pair now supplies consumer and exact-candidate
qualification evidence; owning acceptance closure and 1.0 stability decisions
still require explicit reconciliation. Separately approved
experimental ionic, pi-pi, cation-pi, halogen, hydrophobic, metal-candidate and
one- and two-water hydrogen-bond families are now implemented; these are not new 1.0
requirements. Metal-specific rules and paths through more than two waters remain
extensions. The public `Interactions` contract (#251),
optional native `MolSys` attachment and H5MSM persistence (#252), and a tested
MolSysViewer integration (`uibcdf/molsysviewer#114`) are now required before
the 1.0 candidate freeze. Native attachment, local-to-source maps, declared
atom search scope, and standalone and grouped HDF5 codecs have focused tests.
Public H5MSM 0.5 round trips for named analyses and supported partial `MolSys`
combinations are contract-tested. Incremental interaction editing and bounded
public file access remain unsupported. The experimental consumer contract is
agreed; the pre-1.0 pair is qualified, while 1.0 stabilization remains open.
The [S2 review packet](interactions_molsysviewer_review.md#s2-stabilization-review--2026-10-05)
records local provider/consumer projection and session parity for all nine
families and both water orders. This supersedes the earlier two-family local
smoke, while actual canvas acceptance and installed-pair qualification remain
separate obligations.
TopoMT, PharmacophoreMT, and DockingMT integrations do not gate 1.0.

The 2026-10-01 naming/attribution checkpoint at clean provider `e21f03d99`
adds scientific/descriptive selectors, exact profiles, compatibility aliases
and detached optional Ackredit bibliography. Whole-library and suite-wide
adoption remain partial under `uibcdf/molsysmt#27`, `uibcdf/ackredit#75` and
`uibcdf/molsyssuite#68`. Real local MolSysViewer qualification passed four
scientific workloads, geometry/query checks and H5MSM/session round trips.
A new optional public-client guard also passed for original bibliography,
producer versions and absence of reader calculation credits (18 focused tests,
none skipped). [The implementation record](archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md#consumer-and-attribution-checkpoint--2026-10-01)
identifies the clean provider, dirty consumer source and measurement limits.
This advances local interoperability; it is not an installed published-pair
qualification, a new browser/GPU run or the exact-candidate 1.0 release gate.

The 2026-10-01 detector checkpoint adds an experimental cation-pi API with the
attributed ProLIF 2.2.2 core definition as default and a separately named MolSysMT
proposal. Its original-detector parity, declared hydrogen conversion repair,
forms/units/scopes/PBC/persistence, executed documentation and bounded scale
measurements are recorded in
[the completed implementation report](archive/resolved_proposals/implement_cation_pi_observations_with_reusable_charge_and_plane_tools.md)
and [the benchmark guide](benchmarking/cation_pi.md).
The general SMARTS tool belongs to topology. Broader scientific comparison remains
open in uibcdf/molsysmt#271 and does not gate 1.0; no claim of superior physical
accuracy or a passed final release-candidate gate follows from this checkpoint.
The 2026-09-29 integration inspection found that H5MSM 0.4 extraction
materializes and rewrites a full `MolSys`; it cannot preserve attached
interactions and now rejects that export. Native copy, extraction, atom
addition, and structure append have bounded experimental rules. On 2026-09-29 the
scope decision advanced the full H5MSM 0.5 modular layout, with separate
chemical-state and interaction layers, onto the pre-1.0 path; the earlier
0.4.1 extension candidate was withdrawn. An explicit public
`molsysmt.h5msm` API now reads and writes the 0.5 layout and offers a
0.3/0.4-to-0.5 migration helper. Public `molsysmt.convert` now writes 0.5 by
default and reads 0.5 through the native codec; legacy adapter operations remain
for 0.3/0.4. Reading a legacy file emits an actionable warning without dropping
support. This is not release evidence. Candidate freeze awaits
remaining 0.5 form operations, schema coverage,
the required lifecycle gates, and exact-candidate MolSysViewer tests. The runnable
experimental provider handoff has already enabled `view.interactions` development;
current client evidence must still be agreed before the MolSysMT result API is
stabilized. `ChemicalStates` is now a separate
native domain; its wider release validation remains open.
H5MSM 0.5 native routes now round-trip all seven primary combinations
of topology, chemical states, and structures, preserving absent layers through
copy and pickle. Full field fidelity, general append behavior, and large-trajectory gates
remain open. Public `read` now reconstructs a partial native `MolSys` from
named interaction-only payloads, using their declared atom and structure
index domains. A present-empty interaction layer still requires `read_layers`
because it declares neither domain.
Native 0.5 write/read now also round-trips structures plus named interactions
without chemical states, with or without topology, and rejects missing
interaction-axis associations instead of guessing from matching lengths.
The public structures-only read path is guarded for coordinate-bearing and
time-only files: both become partial `MolSys` objects with absent topology and
chemical states, and the time-only case retains an unknown atom count.
The public
0.5 writer now round-trips typed bioassembly transforms, including translations
converted from angstroms to nanometers in the bundled TcTIM BinaryCIF case.
Sparse alternate locations now round-trip through the public 0.5 route on
the bundled PDB example, and structure IDs retain integer or string type.
Sparse alternate-location columns can append when both stored and incoming
blocks declare them. `MolecularMechanics` remains a minimal, experimental
native domain before 1.0. Its persistence is explicitly deferred to H5MSM
0.6 after 1.0 (`uibcdf/molsysmt#256`); H5MSM 0.5 has no mechanics layer and rejects nonempty
mechanics data before writing rather than dropping it.
The public topology-free file path can append complete frame rows and read
nonconsecutive selections,
including files with chemical states and atom-axis links. It can extend one
structure-to-state map when new state indices are supplied. Append involving
topology, interactions, other structure-axis associations, and crash recovery
are still unimplemented.

For the MolSysViewer review of `uibcdf/molsysviewer#114`, the public parity
test `tests/interactions/test_public_molsys_h5msm_workflow.py` and
`devtools/scripts/create_molsysviewer_interactions_fixture.py` now provide
synthetic native and H5MSM 0.5 examples. The fixture generator writes both a
complete `MolSys` file and an interaction-only file that loads as a partial
`MolSys`. The [review packet](archive/resolved_proposals/design_a_sparse_public_interactions_result_and_serialization_contract.md#runnable-molsysviewer-review-packet)
states the implemented query contract and current limitations. MolSysViewer has
accepted the experimental handoff and local qualification has advanced as
recorded above. The original fixture packet alone is not an exact-commit
1.0 release gate.
An expanded local selection covering H5MSM, native forms, interactions,
`MolSys` adapters, conversion, structure append, hydrogen bonds, and
disulfides passed 1,347 tests on 2026-09-29. Ruff, public API stability,
form adapter, dependency, and devguide checks also passed. This dirty-checkout
evidence must be repeated on a review commit before candidate certification.

Use at most 12 pytest workers with `--receptor=llm` for compact local
diagnostics; normal pytest verdicts remain authoritative. Use
[the GH Run Receptor guide](../GH_RUN_RECEPTOR_GUIDE.md) for hosted-run
inspection.

## Status Vocabulary

| Status | Meaning |
| --- | --- |
| `DONE` | The declared exit gate passed with recorded evidence on an identified commit. |
| `IN PROGRESS` | This is the active segment or stage; work has started but its exit gate is not complete. |
| `PENDING` | Accepted work that has not started or cannot start until an earlier dependency closes. |
| `BLOCKED` | Work cannot advance because a named external decision, defect, resource, or prerequisite is unresolved. |
| `DEFERRED` | Explicitly outside the 1.0 critical path unless new correctness evidence promotes it. |

Only one top-level segment should normally be `IN PROGRESS`. If independent
packaging work runs in parallel, record the responsible branch or collaborator
and do not merge it across an unmet integration dependency.

## Pre-1.0 public distribution milestone — 2026-09-25

**Platform policy update (2026-09-27):** Future candidates exclude macOS Intel
(`osx-64`/x86_64). The supported macOS architecture is Apple Silicon (arm64).
The active native Conda matrix is four platforms and, for Python 3.11–3.14,
16 installed-pair cells. Earlier five-platform/20-cell results below remain
valid historical evidence for the published 0.22.4/0.23.4 pair, not future
release requirements. See `uibcdf/molsyssuite#59` and `uibcdf/moli#31`.

MolSysMT 0.22.4 and MolSysViewer 0.23.4 are published GitHub Releases on
their exact tested commits. Their ABI3/noarch Conda artifacts were promoted
as six immutable files; independent public-channel queries verified each
filename and SHA-256. The [public installed-pair matrix](https://github.com/uibcdf/molsysmt/actions/runs/36129993869)
passed 20/20 across five platforms and Python 3.11–3.14, with public
provenance and runtime/BCIF/PDB-text/Viewer-resource checks. The prior
staging matrix passed 20/20 in run `36121427459`. This closes the coordinated
package-availability milestone that had blocked normal Viewer CI.

The promotion action steps and receipt uploads passed, but the final
duplicated post-promotion verifiers falsely ended red after printing each
correct public URL (`uibcdf/molsysmt#246`, `uibcdf/molsysviewer#105`,
`uibcdf/molsyssuite#48`). The public matrix is independent evidence; do not
claim those promotion jobs passed. A replacement read-only verifier passed
on GitHub for the exact public MolSysMT file in
[run 36227235698](https://github.com/uibcdf/molsysmt/actions/runs/36227235698)
and for Viewer in
[run 36227243079](https://github.com/uibcdf/molsysviewer/actions/runs/36227243079).
The original verifier's exit-1 mechanism remains unknown; the old runs remain
red and were not rerun. Both Zenodo version records are now
published and independently verified: MolSysMT 0.22.4 has version DOI
`10.5281/zenodo.22959294`, and Viewer 0.23.4 has version DOI
`10.5281/zenodo.22959304`. They arrived after the initial 900-second
polling window; MolSysMT's verifier also required a tree-tag identifier
absent from the valid record and was corrected under `uibcdf/molsysmt#247`.
This does not imply that Conda/npm artifacts were archived by Zenodo;
the records contain source ZIPs only (`uibcdf/molsyssuite#49`). Viewer
visible-window Qt and complete hosted E2E are explicit
pre-1.0 exceptions, not 1.0 sign-off (`uibcdf/molsysviewer#100`). The
MolSysSuite-wide 3.14 admission decision is separate (`uibcdf/molsyssuite#29`).

## Historical 1.0 certification baseline — not replaced by the 0.22.4 release

The F5/F6 evidence below records the earlier 1.0 workstream and its weighted
closure. Its older commit coordinates are historical 1.0-gate evidence, not
the current `main` head or the 0.22.4 tag. Publication of a pre-1.0 pair does
not close F6. The historical 99% belongs to that campaign's weighted plan;
it does not estimate the remaining scope after later implementation changes.

- **Active segment:** F — lifecycle and release candidate
- **Active stage:** F6 release sign-off and 1.0 tag
- **Historical weighted closure:** 99% of the earlier remaining-plan campaign
- **Historical development evidence:** Segments A and B passed their gates;
  the final exact-commit campaign passed the bounded two-backend oracle,
  independent scientific evidence, and all 9,774 effective application tests
  with Rust forced
- **Historical F5 repository state:** F1–F5 were closed in the earlier
  certification campaign. The recertified F5 candidate
  `38ab61f6e` passed the complete fast, smoke, documentation, wheel, and
  Linux/macOS Python 3.11--3.13 gates after the bounded pre-1.0 corrections.
  That candidate used the published ArgDigest `0.12.0`; a subsequently found
  silent alias collision is fixed upstream and raises the source dependency
  floor to the then-planned `0.12.1` patch release. PyUnitWizard was at
  `0.24.0`. Those coordinates are historical; a new 1.0 candidate must use
  and verify current published dependency floors.
  The remaining Common Core
  exception was removed in `c87a14036`: all 20 modules now use their permanent
  semantic manifest identities and the validator pins the 1–20 contract. The
  PyTraj, OpenFF, OpenMM construction, and missing-converter work that followed
  the 2026-08-07 snapshot is landed through `929d4363e`
- **Historical exact Rust campaign commit:** `6485a0c08`; this is verified
  migration evidence but was not itself a release candidate; Segment F
  lifecycle work was still open at that checkpoint
- **Historical exact Rust packaging commit:** `17be9ea50`; C2 was verified by a
  clean exact-commit `cp311-abi3` wheel and installed-extension smoke
- **Historical C3 exact evidence commit:** `f79ccb4f0`; all five native abi3
  wheels build, audit, install, execute the private-extension smoke, and upload
  successfully in GitHub Actions run `30346103646`
- **Historical C4–C7/E4 exact evidence commit:** `c4d8e9074`; five native wheels,
  15 platform/Python installed checks, three NumPy floors, three public smokes,
  the sdist round trip, and Rust quality/security gates pass in GitHub Actions
  run `30394881487`
- **Historical E3 exact evidence commit:** `692479097`; 9,585 tests passed, two were
  accepted skips, and the fast release gate passes 12/12
- **Historical F5 exact candidate:** `38ab61f6e`; fast gates passed 12/12 locally,
  full matrix run `31781216880` passed on Ubuntu and macOS with Python
  3.11--3.13, wheel run `31781218931` passed the supported Linux/macOS build
  and installed-runtime matrix (with Windows green as experimental evidence
  only), documentation run `31781220979` passed, and smoke run `31781199983`
  passed
- **Current release readiness:** no numerical completion estimate; the
  [frozen scope queue](release_1_0_scope.md) and exact-candidate evidence define
  what still needs closure
- **Normal pytest:** the authority for test results
- **pytest-receptor:** the systematic compact reporter; disagreements must be
  reported upstream immediately
- **Next action:** complete S1–S5 of the frozen scope, using the published
  0.22.4/0.23.4 pair only as an installation baseline, then run every 1.0
  release gate on one new exact candidate before
  any 1.0 tag. Its own GitHub Release and distinct Zenodo version DOI still
  need post-publication verification; the pre-1.0 pair does not close F6
- **Parallel packaging action:** Segment C and installed-wheel validation are
  closed. The separate Conda delivery track has passed staging **and public**
  20-cell, five-platform installed-pair matrices across Python 3.11–3.14.
  Future 1.0 coordinates still need their own exact-candidate gates, but
  public availability of the 0.22.4/0.23.4 pair is no longer pending
- **Parallel documentation and paper action:** with A–E and F1–F5 closed, the
  presentation surface, the documentation and the methods paper are a principal
  parallel workstream rather than a finishing touch. The framing and factual
  corrections landed as `d2b805e74`. Of the three items that required a maintainer
  decision, two are settled on 2026-08-07: Daniel Ibarrola-Sánchez is not an author
  and was removed from `CITATION.cff`, which also removes the ORCID misattributed to
  him, and the unreferenced duplicate landing page is deleted. F6 now selects the
  existing MolSysMT concept DOI, corrects every public citation surface, and separates
  the pre-tag metadata gate from post-release verification of the version DOI. The
  lifecycle is normative in `release_and_citation.md` and executable through the fast
  gate and release workflow. Only the timing of the
  Conda installation instructions remains open, in
  [Presentation and Citation Surface](pending_proposals/presentation_and_citation_surface.md).
  Public-facing code examples must be executed against the installed package
  before they are written: the 2026-07-29 audit found that none of the README's
  examples ran
- **Known independent release-gate debt:** the F6 working candidate passes the
  expanded fast release gate 13/13 on 2026-08-14, including the new citation
  metadata gate. Form-adapter delivery is green with 89/89 forms, 78 accepted
  lower-tier declarations across nine forms, 343 resolved baseline
  declarations, and no Tier-1 debt. Conversion fidelity reports 40 exhaustive
  Tier-1 edges, 441 accepted non-exhaustive edges, 29 resolved baseline edges,
  and zero new debt

The 99% figure measures only the newly defined remaining-plan exit gates. It
does not attempt to restate the much larger body of MolSysMT development,
consolidation, or Rust kernel work completed before this ledger was created.

## Historical F6 blocker assessment — 2026-08-19

The following assessment describes the 2026-08-19 candidate, not the newly
published 0.22.4/0.23.4 pair. Recheck its source pins and workflow triggers
against current `main` before carrying either item into a new 1.0 candidate.

Both are recorded here rather than tracked elsewhere because they block the tag
itself, and a release blocker with no home is how the 2026-08-17 weekly failure went
four weeks unread.

**The pinned MolSysViewer revision is stale, and `ci-full` is red because of it.**
Deferred by maintainer decision on 2026-08-19; local suites are green and the
deferral is not a disagreement about the diagnosis.

`.github/workflows/{ci-full,ci-smoke,ci-weekly,sphinx_docs_to_gh_pages}.yaml` all pin
`molsysviewer@7a1522662e30575caf580a9447e3e6d80b628e07`, dated 2026-08-13 and 26
commits behind that project's `main`. The pinned revision predates `a80270a2`,
"adopt the shared MolSysSuite unit policy", so it declares the old mass standard and
`tests/cross_repo/test_unit_policy_authority.py` fails — 3 tests, identically on
ubuntu and macOS across Python 3.11, 3.12 and 3.13, with 9 980+ passing around them.

Note that the Conda channel is irrelevant here: `devtools/controlled_sources.txt`
installs the suite projects from pinned Git revisions with `--no-deps`, precisely so
the solver cannot substitute them. Publishing a package does not move this pin.

**`ci-full.yaml` runs only on `workflow_dispatch`.** `release_gate.md` requires a
green matrix on the exact committed tag candidate, and nothing produces one
automatically. This was excluded from the scope of `uibcdf/molsysmt#171`, which
covered running the suite on push.

Both must be resolved before F6 can be signed off. Neither affects library
correctness: the fast gate is 13/13 and the full suite passes locally.

## Segment Ledger

| Segment | Weight | Status | Earned | Current evidence or reason |
| --- | ---: | --- | ---: | --- |
| A — conversion-fidelity coherence | 25% | `DONE` | 25% | 40 exhaustive Tier-1 edges, 441 accepted non-exhaustive edges, 29 resolved baseline edges, zero new debt, and all conversion/form gates pass |
| B — final Numba oracle | 10% | `DONE` | 10% | exact commit `6485a0c08` passes the 264-test bounded two-backend oracle, combined scientific and blocker gates, and the complete forced-Rust suite with 9,769 passed and 5 accepted skips; the dated artifact preserves source and binary hashes |
| C — Rust packaging | 20% | `DONE` | 20% | C1–C7 pass: permanent backend, private abi3 integration, five native wheels, Python 3.11–3.13, NumPy floors, sdist/package parity, and Rust quality/security gates |
| D — Rust-only cut | 20% | `DONE` | 20% | the runtime, dependencies, tests, controls, and GPU experiments are Numba-free; compatibility facades route to Rust, the executable zero gate passes, and the affected scientific surface passes 450 tests |
| E — scientific and ecosystem validation | 15% | `DONE` | 15% | E1–E6 pass: Rust/scientific/full-suite gates, installed-wheel matrix, maturity-weighted consumers, and runtime/thread benchmarks |
| F — lifecycle and release candidate | 10% | `IN PROGRESS` | 9% | F1–F5 are done; only F6 sign-off and the verified tag remain |
| **Total** | **100%** | **`IN PROGRESS`** | **99%** | A–E use complete segment gates; F uses the explicit stage weights below |

The detailed A–E notes below preserve the earlier certification campaign.
Their dated uses of "current" and "next" refer to that campaign, not the
present F6 handoff at the top of this file.

### Historical B4 Pause Checkpoint — Transactional Structural Growth

At the time of this pause, the uncommitted vertical defined one
structural-axis contract for
`Structures`, `StructuresDict`, `MolSys`, `append_structures()`, and
`concatenate_structures()`:

- topology-free structural sources remain valid when atom counts match;
- every materialized structural series covers the complete structure axis;
- append validates the source and target before mutation;
- `attribute_policy='intersection'` retains shared series and reports all
  discarded one-sided attributes;
- `attribute_policy='strict'` rejects one-sided attributes without modifying
  the target;
- the public API, User Guide, Common Core course, and native contract describe
  the same behavior.

Evidence before pausing:

- focused native/API gate: 51 passed;
- expanded native-form/H5MSM gate: 1,254 passed;
- warning reconstruction and public structural-growth gate: 20 passed;
- both edited User Guide notebooks parse as valid JSON;
- pytest-receptor agreed with pytest on every verdict and exit code.

That checkpoint subsequently landed. Its then-next work was the remaining
NGL adapter causes and an exact-commit Rust wheel and forced-Rust release
gate; it is not the present instruction to resume or a claim that today's
worktree contains that WIP.

The H5MSM 0.5 independent-layer design discovered during this vertical is
recorded separately in
[H5MSM 0.5 Modular Layer Contract](pending_proposals/h5msm_0_5_modular_layers.md).
It is not part of this implementation checkpoint or the default 1.0 critical
path.

### B4 NGLView Fidelity Checkpoint

The three remaining NGLView causes from the first campaign are closed in this
checkpoint:

- MolSysMT-created single-component widgets retain an isolated private topology
  snapshot instead of losing identifiers and chemical bond metadata through
  PDB;
- external, empty, coordinate-only, and multicomponent widgets do not
  implicitly acquire that snapshot or claim topology they do not contain;
- multi-structure trajectories keep their complete coordinate axis without
  retaining one-structure PDB metadata as a partial series;
- group-level hydrogen-bond rendering preserves the input pair order instead
  of relying on the canonical sorted selection result.

Evidence at landing:

- complete NGLView surface: 45 passed under forced Rust;
- broad conversion/get/compare/view/PDB/Structures surface: 746 passed under
  forced Rust;
- Ruff and `git diff --check`: pass.

The instance-level contract is recorded in
[NGLView Adapter Contract](nglview_adapter_contract.md). With this checkpoint
landed, B4 has no known targeted application root cause remaining and must move
directly to the new exact-commit campaign.

## Segment A — Conversion-Fidelity Coherence

**Canonical bug:**
[Conversion Fidelity WIP Exposes Multiple Contract Gaps](archive/resolved_bugs/conversion_fidelity_wip_contract_gaps.md)

| Stage | Status | Dependency | Closure evidence required |
| --- | --- | --- | --- |
| A1 — audit-scope contract | `DONE` | none | landed as `504df91d0`; scope API, compatibility, tests, and lifecycle docs complete |
| A2 — exhaustive native-dictionary audit | `DONE` | A1 | three evidence-backed native-to-dictionary profiles landed; 51 focused tests and the Tier-1 ratchet pass |
| A3 — independent schema/adapter repairs | `DONE` | A1–A2 stable | direct native projections and all four builder routes have evidence-backed exhaustive reports; the broad native-scope module is green |
| A4 — PDB fidelity | `DONE` | A1–A2 stable | one handler-owned normalized parser feeds file, text, and handler routes; 22 fidelity tests and the historical PDB corpus pass; 11 exhaustive profiles landed as `1f656fe9f` |
| A5 — segment integration gate | `DONE` | A1–A4 | 40/481 edges are exhaustive, 441 are accepted debt, 29 baseline edges are resolved, zero are new; adapter delivery and lifecycle gates pass |

| A2 cohort | Status | Evidence |
| --- | --- | --- |
| A2.1 — `Structures -> StructuresDict` | `DONE` | exhaustive 22-attribute contract partition, current schema-loss reporting, strict rejection, lifecycle documentation, and conservative fidelity ratchet landed as `cb123e226` |
| A2.2 — `Topology -> TopologyDict` | `DONE` | 76-attribute contract partition, 24 value-dependent loss candidates, multi-state collapse, conditional aromatic mapping, strict rejection, and lifecycle documentation landed as `4a4773986` |
| A2.3 — `MolSys -> MolSysDict` | `DONE` | composed 114-attribute contract, seven structural losses, 18 mechanical losses, state association, strict rejection, and lifecycle documentation landed as `01067f2c5` |

### Completed A1 Objective

Implement one authoritative scope contract:

1. add backward-compatible `ConversionIssue.scope`;
2. add `get_conversion_audit_scopes(source, target)`;
3. add `is_conversion_audit_exhaustive(source, target)`;
4. make the helpers authoritative for conservative static graph coverage;
5. let instance-aware reports strengthen the static result only with explicit
   evidence;
6. keep the exhaustive-pair registry empty until A2 implements and tests the
   corresponding schema traversal.

### Current A1 Non-Goals

- exhaustive schema traversal, which belongs to A2;
- independent schema and adapter fixes, which belong to A3;
- PDB identifier and strictness repairs, which belong to A4;
- implementing or repairing the complete conversion graph;
- Rust packaging or Numba deletion.

### Conversion Critical-Path Rule

A conversion blocks Segment A only when it exposes:

- shared audit or conversion infrastructure failure;
- silent corruption or incorrect success;
- atom/structure misalignment;
- an advertised Tier 1 contract violation;
- new, unclassified fidelity debt.

Known, reported non-exhaustive behavior and low-priority Tier 2/3 routes remain
visible in the baseline or backlog and may be addressed later. They must not be
silently reclassified merely to make the gate green.

### A2 Cohort Design

The native-dictionary audit is divided into three reviewable cohorts:

1. **A2.1 — `Structures -> StructuresDict`:** classify every semantic in the
   declared `molsysmt.Structures` form contract as preserved, derived, absent in
   the source instance, or lost by the current dictionary schema.
2. **A2.2 — `Topology -> TopologyDict`:** apply the same contract to stable
   topology and chemical-state semantics, including optional bond and atom
   state fields.
3. **A2.3 — `MolSys -> MolSysDict`:** compose the proven topology and
   structures audits, then add molecular-mechanics and
   structure-to-chemical-state association semantics.

`is_exhaustive` is relative to the declared public semantic contract of the
source form, not every private implementation field and not every attribute
that another form happens to expose. Derived attributes are not reported as
lost when their required information remains representable.

Each cohort requires an explicit conversion-schema manifest. The ordinary form
`attributes` mapping is not sufficient evidence: it describes query
capabilities, while conversion fidelity asks which source semantics the
specific serializer actually preserves. This distinction is already visible
in `TopologyDict`, whose capability declaration mirrors `Topology` although
the current 0.1 serializer stores a narrower payload.

The first cohort is deliberately `Structures -> StructuresDict`: its native
storage contract is bounded, and it can prove the audit machinery before the
multi-state topology model is involved. A2.1 must report current unsupported
thermodynamic and bioassembly payloads honestly; extending the dictionary
schema or converter remains an independent A3 repair.

### A2.2 Topology Profile Design

The `Topology -> TopologyDict` profile covers the 76 attributes declared by
the native topology form. It must classify them in the following groups:

1. **Direct stable inventory:** atom, group, chain, molecule, and entity
   identifiers, names, types, membership, isotope, bond endpoints, formal bond
   order, and bond relationship type written by the 0.1 converter.
2. **Derived without loss:** indices, counts, inner-bond views, bonded-atom
   views, and biomolecule counts whose complete source data remain available.
3. **State-inventory limitations:** multiple chemical states collapse to one
   resolved state; a non-default state identifier, reference-state choice, and
   completeness/evidence metadata require value-aware checks.
4. **Component limitations:** version 0.1 has no component section. Connectivity
   can reconstruct a partition, but explicit component membership and
   component IDs, names, types, completeness, and evidence are not thereby
   proven preserved.
5. **Optional atom-state limitations:** formal charge, aromaticity, radicals,
   implicit-hydrogen policy, and stereochemistry are absent from the 0.1
   payload.
6. **Optional bond-state limitations:** bond ID, fractional order, conjugation,
   stereochemistry and reference atoms, donor/acceptor direction,
   component-joining semantics, and evidence are absent.
7. **Conditional aromatic mapping:** the converter can encode an aromatic flag
   through the legacy `bond_order="aromatic"` value only when no formal bond
   order takes precedence. The audit must not call this preservation in a
   source row that carries both semantics.

Presence checks must inspect the selected native chemical state directly.
`Topology.has_attribute()` is a public query-capability helper and currently
returns true for some default or absent state metadata; using it blindly would
create false losses. Multi-state inspection must cover every stored state even
when a reference state exists, because the serializer emits only one state.

A2.2 reports current schema losses. It does not add fields to `TopologyDict`,
change component inference, or repair an independent converter defect. Those
remain focused A3 work.

### A3 Repair Partition

The nine remaining failures in the broad native-scope module are not one gate:

| Cohort | Classification | Release treatment |
| --- | --- | --- |
| unconditional preflight on ordinary `convert()` | systemic performance and layering defect | first A3 repair |
| `atom_index` and `n_atoms` not classified as structural | central attribute-policy contradiction | second A3 repair |
| missing thermodynamic series in `StructuresDict` | schema and two-way adapter gap | focused A3 repair |
| `StructuresDict -> MolSys` lacks `skip_digestion` | adapter signature defect | focused A3 repair |
| unconditional `chemical_state_id` expectation for a `None` ID | WIP test-contract error | correct the test; do not invent an ID or loss |
| native `MolSys` projections | additional exhaustive route profiles | assess after systemic repairs; not part of the dictionary-profile gate |
| `MolSys <-> MolSysBuilder` and builder-to-dictionary routes | additional exhaustive route profiles | assess after systemic repairs; do not make them block unrelated work |

The four coordinate-trajectory failures are also route-promotion requests
(`XYZ`, ASCII XYZ, DCD, and XTC), not demonstrated conversion failures. Their
selection, units, and cursor assertions execute beyond the report assertion.
They remain visible candidates for bounded Tier-1 profiles but do not join the
A3 critical path merely because they request `is_exhaustive=True`.

The PDB `evidence` and `int("fram")` symptoms belong to A4 with the rest of the
PDB fidelity causes. Moving them out of A3 prevents a PDB-specific parser
workstream from blocking independent schema repairs.

A3 order:

1. bypass preflight when no report or strictness is requested;
2. align atom-inventory attribute classification;
3. extend and round-trip the selected `StructuresDict` thermodynamic fields;
4. repair the `skip_digestion` adapter signature;
5. correct the invalid `chemical_state_id` expectation;
6. decide which remaining native projection or builder profiles are required
   for the advertised 1.0 Tier-1 surface and defer the rest explicitly.

| A3 cohort | Status | Evidence |
| --- | --- | --- |
| A3.1 — opt-in conversion preflight | `DONE` | ordinary conversion bypass, explicit-report execution, strict rejection, public doctest, and lifecycle documentation landed as `dd13cb351` |
| A3.2 — atom-inventory classification | `DONE` | shared topological/structural classification, focused policy tests, 74 consumer tests, lifecycle documentation, and course validation landed as `998abe325` |
| A3.3 — `StructuresDict` thermodynamic series | `DONE` | two-way unit-bearing series, derived total energy, ordered selection, capability queries, report preservation, lifecycle documentation, and 19 focused tests landed as `006d9e4ed` |
| A3.4 — `StructuresDict -> MolSys` signature | `DONE` | standard signatures, correct local mechanics adapter, matched selected atom axes, lifecycle documentation, and 15 form tests landed as `ab28213c0` |
| A3.5 — invalid state-ID expectation | `DONE` | WIP expectation corrected without fabricating an ID; explicit tracked regression landed as `0434b9b42` |
| A3.6 — remaining native/builder profiles | `DONE` | direct projections, complete builder contracts, builder routes, and bounded coordinate-trajectory profiles are integrated |

A3.6 is split so incomplete builder metadata cannot block or weaken direct
native projection evidence:

| A3.6 cohort | Status | Decision and closure boundary |
| --- | --- | --- |
| A3.6a — direct native projections | `DONE` | four Tier-1 profiles traverse every declared source attribute with instance-aware scope and strict-loss evidence; 37 focused tests and the 481-edge ratchet pass; landed as `c40e3154e` |
| A3.6b — complete native/builder attribute contract | `DONE` | native presence composes stored state; builder declares the exact 96-attribute topology/structures union and delivers every declaration directly; landed as `53fec7b09` and `eb07e6e28` |
| A3.6c — builder conversion profiles | `DONE` | four routes are exhaustive; selected dictionary export canonicalizes atoms, preserves structure order, reports reduced-schema loss, and reconstructs components without inventing hierarchy fallbacks; landed as `4bc1dde7b` |

Direct projection profiles may use one declared-contract traversal shared by
the four approved pairs. This is exhaustive only because it iterates every
attribute the source form declares, performs instance-aware presence checks,
and records every present attribute unsupported by the target with its
topology, structures, chemical-state, or molecular-mechanics scope. It must
not be applied to `MolSysBuilder` until the builder's declaration matches its
actual stored semantics.

A3.6b has two ordered prerequisites:

1. **A3.6b.1 — native instance presence.** Complete and test
   `Topology.has_attribute()` and `Structures.has_attribute()`, then make
   `MolSys.has_attribute()` compose those authoritative helpers rather than
   duplicate partial lists. Minimal empty objects currently report absent
   `temperature`, energy, occupancy, bioassembly, state-ID, and component
   metadata as present; reference-state semantics require an explicit
   single-state versus multi-state distinction.
2. **A3.6b.2 — builder contract.** Define `MolSysBuilder.attributes` as the
   exact union of the native topology and structures contracts (96 current
   attributes, 64 more than its present declaration), delegate missing getters
   directly to `builder.topology` or `builder.structures` without calling
   `build()`, and compose instance presence from the corrected native helpers.

The builder must not declare molecular-mechanics fields or
`structure_chemical_state_index`: it stores neither domain. A test must assert
both union equality and getter availability for every declared attribute so
the contract cannot silently drift again.

The untracked native-scope test module was not one A2 gate. It originally
exposed 13 failures across:

- the three A2 audit cohorts;
- attribute-policy classification;
- thermodynamic schema expansion;
- a `skip_digestion` adapter defect;
- ordinary-conversion preflight bypass;
- `MolSysBuilder` fidelity;
- reverse and projection routes.

Tests must be split or selected by contract rather than made green through one
cross-cutting change.

After A2, A3.1, and A3.2, the same module reports 7 failures and 6 passes. The
atom-inventory failure closed independently; the remaining failures still map
to A3.3–A3.6.

### A3.3 Design Boundary

`molsysmt.native.structures_dict.structures_parameters` already declares
`temperature`, `potential_energy`, and `kinetic_energy`. A3.3 therefore repairs
an incomplete implementation of the existing native dictionary contract; it
does not introduce a new schema or require an H5MSM version increase.

The focused repair must:

1. serialize the three materialized series from `Structures`, preserving
   quantity units and requested structure order;
2. expose them through the `StructuresDict` attribute map, getters, and
   instance-aware `has_attribute()`;
3. derive `total_energy` only when both energy series are present;
4. rebuild `Structures` with the three series and preserve repeated or
   non-monotonic `structure_indices`;
5. update the exhaustive conversion profile so these fields cease to be
   reported as losses only after the executable round trip passes;
6. keep absent optional series absent rather than synthesizing values.

A3.3 does not silently absorb the broader coordinate-free native-structures
contract. `native_structures_contract.md` says that a thermodynamic-only
representation is valid, while the current `Structures.n_structures` and parts
of `StructuresDict` still infer axes primarily from coordinates, velocities,
or box. That systemic inconsistency requires its own bounded repair and
evidence; it must not be hidden inside the dictionary adapter commit.

The untracked compact baseline was created with 62 routes already assumed
exhaustive, before executable audit profiles existed. Because it has never
landed as a release baseline, it must be regenerated once from the conservative
A1 state. Thereafter, each A2 cohort removes only the route it has earned from
accepted non-exhaustive debt. This is a correction of an aspirational initial
baseline, not permission to weaken a landed ratchet.

### Current A1 Evidence to Capture

- **Focused contract and regression tests:** 28 passed with
  `tests/_private/test_conversion_report_scopes.py` and
  `tests/conversion_truth/test_native_bond_seam_adapters.py`.
- **Combined audit observation:** 31 passed and 2 expected A2 failures. The
  former five-test ImportError root cause is closed.
- **Static audit:** reaches its report and records 481 non-exhaustive edges,
  including 62 new relative to the aspirational baseline. A2 must earn those
  exhaustive classifications; A1 does not hide them.
- **Compatibility:** existing two- and three-positional-argument
  `ConversionIssue` construction remains valid because `scope` follows `kind`
  with a `chemical_state` default.
- **Ruff:** changed Python files pass.
- **Public docstring doctest:** 1 passed.
- **Lifecycle documentation:** the existing User Guide Foundations, Toolbox,
  Cookbook, and Common Core conversion-report explanations now document issue
  scope; all four notebooks remain valid JSON.
- **Developer-guide validation and `git diff --check`:** pass.
- **Files changed for implementation:**
  `molsysmt/basic/conversion_report.py`,
  `molsysmt/_private/conversion_report.py`, and
  `tests/_private/test_conversion_report_scopes.py`.
- **Landing:** focused implementation, tests, and lifecycle documentation
  committed as `504df91d0`.

## Segment B — Final Numba Oracle

| Stage | Status |
| --- | --- |
| B1 — generated active-Numba inventory | `DONE` |
| B2 — CPU kernel-to-consumer/evidence manifest | `DONE` |
| B3 — deliberate divergence and tolerance record | `DONE` |
| B4 — final forced-Rust campaign plus bounded Numba oracle | `DONE` |
| B5 — dated, committed oracle artifact | `DONE` |

Existing Rust port and dogfooding results are prerequisites, not B-segment
completion. No new Numba capability may be added while this segment is pending.

## Segment C — Rust Packaging

| Stage | Status |
| --- | --- |
| C1 — permanent crate/module and build-backend design review | `DONE` |
| C2 — production crate relocation and private extension integration | `DONE` |
| C3 — supported Linux/macOS and experimental Windows abi3 wheel CI | `DONE` |
| C4 — Python 3.11–3.13 and supported NumPy installed-wheel tests | `DONE` |
| C5 — sdist contract | `DONE` |
| C6 — metadata, resources, entry points, typing, and lazy-discovery parity | `DONE` |
| C7 — Rust quality, security, license, and portability gates | `DONE` |

Conda publication is tracked separately and does not block C4: controlled
preinstalled sibling dependencies may be used to validate the MolSysMT wheel.
The local pilot wheel closed the C1 design question. The clean exact-commit
wheel recorded in
[C2 Rust Packaging Artifact](release_1_0_rust_packaging_c2_artifact.md)
closes C2 but does not substitute for the C3-C7 matrices.

C1 is closed by [C1 — Permanent crate/module and build-backend design
review](archive/resolved_proposals/rust_packaging_backend_design.md): keep `setuptools`, add
`setuptools-rust`, ship one private `molsysmt._rust` abi3 extension inside the official
Conda package, and do not adopt maturin or a separate `msm_rust_kernels` distribution. Two
findings became binding C3 contracts (clean-build isolation with automated wheel
inspection, and abi3 proven per target rather than assumed from the tag). The earlier
report of a PyPI resolution failure as a C4 blocker is **corrected**: neither
PyPI nor the coordinated Conda channel is a prerequisite for validating the
MolSysMT wheel itself.

C2 started only after B4 closed. Commit `17be9ea50` relocates the crate to
`rust/`, integrates it as `molsysmt._rust`, removes the obsolete separate-package
prototype, and adds an executable wheel-content validator. A clean clone of that
exact commit produced
`molsysmt-0.20.0+156.g17be9ea50-cp311-abi3-linux_x86_64.whl` with SHA256
`a7da5d72804e0df12bbeb7b32c52e55cd34633ae9f0bc3ee34bcf15e4a7ecca5`;
the installed extension exposed all 97 entries and passed a minimum-image smoke.

C4–C7 close on exact commit `c4d8e9074` and GitHub Actions run
`30394881487`. Five native wheels pass 15 platform/Python checks, three NumPy
floors, three installed public smokes, the source-distribution round trip, and
the complete Rust quality/security boundary. The exact artifact names, hashes,
scope, and non-Conda qualification are recorded in
[C4–C7 Rust Packaging Artifact](release_1_0_rust_packaging_c4_c7_artifact.md).

## Segment D — Rust-Only Cut

| Stage | Status |
| --- | --- |
| D1 — direct Rust CPU routing and dispatch removal | `DONE` |
| D2 — CPU Numba/JIT implementation deletion | `DONE` |
| D3 — GPU capability audit and Numba-CUDA deletion | `DONE` |
| D4 — dependencies, warmup, diagnostics, API, docs, and course cleanup | `DONE` |
| D5 — executable zero-Numba/Numba-CUDA/llvmlite gate | `DONE` |
| D6 — session and per-function Rayon resource controls | `DONE` |

## Segment E — Rust-Only Validation

| Stage | Status |
| --- | --- |
| E1 — Rust unit, property, error, panic, GIL, and threading tests | `DONE` |
| E2 — independent scientific-truth matrix | `DONE` |
| E3 — complete MolSysMT suite and release fast gates | `DONE` |
| E4 — installed-wheel platform/Python matrix | `DONE` |
| E5 — maturity-weighted direct-consumer smoke | `DONE` |
| E6 — cold/warm, memory, thread, and oversubscription benchmarks | `DONE` |

### E1–E2 Closure Evidence — 2026-07-28

- `cargo test --manifest-path rust/Cargo.toml --no-default-features`: 80 passed.
- `cargo clippy --manifest-path rust/Cargo.toml --no-default-features -- -D warnings`:
  pass. Deliberate fixed-size and FFI exceptions are local, documented, and do
  not rewrite hot loops solely to satisfy style.
- `python -m pytest --receptor=llm tests/basic/test_parallel_control.py tests/rust -n 4`:
  100 passed before the three boundary regressions were added.
- `tests/rust/test_threading_boundaries.py`: 3 passed, proving representative
  GIL release, simultaneous cached Rayon pools with bounded oversubscription,
  result stability, and conversion of a native panic into a contained Python
  process failure.
- `python -m pytest --receptor=llm tests/scientific_truth -n 12`: 98 passed.
- `validate_scientific_evidence.py`: 43 validated, 0 partial, 0 gaps.
- `check_rust_hot_paths.py`: 18 Rust hot-path files clean.

E1 validates the private extension through representative boundary families;
public wrappers remain the authority for typed argument validation. The
private extension is not a supported user API.

### E5 Consumer Compatibility Evidence — 2026-07-28

Consumer evidence is weighted by release maturity. MolSysViewer is a
foundational MolSysSuite component and therefore a blocking integration gate.
TopoMT and PharmacophoreMT are earlier-stage consumers: their smoke workflows
are diagnostic, and consumer-local adaptation debt does not block MolSysMT
1.0.

- MolSysViewer direct MolSysMT integration and loader smoke: 5 passed.
- TopoMT pocket, physicochemistry, and parity smoke: 7 passed.
- PharmacophoreMT import smoke: passed.
- PharmacophoreMT ER-alpha workflow: failed in consumer code because
  `complex_based.py` calls `msm.get(..., element=True)`. In MolSysMT,
  `element` selects the semantic element level and is not an attribute request.
  The consumer must request the atom element-symbol attribute through the
  current public contract. This is classified as non-blocking
  PharmacophoreMT adaptation debt.

No consumer repository was modified during this audit. TopoMT also retains a
best-effort, exception-swallowed call to the removed `msm.warmup()` in its test
configuration; that cleanup belongs to TopoMT and does not affect the passing
runtime smoke.

### E6 Runtime Benchmark Evidence — 2026-07-28

The exact clean commit `746e22c5f` was measured through the isolated,
correctness-checking Rust-only release benchmark. The machine-readable result
is `release_1_0_rust_runtime_benchmark.json`; its interpretation and
reproduction command are in
[MolSysMT 1.0 Rust Runtime Benchmark](release_1_0_rust_runtime_benchmark.md).

- first native call / best repeated call: 1.60x, with zero Numba cache files;
- incremental peak over a 27.48 MiB payload: 3.80 MiB;
- measured two/four-thread speedups: 1.93x and 3.47x;
- four concurrent calls using two Rayon threads each completed with identical
  correct results;
- the complete suite had already passed under `-n 12`, covering the
  xdist-plus-Rayon process surface.

The numbers describe one recorded host and are not cross-platform performance
guarantees. Installed-wheel identity is separately proven by the closed C4/E4
matrix.

## Parallel Conda Delivery Track

This track is required before claiming a validated package is available from
the `uibcdf` Conda channel, but it is not part of the technical critical path
for the 1.0 source/tag, scientific validation, or manuscript:

1. Resolve the lower dependency chain for Python 3.11–3.14: demonstrated for
   the technical staging candidates, not yet a final release freeze.
2. Build and test an exact MolSysMT ABI3 package on each of five native Conda
   platforms, alongside the MolSysViewer noarch package: **done in staging**
   for technical coordinates MolSysMT `0.22.3` build 0 and MolSysViewer
   `0.23.3` build 0, from pinned source commits.
3. Install that exact pair from staging in fresh Python 3.11–3.14 environments
   without checkout leakage: **20/20 cells passed** on 2026-09-24 in five
   platform-targeted runs. Each cell verified package versions, staging
   URL/SHA-256 provenance, native code, BCIF/PDB-text conversion, and Viewer
   loading/resources. See [the Python 3.14 paired checkpoint](python_3_14_checkpoint.md)
   for the source/artifact hashes and run IDs. This is a major intermediate
   1.0 distribution milestone, not a public release or a full product gate.
4. Still open: choose final coordinated release coordinates and resolve the
   earlier 3.11–3.13 candidate path explicitly; run the exact-commit scientific,
   Viewer, documentation, Qt-where-claimed, and release gates; publish both
   packages without a dependency-cycle exception; verify fresh installations
   from the **public** channel and the resulting release/archival records.

The separate MolSysViewer 3.11–3.13 staging-enabled hosted gates advanced on
2026-09-24. Its Documentation notebooks run `36016496850` passed every
notebook on Viewer source commit `7c4e0cd9` against the staged MolSysMT
0.22.0 dependency. The Qt pipeline passed in `CI` run `36017021764`, but all
six Python matrix jobs failed on missing test-environment requirements after
resolving the dependency pair; the Viewer branch has local fixes awaiting a
hosted rerun. `CI_e2e` run `36016496630` never entered the browser tests:
Playwright's redundant Chromium archive extraction timed out, and the Viewer
workflow now selects the Chrome already used by its E2E harness. These results
are neither a green Viewer release gate nor a test of the newer 20-cell
3.14 package matrix. The diagnosis and next run belong to
`uibcdf/molsysviewer#88`.

The next Viewer runs narrowed, but did not close, this gap: `CI`
`36019810641` passed Qt and four of six Python matrix jobs; the other two
exposed a Node 26 JS-tool incompatibility and a fast-close WebSocket test
race. `CI_e2e` `36019810581` ran real Chrome and passed its first 22
scenarios before a PNG-download timeout. That scenario passed locally on the
source pair, but the local aggregate then stopped at scenario 25 because
this host cannot navigate command-line Chrome to the render-worker localhost
page. Thus neither hosted nor local E2E is 37/37. The proposed evidence-lane
redesign is uibcdf/molsysviewer#100; it does not waive the Viewer release
gate or change the 20-cell installed-pair result.

The next local source-pair pass separated browser evidence from the managed
server-GPU worker: MolSysViewer's 36 portable E2E scenarios all passed with
Chrome 149 and WebGL2. Hosted `CI_e2e` is configured to run that explicit
portable lane but has not yet been rerun. The independent `remote-session`
GPU lane remains failing locally because its Chrome process does not navigate
to the worker's loopback page; a CDP-navigation attempt also timed out and
was reverted. This is tracked by uibcdf/molsysviewer#100 and deferred until
after the coordinated pre-1.0 MolSysMT/MolSysViewer package publication. Do
not convert 36/36 portable into a full 37/37 or a 1.0 sign-off.

The next staging-enabled Viewer `CI` run `36034111547` passed Qt but its
six Python jobs stopped at one stale repository test that selected the
old E2E workflow step name. Viewer corrected the guard to select the actual
portable command, with 24 focused local tests passing. The staging-enabled
Viewer rerun `36036802158` on commit `2594f1a2` passed all seven jobs (six
Python matrix cells and Qt), confirming branch CI with staged MolSysMT. The
hosted portable `CI_e2e` rerun `36038233512` repeated the prior failure at
scenario 23/36: `remote-client-rendering` timed out waiting for the PNG
download, although it passed in the local 36/36 portable run. Do not count
this as hosted E2E success or rerun the unchanged test; #100 tracks the
deferred evidence-lane decision. The public-channel `main` gate and managed
server-GPU lane remain separate. This does not change the installed-pair
20/20 evidence.

The 20-cell result does not promote the technical `0.22.3`/`0.23.3` coordinates
into a release decision or alter the independent F6 sign-off. Windows passed
the core installation gate but remains experimental as a product-support
platform; optional Qt-host coverage has its own boundary.

### Next immutable candidate — 2026-09-24

The `python-3.14-support` branches now include the latest `main` commits of
both repositories. Select fresh coordinates MolSysMT `0.22.4` ABI3 build 0
and MolSysViewer `0.23.4` noarch build 0: neither version existed in the
Anaconda release registry (HTTP 404 for both), so the older technical staged
files are not repurposed. The committed route plans select staging. Release
events for these versions will not rebuild the files; exact SHA-256 promotion
to `main` has its own workflow and requires a successful full 20-cell pair
run. The five-platform promotion has not yet been exercised on GitHub.

MolSysViewer's prior 7/7 staged CI run pinned MolSysMT `0.22.0`, not the
newer technical `0.22.3` or this planned `0.22.4` candidate. Its three
manual hosted gates now take an explicit MolSysMT version input; they must be
rerun against `0.22.4` after its staging build. At candidate selection,
neither new version had been uploaded; build-0 staging is recorded below. The
hosted E2E PNG timeout remains an open defect under uibcdf/molsysviewer#100.

The maintainers now accept a narrowly scoped pre-1.0 exception for that
`0.22.4`/`0.23.4` package candidate: Viewer hosted portable E2E run
`36038233512` failed at scenario 23/36, while local portable E2E passed
36/36 and the separate server-GPU lane is unvalidated. This is permission to
advance the paired package publication once its other exact-commit gates
pass, **not** a hosted E2E pass, a full 37/37 result, or a 1.0 sign-off.
uibcdf/molsysviewer#100 stays open and the 1.0 release gate is unchanged.

The local MolSysMT source-pair suite now passes **10,225 tests with 11 known
skips**, using 12 workers and explicit paths for this MolSysMT branch, this
MolSysViewer branch and the released SMonitor `0.16.0` tag. The first attempt
accidentally imported the editable main checkout and was discarded as invalid
evidence. The corrected run exposed the already-tracked warning round-trip
defect in uibcdf/molsysmt#236; a consumer-side args-only path and
`smonitor>=0.16.0` floor close it locally while uibcdf/smonitor#21 remains
open. The suite also exposed an obsolete fixed water count in the native
peptide overlap test; it now checks the initial contact count against the
removed waters and that no contacts remain, without requiring optional
`tleap`. The release metadata was first prepared for `0.22.4` on 2026-09-24
and refreshed to the intended 2026-09-25 publication date after the local
date changed. The build-0 artifacts recorded below have not
passed the final exact-commit gates; if publication moves to another date,
update citation metadata and revalidate the resulting candidate before tagging.
MolSysSuite authorized the two transition issues (`uibcdf/molsysmt#237` and
`uibcdf/molsysviewer#93`) in `policy-v1.4.11` on 2026-09-24. Both candidate
callers now pin that release, their synchronized suite guides identify the
same effective snapshot, and the exact central repository checker passes
locally for both. `authorized` requires Python 3.14 metadata and CI, but the
canonical README badge remains at the publicly admitted 3.11–3.13 range until
the coordinated release and independent channel installations permit central
`admitted` status. The 3.14 package contract remains in the candidates; no
public-channel or suite-wide 3.14 claim follows from authorization alone.
Any later source change requires new exact-commit gates; the final
installed-pair and other release gates remain open.
The new policy's Ruff 0.16.5 formatting gate exposed three older files in
the Conda release route and its tests; they were formatted without changing
behavior. Repository-wide Ruff lint and format checks now pass, the two
focused release-route test modules pass 8/8, and the fast release gate remains
13/13.
The earlier exact-source-pair run `36061167557` passed Linux and macOS/Python
3.14 but failed Windows in Viewer's release-route test: Windows resolved
`bash -n` to the WSL launcher, although the promoted script is hosted only on
Ubuntu. Both repositories now retain the promotion identity assertions on
Windows and check Bash syntax on POSIX, with an explicit Ubuntu-runner guard.
This test correction still requires an exact-new-commit hosted Windows rerun;
the failed run is not counted as a passing 3.14 gate.
The corrected source-pair run `36062983964` subsequently passed Linux,
macOS and Windows/Python 3.14. Technical staging build 0 produced all five
native MolSysMT ABI3 files (`36063170604`) and the paired Viewer noarch file
(`36064255601`); the installed-pair run `36065287565` passed all 20 cells
(five platforms times Python 3.11–3.14). Viewer CI against staged MolSysMT
passed all seven jobs in `36064424260`, and its notebooks passed in
`36064424563`. The first MolSysMT full-CI run `36063386092` exposed a
different dependency floor error: its controlled ArgDigest commit predates
the catalog exception fix needed with SMonitor 0.16.0, so the same ten
error-contract tests failed in each of its six cells. Published ArgDigest
0.13.0 (exact tag commit
`9880fa7b990fd0987ff0de715b665eb9e11c11b2`) has that fix and passes
the 27 affected local contract tests with the released SMonitor 0.16.0 tag.
The complete local MolSysMT suite with those exact dependency sources passed
10,225 tests with 11 skips; the matching Viewer suite passed 2,112 tests
with 14 skips, both using 12 workers.
Both component candidates now require ArgDigest 0.13.0 and the controlled CI
pin names its exact release source. A new early CI check rejects controlled
source pins whose installed versions violate the declared runtime floor.
Build-0 staging and its passing 20-cell run are diagnostic only for this
corrected contract; build 1 must supersede each staged file and receive fresh
exact-commit gates before promotion. A local
Sphinx build on the source pair completed without missing-toctree warnings;
it still reported 744 unrelated/baselined warnings. The hosted Pages workflow
was not dispatched from the candidate branch because it would deploy public
documentation and currently pins an older Viewer source.
The build-1 Conda producers (`36102277287`, five of five ABI3 platforms;
`36102277047`, one noarch package) passed, and the corrected Python 3.14
source-pair workflow `36102309036` passed all three operating systems. The
exact-commit Rust-wheel gate `36102309653` built its artifacts but failed its
three installed-public-smoke cells: that job independently checked out old
PyUnitWizard and other sibling SHAs, then crashed on the missing
`configure.has_active_policy()` API. The function is present in PyUnitWizard
0.25.0 but not 0.24.0. Both component metadata floors and their Conda recipes
now require 0.25.0, and the wheel smoke consumes the single controlled-source
manifest plus an exact Viewer SHA input. The build-1 full CI `36102308805`
passed 7/7, and the exact installed-pair run `36105020606` passed 20/20;
they are diagnostic evidence only because the metadata floor and wheel
workflow changed afterward. Build 2 and all exact-commit gates must be rerun
before promotion. Local dependency-contract experiment
`uibcdf/molsysmt#245` now audits `pyproject.toml` against both recipes,
runtime environments, the hard/soft form registry, and source-consuming CI
jobs. Its first pass found the missing `py-mmcif` Rattler dependency,
unbounded environment floors, and a benchmark job without its controlled
siblings; these were corrected. Nine mutation/integration tests and the
expanded local fast gate 14/14 pass. The obsolete requirements broadcaster
and its inventory were retired; the active source manifest was relocated to
`devtools/controlled_sources.txt` with every workflow consumer updated.
The next exact-source attempt produced all five MolSysMT staging build-2
artifacts (`36111977722`) and the MolSysViewer noarch build-2 artifact
(`36111980483`); the Viewer Python 3.14 source pair passed three operating
systems (`36112007408`). MolSysMT full CI (`36112007337`) and the installed
Rust-wheel smoke (`36112007478`) correctly rejected the controlled
PyUnitWizard source pin: although commit `c69192ec` has the needed API, it
builds as `0.24.0+35`, below the new runtime floor `>=0.25.0`. The source
manifest now pins exact PyUnitWizard `0.26.0` tag commit `026be28d`, which
contains the API and declares Python 3.14 support. The dependency auditor,
23 focused tests, and the fast release gate 14/14 pass locally after this
correction. Build-2 artifacts and their earlier gates remain diagnostic;
the corrected commit still requires fresh exact-source gates and a new
staging build number before promotion.

## Segment F — Lifecycle and Release Candidate

| Stage | Weight | Status | Earned |
| --- | ---: | --- | ---: |
| F1 — Four Paths numbering and structural validation | 1% | `DONE` — 20 + 4x34 notebooks, semantic manifest identities and no validator exception at `c87a14036` | 1% |
| F2 — applicable Common Core and changed-behavior notebook execution | 2% | `DONE` — 40/40 pass from clean kernels at `2f6fd59d1` | 2% |
| F3 — function support-tier and pending-guide hygiene | 1% | `DONE` — 117 Tier 1, 56 Tier 3, seven outside-contract; completed records archived | 1% |
| F4 — User Guide, Cookbook, API, demos, and course lifecycle closure | 2% | `DONE` | 2% |
| F5 — clean exact-commit fast, full, wheel, and documentation gates | 3% | `DONE` — exact commit `38ab61f6e` passes every declared F5 gate | 3% |
| F6 — 1.0 release candidate and tag | 1% | `IN PROGRESS` — citation metadata and governance are prepared; exact final gates, tag, GitHub Release, and Zenodo version verification remain | 0% |
| **Segment F total** | **10%** | **`IN PROGRESS`** | **9%** |

## Deferred Work

These remain `DEFERRED` unless a correctness defect promotes them:

- additional native format parsers;
- Arrow and optional-column memory experiments;
- additional interaction families and reactive chemical-state expansion beyond
  the accepted 1.0 interaction result and persistence scope;
- speculative Rust GPU work and fused multi-observable kernels;
- broad Tier 2 and Tier 3 adapter expansion;
- nonessential post-threshold micro-optimization;
- paper extensions that alter no release contract.

## Update Procedure

Update this ledger whenever a stage changes status:

1. change only the affected stage and segment rows;
2. record the exact command, result, and commit in the execution log;
3. add earned weight only when the applicable segment or explicit F-stage exit
   gate passes; never count the F total again after summing its stages;
4. name blockers explicitly; never hide them inside `PENDING`;
5. preserve accepted omissions and deferred work;
6. identify the next active stage;
7. run `python devtools/scripts/validate_devguide.py`;
8. include the ledger update with the stage-closing commit.

If evidence was produced on a dirty tree, label it development evidence. Replace
it with exact-commit evidence before marking a release gate `DONE`.

## Execution Log

| Date | Segment/stage | Transition | Evidence | Commit |
| --- | --- | --- | --- | --- |
| 2026-07-26 | Overall plan | status ledger created | planning and repository audit; no implementation gate claimed | dirty WIP at `7ab96e791` |
| 2026-07-26 | A / A1 | `PENDING` → `IN PROGRESS` | 38-failure diagnosis and four-stage resolution plan accepted | dirty WIP at `7ab96e791` |
| 2026-07-26 | A1 implementation | remains `IN PROGRESS` pending landing | 28 focused passes; 1 doctest; combined audit surface 31 passed / 2 A2 failures; Ruff, notebook JSON, and devguide green | dirty WIP based at `7ab96e791` |
| 2026-07-26 | A1 | `IN PROGRESS` → `DONE` | scope contract, regression tests, and lifecycle documentation landed | `504df91d0` |
| 2026-07-26 | A2 design | `PENDING` → `IN PROGRESS` | conservative registry exposes 62 aspirational exhaustive routes requiring evidence-backed cohorting | dirty WIP after `504df91d0` |
| 2026-07-26 | A2 design audit | remains `IN PROGRESS` | 118 canonical attributes inspected; form capability maps and serialized-schema fidelity are distinct; focused module reports 13 independent root causes; A2 split into three native-to-dictionary cohorts | dirty WIP after `504df91d0` |
| 2026-07-26 | A2.1 | `IN PROGRESS` → `DONE` | 38 focused tests; 1 exhaustive and 480 accepted non-exhaustive Tier-1 edges; zero new debt; Ruff, lifecycle notebooks, and developer-guide validation pass | `cb123e226` |
| 2026-07-26 | A2.2 | `PENDING` → `IN PROGRESS` | topology serialization-boundary audit selected as the next cohort | dirty WIP after `cb123e226` |
| 2026-07-26 | A2.2 design audit | remains `IN PROGRESS` | 76 declared topology attributes partitioned into stable, derived, state-inventory, component, optional atom/bond, and conditional aromatic semantics | dirty WIP after `cb123e226` |
| 2026-07-26 | A2.2 | `IN PROGRESS` → `DONE` | 44 focused tests; 2 exhaustive and 479 accepted non-exhaustive Tier-1 edges; zero new debt; Ruff, lifecycle notebooks, and developer-guide validation pass | `4a4773986` |
| 2026-07-26 | A2.3 | `PENDING` → `IN PROGRESS` | composed native MolSys audit selected as the next cohort | dirty WIP after `4a4773986` |
| 2026-07-26 | A2.3 | `IN PROGRESS` → `DONE` | 51 focused tests; 3 exhaustive and 478 accepted non-exhaustive Tier-1 edges; zero new debt; broad native-scope module reduced to 9 independent failures | `01067f2c5` |
| 2026-07-26 | A2 | `IN PROGRESS` → `DONE` | all three native dictionary cohorts landed with explicit complete-source contracts | `cb123e226`, `4a4773986`, `01067f2c5` |
| 2026-07-26 | A3 | `PENDING` → `IN PROGRESS` | remaining independent schema, attribute-policy, adapter, and preflight repairs selected for classification | dirty WIP after `01067f2c5` |
| 2026-07-26 | A3 classification | remains `IN PROGRESS` | 9 broad native-scope failures split into 5 focused repairs and optional route promotion; 4 coordinate failures classified as profile requests; PDB-specific symptoms assigned to A4 | dirty WIP after `01067f2c5` |
| 2026-07-26 | A3.1 | `IN PROGRESS` → `DONE` | 54 focused tests and public doctest pass; ordinary conversion no longer constructs an unused preflight; broad native-scope module reduced to 8 independent failures | `dd13cb351` |
| 2026-07-26 | A3.2 | `PENDING` → `IN PROGRESS` | atom inventory classification selected as the next systemic repair | dirty WIP after `dd13cb351` |
| 2026-07-26 | A3.2 | `IN PROGRESS` → `DONE` | 74 consumer tests pass across attribute policy, compare, iterator, get, and StructuresDict round-trip; broad native-scope module reduced from 8 to 7 independent failures; Ruff, notebook JSON, and course validation pass | `998abe325` |
| 2026-07-26 | A3.3 design audit | `PENDING` → `IN PROGRESS` | thermodynamic keys already belong to the declared StructuresDict contract; missing two-way adapters, getters, capabilities, selection, and audit-profile preservation identified; coordinate-free native contract explicitly kept separate | dirty WIP after `998abe325` |
| 2026-07-26 | A3.3 | `IN PROGRESS` → `DONE` | optional temperature and energy series preserve units and arbitrary requested order in both directions; total energy remains derived; broad native-scope module reduced from 7 to 6 failures | `006d9e4ed` |
| 2026-07-26 | A3.4 | `PENDING` → `DONE` | standard adapter signatures, correct local mechanics dispatch, and matching selected topology/structure atom axes; 15 form tests pass | `ab28213c0` |
| 2026-07-26 | A3.5 | `PENDING` → `DONE` | absent optional state ID no longer expected as a loss; production unchanged; 15 contract tests pass and broad module reduced to 5 route-profile failures | `0434b9b42` plus corrected untracked WIP test |
| 2026-07-26 | A3.6 design audit | `PENDING` → `IN PROGRESS` | four direct native projections accepted as Tier 1; builder profiles held behind a complete builder attribute-contract audit | dirty WIP after `0434b9b42` |
| 2026-07-26 | A3.6a | `IN PROGRESS` → `DONE` | 37 focused tests; four direct profiles accepted; exhaustive coverage 3 → 7 and accepted debt 478 → 474 with zero new or unresolved baseline drift; lifecycle documentation and course validation pass | `c40e3154e` |
| 2026-07-26 | A3.6b | `PENDING` → `IN PROGRESS` | complete builder attribute contract selected as the prerequisite to any builder-profile promise | dirty WIP after `c40e3154e` |
| 2026-07-26 | A3.6b design audit | remains `IN PROGRESS` | builder declares 32 of 96 stored native attributes; 64 missing; empty native forms demonstrably return false-positive presence for optional thermodynamic, occupancy, bioassembly, state-ID, and component fields; reference-state semantics require separate review; native presence repair ordered before builder delegation | dirty WIP after `c40e3154e` |
| 2026-07-26 | A3.6b.1 | `IN PROGRESS` → `DONE` | native `Topology`, `Structures`, and composed `MolSys` presence contracts now distinguish declared capability from instance state; 1,601 broad consumers and 70 focused tests pass | `53fec7b09` |
| 2026-07-26 | A3.6b.2 | `IN PROGRESS` → `DONE` | builder declares the exact 96-attribute stored union, all declarations have direct getters, representative chemistry and thermodynamic reads do not materialize `MolSys`, 185 consumer tests pass, and five lifecycle notebooks execute successfully | `eb07e6e28` |
| 2026-07-26 | A3.6c | `PENDING` → `IN PROGRESS` | the broad native-scope module now has exactly three independent failures, all caused by missing exhaustive builder conversion profiles; conversion ratchet remains 7 exhaustive, 474 accepted debt, and zero drift | dirty WIP after `eb07e6e28` |
| 2026-07-26 | A3.6c | `IN PROGRESS` → `DONE` | four builder routes promoted with distinct evidence; atom selection and structure ordering fixed; isotope and derived-component seams repaired; 13 broad-scope, 88 builder/dictionary, and 49 convert tests pass; five lifecycle notebooks execute; coverage 7 → 11 and accepted debt 474 → 470 with zero drift | `4bc1dde7b` |
| 2026-07-26 | A3 | `IN PROGRESS` → `DONE` | all independent native schema, adapter, presence, projection, and builder-profile repairs are landed; PDB-specific work remains isolated in A4 | `dd13cb351` through `4bc1dde7b` |
| 2026-07-26 | A4 design audit | `PENDING` → `IN PROGRESS` | 21 PDB failures reduced to five shared causes; duplicate parsing between the handler and native adapters identified as the architectural root | dirty WIP after `18136a95d` |
| 2026-07-26 | A4 | `IN PROGRESS` → `DONE` | handler-owned normalized content now governs file, text, and handler input; canonical alternate sites, explicit chemistry, bioassemblies, canonical writing, payload-aware reports, 22 PDB tests, 139 historical/integration tests, and 60 convert tests pass; exhaustive coverage 11 → 22 with zero new debt | `1f656fe9f` |
| 2026-07-26 | A5 | `PENDING` → `IN PROGRESS` | Segment A integration gate selected; known external-form attribute-delivery debt remains explicit and PDB adapters themselves pass | dirty WIP after `1f656fe9f` |
| 2026-07-26 | A5 / Segment A | `IN PROGRESS` → `DONE` | isolated committed-snapshot reconstruction passes 85 tests; form adapters 89/89; exhaustive conversion coverage 22 → 37; accepted debt 470 → 444; zero new debt; Ruff, dependencies, devguide, course, demos, resources, scientific evidence, Rust hot paths, and public smoke pass; the only aggregate-gate red is independent F3 function-tier hygiene | `9660f6e79` |
| 2026-07-26 | B / B1 | `PENDING` → `IN PROGRESS` | Segment A dependency closed; generated active-Numba runtime inventory selected as the next oracle stage | dirty WIP after `9660f6e79` |
| 2026-07-26 | B1 | `IN PROGRESS` → `DONE` | AST inventory freezes 48 direct Numba/llvmlite imports, 108 CPU JIT callables, 52 CUDA JIT callables across 13 CUDA-coupled modules, and 46 direct consumers; broader runtime, dependency, test, tool, build, experiment, and documentation surfaces are recorded; three ratchet tests, Ruff, YAML parsing, and the live audit pass; smoke CI rejects new guarded coupling | `de2ccf988` plus the immediate nested-`try` traversal correction |
| 2026-07-26 | B2 | `PENDING` → `IN PROGRESS` | B1 baseline landed; CPU kernel-to-Rust-consumer-evidence classification selected | dirty WIP after `de2ccf988` |
| 2026-07-26 | B2 | `IN PROGRESS` → `DONE` | generated manifest maps all 108 CPU JIT callables across 15 families: 87 direct Rust dispatchers, one alias, and 20 explicitly absorbed helpers; every family names consumers, parity tests, and independent scientific or property evidence; 264 Rust tests and 82 selected scientific-truth tests pass; the live and isolated-environment audits, six ratchet tests, Ruff, CI YAML, and devguide validation pass | `863c77fb7` |
| 2026-07-26 | B3 | `PENDING` → `IN PROGRESS` | complete B2 map landed; deliberate numerical and behavioral divergence extraction selected as the next oracle gate | dirty WIP after `863c77fb7` |
| 2026-07-26 | B3 | `IN PROGRESS` → `DONE` | all 14 parity modules have accepted policies; 77 closeness sites declare both tolerances; 63 formerly implicit `rtol=1e-5` comparisons remain green with explicit strict contracts; eight deliberate divergences and four must-match contracts have executable evidence; 274 Rust/validator tests and 82 selected scientific-truth tests pass; zero provisional decisions remain | `b4b6bae25` |
| 2026-07-26 | B4 | `PENDING` → `IN PROGRESS` | closed B3 contract landed; reproducible final two-backend campaign selected | dirty WIP after `b4b6bae25` |
| 2026-07-26 | B4 strategy refinement | remains `IN PROGRESS` | the release runtime receives the complete forced-Rust suite; Numba is limited to the bounded oracle surface and failed-node attribution because it will not ship in 1.0 | `481271204` |
| 2026-07-26 | B4 checkpoint | `IN PROGRESS` → `BLOCKED` | exact source and wheel hashes recorded; forced-Rust smoke 15/15, Rust oracle 264 passed with three documented skips, and 82 scientific tests pass; complete forced-Rust suite reaches 9,361 passed but has 36 failed and 342 errors in 11 non-Rust root causes; all 378 unsuccessful node IDs reproduce with forced Numba; B4 requires a new green exact-commit run after the active WIP is landed | `481271204`; see `release_1_0_rust_campaign_checkpoint.md` |
| 2026-07-26 | B4 blocker reduction | remains `BLOCKED` | native bioassembly translations remove the 342-error PDB cascade; `MolSys` now delivers `structure_index`; H5MSM preserves optional structural and thermodynamic series, repeated structure order, partial-layer semantics, and multi-state inventory queries; the relevant H5MSM/report gate passes 1,074 tests and the known targeted residual is six root causes | `30d12a7c9`, `64ac440de`, `7cf7d7206` |
| 2026-07-26 | C1 packaging design review | `PENDING` → `DONE` | `python -m pip wheel . --no-deps` on branch `packaging/rust-c1-spike` produced `molsysmt-0.20.0+149.gcb3341fd5.dirty-cp311-abi3-linux_x86_64.whl` carrying `molsysmt/_rust.abi3.so`, `py.typed`, 292 `molsysmt.data` files, the `molsysviewer.addons` entry point and a versioningit Git version; the extension built under CPython 3.13 loaded in a clean 3.12 virtualenv, exposed 97 kernels and returned the correct minimum-image distance; development evidence from a dirty tree, accepted for the design question only; C keeps 0% earned weight | `87317ba76` (branch, not merged) |
| 2026-07-28 | B4 NGLView blocker reduction | remains `BLOCKED` pending exact campaign | optional topology snapshots preserve MolSysMT-origin IDs and chemical bond metadata without granting fictitious topology to generic widgets; multi-structure conversion drops partial PDB metadata; group-level hydrogen bonds preserve pair order; 45 NGLView and 746 broad consumer tests pass under forced Rust | NGLView fidelity checkpoint following `6f527bb44` |
| 2026-07-28 | B4 final exact campaign | `BLOCKED` → `DONE` | clean source archive and exact Rust wheel rebuilt from `6485a0c08`; bounded oracle passes 264 tests with 3 documented skips; combined migration/scientific gate passes 501 tests with 3 skips; complete forced-Rust suite passes 9,769 tests with 5 accepted skips and zero unsuccessful outcomes | `6485a0c08`; `release_1_0_final_numba_oracle_artifact.md` |
| 2026-07-28 | B5 oracle artifact | `PENDING` → `DONE` | dated artifact preserves the exact commit, environment, commands, source archive hash, wheel hash, installed-extension hash, bounded two-backend result, independent evidence, and complete application result | `release_1_0_final_numba_oracle_artifact.md` |
| 2026-07-28 | C2 production Rust integration | `PENDING` → `DONE` | crate relocated to `rust/`; private `molsysmt._rust` integrated through setuptools-rust; separate-package traps removed; 80 Rust and 270 Python tests pass with 3 documented skips; exact-commit Linux wheel is `cp311-abi3`, passes automated content validation, installs non-editably, exposes 97 entries, and computes the minimum image correctly | `17be9ea50`; `release_1_0_rust_packaging_c2_artifact.md` |
| 2026-07-28 | C3 multiplatform wheel CI implementation | remains `IN PROGRESS` | five native targets, pinned Rust/cibuildwheel configuration, strict abi3/content inspection, isolated installed-extension smoke, and artifact retention implemented; 12 contract tests, 80 Rust tests, Ruff, dependency validation, and local C2-wheel smoke pass; remote five-target run pending; pre-existing rustfmt debt assigned to C7 | `30b86cdf2`; `release_1_0_rust_packaging_c3_checkpoint.md` |
| 2026-07-28 | C3 exact-commit remote matrix | `IN PROGRESS` → `DONE` | GitHub Actions run `30346103646` passes Linux x86_64/aarch64, macOS x86_64/arm64, and Windows x86_64; every `cp311-abi3` wheel passes build/audit, non-editable installed-extension validation, 97-export and minimum-image smoke, and artifact upload; exact wheel hashes and runner images are preserved | `f79ccb4f0`; `release_1_0_rust_packaging_c3_checkpoint.md` |
| 2026-07-28 | C4 installed-wheel matrix | `PENDING` → `IN PROGRESS` | C3 portability dependency closed; Python 3.11–3.13 and supported NumPy installed-wheel execution selected as the active packaging gate | after `f79ccb4f0` |
| 2026-07-28 | D1–D5 / Segment D | `PENDING` → `DONE` | production routing is Rust-only; CPU JIT, CUDA, incomplete Taichi experiments, runtime controls, dependencies, JIT warm-up API, diagnostics, and migration parity tests are removed; low-level compatibility paths remain Rust-backed; the executable zero gate passes; 122 focused and 450 broad affected tests pass, with one separate network-dependent test excluded | dirty implementation; `release_1_0_rust_only_cut_artifact.md` |
| 2026-07-28 | D6 Rayon controls | `PENDING` → `DONE` | session defaults and function-local overrides resolve to reusable Rayon pools; nested overrides remain local; 1/2/4-thread execution is directly observable; 165 affected tests pass; representative release-build speedups at four threads are 2.99× distances, 3.54× centers, 3.51× radius of gyration, and 2.73× RMSF | dirty implementation; resolved bug record and `performance_and_jit.md` |
| 2026-07-28 | WIP integration | dirty tree → clean `main` | release gates, function-tier policy, conversion-fidelity records, and native dictionary extraction landed in three focused commits; fast gate 12/12 and 107 conversion-truth tests pass | `83a573f09`, `8579b8e7a`, `0a9353ffc` |
| 2026-07-28 | Conda scheduling | critical-path prerequisite → parallel delivery track | coordinated sibling and MolSysMT Conda publication may proceed during manuscript writing/review; local installed-wheel evidence remains in C/E, while channel availability blocks only the Conda delivery claim | maintainer decision recorded in the execution plan and Conda coordination report |
| 2026-07-28 | E1–E2 | `PENDING` → `DONE` | 80 Rust unit/property tests, Clippy with warnings denied, 103 Python Rust/control/boundary tests, 98 scientific-truth tests, 43/0/0 evidence registry, and 18-file hot-path lint pass; representative GIL release, concurrent Rayon pools, bounded oversubscription, and panic containment are executable regressions | stage-closing Rust validation commit |
| 2026-07-28 | E3 | `IN PROGRESS` → `DONE` | complete Rust-only suite passes 9,585 tests with two accepted skips under `-n 12`; fast release gate passes 12/12; Ruff passes across package, tests, devtools, and root conftest | `692479097` |
| 2026-07-28 | E5 | `PENDING` → `DONE` | maturity-weighted consumer audit: MolSysViewer passes 5/5 as the blocking foundational consumer; TopoMT passes 7/7; PharmacophoreMT imports but its ER-alpha workflow exposes a consumer-local obsolete `element=True` call, recorded as non-blocking adaptation debt | status-ledger commit following `9fbb95569` |
| 2026-07-28 | E6 | `IN PROGRESS` → `DONE` | exact clean-commit Rust-only benchmark records first/repeated calls, memory, raw 1/2/4-thread samples, bounded nested concurrency, native-extension hash, scientific checks, and zero JIT-cache creation | `746e22c5f`; `release_1_0_rust_runtime_benchmark.{md,json}` |
| 2026-07-28 | Minimal installed-runtime defect | discovered → `DONE` | optional forms remain visible but detectors whose mapped soft dependency is absent no longer execute; the missing OpenMM mapping is restored; 449 basic tests and local non-editable smoke without OpenMM pass | `c4d8e9074`; `archive/resolved_bugs/optional_form_detection_broke_minimal_install.md` |
| 2026-07-28 | C4–C7 / E4 / Segments C and E | `IN PROGRESS` → `DONE` | exact run passes five native abi3 wheels, 15 platform/Python checks, three NumPy floors, three installed public smokes, sdist round trip, exact 99-export validation, and Rust formatting, Clippy, tests, advisory, dependency, and license gates | `c4d8e9074`; run `30394881487`; `release_1_0_rust_packaging_c4_c7_artifact.md` |
| 2026-07-28 | F1 status correction | `PENDING` → `DONE` | commit history and the live validator confirm that F1 had already landed: 156 notebooks, core 1–20, four paths 21–54, complete toctrees, unique semantic labels, and a matching manifest; the two remaining editorial references and Sphinx confirmation belong to later lifecycle stages | `f5d96218b`; `python devtools/scripts/validate_course.py` |
| 2026-07-28 | F / F2 | `PENDING` → `IN PROGRESS` | F1 historical evidence recovered; existing notebook-execution evidence must be audited before scheduling new execution or edits | after `03a170442` |
| 2026-07-28 | F2 execution audit checkpoint | remains `IN PROGRESS` | required union reconstructed as 37 notebooks; in-memory clean-kernel run passes 14/26 deterministic notebooks, exposes 12 failures requiring ownership classification, and defers 11 network/interactive notebooks; no notebook outputs or content were modified | `release_1_0_f2_notebook_execution_checkpoint.md` |
| 2026-07-28 | F2 correction pass | remains `IN PROGRESS`, ready to land | all 26 deterministic and all 11 network/headless notebooks pass from clean kernels; seven bounded library-contract corrections have regression coverage; affected User Guide notebooks execute; formal closure awaits validation, landing, and exact-commit 37/37 rerun | dirty worktree based on `2340d1eff`; `release_1_0_f2_notebook_execution_checkpoint.md` |
| 2026-07-29 | F2 exact-commit closure | `IN PROGRESS` → `DONE`; F3 becomes active | final scope expands from 37 to 40 because Scalability corrections affect all four Paths; the complete Common Core plus notebooks 28, 29, 47, 48, and 49 of every Path pass from fresh kernels with no persisted outputs | `2f6fd59d1`; `release_1_0_f2_notebook_execution_checkpoint.md` |
| 2026-07-29 | F3 support-tier and lifecycle reconciliation | `IN PROGRESS` → `DONE`; F4 becomes active | function tiers derive from the exhaustive API stability registry and validate as 117 Tier 1, 56 Tier 3, and seven outside-contract; nine completed/superseded proposals and one historical audit leave the pending queue; normative links and resolution records are updated | `release_1_0_f3_support_and_lifecycle_checkpoint.md`; documentation-only work based on `fd19f9196` |
| 2026-07-29 | F4 documentation lifecycle | `IN PROGRESS` → `DONE`; F5 becomes active | final course narrative references use stable semantic targets; the numbering report and Rust migration residue are archived; the missing dihedral broadcast regression passes on vacuum and periodic paths; checked-in autosummary surfaces are refreshed; 11 stale toctree targets are repaired; Sphinx builds successfully and the remaining warning families are measured as accepted documentation debt | `672f8f065`; `release_1_0_f4_documentation_lifecycle_checkpoint.md` |
| 2026-07-29 | Segment F progress accounting | no stage transition; weighted closure 90% → 96% | the fixed 10% Segment F budget is partitioned across six independently gated stages; completed F1–F4 earn 6%, while F5 and F6 retain the remaining 4%; no technical exit criterion or release requirement changes | maintainer-approved accounting update after `075cb0432` |
| 2026-07-29 | Atom-axis `add()` WIP integration | dirty pre-F5 worktree → clean candidate base; no stage transition | native and public addition share one atom-axis contract; MolSys mutation is transactional; adapters, multiple-source dispatch, scalar returns, lifecycle documentation, and regressions are synchronized; 30 focused and 554 expanded tests pass, two notebooks execute, Ruff passes, and the fast gate passes 12/12 | `2865c3122`; `release_1_0_atom_axis_add_checkpoint.md` |
| 2026-07-29 | Atom-axis `add()` semantic follow-up | F5 remains active; bounded audit inserted before its expensive exact-commit matrix | multi-source selection/cardinality, whole-call transaction scope, one-sided atom-aligned data, structure metadata and energy validity, coordinate-free structures, adapter parity, diagnostics, and memory are recorded with phases and acceptance criteria; no behavior or weighted progress changed | `87ccfc289`; `pending_proposals/atom_axis_add_semantic_audit.md` |
| 2026-07-28 | Developer-guide coherence pass | no stage transition | post-migration documentation debt cleared: four Numba-era bug reports and four Numba-era proposals archived with resolution notes after verifying each against the Rust runtime; one stale duplicate report removed; the three Numba migration documents relabelled as historical evidence; snapshot sentences that still called Segment C open corrected; `pending_bugs` and `pending_proposals` indexes rewritten; 11 broken intra-guide links repaired; devguide validation and the fast gate pass 12/12; code, tests, and notebooks untouched, with the residue recorded in `archive/resolved_proposals/rust_migration_documentation_and_test_residue.md` | `2340d1eff` |
| 2026-07-29 | Presentation surface | no stage transition | the README and documentation landing pages described MolSysMT as middleware between other libraries and advertised the removed Numba/CUDA architecture; `docs/content/about/what.md` disowned the library's own native capability. Reframed with the molecular system as subject. Verified against the installed package: seven `to=` calls should be `to_form=`, the sequence and dihedral examples raise, and the cross-library showcase raises `NotImplementedConversionError` because no route to `MDAnalysis.Universe` exists. The tier table showed about eleven Tier 1 forms where the live registry reports 75 of 89, and claimed any Tier 1 pair converts. The Conda recipe had an empty summary. Every example now executes; ruff, devguide, course, and fast gate 12/12 pass | `d2b805e74`; `pending_proposals/readme_positioning_and_1_0_refresh.md` |
| 2026-07-29 | Documentation and paper track | critical-path work → named parallel track | with A–E and F1–F4 closed, presentation, documentation and the methods paper become a principal parallel workstream; the three items the positioning pass could not close are specified with acceptance criteria | `pending_proposals/presentation_and_citation_surface.md` |
| 2026-08-03 | Topology vocabulary, DCD backend noise and the course gate | three reports → `DONE`; no stage transition | `get_covalent_chains` is renamed `get_covalent_paths`: `chain` is an element of a molecular system while the function walks the covalent graph returning paths, and `get_covalent_blocks` was already named to avoid the same collision with `component`. No deprecation cycle, the policy starts at 1.0.0. `get_dihedral_quartets(with_blocks=True)` raised on every real system by pushing ragged block sets through `np.array`; on T4 lysozyme 158 of 161 phi quartets split in two and 3 do not, and those 3 are the prolines. Module 13 of the Common Core taught `get_covalent_blocks` as the way to obtain components, contradicting its own tutorial, and the quickstart placed four topology functions in `molsysmt.structure`. MDTraj's DCD reader printed to the C standard output on every open and every read with no way to disable it; suppressed behind `configure.silence_backend_stdout`, 26 lines to 0, and recorded as evidence in the native-parser proposals rather than as a reason to write one. `validate_course.py` was red with 20 errors because it asserted a Common Core module count and a label scheme the section has not settled; both deferred explicitly, gate green at 155 notebooks | `dfa57c073`; `647694061`; `1541f8775`; `acd4404c7`; `archive/resolved_bugs/dihedral_quartets_with_blocks_raises_on_ragged_blocks.md`; `pending_bugs/course_gate_red_after_common_core_renumbering.md` |
| 2026-08-03 | Structure axis of a composite molecular system | two reports → `DONE`; no stage transition | a molecular system spread over complementary items had no structure axis of its own, so `where_is_attribute` broke its tie between providers that are not interchangeable. `msm.get([h5msm, dcd], n_structures=True)` returned 20 while `msm.get([dcd, h5msm], n_structures=True)` returned 1, `msm.convert` on the second order discarded nineteen structures with no diagnostic, and `get` returned `time` of length 1 beside `coordinates` of length 20 for one system. The axis is now the largest structure count among the items carrying structural data, order-independent; only items spanning it may deliver a structural attribute, with the existing last-matching-item tie-break applying among those; an item holding zero or one structure below the axis is a reference conformation whose series are dropped with the new `StructuralAttributeOffAxisWarning` (`MSM-WARN-STRUCT-006`); and two items each holding more than one structure, of different lengths, raise `StructuralInconsistencyError` naming `molsysmt.concatenate_structures`. This completes on the structure axis the consistency contract already enforced on the atom axis by `_private/molecular_system_validation.py:144-151`, and the asymmetry between raising on atoms and warning on structures is deliberate: `[pdb, xtc]` is one structure beside a trajectory and must keep working. `convert` needed its own intervention because it never resolved attributes through `where_is_attribute`. The `Iterator` defects closed with it, including an unguarded `append` that yielded zero items without error depending on keyword order, and an H5MSM reader indexing an empty `structures/id` dataset. 7913 tests pass; the only failure is a pre-existing third-party `openff.toolkit` import error reproducible without MolSysMT | `2de6b4d6d`; `archive/resolved_bugs/structural_attribute_resolution_ignores_the_structure_axis.md`; `archive/resolved_bugs/iterator_without_explicit_attributes_fails_for_partial_forms.md` |
| 2026-08-03 | `msm.info()` table styling in the built documentation | reported → `DONE`; no stage transition | compiled pages rendered `msm.info()` flat while the notebooks stayed striped. `info()` returns a `Styler`, which emits no HTML class, so it was styled only by MyST-NB's class-agnostic pandas rule — dropped in v1.4.0, the dark-mode rework — while pydata-sphinx-theme reaches notebook tables solely through `table.dataframe`. `info()` now tags the table `dataframe`, the class `DataFrame.to_html()` emits, which restores striping in both themes and removes a dark-mode fallback that painted the output as an inverted light box. Verified on a rebuilt page: all 8 tables of `info.ipynb` emit the class under `.bd-content` → `div.cell_output`, with the striping now coming from the theme alone. A CSS override and pinning `myst-nb<1.4` were both rejected as patches; a stable `Styler` uuid was rejected because no library-side value is both stable and unique — 5 of 62 notebooks hold two identical tables by design. `docs/execute_notebooks.py` keys staleness off notebooks, never the library, so the remaining 61 need an explicit force | `d92d4fe76`; `archive/resolved_bugs/docs_styler_zebra_striping_lost_with_myst_nb_1_4.md` |
| 2026-07-31 | `MolSys → ViewerJSON` deep-copy defect | reported → `DONE`; no stage transition | the conversion read two fresh, local, discarded intermediates through the deep-copying default of `ViewerJSON.to_dict()`, spending about 93% of its time in 1,350,867 `deepcopy` calls; reading them with `copy=False` takes the reported 62-atom × 5,000-structure case from 1.67 s to 0.32 s. Neither intermediate aliases the source, so the copy protected nothing: a non-aliasing regression test mutates the returned payload and asserts the source `MolSys` and a second conversion are untouched, and it stays green with `copy=True` restored while the timing regresses to 1.58 s. The `ViewerJSON` identity conversion was audited and deliberately left deep-copying: it is unreachable from this chain. 508 viewer, form, view and cross-repo tests and Ruff pass | `b63a2f6c5`; `archive/resolved_bugs/viewer_json_conversion_deep_copies_twice.md` |
| 2026-08-07 | Fast release gate | `FAIL` (11/12) → `PASS` (12/12); no stage transition | the developer-guide gate had been red since the documentation queues were reorganized: `devguide/README.md` still linked the deleted `docs/README.md`, and `forms_and_conversions.md` and `pending_proposals/docs/README.md` both linked a proposal that `ae29169e8` had archived. The archiving was correct — the *Multiple items into one* section of `convert.ipynb` now composes a PSF topology with a DCD trajectory and states that the multi-structure item dictates the structure axis — but its two referrers were never updated, and the empty `devguide/docs/` tree was left behind. This ledger's previous claim that the gate passed 12/12 was measured before that reorganization | see the commit closing this row |
| 2026-08-07 | `file:prmtop → molsysmt.MolSys` | reported → `DONE`; no stage transition | the converter imported a `to_molsysmt_Structures` sibling that never existed in the form package. The name was unused — the body builds an empty `Structures()` because a prmtop carries topology only — but the import runs at call time, so the library's central form was unreachable from an entire input format, and MolSysViewer failed the same way. Conversions register in `_convert_to` as function objects and their inner imports are function-local, so the catalogue proves only that `to_*.py` imports; nothing calls every registered edge. The sweep that found it is now `tests/form/test_converter_imports_resolve.py`, carrying the two remaining cases as a baseline that cannot grow, and the conversion is guarded by `tests/form/file_prmtop/test_to_molsysmt_MolSys.py`. 115 supported, conversion-truth and form tests pass; fast gate 12/12; Ruff clean | see the commit closing this row |
| 2026-08-07 | Presentation and citation surface | two of three items `PENDING` → `DONE`; no stage transition | maintainer decisions taken and applied. Daniel Ibarrola-Sánchez is not an author: removing him from `CITATION.cff` also removes the ORCID that file attributed to him but which belongs to Diego Prada-Gracia, and the record now agrees with `.zenodo.json` on the same two authors and with the README, which acknowledges his contributions to MolSysMT's early development. The unreferenced duplicate landing page `docs/content/user/index_v2.ipynb` is deleted with its two `nbconvert` artifacts, verified to have no inbound reference from any page; three further orphans of the same `_v2` experiment are recorded in the proposal. The DOI, version, title and date are decided but deferred: `CITATION.cff` is a placeholder until 1.0 closes, and the update is now a line in the release-gate sign-off so it cannot drift again as it did for two years. Item 3, the timing of the Conda installation instructions, stays open | see the commit closing this row |
| 2026-08-07 | Atom-axis `add()` semantic audit | Phases 1-3 `PENDING` → `DONE`; Phase 4 open; no stage transition | Phase 1 audited the contract read-only and measured every claim with a probe. It found the scope far narrower than assumed — only `molsysmt.MolSys` and `molsysmt.Structures` implement `add()`, and the dispatcher selects on the target form — and it found most of audit question 1 unreachable, because digestion rejects a list of independent molecular systems before the target × source loop can run. Two of the audit's own premises were wrong: adding a topology-only source does not drop the coordinates, it fails first with an `ArgumentLengthError` naming an argument the caller never passed; and the one list that survives digestion is a composite system, which `add` iterated as independent sources, contradicting the composite contract. Phase 2 landed the regression matrix with the decisions as `xfail(strict=True)`, which is also how a cross-cutting defect surfaced: a test asserting `add()` honours `attribute_policy` passed against a function with no such parameter, filed as `pending_bugs/public_functions_silently_ignore_unknown_keywords.md`. Phase 3 implemented D1-D7 and the four defects: the target's box prevails with `IncompatibleBoxWarning` (MSM-WARN-STRUCT-007), `temperature` and the energies are dropped while `structure_id`, `time` and `time_step` survive, `attribute_policy` gains `intersection`/`strict`, bioassemblies merge on the chain axis with `BioassemblyIdentifierCollisionWarning` (MSM-WARN-STRUCT-008), `alternate_location` merges with remapped atom indices, `atoms_ff` follows the policy, and `add()` is one-to-one with the loop deleted. 40 add tests pass with no pending markers; 886 basic, native and element tests pass; the contract is now in `native_structures_contract.md` | see the commit closing this row |
| 2026-08-07 | Atom-axis `add()` semantic audit | Phase 4 `PENDING` → `DONE`; proposal archived; no stage transition | the lifecycle closed and all ten acceptance criteria hold, so the proposal and its Phase 1 findings moved to `archive/resolved_proposals/`. `molsysmt.basic.add` documents `attribute_policy` and the four Notes that changed; the User Guide page gained two sections and a warning admonition, written against a real case rather than an illustrative one — T4 lysozyme from a PDB carries B factors and a unit cell, a built peptide carries neither, so one addition exercises the drop and both new diagnostics — and the notebook was re-executed so its printed outputs are measured. Common Core modules 17 and 18 needed no correction: they already use one target and one source. Writing the documentation surfaced a diagnostic defect of its own, a doubled period in the `strict` rejection message, fixed at both call sites. Two coverage gaps found while walking the criteria were closed rather than waived: `velocities` joined the one-sided parametrisation, and a string selection over an assembled composite source is now pinned. 43 add tests pass; Ruff, dependencies, devguide and course gates green; fast release gate 12/12 | see the commit closing this row |
| 2026-08-07 | Public argument contract | reported → `DONE`; no stage transition | a typo in a keyword argument was silent in 22 of the 26 public callables and uncatalogued in the other four: `structure_indeces` for `structure_indices` returned all 5,000 structures of a trajectory instead of the three requested, with a well-formed result and no diagnostic. The cause was a binding step making a policy decision — ArgDigest discarded any keyword outside the signature before the layer designed to judge it could see it — which left it more permissive than Python itself, and left MolSysMT's own `STRICTNESS='warn'` policy unreachable for those 22. Fixed upstream in ArgDigest 0.10.0 by adding the missing axis, the function argument contract, and declared here with three configuration lines, one domain pointing at the attribute catalogue, and two contract modules; the 19 closed signatures are protected with no declaration at all. Two claims in the original triage were wrong and are corrected in the archived report: `contains` and `is_composed_of` implement deliberate no-criterion branches, so no `requires_any_of` rule was declared. Reading those bodies found a real defect instead — `get_label` declares `**kwargs` and never reads it. `molsysmt.basic.convert` keeps the permissive default because its domain resolves from `to_form` at call time; the gap is recorded and pinned by a test. ~8300 tests pass with the policy at `error`, plus 1296 MolSysViewer tests with nothing declared on its side; Ruff clean; fast release gate 12/12 | see the commit closing this row; `archive/resolved_bugs/public_functions_silently_ignore_unknown_keywords.md` |
| 2026-08-07 | Cross-repo test drift | reported → `DONE`; no stage transition | two tests in `tests/molsysviewer_molsysmt/` read `MolSysView._message_history`, a private attribute MolSysViewer replaced with a narrower `_shape_history` and a `scene_history` model, so the suite carried two known failures — and a suite with known failures stops detecting new ones, which blocks the F5 exact-commit gate. Both tests already intercepted `apply_system_edit` and recorded the edited molecular system, then ignored it to inspect the message the viewer built from it. That was the defect the refactor exposed: what the facade owes the viewer is an edited system handed to `apply_system_edit`, and how the viewer serializes it afterwards is not this side's business. They now assert on the recorded system. Renaming the attribute to `_shape_history` was deliberately not done: it is not the same thing, so the tests would have passed asserting something else. 115 cross-repo tests pass and the MolSysMT suite is clean | see the commit closing this row; `archive/resolved_bugs/cross_repo_test_reads_a_removed_molsysviewer_attribute.md` |
| 2026-08-12 | Pre-F5 adapter and course consolidation | no stage transition; candidate base ready | comparison now treats incompatible shapes as unequal; OpenFF unit adapters coexist safely; PyTraj trajectory conversion preserves its supported contract; OpenMM simulations are built only from complete inputs and initialize from the selected structure; every registered converter module resolves; conversion fidelity advances to 40 exhaustive / 441 accepted / 29 resolved with zero new debt; the Common Core is fixed at 20 modules and all labels match permanent manifest identities with no validator exception. The fast gate passes 12/12, Ruff is clean, form adapters pass 89/89 with 78 accepted lower-tier declarations, and the course contract passes 156/156 notebooks | `3fb639010` through `c87a14036` |
| 2026-08-12 | F5 exact-commit release gates | `IN PROGRESS` → `DONE`; weighted closure 96% → 99%; F6 becomes active | exact commit `8faf62785` passes the fast gate 12/12; full matrix run `31589594289` passes Ubuntu and macOS on Python 3.11--3.13; wheel run `31589594286` passes supported Linux/macOS builds, abi3 Python/NumPy compatibility, installed public smoke, sdist, Rust quality and security, with Windows green as experimental evidence; documentation run `31589594273` and smoke run `31589594438` pass. Packaging defect #145 and clean-source CI defect #146 satisfy their acceptance criteria and are archived | `8faf62785`; `archive/resolved_bugs/built_wheels_omit_the_dynamic_form_catalogue.md`; `archive/resolved_bugs/ci_shadows_the_installed_rust_extension_with_the_source_checkout.md` |
| 2026-08-13 | Bounded pre-1.0 corrections | F5 `DONE` → `IN PROGRESS`; weighted closure 99% → 96% | the declared selection syntaxes become an executable directional contract, large molecular strings no longer enter unbounded filename tokenization, and the stale `_private` API branch is removed from the published reference. Focused and expanded guards pass; a new exact-commit release campaign is required before F5 can close again | `d5b066a35`; uibcdf/molsysmt#148, #149, #150 |
| 2026-08-13 | Generated form-function identity | reported → `DONE`; no stage or weighted-progress transition | nine `exec()`-based getter modules created 2,162 distinct decorated functions without `__module__`, so ArgDigest received `None.<name>`, caller-specific contracts could not identify them, and diagnostics named no resolvable origin. Each generator now seeds `__name__` before decoration; exact module identity, structured diagnostics, and future generators are guarded. The passport decision remains independent and untouched | `5412489c9`; uibcdf/molsysmt#152 |
| 2026-08-13 | Retired ArgDigest passport dependency | reported → `DONE`; no stage or weighted-progress transition | the only `ValidatedPayload` issuance path and its paired trusted-array branch were unreachable: 13,319 distinct decorated callables and the instrumented full suite produced no caller under `molsysmt.lib.*`. Both branches, the import, and the obsolete sandbox are removed without replacement; active rules use ordinary digestion or explicit caller-owned `skip_digestion=True`. The complete 372-test private-digester surface passes against both the pre-removal ArgDigest tree and `refactor/remove-the-passport` with `argdigest.core.contract` absent; fast release gate 12/12 | `2eca46926`; uibcdf/molsysmt#153; `tests/_private/argdigest/test_no_validated_payload.py` |
| 2026-08-13 | Pre-1.0 scope freeze | no stage or weighted-progress transition; F5 remains active | uibcdf/molsysmt#151 remains a post-1.0 expert-interface proposal: automatic detection is already bounded and safe, no post-fix end-to-end speedup has been measured, and adding a public signature plus unresolved heterogeneous-list semantics would expand rather than stabilize the candidate. No further implementation item is admitted before the exact-commit campaign | `pending_proposals/add_an_explicit_source_form_hint_to_convert.md`; checkpoint commit following `2eca46926` |
| 2026-08-13 | Boundary-digestion re-audit | uibcdf/molsysmt#147 withdrawn; no stage or weighted-progress transition | instrumentation distinguishes 21 ordinarily digested calls from 568 fast-path calls in the representative viewer action: all 510 form-level `has_attribute` calls already use `skip_digestion=True`, perform zero molecular-system assessments, and forcing the bypass changes 46.62 ms to 46.82 ms. The original 29 ms diagnosis is refuted. The two real findings are separated into uibcdf/molsysviewer#32, where operation-local inventory reuse measures 46.71 ms → 26.62 ms, and post-1.0 uibcdf/molsysmt#154, where one direct public predicate performs four assessments | `archive/withdrawn_bugs/boundary_digestion_on_internal_predicates.md`; checkpoint commit before F5 |
| 2026-08-14 | F5 controlled sibling alignment | remains `IN PROGRESS`; no weighted-progress transition | public metadata advances to ArgDigest `>=0.12.0` and PyUnitWizard `>=0.24.0`; controlled workflows pin their immutable release commits and the already-tested MolSysViewer commit; a clean Python 3.13 Conda environment resolves ArgDigest 0.12.0, PyUnitWizard 0.24.0, SMonitor 0.12.0, and DepDigest 0.10.1 from channels and imports them from `site-packages`; 17 focused workflow, receptor, and fast-path tests pass | candidate-preparation commit following `eca56ef1d` |
| 2026-08-14 | F5 exact-commit recertification | `IN PROGRESS` → `DONE`; weighted closure 96% → 99%; F6 becomes active | exact commit `38ab61f6e` passes the fast gate 12/12; smoke `31781199983` and documentation `31781220979` pass; wheel run `31781218931` passes 28 jobs covering supported Linux/macOS artifacts, installed Python 3.11--3.13 checks, NumPy floors, sdist and Rust quality, with Windows retained only as non-blocking experimental evidence; full matrix `31781216880` passes all six Ubuntu/macOS Python 3.11--3.13 cells | `38ab61f6e`; post-gate status checkpoint |
| 2026-08-14 | F6 citation and preservation preparation | remains `IN PROGRESS`; weighted closure stays 99% | the existing MolSysMT concept family `10.5281/zenodo.1298752` is verified through its 0.12.0 record; every current public surface uses that concept DOI; `CITATION.cff` and `.zenodo.json` agree; the old MolModMT DOI is removed; release preparation, offline validation, and post-release Zenodo verification are executable and documented for reuse across MolSysSuite; four focused tests, Ruff, devguide, and the expanded fast gate 13/13 pass; exact final commit gates, tag, GitHub Release, and 1.0.0 version DOI remain | dirty F6 candidate based on `503612269`; `release_and_citation.md` |
| 2026-08-14 | Public MolSysSuite alias contract | uibcdf/molsysmt#157 `OPEN` → `DONE`; no stage or weighted-progress transition | `molsysmt.attribute.get_argument_aliases()` exposes schema-versioned defensive-copy plain data for attribute synonyms and explicit element-dependent short names; MolSysMT derives its own caller-scoped ArgDigest tables from that source; MolSysViewer removes both private imports while preserving its `viewer`, `Region`, and `Whole` behavior. The User Guide and Common Core module 8 reflect the alias contract and both notebooks execute. 119 MolSysMT tests, 23 focused MolSysViewer tests, Ruff, dependency/devguide/course/API validation, and the fast release gate 13/13 pass; MolSysViewer's full suite has 1609 passes, four accepted skips, and one unrelated pre-existing documentation failure from deprecated `add_label()` usage | closing commit for uibcdf/molsysmt#157; `archive/resolved_proposals/public_alias_contract_for_molsyssuite_consumers.md` |
| 2026-08-14 | Alias-collision downstream guard | ArgDigest runtime fixed; no weighted-progress transition | ArgDigest now rejects alias-plus-canonical and multi-alias target collisions before normalization can discard a value. MolSysMT pins the public `get()` boundary, raises its wheel and Conda floor from `>=0.12.0` to the planned patch `>=0.12.1`, and records that the exact release candidate needs recertification after publication rather than accepting the known-bad release | downstream closure for ArgDigest commit `c46cd01`; `tests/attribute/test_argument_aliases.py` |
| 2026-08-19 | Public documentation audit & standardization pass | remains `IN PROGRESS`; blockers made explicit 2026-09-02 | Foundations, Tools (topology, structure, physchem, pbc, mm, nglview, openmm, tleap), Cookbook (all 9 recipes standardized with MolSysViewer static views), Showcase (all 6 notebooks compiled with matplotlib PNG display data, zebra tables, collapsible notes, and reconstructed NGLView representations/CDN configs), and Course (all 4 paths synchronized) pass with clean Sphinx HTML builds (`make -C docs html`) and Ruff. The `About` positioning and index were already rewritten in `d2b805e74`, and its citation lifecycle was prepared in `d35dc33b1`; final sign-off remains open for two named reasons: the Conda installation claim does not hold on supported Python 3.13 (uibcdf/molsysmt#195), and the exact 1.0 citation remains part of F6 release publication | `3bee6f054`, `d2b805e74`, `d35dc33b1`; uibcdf/molsysmt#195; `release_and_citation.md` |
| 2026-09-02 | Stable API docstring integrity | uibcdf/molsysmt#187 `OPEN` → `DONE`; no stage or weighted-progress transition | the validator now rejects empty descriptions, parameter-name restatements, the generated return placeholder, and non-informative `object` parameter types on the stable surface; 205 parameter entries across 60 stable functions now carry concrete types and operational descriptions; mutation guards pass 10 tests, all 27 affected doctests pass, Ruff is clean, and the fast release gate passes 13/13. Scientific-evidence execution and devguide-guard relevance remain open as uibcdf/molsysmt#196 and uibcdf/molsysmt#197 | `350a7e866`; `archive/resolved_bugs/validators_that_check_form_instead_of_intent_admit_conforming_emptiness.md` |
| 2026-09-04 | Native Conda ABI3 publication | uibcdf/molsysmt#202 `OPEN` → `DONE`; no stage or weighted-progress transition | the shared action no longer renders each recipe twice, and MolSysMT now builds one CEP 20 ABI3 artifact on each native platform instead of recompiling for every supported Python minor. Five platform artifacts execute under all fifteen platform/Python 3.11--3.13 cells; production run `33849332945` publishes all five build-2 artifacts to staging in 19:56, with independently verified ABI3 channel metadata. Production staging/release selects the proven ABI3 recipe, while the coordinated installation gate remains 5 × 3 | `e5820d479`; uibcdf/molsysmt#202; `archive/resolved_proposals/build_one_abi3_conda_artifact_per_native_platform.md` |
| 2026-09-19 | Scientific evidence execution | uibcdf/molsysmt#196 `OPEN` → `DONE`; no stage or weighted-progress transition | the fast validator now certifies registry structure without claiming that pytest ran; the separate heavy gate executes exactly all 47 registered nodes, rejects collection failures and skips, and emits a commit- and environment-bound JSON certificate. The current registry produces 54 parametrized cases, all passing with zero skips; workflow-contract and Scientific Truth validation pass 119 tests, the complete suite passes 10,211 with 11 unrelated dependency skips, and the fast gate remains 13/13. `ci-full` and `ci-weekly` retain one clean-source certificate per matrix cell | closing commit for uibcdf/molsysmt#196; `archive/resolved_bugs/scientific_evidence_registry_accepts_tests_that_were_never_executed.md` |
| 2026-09-19 | Form extraction dispatch | uibcdf/molsysmt#210 `OPEN` → `DONE`; no stage or weighted-progress transition | all 89 form adapters now accept the extraction dispatcher contract with no debt exception; both mechanics forms preserve global settings and subset their conditional per-atom force-field axis; three-letter sequences extract residue positions while retaining the group-indexed converter contract; invalid axes and positions raise catalog errors instead of Python signature/index errors. The adapter census passes 263 tests with two accepted PyTraj skips, the complete suite passes 10,217 with 11 accepted dependency/environment skips under 12 workers, Ruff is clean on every changed Python file, and the fast gate remains 13/13 | closing commit for uibcdf/molsysmt#210; `archive/resolved_bugs/three_forms_declare_an_extract_the_dispatcher_cannot_call.md` |
| 2026-09-19 | Test-suite runtime proposal | uibcdf/molsysmt#122 one-line fixture request → measured profiling proposal; no stage or weighted-progress transition | an accidental serial run reached only 3,793/10,228 executed nodes in 760.75 seconds before interruption, while the documented `-n 12 --dist loadfile` mode completed all 10,228 in 377.90 seconds. The proposal now requires cold/warm profiles, node/module cost attribution, preservation of executed scientific and contract evidence, mutable-fixture isolation, and separate wall-time versus aggregate-work measurements before optimizing | `pending_proposals/profile_and_reduce_test_suite_runtime_without_weakening_coverage.md` |
| 2026-09-19 | Shared guard governance | uibcdf/molsysmt#197 `OPEN` → `BLOCKED` by uibcdf/molsyssuite#26; no stage or weighted-progress transition | the originating MolSysMT defect exposed incompatible guard semantics across all six wave-1 repositories. MolSysSuite now owns the shared addressability, reviewer-relevance, pytest/non-pytest, migration, and rollout decision; #197 is narrowed to MolSysMT's eventual implementation and must not create a competing local policy | central record in uibcdf/molsyssuite#26; `pending_bugs/devguide_closure_accepts_guards_unrelated_to_the_reported_defect.md` |

## S6 source recovery and delivered Viewer candidate — 2026-10-06

The source matrix `37441978743` at `5bd893c85` finishes **failure**: Linux
and macOS Python 3.11 pass; the other six cells each fail only
`tests/basic/test_copy.py::test_copy_1`. Matching undefined chain types become
numeric NaN arrays under pandas 3, and the comparison's numeric branch reports
inequality even for self-comparison. #345 owns the reproduced defect.
All eight registered scientific certificates pass 54 cases with zero skips.
The [recovery receipt](../devtools/data/stabilization_s6_source_recovery_20261006.json)
preserves exact counts, warnings, omissions and original log identities.
Ordinary full-suite omissions are 26 Linux/27 macOS skips and 40 deselections
per cell; the next workflow retains complete JUnit to inspect their reasons.

The correction passes the same 61 compare/copy cases under pandas 2.3.3 and
3.0.6, and the comparison doctest. Public metadata equality now accepts matching
missing numeric entries while rejecting a populated entry in their place.
Ruff passes; the tutorial and course explanations are synchronized. The new
source matrix must execute before treating this correction as full qualification.

The Viewer team delivers stable source
`c046fca173f501c6e259761ef8f3d6b1825f17e8`, tested against MolSysMT
`5e2721691b6a3c175406a8e4c0926dfb7b160671`. It reports Python 3.14 counts
of 2,819/2,792/2,793 passed and 27/54/53 skipped on Linux/macOS/Windows,
with no failures, plus all 39 core browser suites and 17 interaction calculation
forms. Those are consumer observations, not our re-execution. GitHub confirms
the source SHA, and inspection confirms its later `e71eaf63` change is
documentation only. Routine Viewer source routes and upcoming exact-source
inputs select `c046fca...`; their dependency contract audit passes.

This makes a fixed current Viewer candidate available for staging preparation.
It does not qualify the newer corrected MolSysMT pair, Conda-installed files,
Windows artifact compatibility or publication. Preserve both immutable
producer identities and build/file digests in the upcoming installed-pair
gates. Release tag and GitHub Release approval remain separate.

## Next version checkpoint: 0.23.0 — 2026-10-06

The maintainer selects **0.23.0**, rather than 1.0.0, for the next pre-1.0
package checkpoint. The [frozen scope](release_1_0_scope.md#pre-10-version-checkpoint)
continues to admit stabilization fixes and required qualification only.
Use this version to validate packages and the MolSysViewer integration; decide
on 1.0.0 after reviewing that evidence and the remaining acceptance criteria.

Existing source/wheel receipts retain their original producer identities and
development versions. They do not certify packages labelled 0.23.0. No new tag,
release or staging upload is performed by this decision, and citation metadata
still describes the published 0.22.4 release. The exact 0.23.0 producer and the
paired Viewer package version remain to be selected before staging.

## Corrected current source pair — 2026-10-06

MolSysMT `bb4781c5ae0b725d0c904cfd8bae1f44a1b13123` and delivered Viewer
`c046fca173f501c6e259761ef8f3d6b1825f17e8` pass source run
[37449282864](https://github.com/uibcdf/molsysmt/actions/runs/37449282864):
all eight Linux/macOS Python 3.11–3.14 full cells succeed. Each Linux cell
passes 13,290 cases with 26 skips; each macOS cell passes 13,289 with 27 skips.
Every cell has 40 deselections, retained separately from JUnit, and all eight
scientific certificates pass 54 cases without skips. #345 is resolved with its
[missing-metadata regression guard](../tests/basic/compare/test_compare_extended.py)
and [archived diagnosis](archive/resolved_bugs/comparison_rejects_identical_undefined_metadata_under_pandas_3.md).
The original failed source matrix remains recorded.

Wheel run [37449284817](https://github.com/uibcdf/molsysmt/actions/runs/37449284817)
passes all thirty applicable jobs, with one expected PR-only skip. Rust quality
checks and 81 native tests, four wheel builds, sixteen current-NumPy runtime
cells, four NumPy-floor cells, four public installed smokes and the sdist
round trip pass. The
[pair receipt](../devtools/data/stabilization_s6_pair_20261006.json)
retains official results, five artifact/file identities and independently
hashed bytes, eight JUnit results and their skipped nodes/reasons.

This completes the corrected source/wheel checkpoint. These artifacts carry
development version `0.22.4+217.gbb4781c5a`, not 0.23.0. Select and qualify
the actual 0.23.0 package candidate and paired Viewer package version next.
Conda-installed pair, consumer-owned installed/browser/session acceptance,
exact documentation and publication gates remain. No public release is inferred.

The committed Conda route and MolSysMT dispatch defaults now select 0.23.0,
with exact-file promotion after the installed-pair gate. The guarded route
rejects a different version. This prepares the next operation without uploading
packages or changing the published citation metadata. The new Viewer package
version still needs its owner's decision; its historical 0.23.4 dispatch default
is not a selection for this new pair. Pass the agreed versions explicitly.
The five existing route/promotion guards pass in the shared Python 3.14
environment (twelve workers, receptor `llm`, 3.98 s); Ruff, developer-guide
validation and whitespace checks pass. This is scoped route validation,
not another full-suite or installed-package qualification.


## Coordinated interaction query vocabulary — 2026-10-06

uibcdf/molsysmt#346 implements the approved provider counterpart of
uibcdf/molsysviewer#168: `involving_selection`, `within_selection`,
`across_selection_boundary`, and the separate `between_selections` operation.
Legacy query values and `between` remain compatible. Scientific calculation
scope and H5MSM/InteractionsDict schemas are unchanged; the
[normative contract](interactions_query_semantics.md) defines the migration boundary.
The [provider report](archive/resolved_proposals/coordinate_explicit_interactions_selection_query_names.md)
records 1,474 passing scoped tests, eight passing doctests and executed public
examples. Consumer migration remains Viewer-owned. Prior full source/wheel
qualification retains its original producer; it does not certify this new source
or a 0.23.0 artifact. The exact-candidate gates under #334 remain pending.


### Maintainer clarification: use only explicit query names — 2026-10-06

The maintainer withdraws the initial compatibility spellings in #346 before
public adoption. The canonical query names and `between_selections` are the only
supported query API; detector and persisted scientific scope remain unchanged.
The current Viewer checkout still passes `incident` by default, and its existing
real-consumer attribution/session regression fails at that query call. Keep the
regression intact and qualify it again after uibcdf/molsysviewer#168 migrates the
consumer. Prior source-pair evidence does not certify this revised provider API;
the new provider contract and the migration requirement must accompany its source
handoff. No format bump or release publication is implied.


## Released support providers for the next checkpoint — 2026-10-06

The maintainer reports the public SMonitor 0.19.0 and ArgDigest 0.15.0 releases;
the GitHub release records are verified as published, non-draft releases.
`devtools/controlled_sources.txt` now fixes their exact release commits:

- SMonitor 0.19.0: `f604b940ab281df4554869fdd24f796ea6d42c27`.
- ArgDigest 0.15.0: `57447cc4ec1f7ce85078f8a939892efd075bc919`.

The shared Python 3.14.7 environment already contains SMonitor 0.19.0 and
ArgDigest 0.15.0+1.g5c6711e; the latter's runtime source has no changes from the
release tag. Existing argument-digestion, exception/warning, catalog, cross-provider,
interaction-query and dependency-audit guards pass **776 tests in 20.33 s**,
with zero failures/errors/skips and three historical H5MSM migration warnings:

```bash
python -m pytest tests/_private/argdigest tests/_private/smonitor \
  tests/_private/test_smonitor_catalog_integrity.py \
  tests/cross_repo/test_smonitor_contracts.py \
  tests/cross_repo/test_diagnostics_noise.py \
  tests/interactions/test_argument_validation.py \
  tests/interactions/test_public_molsys_h5msm_workflow.py \
  devtools/tests/test_audit_dependency_contract.py \
  -n 12 --dist loadfile --receptor=llm
```

The dependency audit and **14/14 fast gates** also pass. The
[bounded receipt](../devtools/data/support_provider_releases_20261006.json)
retains the pins, actual development versions, scope and JUnit hash under #334.
At that checkpoint, public floors were `argdigest>=0.13.0` and `smonitor>=0.16.0`;
the later #524/#549 bypass receiving above raises the ArgDigest minimum to 0.14.0.
Source qualification
and minimum supported versions are separate contracts. No new restricted-capture
or explicit-digestion feature is adopted by this pin update. That provider
coordination remains uibcdf/molsyssuite#106. These checks do not qualify exact
installed release artifacts or the full provider/Viewer pair, and do not change
the pending Viewer query migration in uibcdf/molsysviewer#168.


## Selected pre-1.0 package pair — 2026-10-06

The maintainer selects **MolSysMT 0.23.0 / MolSysViewer 0.24.0**. The agreed
Viewer source is `5bb59c0e13045ee0aaf34cf336a3533d611197bf`; routine source
pins and the installed-pair workflow now use this source and version. The
committed Conda route remains staged. Build defaults are zero; the actual
Viewer build coordinate must be read from its producer receipt.

The real Viewer attribution/session regression that previously failed on the
withdrawn `incident` query now passes, together with public MolSys/H5MSM and
named-analysis persistence tests: **35 passed, zero failures/errors/skips**.
Release preparation and dependency-route guards pass **25 tests**. The first
route check caught four stale workflow copies of the old Viewer SHA; the
corrected pin passes the dependency audit and **14/14 fast gates**. The
[candidate preparation receipt](../devtools/data/stabilization_023_candidate_preparation_20261006.json)
retains scope, JUnit digests, initial failure and remaining qualification.

The local Sphinx HTML build succeeds. It reports **784 warnings**, matching
the earlier S5 build count, with zero course references to nonexistent
toctree documents. The warning debt remains tracked by uibcdf/molsysmt#144;
a successful build is not a warning-free documentation claim.

Viewer source CI [37530734789](https://github.com/uibcdf/molsysviewer/actions/runs/37530734789)
has completed successfully on Linux, macOS and Windows at
`a48478fcab579095ed6eb7ab2a3620cc8fb3a8df`. Git inspection confirms that the
selected 5bb59c0e source adds documentation/evidence only. This distinction
does not imply an exact-5bb CI execution. The two experimental Qt failures
reported by the Viewer team remain owned by uibcdf/molsysviewer#109.

The standard release preparation tool updates candidate citation surfaces to
0.23.0, dated 2026-10-06. This prepares metadata; it does not publish the
version. Read-only registry preflight found neither selected version present;
that observation must be refreshed before producing or uploading artifacts.
Four untracked Viewer sandbox artifacts are preserved and excluded from the
committed source identity. The Viewer Conda recipe derives its version from
the ephemeral tag. Its committed release plan still selects historical
0.23.4 and needs its owner's 0.24.0 update before its package producer runs.

Full exact-candidate source/native gates and the sixteen installed-pair cells
remain required. Filenames, SHA-256 values and availability on
`uibcdf/label/staging` must be obtained from actual producer files. No public
tag, GitHub Release, registry upload or promotion is performed by this
preparation. Installed/browser/session acceptance remains Viewer-owned under
uibcdf/molsysviewer#93 and uibcdf/molsysviewer#114.

The prepared source candidate is
`46ef28eb60a258aa77d82ff1bc39ee0d1591e3c9`. Its clean-source scientific
certificate passes **54/54 cases for 47 registered nodes**, with zero
failures/errors/skips. All **26 basic doctests** pass with network access;
the first sandbox attempt failed two RCSB-download examples on DNS resolution
and is retained in the receipt. Source matrix
[37534217132](https://github.com/uibcdf/molsysmt/actions/runs/37534217132)
and native wheel matrix
[37534219155](https://github.com/uibcdf/molsysmt/actions/runs/37534219155)
are dispatched against this exact commit and the selected Viewer source.
They remain in progress; the larger local editable-source suite is also
running. Later evidence-only commits do not reselect that producer or qualify
unfinished gates.

The maintainer explicitly authorizes building and uploading the four ABI3
Conda files for **0.23.0, build 0**, from that exact candidate. A fresh
read-only registry preflight confirms that neither selected version is yet
present. Staging producer
[37534744593](https://github.com/uibcdf/molsysmt/actions/runs/37534744593)
is dispatched for `linux-64`, `linux-aarch64`, `osx-arm64` and `win-64`, targeting
`uibcdf/label/staging`. Dispatch is not production or upload verification;
no package file identity is reported before inspecting actual bytes. The
public tag, GitHub Release and main-label promotion remain separate gates.


### Staging files ready for the Viewer handoff — 2026-10-06

Producer 37534744593 completes successfully on all four native platforms.
**MolSysMT 0.23.0, build 0**, from
`46ef28eb60a258aa77d82ff1bc39ee0d1591e3c9`, is available on
`uibcdf/label/staging`. The
[handoff receipt](../devtools/data/stabilization_023_staging_handoff_20261006.json)
records every filename, build string and SHA-256. Producer receipts, registry
metadata and hashes computed from downloaded bytes agree. ABI3 metadata and
seven core source files are verified against the original candidate; Windows
checkout CRLF is the only source-text normalization needed.

MolSysViewer can declare **`molsysmt>=0.23.0`** for the agreed Interactions,
H5MSM 0.5 and coordinated loading/box capabilities. This selects the first
candidate package delivering the current coordinated contract. It does not
declare the experimental interaction contract stabilized or waive installed
consumer qualification.

Importing both MolSysMT and its Rust extension from the actual extracted Linux
Conda payload reports version 0.23.0. Public H5MSM/MolSys, named interactions
and the real Viewer attribution/session regression pass **35 tests** using
that payload in the shared Python 3.14 environment. This is artifact runtime
evidence with shared dependencies; the clean sixteen-cell installed pair
remains required.

The standalone ABI3 validator rejected the correct Python range because it
still expected `<3.14`. uibcdf/molsysmt#347 corrects the tool to compare against
the public project range and adds guards; **13 tests** pass. No package bytes,
build coordinates or producer are changed. The subsequent **14/14 fast gates**
pass. Native wheel run 37534219155 passes thirty jobs with one expected PR-only
skip.

The larger local run records **13,561 passed, 16 failed, 17 errors and two
skipped**, with all 33 unsuccessful cases affected by sandbox DNS restrictions.
Repeating those exact cases with network access on unchanged runtime source
passes **33/33**. Combined outcomes are 13,594 passes and two skips; the receipt
retains the original unsuccessful invocation rather than claiming a second
complete green run. The two omissions are the RDKit-absent alternative test
in an environment with RDKit and the unavailable optional CuPy form.

The eight-cell exact-source matrix is still running. MolSysViewer must provide
its exact 0.24.0 staging file/build/hash before the sixteen-cell installed pair
can run. Public tagging, Release publication and promotion remain pending;
the available files support the next consumer qualification step.

## Native metadata contract stabilization — 2026-10-13

#383 and #384 repair reported native public contracts used by ElastNetMT:
integer/string scalar atom labels now normalize to native string storage without
changing source indices, and system-level B-factor queries retain the requested
structure axis instead of silently selecting every structure. These are bounded
correctness repairs under the existing admission rule, not new chemistry or
storage capabilities. The combined 455-test source scope passes with twelve
workers; the final 18-case label module additionally covers complete-column
scalar broadcasting. Public get/set doctests, independent new Toolbox/course
examples and the lightweight H5MSM metadata recipe execute on Python 3.14.
The documentation build retains the separately tracked warning debt in #144.

Records: [atom labels](archive/resolved_bugs/scalar_atom_id_updates_disagree_with_native_string_storage.md)
and [B-factor structure selection](archive/resolved_bugs/native_b_factor_queries_ignore_selected_structures.md).
Frozen sources, artifacts and publication status are unchanged. Replacement
candidate review and exact installed-consumer qualification remain #334 work;
these focused checks do not qualify new artifacts or resume publication.

## Final adapter-delivery stabilization — 2026-10-10

During the publication pause, #139 is resolved: all 95 registered adapters have
catalog-compatible attribute delivery routes and the accepted delivery masks are
empty. PRMTOP box geometry and TRJPK queries reuse existing readers and general
geometry/count tools; the nonexistent native CIFFileHandler registration and
fake documentation are retired while real CIF file conversions remain tested.
#365 repairs aligned TRJPK subset export with fixed nm/ps storage; #370 repairs
its public identity/copy dispatch. The selected public/dictionary/doctest suite
passes 328 cases, ten strict docstring renders pass, and the three affected
catalog notebooks execute with unchanged code. Records:
[delivery audit](archive/resolved_bugs/form_attributes_declared_without_getters.md),
[TRJPK subsets](archive/resolved_bugs/trjpk_subset_exports_fail_on_list_selections.md)
and [TRJPK identity](archive/resolved_bugs/trjpk_identity_conversion_rejects_its_output_filename.md).

#368 records independent broken legacy CCD regeneration scripts as post-1.0
maintenance; #144 retains broader documentation warning debt. These repairs
neither resume publication nor qualify a replacement candidate. Frozen refs,
artifact hashes and receipts remain unchanged; no new heavy matrix is run.

The first hosted smoke run for this repair, 38031440730, stopped at the legacy
AST signature guard before tests: it rejected the intentional output_filename
addition in #370. The follow-up makes that argument keyword-only, records the
exact function/issue in the existing signature-waiver registry, and adds a public
legacy six-position call plus extra-position rejection guard. Both parent and
original-source transition checks pass; the final TRJPK selection and doctest
pass 31 cases without warnings. This does not replace installed-pair evidence
or qualify any frozen artifact. Hosted smoke must pass on the corrective head.

That corrective head, a1ad51b7c2296c667f6221ccca5cfa37ab74ac67, passes hosted
smoke run 38031801296 and its Ruff, developer-guide, suite-policy and package
governance checks. The failed first invocation remains recorded above.

## Translated fit-anchor stabilization — 2026-10-10

#367 repairs an existing unique-rotation validation contract used by
uibcdf/pharmacophoremt#31 and uibcdf/pharmacophoremt#41. Mean subtraction
could admit three labels at exactly two distinct translated centers. Checking
differences from a represented anchor rejects the underdetermined fit before
coordinate mutation while retaining the existing numerical-rank policy and
Kabsch kernels. The focused fit, analytic geometry, precision and doctest scope
passes **242 tests** with twelve workers; the changed docstring renders without
RST warnings. User Guide, Cookbook and all four affected course modules describe
the constraint. See the [resolved record](archive/resolved_bugs/translated_fit_anchors_admit_underdetermined_rotations.md).

This is main-source stabilization during the publication pause. It does not
qualify a replacement candidate, modify frozen references or resume publication.

## Resource-owner stabilization — 2026-10-10

The preceding fit repair at 70d1400b9514904fbf9b1a5ca126ddf4591e63dc passes all
five applicable hosted checks, including CI smoke 38032696174.

#371 records the component resource-owner review. #372 repairs orphaned owned
storage after failed memmap construction; #373 repairs caller-log custody in the
developer LEaP check and failure cleanup in the wrapper/peptide builder. Selected
regressions and the peptide doctest pass **278 cases** in twelve workers; both
changed public docstrings render without RST warnings. Source inspection,
controlled failure execution and historical cleanup attribution remain distinct.
See the [owner review](archive/resolved_proposals/review_temporary_resource_ownership_and_tool_lifecycle.md)
and [operating contract](temporary_resource_operations.md).

The bounded #374 legacy optional/native-probe debt is completed in the runtime
and native-probe repair checkpoints above, with platform evidence limits stated.
dprada/LMMV own retrospective resource attribution and release closeout under
#334, with review on 2026-10-24 or publication resume. Name/uid metadata alone
does not authorize disposal. Shared environments, active/human resources and
frozen identities remain protected. This block does not resume publication or
qualify a replacement candidate.

## Consumer capability triage — 2026-10-10

Resource-owner stabilization at
`072aa9bdbfb9299f7e3256f9b27f6aae8ea52629` passes all five applicable hosted
checks: CI smoke (38034435967), Ruff, developer-guide integrity, MolSysSuite
policy and Conda publication governance. These source checks do not qualify a
replacement installed candidate.

Provider source/contract inspection classifies three incoming requests as new
capabilities under the existing admission rule:

- uibcdf/molsysmt#366: [explicit small-molecule standardization](pending_proposals/explicit_small_molecule_standardization.md).
- uibcdf/molsysmt#369: [explicit full-domain atom permutation](archive/resolved_proposals/explicit_atom_permutation.md).
- uibcdf/molsysmt#375: [fixed-state hydrogen-bond site directions](pending_proposals/fixed_state_hbond_site_directions.md).

Their records distinguish reusable existing tools from missing contracts,
consumer interim scope and independently checkable acceptance criteria. They
remain open for post-1.0 design/implementation; triage is not feature delivery,
scientific validation or a reason to change extraction/site-recognition semantics.
No runtime code, dependency, frozen reference or candidate artifact changes in
this triage. The publication pause and remaining exact-pair coordination under
uibcdf/molsysmt#334, uibcdf/molsysmt#250 and uibcdf/molsysmt#254 remain in effect.

## Explicit directed-geometry admission — 2026-10-10

The maintainer authorizes the bounded `structure.get_vectors` addition under
uibcdf/molsysmt#375: distance-like atom/center endpoints, aligned source structure
indices, original axes, explicit units/images and compiled Rust execution.
The [scope exception](release_1_0_scope.md#bounded-geometry-admission--2026-10-10)
and [normative geometry contract](structure_vectors.md) preserve the unresolved
acceptor-model/environmental-refinement boundaries. #375 remains partially open.

The public tutorial and H-bond cookbook execute with Python 3.14; the independent
new Common Core 19 section executes and previous course sections are preserved.
[Reproducible optimized-source measurements](benchmarking/vectors.md) cover
100,000 atoms, 5,000 structures, Cartesian products and periodic dictionaries.
They distinguish source runtime from installed candidates and numerical output
bytes from process RSS. This source addition does not rebuild, requalify or
replace frozen candidates and does not resume publication under #334.


The exact local directed-geometry selection passes **119 tests** with twelve
workers and Pytest Receptor, including the new API doctest and strict rendered
docstring. The scope includes distance/center regressions, independent
triclinic controls and all four installed quantity backends. The final fast
release gate passes **14/14 checks**; these are source checks, not the full
platform or installed-pair qualification. #375 remains open for named acceptor
models; its reference-model reconnaissance is in the maintained pending record.

## Bounded conversion stabilization — 2026-10-22

The #181 execution profile now covers 70 declared direct edges among native,
MDTraj and OpenMM resident forms, with 526 edges explicitly outside that profile.
The [conversion guide](conversion_execution.md) and
[receipt](../devtools/data/conversion_execution_engines_20261022.json) retain
scope and commands. This is execution coverage, not whole-graph or full-fidelity
certification. It exposed the repaired #419 source-form delegation failures and
#420 coordinate-unit, selection and explicit-box defects. The broader regression
passes 2,178 cases without skips; all fourteen fast gates pass. Sources are
published through `55f04ebfe364c1918a912e2d76aee8db95959dde`, whose five ordinary
push checks pass. These remain source checks, not a replacement installed pair.

The prior #190 evidence-scope proposal is resolved; experimental claims, independent
oracles, partial evidence and gaps are visible separately in the generated matrix.
The full-site documentation baseline remains 711 warnings and no errors under #144.
Further bounded conversion/documentation cleanup can proceed in the authorized
improvement window; neither completing every conversion profile nor eliminating
all historical warnings is newly made a prerequisite for 1.0.

## H5MSM conversion execution profile — 2026-10-22

The subsequent bounded #181 block extends the profile from 70 to 82 declared
edges, leaving 514 explicit coverage-debt edges. Twelve new disk/handler
witnesses distinguish the low-level legacy schema from public 0.5 conversion.
Additional modular-domain, remapping and handler-rejection controls pass with
the existing H5MSM/interaction/provenance suites: 1,488 passes, no skips/failures.
The [receipt](../devtools/data/conversion_execution_h5msm_20261022.json) retains
commands, versions and limits. No production code or handler capability changes;
source-test coverage is not a replacement candidate qualification. Publication
remains paused under #334 and #181 stays partial.

## PDB conversion execution and repairs — 2026-10-22

The next bounded #181 block adds 32 PDB file/text/handler routes: 114 selected
edges and 482 explicit unexecuted debt edges. Five runtime/resource defects
are repaired under #422–#425, with matching atom/coordinate selections, explicit
units, native multi-structure output and scratch ownership guarded. The broad
regression passes 2,284 tests without skips/failures; the focused profile/repair
run passes 175 cases plus a partition control, and six doctests pass. Three
User Guide/course notebooks are re-executed successfully. The
[receipt](../devtools/data/conversion_execution_pdb_20261022.json) records scope
and environment. #181 remains partial and publication remains paused under #334;
these source repairs are not installed-candidate qualification.

## SDF/PDBQT conversion execution — 2026-10-22

The next bounded #181 block adds 19 declared edges with 38 local syntax/layout
witnesses. The profile now selects 133 of 596 edges and leaves 463 explicit
coverage-debt edges. Rigid/tree PDBQT, V2000/V3000 SDF and explicit native writer
prerequisites execute directly and publicly. A loader sentinel finds #426:
explicit PDBQT detection reached an unrelated RDKit parser. Generic confirmed
prefix lookup repairs this without changing parsers, scientific methods or
public signatures. The broad regression passes 1,015 tests with no skips or
failures; the public doctest, two notebooks and focused developer-page render
also pass. The [receipt](../devtools/data/conversion_execution_docking_20261022.json)
retains versions and warnings, including the existing optional ABI warning
reserved for environment review. This source evidence does not qualify a new
candidate; #181 remains partial and publication stays paused under #334.

## Native SDF legacy and valence input extension — 2026-10-22

Under uibcdf/molsysmt#215, original Vina 1IEP now passes native reading/writing;
versionless 1S63 passes with explicit optional stereo interpretation. Declared
integer-covalent valence retains virtual H inventory in existing ChemicalStates
fields, including H5MSM 0.5 persistence, without inventing atoms or coordinates.
Aromatic/coordination valence interpretation and broader dialects remain pending.
Optional stereo writing of 1IEP still rejects a reconstruction mismatch rather
than silently emitting a changed result; its native round trip is covered.

The #181 docking profile now has 48 direct/public witness cases, with loader
isolation for each. Edge accounting is unchanged: 133 selected, 463 deferred,
596 declared. Neither #215 nor #181 is closed by this bounded expansion. Source
validation does not qualify installed packages or authorize publication.

Qualification: **751 passed, zero failures/skips, 50.79 s**, with 12 workers and
Pytest Receptor; one converter doctest and the updated course notebook pass.
All 14 fast gates pass. Details, warnings, executable-file hashes and environment
are in the [bounded source receipt](../devtools/data/sdf_legacy_valence_20261022.json).

## Prepared-atom projection and completed PDBQT maps — 2026-10-22

The bounded #223 implementation adds experimental
`build.merge_nonpolar_hydrogens`, with explicit H/HD policy, retained/merged/
excluded maps, parent virtual-H bookkeeping and charge conservation before
rounding. Derived assignments preserve their original calculation reports.
The native PDBQT writer still retains every supplied atom; optional
`return_atom_map=True` reports actual written order, ROOT/branch representation,
source axes, precision and payload hash. Ordinary returns remain unchanged.
Ackredit records Meeko as an inspected reference implementation, without making
it a dependency or claiming another source-charge calculation.

The source workflow is documented in the new projection tutorial and executed
course Module 12. Broader upstream generation-map composition, consumer adoption
and MODEL-aware pose reconstruction remain pending in #223/#226. No new format
version, detector or installed/release matrix is introduced. Public API and
scientific-evidence generated views classify the new tool as experimental,
outside the core scientific admission contract. #430 records native composition
limitations discovered here: numeric charge delivery is repaired, while explicit
four-domain reference-state metadata routing remains pending.

Qualification: **799 passed, zero failures/skips, 50.51 s**, with 12 workers
and Pytest Receptor; one meaningful doctest, executable User Guide examples
and the updated course notebook pass. All 14 fast gates pass. Detailed scope,
known warnings, hashes and environment are in the
[projection receipt](../devtools/data/atom_projection_20261022.json).


## Known-source PDBQT pose reader — 2026-10-22

The maintainer-authorized #226 extension is implemented and contract-tested in
`molsysmt.form.read_pdbqt_poses`, under the experimental form namespace. It
requires one complete source state and a completed PDBQT export map; validates
every pose; imports only observed coordinates; and rejects missing source atoms
unless the caller explicitly requests a retained subsystem. It never restores
omitted H from old coordinates. The User Guide, Cookbook and executed course
Module 19 document this boundary.

The final focused source run passed 838 tests with zero failures/skips and 37
unsuppressed warnings. Its real Vina 1IEP case compares imported positions with
the engine's numeric array within PDBQT quantization. One doctest, Ruff, API and
docstring checks and all 14 fast gates pass. See the
[source receipt](../devtools/data/pdbqt_pose_read_20261022.json) and
[resolved #226 record](archive/resolved_proposals/read_pdbqt_pose_ensembles_against_a_known_ligand_source.md).
This does not qualify a new installed pair, change publication authorization
under #334, or complete #223's earlier-preparation map composition.


## Native pandas and domain-composition repairs — 2026-10-22

#431 is repaired in `128a0bbb94e6804f5663e58a45313c77de1cc30d`; all five
exact-commit GitHub checks pass. Warning-strict native topology operations retain
their values, nullable metadata, bond-table identity and independent ownership.
The same 1,366 focused tests pass on pandas 2.3.3 and published 3.1.0. Consumer
receiving and documentation reruns remain owned by uibcdf/molsysviewer#264.
See the [record](archive/resolved_bugs/native_topology_inplace_calls_break_warning_strict_examples.md)
and [receipt](../devtools/data/native_pandas_compatibility_20261022.json).

#430 now composes explicit standalone native Topology, ChemicalStates, Structures
and MolecularMechanics providers through the owning native seam. Explicit
ChemicalStates owns chemistry; known axes validate before selection. Original
mechanical provenance and native ownership rules are retained. Missing structural
atom axes are distinguished from actual zero-length arrays. All 482 focused
source tests and the 76-case pandas 3.1.0 selection pass without failures/skips.
The executed guide/course, public doctest and 14 fast gates pass. See the
[record](archive/resolved_bugs/native_domain_composition_fails_on_charges_and_explicit_chemical_state_metadata.md)
and [receipt](../devtools/data/native_domain_composition_20261022.json).
Partial-MolSys/file composition still excludes mechanics, as does H5MSM 0.5
persistence. These fixes do not change #334's publication pause or replace
exact installed-pair qualification.


## Atom-map stage composition — 2026-10-23

The bounded #223 extension adds experimental `form.compose_atom_maps`: typed
direct and representative correspondences, explicit generated origins, creation/
projection/export/pose stages, incremental JSON round trips and source immutability.
The PDBQT pose adapter respects written versus known-source axes, and normalized
writer metadata retains ROOT order/origin, oriented branches and precision
evidence. Source arrays remain one-dimensional, including the 100,000-atom guard.
The owning [#223 record](archive/resolved_proposals/preserve_atom_correspondence_through_lossy_molecular_exports.md)
and [source receipt](../devtools/data/atom_map_composition_20261023.json) retain
commands, 568 passing focused cases, warnings, 18.5 s course execution and the
14 fast-gate checkpoint. Explicit backend atom-name projection and consumer
receiving remain pending. There is no new molecular form, H5MSM schema, installed
pair qualification or publication authorization under #334.


## Explicit atom-permutation delivery — 2026-10-24

The maintainer brings uibcdf/molsysmt#369 forward after provider completion of
uibcdf/molsysmt#223. The experimental public `basic.permute_atoms` applies a
complete declared atom order, returning detached native domains and optional
`atom_map@1` evidence. Extraction semantics and non-atom index axes remain fixed.
See the [delivery, guards and allocation measurements](archive/resolved_proposals/explicit_atom_permutation.md).
DockingMT migration remains owned by uibcdf/dockingmt#49. These local source
checks neither qualify a replacement installed pair nor authorize publication.

## MolSysViewer expert addon contribution

PR #543's source contribution exposes 240/244 declared callable paths, including
26/26 basic paths and four historical hbonds aliases that use the canonical
bound methods. Native MD stubs remain unavailable. The loaded-primary view
bridge returns a caller-owned visualization without cloning the parent's scene.
Native #568 and #564 repairs are received from their published owner; the
water-box factory still needs its own explicit-input consumer receiving.
Managed protonation remains independent-only under #576; native empty-view
digestion is separately reported under #578. Source exposure is not owner
admission, complete mode/scientific qualification or an installed release.

Current implementation and evidence belong to the
[owning proposal](pending_proposals/molsysviewer_tools_addon.md) and its immutable
[stage receipt](../devtools/data/molsysviewer_tools_navigation_receiving_20261105.json).
Exact-head CI, owner review, remaining native contracts, task GUI and installed
qualification remain separate. Both 1.0 publications stay paused. This compact
entry replaces duplicated unmerged consumer stage narratives; their original
receipts and proposal evidence remain preserved.


### Explicit water-factory contribution receiving

Consumer PR #543 adds `build.make_water_box` over the published #564 repair,
keeping box/form inputs explicit and output independent even from an empty
workspace. No primary read, scene adoption or scientific algorithm is added.
See the [consumer receipt](../devtools/data/molsysviewer_tools_water_factory_receiving_20261105.json).
Source exposure is 241/244, build 30/30; native forces #572, managed protonation
#576, remaining scientific contracts, owner review, CI, GUI and installed
qualification remain separate. Both 1.0 publications stay paused.

### First molecular-tools task panel

Consumer PR #543 now implements System / Remove atoms in source, with bounded
selection review and serialized confirmation through the existing expert
adapter. Local real-browser/native receiving is separate from owner review,
hosted CI, live Jupyter/Qt/popups and installed qualification. Viewer #297/#298
own diagnostic transport and stylesheet lifetime fixes. Geometry, Chemistry,
Analysis and other System tasks remain proposed; both publications stay paused.

### Native model/ion consumer receiving

PR #543 receives native 8c2661293 without authoring native algorithms; expert
exposure is 242/245 and build 31/31. The full addon gate passes 4,506 cases,
362 directed native checks and 321 Viewer controls pass separately. The
[source receipt](../devtools/data/molsysviewer_tools_native_model_ion_receiving_20261105.json)
retains original failures, course preservation and real browser evidence.
Native #583/#584 are reported; #582 and prior #572/#576 remain separate.
No new GUI beyond System / Remove atoms, owner-main integration, installed
qualification or publication is declared. Both 1.0 publications remain paused.

### Execution-platform consumer receiving

PR #543 receives native 50854766d (#559) with CPU/Reference model and result
ownership controls; the source full gate passes 4,512 cases, with 481 native/tool
controls and real browser receiving separately scoped in the
[receipt](../devtools/data/molsysviewer_tools_platform_receiving_20261105.json).
No new functional export, GPU/device qualification or scientific workaround is
introduced. Native #583/#584, #582/#572/#576 and proposed #587 remain explicit;
owner review, hosted CI, remaining tasks and installed qualification are pending.
Both 1.0 publications remain paused.


## Isolated bound-tools source reconciliation — 2026-11-06

An isolated receiving branch combines owner `030c201a5` and PR #543 contribution
`8ab2f5474b2e04c68d31ef2854a238984b645fc8`. This is an uncommitted integration
state, not a main-branch delivery or a qualified candidate. Owner native science,
dependency floors/acquisition metadata and resolved records remain authoritative.
The incoming pending copies of #605/#606/#607/#608/#613/#616 are omitted because
their owner resolutions are already archived; their original PR history and
receiving receipts remain available.

The contribution adds the reviewed System, Geometry, Chemistry and Analysis
source tasks, native force and prepared-protonation consumers, and their guards.
Its dated 246/248 path inventory is exposure, not complete scientific, mode or
graphical acceptance. The original 4,974-case collection has eight failures; the
63-case affected recovery is separate, as recorded in the
[contribution recovery receipt](../devtools/data/molsysviewer_tools_reference_full_recovery_20261106.json).
Those historical results do not qualify this owner/contribution combination.

The five controlled workflows and dependency inventory retain owner Viewer
`42234de839ed047016f8f241ea5eb717cfeb07be` pending the separate preflight and
receiving of a newer exact published host. Viewer #314 has a source correction
in `25061d9e99baf07fa0dcb4021897958a226f0152`; this reconciliation does not yet
select it or claim its combined acceptance. The
[phase-four plan](pre_1_0_robustness_audit_20261106.md#phase-4--bound-tool-contribution-and-graphical-receiving)
and [owning proposal](pending_proposals/molsysviewer_tools_addon.md) retain
remaining source, graphical, installed and human/visible-Qt obligations. No
pytest, new CI run, merge commit, main integration or publication is implied.

## Bound-tools complete source receiving — 2026-11-07

The earlier isolated-reconciliation entry is now superseded for execution state
by merge `653ed8e0b48020a6b6ccf7aeeb186290784eee71` on a separate receiving
branch, with parents owner `030c201a5` and contribution `8ab2f5474`. Main remains
at the owner checkpoint; no main delivery or new candidate is claimed.

Exact published Viewer source `25061d9e99baf07fa0dcb4021897958a226f0152` passes
import/API preflight and complete combined Python receiving: **5,009 passed,
zero failures/errors/skips**, reusing the unchanged native backend. This consists
of 4,974 addon cases and 35 inventory/native-viewer guards; it includes no actual
Jupyter node. Owner science/tests/archives and the incoming addon runtime/guards
are preserved. The five controlled workflows and dependency inventory were
aligned to this host after receiving; their four static checks pass. Native
exits, identities, preservation and unsuccessful nonproduct attempts are in the
[source receipt](../devtools/data/bound_tools_owner_source_receiving_20261107.json).

#421 remains partial. #602, actual Jupyter/popup and conformational navigation
receiving, remaining accepted graphical families, hosted/installed and postponed
human/visible-Qt qualification stay open. Viewer #314's source correction is not
its complete acceptance. Accepted audit progress remains **40%**, with 19
audit-related issues closed. No remote matrix, tag, Release or promotion was
authorized or dispatched by this source checkpoint.

## Explicit bound-tools GUI receiving — 2026-11-07

The exact `653ed8e0` / Viewer `25061d9e9` runtime combination now receives four
implemented scenarios across separate executions. The first campaign has three
passes (Preparation six steps, pending chemistry eight, periodic geometry eight)
and an Analysis server-readiness failure before any browser. A diagnostic
Analysis run reaches nine steps and fails on a root-prepared auxiliary built
with the wrong format. Rebuilding only that test auxiliary by the exact host
command and preflighting its required global/function permits the unchanged
Analysis driver and corrected wrapper to complete all twelve steps (native
zero, 79.964 seconds including pytest startup). The
[GUI receipt](../devtools/data/bound_tools_owner_jupyter_receiving_632_20261107.json)
preserves all outcomes, origins, hashes, native exits and page-error controls.

#632 records the stale seven-step wrapper separately; the local correction
requires the complete ordered twelve-name sequence. Source delivery/closeout
remain pending. The initial server-readiness observation is not the original
#615 canvas stage, and neither is causally closed. #602, all remaining accepted
graphical families, the full Jupyter selection, #314 conformational navigation,
hosted/installed and postponed human/Qt acceptance remain due. Accepted audit
progress is still **40%**, with 19 closed audit-related issues. No publication
or new remote matrix follows from these local source/GUI results.
