# Completing the accepted pre-1.0 plan

**Role:** operational coordination packet under uibcdf/molsysmt#334.
**Basis:** public source `5e7d65a665425fe6077f016dd95cbd65d424ee91`,
2026-11-10. This packet refines execution order; it does not add features,
change original weights, accept missing evidence or authorize publication.
The [scorecard](../devtools/data/pre_1_0_progress_scorecard_20261107.json) owns
original milestone accounting. The [audit](pre_1_0_robustness_audit_20261106.md)
and [release ledger](release_1_0_status.md) retain current evidence and history.

## Later 11 November polishing update

The historical complete receiving below remains valid for its original source.
The clean `01c6266f6` run finishes **failed: 49 failures, 33,748 passes,
16 skips**. The [polishing queue](pre_1_0_robustness_audit_20261106.md#pre-10-polishing-queue--2026-11-11)
and [initial receipt](../devtools/data/pre_1_0_polishing_receiving_334_20261111.json)
retain that result and the #709/#710 corrections. Their 449-case receiving passes.
The later complete `f0dbb58e0` run has **one failure, 33,824 passes and 16 skips**:
the old 49 failures no longer occur, but the fresh-import timeout remains
unexplained under #713. The [follow-up receipt](../devtools/data/pre_1_0_polishing_followup_334_20261111.json)
retains the lost external-supervisor status, recovered artifact/input checks,
isolated success, diagnostic increment and separate legacy-handler corrections.
The next deliberate complete run requires a durable supervisor and pre-deadline
evidence; no passing full-suite or backlog clearance is claimed. Independently reviewed
MolSysViewer default-1.0 source receiving is accepted under #256; format freeze,
#615 and the final exact installed pair remain separate. No new candidate or
hosted execution is requested by this update.

## Work that MolSysMT can advance now

1. **Complete the next deliberate local default suite.** Select a clean
   committed checkpoint containing the #713 diagnostics, unchanged qualified
   native extension 4ffb82e4, verified MolSysViewer 5164f13b and the declared
   frozen support composition, including published PyUnitWizard 0.29.2. Keep
   the three-worker, 6-GiB/three-CPU/no-own-swap limits, aggregate host reserve
   and finite wall budget. Run the external supervisor as a durable service,
   retaining native wait status independently of the agent daemon. Preserve
   the original 60-second child deadline and capture its pre-deadline stack
   if the timeout recurs. Earlier isolated success is not a causal explanation.
   The [follow-up receipt](../devtools/data/pre_1_0_polishing_followup_334_20261111.json)
   owns the failed latest full session; the [earlier complete receipt](../devtools/data/complete_default_source_receiving_334_20261110.json)
   retains 33,549 passes/two skips on its original source. Neither qualifies a
   changed candidate or clears the latest full-suite/nightly backlog. Local
   Linux/Python 3.14 receiving remains separate from platform/installed gates.
2. **Maintain a discriminating #615 investigation.** Separate the original
   executing-cell timeout from later pre-execution, server-startup, replacement,
   deadline and missing-harness observations. The real-server session diagnostic
   is received. An idle kernel after browser retirement does not explain its
   earlier state. Request evidence captured before the failing stage; do not
   repeat a passing workflow without a new question, warm imports, restart a
   live kernel or extend a deadline. A causal correction or an evidenced bounded
   environmental disposition remains required.
3. **Retain #256's bounded P5 acceptance.** DockingMT's independent experimental
   0.6 cases pass under both unit policies. Keep their limited native composition
   distinct from MolSysMT's provider evidence and later explicit 1.0 source receiving. Both clients have received their
   bounded 1.0 profiles; format freeze and exact installed acceptance remain due.
4. **Complete P6 after the default transition.** Source `1951d0822` defaults
   to H5MSM 1.0 and preserves independent whole-file migration, while 0.6 remains
   explicit and experimental. Both clients' bounded earlier profiles are
   received. Independent default-save receiving with MolSysViewer is accepted, including
   mechanics-bearing sessions. Complete the stable-format freeze and retain
   final installed acceptance. Qualify scientific profiles under their own scope.
5. **Use bounded Jupyter startup diagnostics.** The
   [resolved #705 record](archive/resolved_proposals/explicit_bounded_jupyter_server_readiness_budget.md)
   retains the two original deadline defects, 44 passing focused cases and
   two actual startup controls on the integrated #706. #615 requires its
   separate pre-timeout capture.
6. **Maintain the reconciled source/claim ledger.** Keep container/query/persistence
   guarantees separate from detector science, engine support and human/installed
   receiving. Close only the accepted owning scopes, retain original failures
   and select exact candidate work only after the relevant agreements.

The format obligations remain owned by [#256's plan](pending_proposals/h5msm_0_6_molecular_mechanics_persistence.md).
Dependency closure remains owned by [#524](pending_proposals/runtime_dependency_api_floors.md),
and the uncertain startup stage by [#615](pending_bugs/intermittent_jupyter_initial_canvas_timeout.md).

## External handoffs for maintainer coordination

### PyUnitWizard: explicit boundary-safe conversion review

**Owner:** uibcdf/pyunitwizard#143; consumer uibcdf/molsysmt#666.
**Completed.** The published 0.29.2 package passes the native boundary
controls and both real Jupyter contact workflows. The
[#666 resolution](archive/resolved_bugs/contact_cutoff_equality_changes_across_equivalent_length_units.md)
records the dependency floor and regression guard. The original handoff follows.

**Deliverable:** identify a suitable supported conversion/comparison route, or
propose the smallest explicit provider capability with declared guarantees and
limits. An implementation/release is needed only if that review demonstrates
that the current supported API cannot satisfy the agreed requirement.

The reported finite example is two points 0.5 nm apart: inclusive contacts differ
for 0.5 nm, 5 angstrom and 500 pm after existing normalization. A public
[27-case reference](../devtools/data/unit_scale_boundary_reference_666_20261110.json)
uses exact declared SI scales and a single final binary64 rounding. It retains
strict predecessor negatives, without isclose or widening the scientific cutoff.
It is not a production fix or a universal exact-arithmetic promise.

**Forwardable request:**

> Please review uibcdf/pyunitwizard#143 against MolSysMT source 5e7d65a66 and the
> published 27-case reference. Confirm an existing supported route or propose
> a bounded provider-owned capability. State scalar/array, unit/backend and
> representability limits, including strict adjacent-value controls. We will
> receive the chosen route through native contacts under multiple policies,
> CPU routes and PBC before accepting uibcdf/molsysmt#666 or the final contact GUI
> intent. Please return the exact source/API and qualification; a source-only
> result does not establish a new published dependency floor.

### MolSysViewer: contract feedback, startup evidence and artifact plan

**Owner:** uibcdf/molsysviewer#315, with the existing integration/publication
owners. Consumer requirements remain uibcdf/molsysmt#250, #254, #524 and #615.

**Source agreement received.** The review for [uibcdf/molsysviewer#315](https://github.com/uibcdf/molsysviewer/issues/315)
is published at Viewer `4f05a6c6ea3f7ca78929e9f2592360f0e6ae38fa`. It uses
Viewer source `25f482ae0f2145dd4a203287c82ce158beb78a5e` and the MolSysMT
coordination record `af32a559cc6bac6d0e33ee249b3692319028add3`. Individual test
results retain their recorded pairs. Viewer accepts the exercised #250 and
#254 contracts. These include sparse observations with compound participants,
occurrence indices scoped to an analysis revision, evaluated coverage, ordered
nonconsecutive queries, the four atom-selection modes, typed bounded pages,
periodic images, named results and declared maps. Page bounds apply to copies
after query construction. The scene uses the explicit reference chemical state
for its static covalent graph, including a nonzero reference, and rejects an
ambiguous reference. No new provider change was requested for these exercised
paths. Detector profiles, the inspection-page API and Qt remain experimental.
Final-candidate acceptance under #250/#254/#334 is pending.

**Coordinated release pair.** The maintainer confirmed the joint release of
**MolSysMT 1.0.0 and MolSysViewer 1.0.0**, recorded by MolSysViewer in
`f09757122a91dbbf32846738890a96623c2353e2` for uibcdf/molsysviewer#315. Qualify
this exact pair in clean installations under #334 before joint publication.
On 2026-11-11 the maintainer chooses to wait for the final pair, deferring
an intermediate MolSysMT 0.24.0 / MolSysViewer 0.25.0 milestone. Continue the
[pre-1.0 polishing queue](pre_1_0_robustness_audit_20261106.md#pre-10-polishing-queue--2026-11-11)
in the meantime. The published
MolSysMT 0.23.0 / MolSysViewer 0.24.0 pair retains its historical scope. #524
still requires a published compatible host floor and clean installed evidence.

The intended MolSysMT producer is the future clean release source with the
reviewed native domains, redesigned tools addon and qualified stable H5MSM
reader, writer and migration routes. When candidate work resumes, agree exact
producer commits, build strings and supported capabilities, then share
filenames, channels and SHA-256 hashes before running the sixteen installed
cells. Use a higher unused Conda build number for the new MolSysMT producer
and preserve the four existing 1.0.0 build-0 files in staging. Cover real
imports, addon discovery and lifecycle (including `MolSysView.closed`),
native-domain/scientific workflows, session round trips and the applicable
minimum and newer installed dependency routes.

**H5MSM 1.0 client cases.** Include the following cases in final receiving.

The bounded source feedback is received from both clients. MolSysViewer
`97d49215` reports 47 passing cases on the requested provider source and
reference binary. The [session receipt](../devtools/data/molsysviewer_h5msm10_client_receiving_256_20261110.json)
records prior-writer compatibility, explicit 1.0 restoration, sparse queries
and maps, selective invalidation and explicit View synchronization. Its
mechanics-bearing session loaded while the prior 0.5 default refused resaving.
The [default-transition receipt](../devtools/data/h5msm_default_10_receiving_256_20261110.json)
now verifies saving and reopening it with default 1.0 on exact MolSysViewer
`a6a3a309`. Independent consumer receiving is accepted on 2026-11-11:
MolSysViewer `7d29efda6345e2a555402596e9762740a2a257b9`, runtime base
`ed1e118212`, passes 18 session cases and 151 boundary cases on MolSysMT
`aee7aa65d`. The [reviewed receipt](../devtools/data/molsysviewer_default_h5msm_client_receiving_256_20261111.json)
also retains the prior-default control and two prior-writer session artifacts.
The default-save source handoff is complete. Format freeze and exact
installed-candidate receiving remain pending under their existing scope.

1. Save a complete system with explicit reference chemistry and a named periodic
   analysis, project onto nonconsecutive structures, reopen the session and edit
   one selected structure. Verify maps, occurrence geometry, producer identity,
   measure units and invalidation limited to the declared affected coverage.
2. Reopen a partial file and verify domain absence and maps. Attach an
   independent analysis using explicitly declared correspondence. Verify that
   the read and session paths preserve the stored producer and measure units.

The 0.5 and explicit 0.6 evidence retain their original version scope.
These two Viewer workflows require the stable public reader, writer and
migration paths. Mechanics visualization remains outside the receiving scope.

**#615 ownership.** MolSysMT accepts the Analysis runner and matching notebook,
kernel and server samples. Viewer owns the widget mount, scene registration and
first new native draw observations. The [diagnostic disposition](pending_bugs/intermittent_jupyter_initial_canvas_timeout.md#joint-pre-timeout-capture-disposition--2026-11-10)
defines the bounded capture and verdict. Candidate selection, new qualification
runs and publication remain paused.

The detailed current API and native-domain behavior are maintained in
[Interactions](interactions_api.md), [native queries](native_queries.md),
[the core specification](CORE_SPECIFICATION.md) and [H5MSM](h5msm_format.md).
The public owner [delivery record](../devtools/data/native_and_figure_owner_delivery_701_702_703_704_20261110.json)
retains receiving scopes and the original unsuccessful attempts.

### DockingMT: agree only the remaining stable-format client scope

**Owner:** uibcdf/molsysmt#256 with the DockingMT team.
The immutable DockingMT publication 9b077fab and its independently received
reference/E3 records remain accepted for their bounded scopes. Issues
uibcdf/dockingmt#79, #88 and #96 are closed. The provider receipt is
[retained here](../devtools/data/docking_h5msm06_client_receiving_256_20261109.json).
No new docking, preparation, scientific search or reopening is requested.

DockingMT completes the three additional controls on experimental 0.6 with
seven passing cases per unit policy. Its isolated `5e7d65a6` source uses the
previously qualified `5715bda2` ABI3 only for one-atom topology bookkeeping.
The [P5 acceptance and 1.0 handoff](pending_proposals/h5msm_0_6_molecular_mechanics_persistence.md#independent-experimental-06-p5-acceptance--2026-11-10)
identifies the scope and reference inputs. DockingMT then completes ten cases
per policy on the explicit 1.0 route with local ABI3 `2dbcf13d`. The
[accepted P6 receipt](../devtools/data/docking_h5msm_p6_client_receiving_256_20261110.json)
records its separate provider composition and exact checks. Receive the
current default-writing source under the remaining format/consumer scope.
[DockingMT #73](https://github.com/uibcdf/dockingmt/issues/73#issuecomment-6784434374)

The local DockingMT clone was 181 commits behind its fetched upstream during
this checkpoint and was not updated or used as current consumer evidence.
MolSysMT's four human edits and Viewer's fourteen dirty paths were preserved;
PyUnitWizard's inspected clone was clean. Published immutable sources, not
unreviewed local changes, remain the receiving inputs. The first suite-status
invocation had a usage error; the corrected positional-workspace invocation
completed acquisition and reported attention for these preserved states.

## Finite P5 review matrix

The [immutable synthetic fixture packet](../devtools/data/h5msm_p5_review_20261110/README.md)
now supplies complete/projected/nonpolar-H-merged public 0.6 files, explicit
typed expected snapshots and original PDBQT exports, with sizes/SHA-256. They
come from the already executed public branch; no new preparation is required.
The **156-case** provider receiving passes on ee4f72796, including four added
0.5/0.6 topology/interaction append-refusal cases that verify byte-exact file
nonmutation and preserved independently readable layers. Product source is
unchanged from 5e7d65a66. The completed default session on 5e7d65a66 and the
accepted independent DockingMT profiles have their own exact inputs and verdicts.

The table describes the provider controls and the agreed bounded client scope.
The independent client result above resolves its three experimental 0.6 cases.
Reuse the full-reference/E3 records for their original scopes.

| Boundary | Existing assertion-bearing provider guard | Remaining review |
| --- | --- | --- |
| Partial domains and typed mechanics | `tests/form/file_h5msm/test_public_mechanics_v06.py::test_explicit_native_public_roundtrip_preserves_domains_and_original_reports`; `tests/form/file_h5msm/test_mechanics_layer.py::test_nullable_mechanical_columns_keep_values_dtypes_and_missing_policy` | Complete/absent domains, original reports and exact stored units/dtypes; client need not pretend it can use a topology-free system. |
| Fresh public reader and producer/edit ownership | `tests/form/file_h5msm/test_modular_mechanics.py::test_prepared_whole_file_in_a_fresh_reader_retains_provenance_and_edit_ownership` | Its public branch verifies both public read and convert, changed reader version, PDBQT parity, unit-policy preservation, selective analysis invalidation and absence of optional engines. Independent DockingMT receiving remains distinct. |
| Selected/reordered native axes | `tests/form/file_h5msm/test_public_mechanics_v06.py::test_copy_and_selected_file_extraction_retain_root_version_and_mechanics`; `tests/form/file_h5msm/test_public_mechanics_v06.py::test_reordered_prepared_system_retains_correspondence_in_public_roundtrip` | Accepted on 0.6: explicit atom permutation and nonconsecutive structures `[2, 0]`, original producer labels, expected correspondence, typed parameters and named-analysis coverage. Ordinary atom selection uses ascending unique indices. |
| Stored unknown evidence versus usable assignments | `tests/native/test_unknown_mechanical_assignment_reports.py::test_unknown_reports_roundtrip_but_refuse_projection_and_scientific_export` | Accepted on 0.6: transport unknown charge and type reports, then preserve source and refuse unsupported projection/export before output. |
| Supported append versus documented refusal | `tests/form/file_h5msm/test_public_mechanics_v06.py::test_public_append_preserves_mechanics_and_extends_state_assignments`; new refusal guard `tests/form/file_h5msm/test_public_mechanics_v06.py::test_unsupported_append_preserves_existing_file_and_independent_layers` (four cases received) | Provider-owned append supports the documented topology-free/no-interactions composition and explicit state indices. Named-interaction file append is not promised. Confirm actual client use before requesting client execution or broadening support. |
| Absent/present-empty and atomic publication | `tests/form/file_h5msm/test_modular_mechanics.py::test_explicitly_empty_mechanics_keeps_its_independent_presence`; `tests/form/file_h5msm/test_modular_mechanics.py::test_write_failure_after_partial_staging_publishes_nothing` | Keep independent layer presence distinct from native representability, and preserve existing caller files on normal failure. Crash durability remains outside the implemented atomic-visibility guarantee. |

Use a tiny already prepared fixture; do not run another scientific preparation
or docking search. Preserve the source file and current-producer control bytes,
quantities, table dtypes, string labels, state/structure/atom maps and original
evidence. A coordinate edit must exercise the existing selective invalidation
contract rather than claim every assignment depends on geometry. Both policies
read the same immutable source, and each fresh reader records its actual
imports/software. Exact candidate artifacts need their own later qualification.

## P6 implementation order after the bounded client review

This checklist describes the stages before the H5MSM 1.0 format freeze. Explicit
1.0 reading, default writing and modular migration are implemented in development
source. Client feedback on that default and coordinated release gates remain due.

The [P6 wire catalog and public-route audit](pending_proposals/h5msm_0_6_molecular_mechanics_persistence.md#p6-wire-catalog-and-public-route-audit--2026-11-10)
identifies the existing codecs, independent-layer migration, version dispatch,
source-root preservation and explicit stable-root acceptance sequence.

| Step | Concrete work and required control |
| --- | --- |
| Freeze represented meaning | Review the existing root/layer field catalog, independent axes/associations, units/dtypes, missing/empty semantics and unknown-evidence behavior. Identify actual wire changes before assigning versions. Keep experimental scientific-model claims separate from stable transport guarantees. |
| Introduce the stable root | Reuse the owning modular codecs and version-dispatch helpers. Receive actual 1.0 reads/writes, partial domains and unknown-version rejection; no header-only relabeling of existing files. No duplicated codec or placeholder public handler is needed. |
| Reconcile default writers | Make public conversion, `h5msm.write`, `write_layers` and applicable form routes agree on the newest qualified default. Retain explicit older routes only within their represented capabilities; nonempty mechanics must never disappear through an old target. Update the public API stability review for intentional default changes. |
| Preserve migration intent | Version-specific helpers retain their named destination. Public source-preserving conversion can provide the latest-format route after its qualification. Reconcile warnings and their recommended command with the actual latest stable writer; experimental 0.6 alone does not deprecate 0.5. Do not silently rewrite an input file or producer label. |
| Synchronize executable guidance | Update API docstrings/doctests, Foundations/Toolbox/Cookbook/course and the schema/benchmark guidance. Re-execute changed examples and validate stored notebooks without repair. Retain historical fixture/root identities and benchmarks with their original scope. |
| Receive the final pair | Record client feedback, final exact sources and artifacts, complete the mandatory gates and preserve failed attempts. Stable-format/container acceptance does not certify every detector or force field. The exact candidate remains a separate owner decision. |

The next implementation change should follow this order rather than advancing
the root/default first and discovering omitted public paths afterward.

## Exact-candidate and publication boundary

After the outstanding scientific/container/source and format decisions pass,
agree exact compatible sources, versions, builds and qualification scope.
Then follow [the release gate](release_gate.md): eight source OS/Python cells,
applicable native wheels and sixteen installed-pair cells, actual dependency
closure/imports, documentation, client/session behavior, failed-attempt accounting,
final authorization and public-artifact/Zenodo verification. Preserve immutable
older artifacts and tags. The existing candidate/package/tag/Release/promotion/
new hosted-matrix pause remains; ordinary local source development continues.

No new blocker is currently assigned to ArgDigest, DepDigest, SMonitor or
Ackredit by this packet. Their received boundaries and existing owned follow-ups
remain in force. Other client libraries do not become additional initial 1.0
integration gates through this coordination document. A successful local suite,
new issue count or completed handoff earns no extra original milestone credit.
