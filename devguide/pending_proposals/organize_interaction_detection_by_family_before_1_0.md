---
summary: Organize interaction detection by family before 1.0
issue: uibcdf/molsysmt#250
status: partial
opened: 2026-09-28
closed:
verification: measured
area: [api, build, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Organize interaction detection by family before 1.0

**Reported:** 2026-09-28, during pre-1.0 API planning for MolSysMT and its
MolSysSuite consumers.
**Status:** Namespace, detector migration and persistent result routes implemented
and accepted in the published consumer pair; exact-1.0 recertification remains open.

## Published acceptance reconciliation — 2026-10-07

The [updated consumer packet](../interactions_molsysviewer_review.md#published-consumer-acceptance--2026-10-07)
records explicit acceptance from the now-closed uibcdf/molsysviewer#114 and
the published 0.23.0/0.24.0 pair's 8/8 source and 16/16 installed matrices.
Earlier awaiting-feedback statements remain historical checkpoints. This
acceptance preserves the experimental API and existing workload limits.

The issue stays partial because its criteria explicitly retain exact-1.0
release recertification. Implementation and published consumer delivery are
complete; final-candidate obligations remain under #334. No new feature is
added to the frozen scope.

## S2 acceptance reconciliation — 2026-10-05

The [current review packet](../interactions_molsysviewer_review.md#s2-stabilization-review--2026-10-05)
records Python 3.14 provider boundary checks and local Viewer projection/session
parity for all nine families and both water orders. Legacy outputs, namespace
and build-wrapper guards remain separate from actual canvas acceptance.
The [scope freeze](../release_1_0_scope.md) now governs admission; remaining
chemistry/method expansion is not implicitly pre-1.0. No new detector was
implemented at this checkpoint. This issue remains partial pending its
consumer and exact-candidate acceptance criteria.

## Consumer review checkpoint — 2026-10-02

The [updated packet](../interactions_molsysviewer_review.md) pins clean provider
`1986027c353cdcf290e0402b1d8fa23fee6ea637`. The current editable Viewer generated
positive frame scenes for all nine families and both water mediator orders,
with initial/session-restored protocol payload parity. This supersedes the older
two-family projection observation for this particular local consumer checkout.
It does not establish a clean published consumer pair or browser/WebGL support.
Source states, hashes, tests and limits are retained in
[the implementation evidence](../archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md#pinned-consumer-review-packet--2026-10-02).
The inventory below is unchanged; consumer feedback and full integration CI
remain required before treating the experimental contract as settled.

## Current checkpoint — 2026-10-01

The current inventory contains nine implemented experimental families. Their
remaining scope and release qualification are recorded below:

| Planned family | Implemented public entry point | Remaining scope |
| --- | --- | --- |
| Hydrogen bonds | `interactions.hbonds.get_hbonds`, `get_buch_hbonds`, `get_luzard_chandler_hbonds` | Preserve legacy defaults; modern method/profile definitions and optional attribution are implemented. |
| Disulfide candidates | `interactions.disulfides.get_disulfide_candidates` | Geometric observations, not certification or storage of covalent bonds. |
| Ionic observations | `interactions.ionic.get_ionic_interactions` | Bounded formal-charge centers; phosphate/sulfate and aromatic delocalization extensions remain under `uibcdf/molsysmt#262`. |
| Pi-pi | `interactions.pi_pi.get_pi_pi_interactions` | Reference profiles and the explicit-cutoff proposal are implemented; broader comparison remains open. |
| Cation-pi | `interactions.cation_pi.get_cation_pi_interactions` | Reference profiles and the explicit-cutoff proposal are implemented; comparison is tracked by `uibcdf/molsysmt#271`. |
| Halogen bonds | `interactions.halogen_bonds.get_halogen_bonds` | ProLIF-adapted distance/two-angle profile and general site recognition implemented under `uibcdf/molsysmt#277`; original-paper and Mol* alternatives remain distinct. |
| Hydrophobic associations | `interactions.hydrophobic.get_hydrophobic_interactions` | Pinned atomic SMARTS/distance profile and general `physchem.get_hydrophobic_sites` implemented under `uibcdf/molsysmt#278`; distinct from residue scales and an energetic model. |
| Metal coordination | `interactions.metal_coordination.get_metal_coordination` | Pinned metal/ligand SMARTS and inclusive distance candidates under `uibcdf/molsysmt#280`; separate from declared connectivity. |
| Water-mediated hydrogen bonds | `interactions.water_bridges.get_water_bridges` | Exact one- or two-water paths under `uibcdf/molsysmt#281` and `uibcdf/molsysmt#282`; preserve directed hydrogen roles and coherent images. Higher orders remain future work. |

The maintainer added water-mediated hydrogen bonds to the explicit
inventory on 2026-10-01. They extend the initial eight-family list without
becoming a ninth mandatory 1.0 requirement. No public empty family stubs
are introduced. The later [2026-10-05 scope freeze](../release_1_0_scope.md)
now excludes implicit admission of new families or scientific criteria before
1.0. Existing broader chemistry and method comparisons retain their owners.

The current normative contract is [Interaction Analysis API](../interactions_api.md).
Scientific/descriptive method selectors, exact profiles and portable optional
Ackredit attribution are implemented at `e21f03d9992b87af2cc9285211adee888462be41`.
The initial attribution pilot remains partial under `uibcdf/molsysmt#27` because
whole-library and suite adoption are separate work. Named `MolSys.interactions`
and H5MSM 0.5 round trips are implemented under #251/#252. Real local Viewer
qualification now checks geometry, queries and H5MSM/session round trips;
the reproducible evidence and its release limitations are recorded in
[the implementation report](../archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md#consumer-and-attribution-checkpoint--2026-10-01).
The current nine-family provider and existing consumer checks passed at clean
source `3b12fba50`; the exact scope and remaining visual qualification are
recorded in [the provider checkpoint](../archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md#nine-family-provider-qualification--2026-10-01).
The dated migration records below describe earlier checkpoints; their pending
statements do not override this inventory.

## Consumer handoff for the implemented families

The provider now exposes experimental results for hydrogen bonds, disulfide
candidates, ionic observations, pi-pi, cation-pi, halogen bonds, hydrophobic
associations, metal coordination candidates and water-mediated hydrogen bonds.
The last family supports exact paths through one or two distinct waters.

These calculations return the same public `Interactions` model, with their
actual participant roles, searched atom scope, evaluated frames, geometry,
units, method/profile, evidence, periodic images and original producer
attribution. Existing legacy hydrogen-bond and disulfide tuple defaults remain
available. The detector returns an analysis; the caller attaches it under a
name in `MolSys.interactions`. Named analyses survive public H5MSM 0.5
conversion. Calculation and scientific criteria remain provider-owned.

For the next MolSysViewer review, separate accepting and persisting these
analyses from rendering their geometry. The dated two-family consumer smoke
was followed by local Python projection/session parity for all nine families
and both water orders, recorded in the review packet. Actual canvas and clean
candidate acceptance remain separate. Each family needs its documented
visual semantics: rings are composite participants; metal coordination
is a candidate rather than certified bonding; water paths contain multiple
directed donor/hydrogen/acceptor roles and coherent images for every leg.
Unsupported geometry must remain explicit rather than dropping roles or
reinterpreting a compound relation as a single atom pair.

MolSysViewer owns the next visual and session qualification for these families.
Its feedback should identify the provider/client sources tested, the analysis
and method/profile, selection/frame changes, reconstructed periodic geometry,
and persistence or export behavior. Provider stabilization and the complete
1.0 candidate gate remain open; broader chemistry and incremental/out-of-core
extensions keep their existing separate issues.

## What

Introduce a public `molsysmt.interactions` namespace organized by chemically
interpreted families, beginning with `interactions.hbonds` and a disulfide
candidate detector. Keep `molsysmt.build.get_disulfide_bonds` as the existing
build-oriented entry point, potentially delegating to that detector. The
pre-1.0 decision is about the analysis API and its migration. Additional
interaction families are approved and scheduled separately. A persistent
`Interactions` domain inside `MolSys` and H5MSM is required before 1.0;
its contract and implementation are tracked in
[`uibcdf/molsysmt#251`](../archive/resolved_proposals/design_a_sparse_public_interactions_result_and_serialization_contract.md)
and [`uibcdf/molsysmt#252`](../archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md).

The candidate families are hydrogen bonds, ionic or salt-bridge interactions,
halogen bonds, hydrophobic associations, metal coordination, aromatic stacking,
cation-pi interactions, and disulfide candidates. This is a planning inventory,
not a promise that each family will ship in 1.0 or that each relationship has
the same chemistry or representation.

## How

### Accepted boundary for the namespace

- `interactions` classifies relationships using explicit chemical and geometric
  criteria. A distance-only contact map remains a geometric primitive in
  `structure`; proximity alone is not an interaction classification.
- `interactions.hbonds` owns hydrogen-bond analysis. Existing Buch and
  Luzard–Chandler methods and donor/acceptor helpers provide the first migration
  candidates. Preserve method identity rather than presenting different
  criteria as interchangeable.
- `interactions.disulfides` owns **candidate detection** from chemistry and
  structure. A candidate inferred from S–S proximity is not an authoritative
  covalent bond. Recorded covalent connectivity belongs to `ChemicalStates`,
  with `Topology.bonds` retained as a compatibility facade; build
  continues to decide how candidates contribute to repair or missing-bond
  inference. The public detector is `get_disulfide_candidates`, returning
  atom-index pair arrays and aligned distance quantities per requested
  structure. The build entry point continues to return pairs for one structure.
- Metal coordination likewise needs an explicit distinction between observed
  coordination geometry and any connectivity declared in a chemical state.
- This callable namespace is distinct from the proposed native or form-level
  `Interactions` information domain. The latter currently targets non-covalent
  and coordination relationships, not covalent bond truth. The distinction must
  be resolved in the documentation before either surface is made stable.

### Roadmap and decision gates

| Stage | Proposed timing | Deliverable and exit condition |
| --- | --- | --- |
| 0. Decide the contract | Before implementation | Agree the namespace tree, meaning of `disulfides`, naming and compatibility policy for `msm.hbonds`, single- versus multi-structure semantics, and the minimum shared result contract. Record the maintainer decision here and on issue closure. |
| 1. Establish the namespace | Before 1.0 if stage 0 is accepted | Add lazy public discovery and stability classifications for `msm.interactions` and implemented family modules. Do not publish empty family stubs. Keep optional imports lazy and audit import cost. |
| 2. Migrate hydrogen bonds | Before 1.0 if stage 0 is accepted | Make `interactions.hbonds` canonical, retain or retire `msm.hbonds` according to the agreed compatibility policy, preserve named-method behavior, and cover empty, selected, PBC, and multiple-structure cases. Reject unsupported advertised combinations explicitly. |
| 3. Separate disulfide detection from build | Before 1.0 if stage 0 is accepted | Define per-structure S–S candidates with the evidence used to infer them. Make `build.get_disulfide_bonds` a thin compatibility entry point and keep `build.get_missing_bonds` behavior explicit. Test candidates, already-recorded bonds, group filters, PBC, and selection. |
| 4. Integrate and recertify | Before the 1.0 candidate freeze | Update API registry, argument digestion callers, User Guide, API reference, Cookbook or examples, affected Four Paths modules, and MolSysViewer compatibility or its bridge. Run focused scientific and consumer checks, then all applicable release gates on the new exact commit. |
| 5. Add further families | Separately scheduled; not a closure gate for this pre-1.0 migration | Prioritize ionic/salt-bridge, pi-pi, cation-pi, halogen, hydrophobic, metal-coordination, and mediated interactions from consumer use cases and available chemical-state evidence. Each family needs its own method definition and independent validation. The first ionic delivery is tracked by #261. |
| 6. Integrate persistent interaction data | Before 1.0, tracked by #251 and #252 | Attach optional results to `MolSys`; define remap or invalidation on source edits; persist and recover them in a versioned H5MSM interaction layer. The broader attribute-centric architecture and cross-system alignment remain separate decisions. Stage 5 is not a closure criterion for this namespace issue. |

The minimum result contract in stage 0 must distinguish: participant roles and
index spaces; selected structure indices and their order; observed versus
declared relationships; method, parameters, and units; empty evaluated results
versus analysis not run; and periodic images when they identify a different
observed participant. It must allow hydrogen-bond triples and ring/group
participants, not only atom pairs. The concrete result class and schema are
tracked in [`uibcdf/molsysmt#251`](../archive/resolved_proposals/design_a_sparse_public_interactions_result_and_serialization_contract.md).

The detector-to-result route is separate from MolSysViewer's initial use of
already constructed analyses. Preserve existing detector outputs by default
and add opt-in `Interactions` results only when each method can report actual
atom-role eligibility, evaluated frames including empty ones, parameters,
units, evidence, and periodic images when used. The disulfide candidate
detector and both hydrogen-bond methods now have opt-in routes, with
calculation-time software versions preserved in the result and H5MSM.
The returned analysis is attached to `MolSys.interactions` by an explicit
name; a calculation does not silently replace stored analyses. One named
result represents one method and evaluation scope, although that method may
classify multiple interaction types.

The Rust neighbour-list kernel still returns only indices and distances.
The disulfide adapter runs a sparse observed-pair MIC pass using the same
minimum-image algorithm, derives each S-S lattice shift in the original box
basis, and verifies that its distance matches the detector output. This does
not add image columns to the default neighbour path. The Buch adapter uses
consistent D-H and H-A images, anchored on the donor, and verifies the
observed H-A distance. It declares automatic role-selection rules and the
eligible participant universe, including attached hydrogens outside an atom
selection. Evaluated-empty and varying-count frames are now supported by the
Buch tuple result as well, resolving `uibcdf/molsysmt#253`. Its optional
analysis rejects supplied roles, a second structure axis, and partially
overlapping participant universes; these require further contracts. A
Luzard–Chandler triple now uses donor-anchored D-H and D-A images and checks
both D-A distance and H-D-A angle. Its default output preserves empty and
varying-count frames under `uibcdf/molsysmt#259`. Analytical fixtures protect
triclinic boxes, rotated orthogonal boxes, angular evidence, and the half-box
tie chosen by the angle kernel. A distance-only recomputation is insufficient
evidence for a chosen image. Benchmark the
sparse observed-pair pass before relying on its cost at trajectory scale.
Large trajectory methods should use the maintained chunked-execution
policy and avoid dense atom-pair-by-frame output by default.

The observed-pair work exposed a prior MIC defect: rotated orthogonal boxes
were sent through a Cartesian-diagonal fast path. Its correction and
independent lattice-image guard are tracked by `uibcdf/molsysmt#257`.

Participant checks also found the donor helper could sort its two columns
independently and break covalent donor-H membership. The intact-row correction
and interleaved-index guards are tracked by `uibcdf/molsysmt#258` and apply to
both existing hydrogen-bond detectors.

Cross-system analysis requires explicit atom and frame/time alignment. It must
not be inferred from matching positional frame numbers. Current hydrogen-bond
signatures advertising a second molecular system need an implementation audit
before their new paths become canonical.

MolSysMT owns the general molecular-system detectors and their scientific
contracts. MolSysViewer owns presentation, TopoMT owns pocket-specific
interpretation, and PharmacophoreMT owns pharmacophoric features and models.
MolSysViewer integration is required before 1.0 under
`uibcdf/molsysviewer#114`; the other client integrations can follow later.
If acceptance creates a shared result or rollout contract for
multiple suite members, open a linked `uibcdf/molsyssuite` coordination issue
under the suite ownership policy; this MolSysMT issue remains the provider
implementation record.

## Why — original motivation (2026-09-28)

[The public root](../../molsysmt/__init__.py)
originally exported `hbonds` separately, while
[`build.get_disulfide_bonds`](../../molsysmt/build/get_disulfide_bonds.py)
uses geometric contacts to infer pairs and
[`build.get_missing_bonds`](../../molsysmt/build/get_missing_bonds.py) consumes
those pairs for repair analysis. The
[API stability registry](../api_stability_registry.md) currently classifies
both surfaces as experimental. Moving the analysis boundary before a 1.x API
contract is established is feasible, but requires more than a directory move:
public imports, argument digesters, docs, course examples, and the
[MolSysViewer addon](../molsysviewer_addon.md) refer to the current paths.

The [attribute-centric architecture proposal](attribute_centric_molecular_system_model.md)
already identifies hydrogen bonds, aromatic interactions, cation-pi, halogen,
metal coordination, and frame-dependent occurrences. Its broader architecture
remains a separate proposal. This report covers the analysis namespace;
#251 and #252 cover the required native and H5MSM interaction domain.

## Decision record and implementation evidence

### Modular extension decision — 2026-09-30

The maintainer accepts ionic, pi-pi, and cation-pi as the next sequence,
starting with the independently scoped [ionic proposal #261](../archive/resolved_proposals/implement_ionic_interactions_with_reusable_molecular_tools.md).
Reusable charge interpretation and hydrophobic typing belong in `physchem`,
connectivity tools in `topology`, geometry in `structure`, and reconstruction
and image conventions in `pbc`. Family detectors orchestrate those tools and
apply their named scientific criteria. Existing compiled primitives are
reused; further heavy routines may be implemented in Rust with profiling and
scientific parity evidence. This supersedes the earlier assumption that every
additional family must wait until after 1.0; it does not add them as release
or closure gates. Delivery dates remain separately scheduled.

The component reconstruction already exists through `pbc.wrap_to_mic` and
`pbc.wrap_to_pbc` with `compact='component'`. Returning reconstruction image
shifts and representing split compound participants in Interactions remain
separate design work. Residue hydrophobicity scales already exist, whereas
atom hydrophobic typing needs its own explicit definition. The new record
documents inspection evidence and intended work, not implemented detectors.

### Original migration decision and evidence

- The accepted pre-1.0 tree contains `interactions.hbonds` and
  `interactions.disulfides`; other families remain separately scoped decisions.
  `msm.hbonds` and its direct module imports remain compatible aliases, without
  a deprecation decision in this release.
- The existing Buch and Luzar–Chandler implementations were moved with their
  criteria unchanged. The public disulfide detector returns one pair array and
  one aligned distance quantity per requested structure, including empty
  evaluated structures. These are observations, irrespective of whether the
  corresponding bond is already recorded in topology.
- `build.get_disulfide_bonds` delegates to the detector and preserves its
  single-structure list-of-pairs result. `build.get_missing_bonds` continues to
  consume that build entry point.
- The current contracts and evidence level are recorded in
  [Interaction Analysis API](../interactions_api.md). The two hydrogen-bond
  methods retain legacy method-specific default output layouts. At this initial
  checkpoint, the optional common result schema had not yet been adopted;
  its subsequent implementation is summarized above and in #251/#252.
- Focused migration tests pass for the legacy hydrogen-bond namespace and for
  empty single-selection hydrogen-bond results, as well as disulfide selection,
  group filtering, periodic geometry, frame order, empty results, and recorded
  bonds. Broader trajectory and cross-selection behavior, documentation,
  consumer, and release
  gates are still pending; this is not release evidence yet.

## Original inspection and assumptions — 2026-09-28

- **Inspected:** the root lazy registry exposes `hbonds`; the hbonds package
  exports four rule lists, two atom helpers, and two named methods; the disulfide detector
  returns pairs inferred from S–S distance and group filters; and
  `get_missing_bonds` consumes those pairs. No runtime or scientific-validation
  measurement was made for this report.
- **Inspected:** the public stability registry marks `molsysmt.hbonds`, its
  functions, and `molsysmt.build.get_disulfide_bonds` experimental.
- **Consumer requirement:** MolSysViewer needs the provider result before
  1.0 under `uibcdf/molsysviewer#114`. TopoMT, PharmacophoreMT, and DockingMT
  may need it later; their integrations do not gate this release.
- **Estimate:** a bounded namespace migration can fit before 1.0 if the
  compatibility and scientific gates are limited to the existing hbonds and
  disulfide surfaces. This is a planning judgement, not a schedule measurement.

## What was refuted

- A flat list of every future detector at the `interactions` root would obscure
  family-specific criteria and helper operations. Family modules are the
  current design preference.
- Treating all distance-only contacts as interactions would confuse candidate
  generation with chemical classification. `structure.get_contacts` remains a
  useful primitive and should not be migrated for that reason alone.
- Moving the covalent bond record into `Interactions` would confuse inferred
  observations with declared chemical-state truth. A disulfide detector can
  live in the analysis namespace while `ChemicalStates` owns recorded bonds.
- Requiring every proposed interaction family for 1.0 would expand this
  namespace decision into an unvalidated scientific program. The generic
  `Interactions` domain and its persistence are separate required work.

## Scope and exclusions

The accepted pre-1.0 slice covers public API organization, hydrogen-bond
migration, disulfide-candidate extraction, the build wrapper, and their
contract/documentation/consumer checks. It does not add a general interaction classifier, a force-field energy
decomposition, a pharmacophore model, arbitrary contact storage, reactive
bonds, or implementations of the deferred families. Attached interaction
datasets are required before 1.0 under #251 and #252, outside this namespace
migration issue's implementation scope.

## Acceptance criteria

If the proposal is accepted for implementation, close this issue only when:

1. A recorded decision fixes the family namespace, the distinction between
   candidate and recorded disulfides, the compatibility policy, and the minimum
   per-structure result contract.
2. The bounded pre-1.0 API is implemented and covered by behavior and failure
   tests, including a guard for the canonical path and the build wrapper.
3. The stability registry, argument validation, public documentation, affected
   course material, and MolSysViewer compatibility are reconciled. Consumer
   handoffs are linked by issue number where needed. Native `MolSys` and H5MSM
   persistence remain required pre-1.0 gates under #251 and #252, even if this
   namespace migration issue closes earlier.
4. Every accepted interaction method has its criteria, limitations, and
   scientific evidence level recorded. No method is called scientifically
   validated without an independent oracle; unsupported modes fail visibly.
5. Applicable 1.0 release gates are rerun on the final candidate commit, with
   the new evidence entered in the operational status ledger.
6. Durable rules move to normative documentation, the report is archived with
   a valid `guard` or `normative` path, and issue #250 closes with the final
   user-facing decision and record. Deferred families have separate issues
   when their implementation is approved.

If the design is rejected or superseded, close it with that decision and archive
the report using the corresponding lifecycle status. Planning alone does not
meet the implementation closure criteria.

## Dependencies and risks

- The current hbonds surface is experimental but already referenced by guides,
  course notebooks, tests, and MolSysViewer. A compatibility policy is needed
  even before stable 1.x guarantees apply.
- Argument digesters contain caller-specific paths for current hbonds methods;
  moved methods must retain correct validation and errors.
- Pi-pi and cation-pi require credible aromatic-group and charge assignments.
  Metal coordination, halogen bonding, and hydrophobic association each need
  family-specific criteria. These are reasons to stage the families, not to
  create placeholder implementations.
- Any accepted pre-1.0 code change invalidates exact-commit release evidence
  and requires recertification; it must be decided before candidate freeze.
