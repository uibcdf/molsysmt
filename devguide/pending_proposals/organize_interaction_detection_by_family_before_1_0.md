---
summary: Organize interaction detection by family before 1.0
issue: uibcdf/molsysmt#250
status: active
opened: 2026-09-28
closed:
verification: inspected
area: [api, build, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Organize interaction detection by family before 1.0

**Reported:** 2026-09-28, during pre-1.0 API planning for MolSysMT and its
MolSysSuite consumers.
**Status:** Accepted for the bounded pre-1.0 migration; implementation and
recertification are in progress.

## What

Introduce a public `molsysmt.interactions` namespace organized by chemically
interpreted families, beginning with `interactions.hbonds` and a disulfide
candidate detector. Keep `molsysmt.build.get_disulfide_bonds` as the existing
build-oriented entry point, potentially delegating to that detector. The
pre-1.0 decision is about the analysis API and its migration. Additional
interaction families can be approved separately after 1.0. A persistent
`Interactions` domain inside `MolSys` and H5MSM is required before 1.0;
its contract and implementation are tracked in
[`uibcdf/molsysmt#251`](design_a_sparse_public_interactions_result_and_serialization_contract.md)
and [`uibcdf/molsysmt#252`](implement_experimental_sparse_interactions_results_and_queries.md).

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
  covalent bond. Recorded covalent connectivity remains in topology; build
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
| 5. Add further families | After 1.0, in separate scoped issues | Prioritize ionic/salt-bridge, pi-pi, cation-pi, halogen, hydrophobic, metal-coordination, and mediated interactions from consumer use cases and available chemical-state evidence. Each family needs its own method definition and independent validation. |
| 6. Integrate persistent interaction data | Before 1.0, tracked by #251 and #252 | Attach optional results to `MolSys`; define remap or invalidation on source edits; persist and recover them in a versioned H5MSM interaction layer. The broader attribute-centric architecture and cross-system alignment remain separate decisions. Stage 5 is not a closure criterion for this namespace issue. |

The minimum result contract in stage 0 must distinguish: participant roles and
index spaces; selected structure indices and their order; observed versus
declared relationships; method, parameters, and units; empty evaluated results
versus analysis not run; and periodic images when they identify a different
observed participant. It must allow hydrogen-bond triples and ring/group
participants, not only atom pairs. The concrete result class and schema are
tracked in [`uibcdf/molsysmt#251`](design_a_sparse_public_interactions_result_and_serialization_contract.md).
Large trajectory methods should use the maintained chunked-execution
policy and avoid dense atom-pair-by-frame output by default.

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

## Why

[The current public root](../../molsysmt/__init__.py)
exports `hbonds` separately, while
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

- The accepted pre-1.0 tree contains `interactions.hbonds` and
  `interactions.disulfides`; other families remain separate post-1.0 decisions.
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
  methods retain legacy method-specific output layouts; a common result schema
  has not been adopted.
- Focused migration tests pass for the legacy hydrogen-bond namespace and for
  empty single-selection hydrogen-bond results, as well as disulfide selection,
  group filtering, periodic geometry, frame order, empty results, and recorded
  bonds. Broader trajectory and cross-selection behavior, documentation,
  consumer, and release
  gates are still pending; this is not release evidence yet.

## What is measured and what is assumed

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
  observations with topology truth. A disulfide detector can live in the
  analysis namespace while recorded bonds remain topological.
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
