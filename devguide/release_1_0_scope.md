# Frozen MolSysMT 1.0 Scope

**Role:** normative release-scope decision
**Accepted:** 2026-10-05 by the maintainer
**Tracking:** uibcdf/molsysmt#334

The maintainer freezes the feature scope at source
`d609187ae17af089ef976116252e5a64b6331210`. Development now completes the
bounded stabilization queue below. This decision does not certify that source,
authorize a tag or release, or replace the [exact-candidate release gate](release_gate.md).
The [execution ledger](release_1_0_status.md) records completion and evidence.

## Pre-1.0 version checkpoint

On 2026-10-06 the maintainer selects **MolSysMT 0.23.0 / MolSysViewer 0.24.0**
as the next pre-1.0 version checkpoint. Prepare and qualify their packages
before deciding whether the evidence supports 1.0.0. The feature freeze and
stabilization admission rule below remain in effect; this checkpoint does not
reopen feature development or declare experimental contracts stable.

The maintainer has separately authorized candidate construction and upload to
staging. This authorization does not authorize a public tag, GitHub Release or
main-label promotion. Preserve source/artifact receipts with their original
versions, producers and digests, and execute the applicable exact-candidate
gates. Publication requires separate final approval. The
[execution ledger](release_1_0_status.md#resume-from-here) owns the selected
source identities, staged-file evidence and remaining qualification work;
historical package receipts do not qualify a different candidate.

## Admission rule

Admit a change before 1.0 when it fixes incorrect results, lost information,
inconsistent public contracts, an installability/policy defect, or a failed
workflow within the accepted scope. Documentation and tests for those changes
are part of the fix. A missing capability is not automatically a defect in a
method that explicitly excludes it.

New methods, chemistry coverage, forms, storage capabilities and performance
redesigns require an explicit maintainer scope change. Otherwise preserve them
in an owned post-1.0 issue. A measured performance defect that prevents an
accepted workflow may be promoted with evidence; an opportunity to be faster
alone does not expand the release queue. Public experimental APIs remain
experimental unless a separately justified stability decision changes the registry.

## Included behavior

### Bounded geometry admission — 2026-10-10

The maintainer explicitly admits `structure.get_vectors` under
uibcdf/molsysmt#375 after reviewing its name, distance-like endpoint/center and
structure-pair semantics, and Rust execution requirement. Admission covers the
experimental general geometry tool and its documented composition with existing
fixed-state donor-H recognition. It does not admit an acceptor lone-pair model,
environmental hydrogen refinement, GPU execution or another detector. Frozen
installed candidates retain their original identity; this source addition needs
later qualification under uibcdf/molsysmt#334 before inclusion in a new candidate.

The maintainer subsequently admitted `interactions.hbonds.get_hbond_site_directions` in
the same discussion. This bounded experimental source addition covers observed
indexed donor-H directions and ideal carbonyl, pyridine-like N and nitrile N
hypotheses, with explicit unsupported/undefined outcomes. It composes existing
chemical and geometric owners; broader lone-pair models, environmental
refinement and another detector remain outside the exception. See the
[normative site-direction contract](hbond_site_directions.md). This admission
does not change frozen artifacts or authorize publication.

### Existing scope

- The existing form-agnostic public API, supported form tiers, strict-loss and
  accepted-debt contracts remain authoritative. No universal conversion coverage
  claim or new optional backend is added.
- `MolSys` retains independent topology, chemical-state, structure and named
  interaction domains, including supported partial combinations. `ChemicalStates`
  owns chemical assignments and bonds. Keep `Topology.bonds` as its documented
  compatibility facade; retirement remains #255.
- Public writers emit H5MSM 0.5. Preserve supported domain associations, named
  analyses, original producers, quantity records and preparation history. Read
  legacy 0.3/0.4 with the documented warning and migration route. Structures-only
  files must load as partial `MolSys` and support explicit index extraction.
  Unsupported compositions must fail before silently losing information.
- The implemented sparse `Interactions` contract includes roles and compound
  participants, parallel observations, occurrence indices, explicit evaluated
  coverage/search scope, atom/structure queries, source maps, units, evidence,
  periodic images, execution provenance and typed persistence. Preserve invalidation
  on supported coordinate/chemistry edits, compatible structure replacement,
  bounded resident export and explicit compaction. This is not a general mutable
  observation editor or direct detector-to-file stream.
- Keep the nine implemented interaction families and their documented methods
  within their current experimental profiles, including exact one- and two-water
  paths and broad metal-distance candidates. New families, metal-specific physics,
  longer water networks and scientific superiority claims are outside this release.
- Preserve the implemented experimental SDF/PDBQT and chemical-preparation tools
  within their explicit profiles: declared maps/templates, fixed chemical states,
  readiness/coverage, optional RDKit H placement, named charge/type models and
  bounded native covalent inference. Unknown bond orders, unresolved H names,
  ambiguous geometry and unsupported encodings must remain visible. There is no
  promise to prepare every ligand/receptor or reproduce every OpenMM edge.
- Preserve optional lazy Ackredit attribution in the interaction pilot, original
  bibliography and producer versions. Portable-provider migration and whole-library
  instrumentation remain #292/#27; provider absence must not lose completed science.
- `MolecularMechanics` remains minimal and experimental. Its persistence stays
  outside H5MSM 0.5 and is rejected when nonempty, pending #256/H5MSM 0.6.

The symbol stability registry and owning normative documents define exact
signatures and semantics. This scope decision does not redefine their methods.

## Finite stabilization queue

These six packages identify decisions and evidence still needed, not six proven
runtime failures. Complete each package against a named source before selecting
the final release candidate.

| Package | Owning issues | Exit condition |
| --- | --- | --- |
| S1. Triage old reported defects | #25, #30, #112 | Reproduce or inspect the original naming, GRO/MDTraj topology and empty-alternate claims against current source. Classify each as fixed with an addressable guard, an accepted convention/limitation with justification, or a reproduced defect requiring repair. An old title alone is neither proof nor dismissal. |
| S2. Close the existing native/result contracts | #250, #251, #252, #254 | Reconcile acceptance criteria against current code and guards for independent domains, remap/invalidation, typed results and supported H5MSM round trips. Obtain explicit MolSysViewer feedback on the updated result, coordinate images, selections and saved-session workflow under uibcdf/molsysviewer#114. No new interaction family or arbitrary editor is required. |
| S3. Qualify the current experimental preparation/form profiles | #334, with evidence from #214, #215, #304 and resolved preparation work | Test/review the already implemented public paths, original atom/structure axes, units, state/history persistence and conservative exclusions. Repair correctness defects in that scope. Broad parser chemistry, H aliases, terminal/disulfide inference and new preparation engines remain their post-1.0 extensions. |
| S4. Reconcile public claims and documentation | #186, #192, #199 | Verify actual README/landing-page claims, experimental labels, suite positioning and affected exported views. Close obsolete reports with existing evidence or correct the current affected surfaces. User Guide, Cookbook, course, doctests and the required documentation build must reflect included behavior; a global warning-clean rewrite is not required. |
| S5. Reconcile dependencies, Python and policy | #237, #244, #245, #286 | Audit public dependency floors and source/install routes, finish required Python 3.11–3.14 workflow/admission obligations, and record support-library/developer-tool reviews or permissible bounded exceptions. Review current coverage evidence and its accepted badge absence; do not run a separate full suite solely for the badge. Old pre-1.0 exceptions do not authorize 1.0 omissions. |
| S6. Qualify and approve exact artifacts | #334; release gate and Viewer-owned gates | Choose exact provider/Viewer candidates, execute every required scientific/full-suite, source, wheel, Conda/installed-pair and documentation gate, retain artifact identities/digests and resolve failures. Publication requires separate final approval. Complete public-artifact and Zenodo verification afterwards. |

MolSysMT requires the agreed MolSysViewer provider integration. The Viewer team
owns canvas, browser/Qt and session presentation; MolSysMT owns scientific and
persistence fidelity. TopoMT, DockingMT and PharmacophoreMT integrations remain
valuable follow-up evidence without becoming additional 1.0 integration gates.
Existing tests or consumer feedback may expose a provider correctness defect;
such a defect is triaged under the admission rule regardless of who found it.

S1 and S4 are review work, not authorization to close issues without evidence.
S5 includes reconciling the old 3.13 scientific routes with the accepted 3.14
policy under #237. A partial full matrix or a historical installed pair does
not, alone, establish that updated requirement. No heavy matrix is
executed by this scope decision.

## Preserved post-1.0 work

Milestones classify the **remaining work of an issue**, not whether code already
implemented under that issue ships in 1.0. For example, #304 stays open for
broader chemistry while its bounded engine/policy contract remains included.
Do not close an issue merely to clear a milestone or move an unresolved
current-profile correctness defect into an extension backlog.

The 2026-10-05 read-only board snapshot contained 75 open issues. Four additional
extension issues now preserve previously discussed work independently of the
1.0 result contract. Together with #334, this classification covers that snapshot
and the five new issues. Future reports use the same admission rule.

| Deferred theme | Owning issues | Preserved boundary / next question |
| --- | --- | --- |
| General APIs, forms and older request reconciliation | #1, #9, #12, #22, #28, #47, #95, #106, #113, #114, #119, #120, #121, #123, #124, #134, #135, #173, #188, #206, #242, #243 | Evaluate remaining additive APIs/format coverage and reconcile already delivered portions before implementing anything. Existing output/CI/copy capabilities are not declared missing merely because their old issue is open. |
| Performance and backend experiments | #7, #8, #110, #122, #125, #128, #130, #132, #151, #154, #155, #205 | Profile relevant workloads before choosing graph/dataframe/search, unit-boundary, compilation or packaging changes. Preserve scientifically correct current behavior. |
| Chemical preparation, states and docking correspondence | #177, #219, #220, #223, #225, #226, #229, #230, #249, #304, #308, #310, #323, #327 | Keep environment-dependent pKa, conformer/state enumeration, mapped lossy exports/poses, additional native PDB chemistry, native ligand H, symmetry correspondence and constrained repair/refinement as separately qualified extensions. #304 retains H-name/terminal/group/disulfide/declaration/performance work and the original-input disagreements. |
| Broader adapter/form qualification | #181, #214, #215 | Preserve the delivered experimental profiles; defer exhaustive conversion-edge coverage and new unsupported PDBQT/SDF encodings or wider chemistry. |
| Accepted delivery/documentation debt | #139, #144 | Maintain truthful supported tiers, existing ratchets and documentation integrity. Broader lower-tier remediation and global Sphinx cleanup remain visible; newly broken included workflows are not accepted debt. |
| Attribution expansion | #27, #292 | Keep the pilot intact; review portable provider compatibility/publication and wider instrumentation separately. |
| Scientific interaction extensions and comparison | #262, #271, #337, #338 | Extend formal-charge motifs, compare cation-pi definitions, study metal-specific coordination and assess longer water paths. No automatic implementation or improved-accuracy claim. |
| Native ownership and mechanical persistence evolution | #255, #256 | Retire the compatibility bond facade and design H5MSM 0.6 mechanics after 1.0. |
| Manuscript/evidence presentation expansion | #190, #191 | Define manuscript claims and extend the experimental claimed-evidence view before the relevant publication. Current software claims must already be truthful under S4. |
| Individual interaction editing | #335 | Add/remove individual observations and optionally prune unused definitions with explicit occurrence/relation-handle semantics, immutable snapshots and bounded costs. Structure replacement/invalidation/compaction are already implemented. |
| Streaming and resumable H5MSM | #336 | Direct detector-to-file accumulation, append with topology/named analyses, transactional visibility and crash recovery. Existing numeric-window export and narrowly supported topology-free append remain available. |

At the scope-freeze checkpoint, the public board uses `1.0.0` for S1/S2/S4/S5 owner issues and #334, and
`Post-1.0` for the extension/debt issues above. The associated proposal/bug
documents retain their actual lifecycle status; deferral is not resolution.
Subsequent triage may move an extension-only remainder to `Post-1.0` or close
a verified defect. The execution ledger records those decisions; the original
snapshot is not a requirement to keep completed reviews in the release queue.

## Stop and publication decisions

1. Stop adding capabilities now; complete S1–S5 and repair admitted defects.
2. Once the supported contracts and client feedback agree, freeze exact candidate
   sources and artifact plans for S6. There is no new calendar deadline or
   unsupported progress percentage in this decision.
3. A gate failure returns only its affected scope to stabilization. A feature
   request goes to the backlog unless the maintainer explicitly changes scope.
4. A source scope freeze is distinct from candidate qualification, publication
   approval, artifact availability and archival sign-off.

The older 99% number in the execution ledger belongs to the completed historical
weighted campaign. It must not be used as an estimate of how much current
stabilization or recertification remains after the subsequent API changes.
