# Pre-1.0 robustness audit and action plan — 6 November 2026

The [Viewer source agreement checkpoint](release_1_0_status.md#viewer-source-agreement-received--2026-11-10)
receives #250/#254 source feedback and sets the remaining installed, format and
diagnostic work. The composite milestones retain their final acceptance criteria.

## Pre-1.0 polishing queue — 2026-11-11

**Owner:** uibcdf/molsysmt#334. **Role:** supplemental operational queue under
the [maintainer's polishing admission](release_1_0_scope.md#pre-10-polishing-admission--2026-11-11).
The maintainer chooses to wait for the final MolSysMT 1.0.0 / MolSysViewer
1.0.0 pair and requests attending worthwhile findings and pertinent issues
before publication. The intermediate 0.24.0 / 0.25.0 milestone is deferred.

### Review coverage and order

1. **Correctness and data integrity:** numerical and scientific meaning,
   quantities under non-default policies, selections/maps, chemical-state and
   interaction validity, partial systems, persistence and explicit loss/refusal.
2. **Public use and robustness:** argument validation, optional dependencies,
   diagnostics, empty/degenerate inputs, resource bounds and supported workflows.
   Use ArgDigest, DepDigest, SMonitor and PyUnitWizard at their actual owning
   boundaries; preserve optional Ackredit attribution where applicable.
3. **Documentation and examples:** reconcile API/docstrings, User Guide,
   Cookbook and course against current code. Check installation instructions,
   native-domain ownership, defaults, units, scientific limits, terminology,
   links and executable examples. A warning-free build alone does not establish
   scientific or instructional accuracy.
4. **Efficiency and maintainability:** take bounded, justified improvements
   with relevant measurements and unchanged scientific behavior. Under #567,
   slower correct implementations remain available; measured efficiency debt
   receives an owned warning/follow-up rather than an automatic release veto.
5. **Issue and PR intake:** acquire the complete inventory at meaningful phase
   checkpoints and before final source selection. Review new correctness and
   data-integrity reports first, including findings currently labelled
   post-1.0. Resolve or explicitly disposition pertinent reports; a label or
   issue age alone does not decide priority.

### Initial work packages

| Item / owner | Observed state | Next action and closure evidence |
| --- | --- | --- |
| P1 — strict API documentation, #334 | Complete HTML on clean `01c6266f6`, `8ada7fe24` and `3546267d0` passes with zero warnings. Eight RST files include the four expressly approved preexisting edits; the original six-title failure is retained. | This bounded correction is received. Recheck affected pages for later changes and run the exact final candidate's documentation gate. |
| P2 — persistence/integration and complete-source receiving, #334 / #256 / #709–#713 | Full `f0dbb58e0` receiving has **one failure, 33,824 passes, 16 skips**; the prior 49 integration failures no longer occur. The failed child import exceeds its original 60-second deadline; #713 adds pre-deadline evidence and passes 134 focused cases, without causal resolution. The daemon restart lost the original supervisor wait status; recovered JUnit/receptor/input checks and telemetry limitations remain explicit. Two legacy-handler defects (#711/#712) have 85 passing bounded controls after 20 failing baseline cases. | Preserve both failed full sessions. Close only the guarded legacy version-preflight/structured-copy-refusal scopes; keep #713 partial. The next deliberate complete receiving needs a durable supervisor and original-deadline diagnostics. Neither isolated import success nor focused checks clears the full-suite/nightly backlog. |
| P3 — semantic documentation review, #334 / #378 | The earlier entry/native/course slice remains received. The new H5MSM file and legacy-handler guidance correct layouts, schema support, units, resource ownership and actual operation limits; two further course lessons are reconciled. All 92 declared handler attributes are listed without promising file availability. Four executions of actual Markdown examples pass under nm/ps and pm/fs; three notebooks retain their code, outputs and execution metadata. | Complete strict HTML on clean `792c14d8a` passes with zero warnings; the five actual article DOMs, 153 internal targets/anchors and 19 implementation source links pass inspection. Continue the wider instructional/scientific review and external-reader work; #378 remains partial. |
| P4 — incoming and remaining issues/PRs, owning issue / #334 | Complete paginated acquisition before this closeout has **633 issues, 92 open, zero open PRs**. The only new issue identities since the preceding review are #711/#712 (guarded legacy fixes) and #713 (partial import-timeout diagnosis). | Close the two verified scopes after publishing their records and retain #713 as pending work. Refresh at the next meaningful checkpoint; counts are dated observations. Resolve or explicitly disposition pertinent incoming reports. |
| P5 — client and final-candidate boundaries, #256 / #250 / #254 / #524 / #615 / #334 | Independent default-specific MolSysViewer source receiving is [reviewed and accepted](pending_proposals/h5msm_0_6_molecular_mechanics_persistence.md#independent-default-specific-molsysviewer-receiving--2026-11-11): 18 session cases and 151 boundary cases on the declared source. The final pair is not frozen; #615's original uncertainty and installed-package evidence remain open. | Complete the stable-format decision and final pair agreement. Keep the published dependency floor, installed matrix and publication decisions distinct from local polish and headless source receiving. |

### Adding and closing findings

For each discovered item, record the observed behavior or misleading claim,
impact, owning issue, scope/priority, proposed action, status and exit evidence.
Reuse an existing issue for the same theme; a distinct substantial defect gets
its own owning issue/report. The detailed report remains the evidence owner;
this queue links it rather than duplicating an independent status register.
Small related corrections may be grouped in their work package.

Admit worthwhile bounded corrections and improvements that can be reviewed and
verified before 1.0. If a change alters a public/scientific contract, complete
its documentation, attribution, units and consumer-impact work as applicable.
For a large new capability or redesign, state alternatives and impact before
implementation. Deferred work records why, who owns it and when to reconsider.

Close a correction only with the implementation/documentation change and a
relevant regression or other appropriate check. Review scientific meaning as
well as output shape; retain failing and interrupted attempts. Select checks by
the actual affected scope, avoid redundant broad runs without a new reason and
monitor shared resources during expensive validation.

**Accounting and release boundary:** the original score remains **77.7381%**
with unchanged weights and **50/50 source graphical intents**. Supplemental
polishing does not earn invented percentage credit or replace an outstanding
candidate/installed milestone. The user has not authorized an intermediate
release or lifted the candidate-construction, hosted-qualification, tag,
promotion or publication pause. Reconcile admitted findings before selecting
the final clean source; complete mandatory exact-candidate gates afterward.

## Current-state claim reconciliation — 2026-11-11

The [source review](release_claims_review_20261111.md) completes the original
`phase5/334-ledger` work package: maintained claims now distinguish native
H5MSM 1.0 defaults, explicit older roots, bounded mechanics and addon defaults;
the ledger has one current resume entry with historical evidence retained.
The original weights and scope are unchanged. Source milestone credit becomes
**77.7381% (approximately 78%)**, with **50/50 graphical intents received at
source level**. This is completion of an explicit documentation/contract
requirement, not new algorithmic or installed qualification.

Phase 5 still needs #250/#254 final-candidate acceptance. Default-specific
H5MSM client receiving/format freeze, #615, #524 and the phase-6 exact pair,
artifact, matrix and publication decisions remain pending. The dated entries
below preserve their original verdicts and percentages.

## Complete corrected-source suite received — 2026-11-10

Frozen **5e7d65a66**, qualified native **4ffb82e4** and verified Viewer
**5164f13b** complete the default Linux/Python 3.14 suite: **33,549 pass, two
explicit skips, zero failures/errors** in **33,551 cases**. All five cases from
the earlier failed session now pass; the original session remains failed.
The receptor's valid final summary retains explicit bounded detail truncation;
complete JUnit and native exit zero remain authority. See the [complete-source
receipt](../devtools/data/complete_default_source_receiving_334_20261110.json).

Three workers stayed below the 6-GiB cap (peak about 5.57 GiB); host available
memory stayed above about **6.44 GiB**. Soft memory.high events and global
pressure warnings remain recorded; no own OOM, hard-limit or reserve stop
occurred. The two skips are missing CuPy and an RDKit-dependent negative form
case, not omitted registered scientific evidence. No installed/platform or
exact-candidate qualification is inferred from this local source result.

The separate **156-case P5** provider cohort includes four later append-refusal
guards, outside that frozen complete session. Its three synthetic fixture sets
and expected typed/PDBQT outputs are public on **1ce072ae7**. Existing DockingMT
acceptance remains closed; independent receiving of the additional finite
profile remains pending under #256. The [coordination packet](pre_1_0_completion_handoffs_20261110.md)
supplies precise PyUnitWizard/Viewer requests, the bounded client profile and
the P6 stable-format implementation order.

New incoming **#705** is [triaged as a bounded server-preparation proposal](archive/resolved_proposals/explicit_bounded_jupyter_server_readiness_budget.md),
with an incoming contribution expected from Viewer. Keep default preparation
and explicitly selected scale budgets distinct from scientific/frontend
deadlines and original #615 causality. The complete intake has **627 issues,
94 open and no open PRs**. Original progress remains **76.2920%, 49/50**.
#666/provider143, #615 disposition, #524 actual public/installed closure,
#250/#254 agreement, #256 P5/P6 and #334 final gates stay explicit. Publication,
candidate/tag/package/promotion and new hosted matrices remain paused.

## Completion handoffs and local full receiving — 2026-11-10

The maintainer requests advancing the original plan to completion and will
coordinate external owners. The [operational handoff packet](pre_1_0_completion_handoffs_20261110.md)
separates local work from exact PyUnitWizard/Viewer requests and a bounded
remaining H5MSM/DockingMT scope. Existing DockingMT #79/#88/#96 acceptance stays
closed; no new initial client-integration gate is introduced.

A new complete local default suite is running on frozen **5e7d65a66**, with
three workers, a monitored **6-GiB/three-CPU** limit, no swap and host-reserve
controls. It has no accepted verdict yet. The earlier failed suite remains
failed. Original progress remains **76.2920%, 49/50**; all final agreement,
format, installed/platform/candidate/publication obligations stay explicit.

## Default-suite defects and retained figure context received — 2026-11-10

The frozen 5f241cfa7 complete default suite is **failed**: **33,519 pass, five
failures and two skips** in 33,526 cases. Its complete JUnit/native verdict and
explicitly truncated receptor phase stream remain preserved. #703 corrects an
unbacked 64-KiB-per-worker numerical admission allowance; #704 completes the
peptide namespace/warning controls. Source 93b3a6ea6 with canonical rebuilt
backend `4ffb82e4` passes **133 directed cases**, **1,782 affected cases**, all
**88 Rust tests**, required library Clippy and **116 scientific cases / 74 nodes**.
The [budget receipt](../devtools/data/numeric_neighbor_budget_receiving_703_704_20261110.json)
keeps all baseline failures and the original budgets/refusals. These overlapping
selections are not a replacement complete-default verdict.

Clean **d36d25929** receives exact **#702 9dff314f8**, with Viewer **5164f13b**.
**5,959 addon/caller/source-route cases** pass without omissions, and **#701**'s
unchanged exact-inventory guard includes all modules in one hosted invocation.
Fifteen fast gates, the HTML build and its inspected new section pass; six
existing title-underline warnings remain. Visual adoption passes six Jupyter
checks; initial Analysis fails after nine checks for a missing test-only
harness. A verified isolated harness build then permits all **22 Analysis
checks** to pass. The representative native Wayland Qt workflow passes **four
reported steps**, including embedded literal context assertions. These are split
receiving scopes with the failed attempt retained, not one invented green campaign.
See the [owner receipt](../devtools/data/figure_context_owner_receiving_701_702_615_20261110.json).

Figures retain native methods, forwarded parameters/weights, ordered populations,
units and historical projections through the public PyUnitWizard quantity
boundary. They do not authenticate source identity or recalculate science.
#615's actual post-attempt session diagnostics are received; original causality
remains unresolved. Public source checkpoint **ddd32ac1a** independently matches
all **39 changed paths**; **#701/#703/#704 are closed** and **#702 is merged by
ancestry**. The four human edits remain byte-exact. The complete board has
**626 issues / 93 open and no open PRs**. See the
[public delivery record](../devtools/data/native_and_figure_owner_delivery_701_702_703_704_20261110.json).

**Current next actions:** receive #666 / PyUnitWizard #143's unit contract and
remaining contact intent; obtain the causal or evidenced environmental
disposition for #615; receive #524's actual published compatible Viewer floor
and clean installed qualification, plus #250/#254's explicit contract feedback.
A bounded 27-case scale reference was delivered to the provider; it is not a
production fix. Original progress remains **76.2920%, 49/50**. #334 and final
#256 P5/P6/exact-candidate gates remain unaccepted. Publication, candidate, tag,
package, promotion and new hosted-matrix operations remain paused.

## Independent notebook gate received — 2026-11-10

#700 is source-resolved on **47682e9d3**: one read-only validator now
protects the fast preflight, local documentation builds and publication workflow.
All **501 stored notebooks** validate without repairs. **1,041 affected cases**,
**521 overlapping minimum-provider API cases** and **15 fast gates** pass.
Invalid sources stop an actual Makefile before an always-successful controlled
Sphinx can run. The first resource-admission refusal and missing historical
provider dependency remain recorded. See the [receipt](../devtools/data/notebook_schema_gate_receiving_700_20261110.json).

This developer-only safeguard adds no original plan credit: **76.2920%, 49/50**.
A bounded **three-worker / 6 GiB** complete default-suite run is in progress on
unchanged scientific source **5f241cfa7**. It is not accepted before completion
and does not replace installed/platform/exact-candidate gates. #615 causality,
#666/PyUnitWizard #143, #524 actual published/installed closure and #250/#254
feedback remain pending. Publication and new hosted-matrix operations stay paused.

## Public construction and native closeout verified — 2026-11-10

Public main **ae2b592ad** independently matches all **78 changed paths**, with
the four human-edited files preserved byte for byte. **#695/#697/#698 are guarded
and closed**. #696 is merged by ancestry; stacked #699 is closed as directly
integrated with its base/head branches preserved. The complete inventory has
**623 issues, 94 open and no open PRs**, and the board agrees with local queues.
Fourteen final fast gates pass on ae2b592ad with byte-identical qualified product,
test, user-documentation, CI and tooling inputs. See the
[public delivery record](../devtools/data/construction_native_owner_delivery_421_695_696_697_698_699_20261110.json).

Accepted original progress is **76.2920% (about 76.3%)**, **49/50 graphical
intents**; the contact intent stays pending under #666 / PyUnitWizard #143.
#615 needs a causal correction or evidenced environmental disposition; passing
new workflows does not supply it. #524 still needs an actual published compatible
Viewer floor and clean installed closure; #250/#254 need explicit contract
feedback. Final #256 P5/P6 and #334 exact-candidate/installed/platform/publication
work remains unaccepted. This checkpoint publishes sources only and does not
lift the candidate/package/tag/Release/new hosted-matrix pause.

## Construction, assessed decisions and native integrity received — 2026-11-10

Exact PR **#696 30b2c8b50** and stacked **#699 400d484f8** are integrated with
assessed protonation and the native #695/#697/#698 corrections on clean
**cdf6e878f**, against raw-blob-verified Viewer **b010ab76**. The
[combined owner receipt](../devtools/data/construction_native_owner_receiving_421_695_696_697_698_699_20261110.json) retains every earlier failed cohort.
The expanded cohort has **8,955 passes and one failed test oracle** comparing
reports from different active unit contexts. The corrected **415-case** receiving
passes with byte-identical product source and exact report/map assertions.
An earlier native cohort passes **8,813 cases**. These selections overlap and
are not summed. **116 scientific cases / 74 nodes**, **76 public/native doctest
examples**, strict validation of seven notebooks, ten inspected HTML pages,
**four actual Jupyter workflows / 26 checks** and **four representative native
Wayland Qt workflows / 24 checks** pass. Eighty-one existing code cells and
outputs remain unchanged. Qt construction checks complete page/profile/window
retirement with the provider's teardown correction.

Shared native publication now validates all structural series and the declared
atom domain before mutation/invalidation. Native builders and complete Iterator
chunks preserve that boundary. Unavailable setters refuse through the existing
typed diagnostic. Selected composed trajectories cannot import off-axis reference
observations or state links merely because selected lengths happen to match;
reference analyses require explicit correspondence. These are guarded source
resolutions, with public delivery/issue closure next. Supplemental repairs earn
no bonus. Proposal #700 retains the future notebook-schema gate improvement.

Only six original intents receive credit: one inspected protonation decision
for explicit managed/independent apply, and peptide, water-cell, assembly,
solvation and ion construction. Native tools still own science, unit-bearing
inputs, seeds, model/charge declarations and complete reports. Physical-model
inspection distinguishes requests, compiled observations and actual execution.
No hidden preparation, equilibration, trajectory solvent loop or new predictor
is implied. **49/50 original intents; 76.2920% (about 76.3%)** with unchanged
weights. This is source/automated receiving, not installed or release readiness.

Next: independently verify public source delivery and close #695/#697/#698 and
the reviewed PRs; receive **#666 / PyUnitWizard #143**'s exact cutoff-unit
contract and the last contact intent; retain **#615**'s unresolved causal stage.
Request **#524**'s actual published compatible Viewer minimum and clean
minimum/newer installed closure, plus explicit **#250/#254** contract feedback.
Those latter two original leaves would reach **81.0539%**, only if genuinely
received. Source b010ab76 is not a published package floor. **#256 P5/P6 and
#334** retain final agreement, qualification, failed-scope and publication work.
Publication/candidate/tag/package/new hosted-matrix operations remain paused.

## New native integrity intake — 2026-11-10

Complete paginated intake after #694 has 620 issues, 94 open issues and one new
PR, #696 at 30b2c8b50. **#695 is prioritized as a native correctness defect**:
full box replacement can silently misalign coordinate/time series without named
analyses. Twelve protected native-only controls fail on public 68bd19103; six
existing attached-analysis guards pass. The shared native publication fix now
passes those eighteen controls. Complete cardinality/unit/selected-axis,
constructor and affected-consumer receiving remains required before closure.
See the [owning record](archive/resolved_bugs/box_assignment_misaligns_native_structure_series.md).

Retain the existing one-box-per-addressed-structure contract; no implicit
ensemble broadcast is introduced. New construction stages its complete payload;
editing an existing object must not leave conflicting axes. Assessed protonation
and #696 physical-model consumer receiving remain separate work. Supplemental
#695 adds no original milestone weight. Publication remains paused.

## Observed secondary structure received — 2026-11-10

#694 is guarded and source-resolved. Product **707ea24b2** and final browser
control **a0a7d5470** retain byte-identical scientific/provider/user-doc inputs.
**186 affected cases**, **116 scientific cases / 74 nodes**, **14 fast gates**,
the executed docstring/tutorial, six inspected HTML pages, **seven actual Jupyter
checks and seven representative native Qt checks** pass. The receipt preserves
two failed browser controls and earlier native/fixture attempts. DSSP accuracy
remains a governed independent-validation gap; this does not promote its method.
See the [receiving record](../devtools/data/secondary_structure_receiving_694_20261110.json).

Credit exactly the original properties/secondary-structure intent: **43/50**,
**76.0364% (about 76.0%)**. Supplemental #694 adds
no bonus. Assessed protonation and five construction intents, contacts/provider143,
#615, #524 clean-installed actual-host minimum, #250/#254 agreement and the final
candidate/publication gates remain separate. No package/tag/Release or hosted
matrix is launched. Continue the native assessed-decision GUI workflow next.

## Public combined closeout verified — 2026-11-10

Public main **76ed1c3a1** independently matches all **39 changed/deleted paths**;
the four human files remain byte-exact. #687 is merged by ancestry, #691 is
closed as directly integrated with its stacked parent unchanged, and **#688 and
#690 are guarded and closed**. The complete board has **618 issues, 93 open,
no open PRs** and agrees with the local queues. A bounded smoke on the actual
main checkout confirms the corrected two-atom query and exact rebuilt backend.
The final lifecycle source passes fourteen gates with unchanged product/tests/
user-doc/CI/tooling bytes. See the [public delivery record](../devtools/data/combined_session_delivery_687_688_691_20261110.json).

Accepted progress is **75.9795% (about 76.0%)**, **42/50 original graphical
intents**. Only interaction reports, mechanical reports and complete session
receive their original credit. Supplemental fixes add none. Viewer #315 has
received the exact source/evidence and the two remaining coordination needs:
#524's actual published minimum/clean installed closure and #250/#254 contract
feedback. Receiving those original leaves would reach about **80.7414%**;
they are still pending. Keep #666/provider143, #615, construction/protonation/
secondary-structure intents, #256 P5/P6 and #334/exact-candidate gates explicit.
Publication remains paused; no new hosted matrix or package/tag/Release occurs.

## Combined interaction, mechanics and session receiving — 2026-11-10

Exact PR **#687 f35112090** and **#691 0fb92602a** are independently received on
clean **81b4fc866**, including the public #690 native correction, against raw-blob-
verified Viewer **b9f3be01**. **5,923 affected cases pass without omissions**,
plus **116 scientific cases / 74 nodes**, **14 fast gates**, the inspected HTML
build, **two actual Jupyter workflows / 13 browser checks** and a representative
**native Qt workflow / four checks**. Nine continuous scientific phases compare
composition/source maps, independent results, real ensembles, named analysis
versus visuals, H5MSM/session recovery and subsequent selective invalidation.
The original empty ensemble stays empty; the positive control uses a deliberate
same-View Replace with different declared structures and unchanged criteria.
See the [combined receipt](../devtools/data/combined_session_receiving_687_688_691_20261110.json).

#688 is source-resolved: the shared private-file context remains the owner,
the conflicting outer unlink is removed, and nine filesystem cases include
an actual-entrypoint foreign-replacement regression. The original reporter
confirms private hash-only retirement; no private credential contents are read.
Original failed native/graphical/fixture/administrative attempts remain failed.
Passing new-host workflows do not establish #615 causality or accept the earlier
old-host complete Analysis deadline failures.

Credit exactly **three original intents**, **39 → 42/50**: interaction reports,
mechanical reports and complete session. Original weights remain fixed:
**75.6386% → 75.9795% (about 76.0%)**. #688/#690 add no repair bonus.
This is source and automated graphical receiving. Interactions/profiles/pages
remain experimental; graphical mechanics currently reviews requested/default
inputs, with compiled physical-recipe adoption retained as separate consumer
work. Full-session Qt, human, clean installed and exact-candidate gates remain.

Next: verify public combined delivery and close the reviewed PRs/#688. Then
continue #666/provider143, remaining original construction/protonation/secondary-
structure intents and #615, while requesting #524's actual published Viewer
floor/clean installed evidence and #250/#254 agreement. Those two original leaves
would add 4.7619 points and reach about **80.7414%** if genuinely received;
more source-only tests cannot replace them. #256 P5/P6 and #334 retain their
own scope. No hosted matrix, package, tag, Release or promotion is launched.

## Native allocation repair received; incoming session work — 2026-11-10

#690 is source-resolved on clean **573476e70** with the canonical rebuilt
backend. Population-bounded cell tables, checked/fallible sizing and shared
observed-output admission replace allocation proportional to empty volume.
The original protected two-atom abort now succeeds without changing the cutoff
or MIC. **954 affected cases, 83 legacy/consumer cases, 87 Rust tests,
116 scientific cases / 74 nodes, fourteen fast gates and required Clippy pass**.
Eight rendered pages and 37 unchanged notebook code cells/outputs are inspected.
See the [native receiving record](../devtools/data/native_neighbor_allocation_receiving_690_20261110.json)
and [resolution](archive/resolved_bugs/native_neighbor_cell_grids_can_allocate_gigabytes_for_two_atoms_and_a_small_cutoff.md).

All three actual-Jupyter attempts remain failed: two late-workflow deadlines
and one cold server-startup deadline. Their completed numeric checks do not
accept the entire workflow; #421 retains UI receiving and #615 remains causally
unresolved. The supplemental all-targets Clippy failure is retained separately
from the passing required command. Short paired kernel medians suggest about
8–21% extra cost; #692 owns advisory optimization, while #693 owns additional
Python compatibility-output accounting. Neither adds a new release blocker or
changes scientific criteria. Resource caps preserve the shared-host reserve;
no own OOM or reserve stop occurs in the correction receiving.

The complete checkpoint finds **616 issues / 93 open** before our two bounded
proposals, plus incoming draft **#691** stacked on updated **#687**. Review their
exact 0fb92602a/f35112090 heads against raw-blob-verified Viewer b9f3be01,
reconcile the native recipe and scoped launcher, then receive actual combined
interaction/mechanics/continuous-session behavior. The reporter's #688 retirement
handoff is now supplied in #691; its call-site cleanup correction still needs
owner receiving before closure. Formal progress stays **75.6386% (75.6%)**,
**39/50 graphical intents**, with no repair bonus. #524 actual installed floors,
#250/#254 agreement, #256 P5/P6 and #334 exact-candidate gates remain separate.
No hosted matrix, package, tag, Release or promotion is launched.

## Model and context closeout received — 2026-11-10

Public main **1ba5d8af9** is independently verified across all **62 changed
paths**, preserving the four human edits. **#582 and #689 are closed**; #686
was closed earlier in this block. #688 and draft #687 have received the exact
source and handoff notice. See the [public delivery record](../devtools/data/model_and_context_delivery_582_688_689_20261110.json).

#582's experimental physical-model recipe and shared unsupported-control
refusal are accepted. #689 corrects PDBFixer terminal assessment: full molecular
context precedes source-group filtering, including the requested query syntax.
#688's scoped create-only runtime files pass filesystem and actual Jupyter/popup
receiving; its original reporter must still confirm retirement of their own
unused private remnants. Draft PR #687 is newly received for review, not merged.

Clean numerical source 075cd4a40 passes **7,171 affected native/addon cases**
without omissions. All **114 scientific cases / 73 nodes**, **14 final fast
gates**, **10 inspected HTML pages** and **8 filesystem guards plus one actual
six-check Jupyter workflow** pass on the recorded cohorts. Existing code cells,
outputs and execution metadata in eleven affected notebooks remain exact.
Product/registered-science bytes remain equal across the later launcher/docs
cohort; original failed attempts and resource-pressure observations are retained
in the [receiving record](../devtools/data/model_and_context_receiving_582_688_689_20261110.json).

Only the existing #582 leaf gains its original **1.428571 points**. Progress is
**75.6386% (75.6%)**, with **39/50 graphical intents**. Bug repairs and another
passing existing Jupyter scenario add no invented weight. A concrete route past
80% is to receive #524's actual public-floor/clean-installed requirement
(3.333333 points), then agree the #250/#254 surface/final-client requirement
(1.428571 points): approximately **80.4005%**, if genuinely accepted. Those
requirements cannot be replaced by more source-only tests.

### Next work order

**New priority #690:** source inspection confirms an empty-volume dense grid
can request gigabytes for two atoms. Allocation-safe reproduction, checked/bounded
native search and numerical-budget/output receiving precede draft #687. This
critical correctness/resource report adds no weight and is not covered by the
completed model/context receipt. See the [owning diagnosis](archive/resolved_bugs/native_neighbor_cell_grids_can_allocate_gigabytes_for_two_atoms_and_a_small_cutoff.md).

1. Completed: public source/blob verification, #582/#689 guarded closure and
   exact-source notices to #688/#687. Their retained receipts define the scope.
2. Review draft #687 against its exact corrected Viewer b9f3be01, reconcile the
   native recipe/refusal owner and scoped launcher, then receive its combined
   actual interaction/mechanics workflows before any original intent credit.
3. Complete the original #421 construction/protonation/secondary-structure and
   complete-session intents; keep #666/provider143's scientific cutoff boundary
   and #615's causal or evidenced environment disposition explicit.
4. Continue #524's actual installed floors, #250/#254 agreement, #256 P5/P6 stable
   H5MSM review and #334's exact-source/installed/platform/final ledger gates.

This authorized [skip ci] source checkpoint performs no new hosted matrix,
package, tag, Release or promotion. Mandatory candidate gates and publication
remain separate. Historical receipts below retain their original scope/date.

## Native peptide endpoints received — 2026-11-10

#686 is source-resolved: the shared public experimental
`chemical_states.get_peptide_termini` follows stored named backbone bonds instead
of IDs or inventory order. Strict/report modes distinguish ambiguous chains,
cycles and real cap attachments. Native terminal assessment, local completion,
cap anchors and the read-only addon facade reuse it. The 1BRS model has actual
chain interruptions: its native adder now preserves uncertain OXT rather than
choosing an endpoint by label; PDBFixer retains its independent profile.

Clean source receiving passes **342 affected/consumer cases**, **110 scientific
cases / 71 nodes**, **14 fast gates**, **six inspected HTML pages** and actual
execution of both affected tutorials (**17 code cells**). Original failures and
source-cohort identities remain in the [receipt](../devtools/data/peptide_termini_receiving_686_20261110.json).
No extra graphical intent or weighted bonus is added: progress stays **74.2101%**.
Public main da45bb569 is independently verified across all 41 changed paths;
#686 is closed. Human edits were preserved. See the [delivery record](../devtools/data/peptide_termini_delivery_686_20261110.json).
Continue #582's effective model/control contract; #666/provider143, remaining
#421, #256, #524/#615 and #334 gates retain their scope and external dependencies.

## Public combined delivery verified — 2026-11-09

Public main **c9bb16eab** contains the four reviewed PR heads; all **51** changed
or deleted public tree paths are verified and the four human files stay byte-exact.
**#678/#681/#682/#683 are closed** after integration: #678 is marked merged by
ancestry, while the dependent drafts are explicitly closed as directly integrated.
No branch was retargeted or deleted. The complete board now has **613 issues,
93 open, and no open PRs**. #677/#679/#680/#684 remain verified closed.
See the [public delivery record](../devtools/data/molsysviewer_stacked_panels_delivery_678_681_682_683_20261110.json).

The received progress is **39/50 graphical intents** and **74.2101%** under the
original weights. Next is **#686** chemical-terminal correctness, then the
remaining #582/#421 source work and #666/provider143; #256, #524/#615 and #334
retain their independent installed/platform/exact-candidate obligations.
The new #685 proposal is recorded as bounded design/backlog. The source-only
`[skip ci]` checkpoint does not waive future mandatory gates or authorize a
package, tag, Release or promotion. Detailed receiving and prior failures follow.

## Combined graphical receiving and new issue intake — 2026-11-09

The four reviewed PR heads (#678/#681/#682/#683) are ancestors of clean combined
`528c460a9523a2c69aa8116c8e97c26fcfeca9c1`. Against exact Viewer
`9b8662cfb198e6896751c30ee2c7c8780ac85f4c`, **5,857 addon/preflight cases**,
**five actual Jupyter/AnyWidget/Mol* scenarios with 44 checks**, **107 scientific
cases / 68 registered nodes**, **14/14 fast gates** and the HTML build pass.
Five new rendered guide sections are inspected. The original combined run
remains failed (5,856 pass / one obsolete fake-terminal expectation); correcting
that expectation has a separate 63-case consumer receipt and the complete rerun.
Native/addon/workflow/benchmark/user-doc bytes are unchanged between cohorts.
See the [combined receipt](../devtools/data/molsysviewer_stacked_panels_receiving_678_681_682_683_20261110.json).

Credit exactly **eight existing graphical intents**, **31 → 39/50**: PCA,
refinement, five repair/assignment intents and sequence/connectivity reports.
Original nested weights stay fixed: **73.7664% → 74.2101% (about 74.2%)**.
The complete properties leaf still requires secondary structure; removing
rule-defined hydrogens does not complete protonation reconciliation. Explicit
color/plot adoption adds no artificial intent or score. This is source and
automated graphical receiving, not complete scientific readiness, fresh combined
Qt/human acceptance, installed qualification or an exact release candidate.

The complete board refresh has 612 issues, 92 open, before filing our new #686;
four PR heads are unchanged, with #681–#683 now explicitly draft. Public main
`0c6f9c746` already delivers the four closed core defects #677/#679/#680/#684.
The following intake and next work order extend the maintained plan without
silently changing its six weights or release scope:

| Order | Owner | Disposition / next acceptance |
| --- | --- | --- |
| 1 | #686 | Newly reproduced: changing only group ID labels moves the reported C terminus. Review chemical endpoint recognition, ambiguous/cyclic/capped cases and public addition consumers; add a scientific regression before optional enhancements. [Diagnosis](archive/resolved_bugs/native_terminal_detection_mistakes_group_id_labels_for_chemical_sequence.md). |
| 2 | #582 and remaining #421 | Complete the effective engine-neutral mechanical recipe and original unreceived graphical intents; retain the partial properties/protonation distinctions. Receive native/scientific behavior and actual graphical workflows before credit. |
| 3 | #666 / uibcdf/pyunitwizard#143 | Resolve the native cutoff/unit boundary before accepting the contact prototype; no GUI-specific tolerance workaround. |
| 4 | #256, #524, #615, #334 | Continue independent H5MSM/stable-format review, actual dependency-floor/installed closure, diagnostic causality and final exact-candidate/platform gates. |
| Backlog / bounded design | #685 | New PeptideMT request: explicit capped and stereochemically declared coordinate-free peptide references. Reuse the existing peptide/CCD template, assessment/application and CIP owners; do not infer missing experimental chemistry, equate L with S, or confuse primary carboxamide with N-methylamide. This proposal adds no automatic 1.0 blocker. |

Resource caps measured about **4.51 GiB** for the four-worker addon run and
**2.57 GiB** for the graphical run; host availability stayed above **7.5 GiB**,
with no own OOM or reserve stop. Known plain-Jupyter debugger errors remain in
the evidence and have the same fingerprints as the control. Contributor Qt and
historical hosted CI keep their original identities. No new remote matrix,
package, tag, Release or promotion is authorized. Combined public integration
and verified PR closeout follow this received checkpoint.

## Incoming core defects received — 2026-11-09

#677/#679/#680/#684 have source-qualified corrections: actual demo inventory,
source atom selection and full-chain terminal context, format-safe actual PDB
producer version, and component-keyed cap insertion independent of stable molecules.
Clean c643a728f passes **170** expanded native/reference/doctest cases, **16**
benchmark/evidence controls including two actual 21-case campaigns, **14/14**
fast gates and five inspected HTML pages. The dynamic catalog re-executes both
original cells; other guide/course/cookbook code, outputs and metadata stay exact.
See the [core receipt](../devtools/data/incoming_core_receiving_677_679_680_684_20261110.json).
The former false-terminal expectation in the existing addon audit is corrected;
its **63-case** module passes separately on byte-identical native code. Original
combined-addon failure stays failed; the [consumer receipt](../devtools/data/terminal_audit_consumer_receiving_679_20261110.json)
does not replace a rerun. Source publication/issue closure follow this checkpoint.

The complete refresh added stacked PRs #681/#682/#683 under #678 to the existing
#421 plan. Their isolated combined source is under review/testing against exact
Viewer 9b8662cf. No contributor result is reassigned to the combined source, no
GUI intent is credited yet, and core repairs add no artificial weighted bonus:
progress remains **73.7664%**, graphical intents **31/50**. Continue their native,
actual Jupyter and scientific receiving before integration; #582, #666/provider143,
#524/#615, broader #256 and #334 installed/platform/final-candidate gates remain.
All operations retain capped resources and the authorized [skip ci] source route;
no new remote matrix, package, tag, Release or promotion is launched.

## Incoming review and execution block — 2026-11-09

The complete board refresh retains 610 issues (94 open) and finds four open
stacked PRs. #681–#683 are new since the previous checkpoint; #678 remains
unreceived. Their claims are contributor evidence until combined-source review.
The original plan and its weights stay unchanged; these PRs implement existing
#421 task families, not newly added requirements.

| Order | Owner | Work and acceptance |
| --- | --- | --- |
| 1 | #679 | Resolve terminal-capping selection once on the source atom axis; project explicit group/component populations through reconstruction. Cover numeric/expression/mask equivalence, partial populations, multiple structures/components and source preservation. |
| 2 | #677 | Query the actual bundled alanine inventory, reconcile its catalog and manifest, and re-execute the generated catalog notebook without changing the dataset. |
| 3 | #680 | Use actual cached producer version in format-safe PDB provenance; preserve scientific records and deterministic benchmark-owned preparation. |
| 4 | PR #678 | Review existing PCA inspection/refinement, contributor analytic/engine controls and actual Jupyter/Qt evidence. Receive the compatible combined source before credit. |
| 5 | PR #681 | Review chemical repair/assignment panels and explicit atom-to-group scope; #679 remains provider-owned. |
| 6 | PR #682 | Review source-mapped property/report tasks, units, static versus structural semantics and bounded queries. |
| 7 | PR #683 | Review deliberate report color/plot adoption, coverage/refusal/undo and source-structure navigation against its exact Viewer runtime. |

After this block continue #582's effective engine-neutral recipe, remaining #421
intents, #666/provider143, #524/#615, broader #256 and #334 final installed/platform
requirements. Keep published failures and receipts, the source/installed boundary,
the publication pause, resource supervision and [skip ci] source checkpoints.
Accepted weighted progress remains 73.7664% and graphical intents 31/50 until
original owning leaves have independently received evidence.

## Comparability and incoming diagnostics received — 2026-11-09

#567's full comparable-session contract is received: known runtime/provider/
resource/unit identities, actual observables/inputs/precision, raw repetitions,
typed advisory dispositions and reviewed reference renewal. Clean 3547b0977
passes **172** benchmark controls, including two real **21-case** tiny campaigns.
#673 repairs invalid comparative RMSD/PBC workloads and the mislabeled MDTraj
route; #676 replaces inherited competitive workers with fresh factories and
finite lifetimes. The original failures and historical baseline stay exact;
no new reference or representative speed ranking is selected. See the
[benchmark receiving record](../devtools/data/benchmark_comparability_receiving_567_673_676_20261109.json)
and [maintained contract](benchmarking/comparable_sessions.md).

Clean combined ecf05b066 passes **187** composition/axis/active-unit cases and
**14/14** fast gates. #674 preserves an already loaded Pint registry rather than
making an ineffective cache request; #675 distinguishes regenerated positional
indices from lost structural observations. Real off-axis warnings/incompatible
axes remain enforced. All previous fixture/launcher/source-mutation failures
remain in the [diagnostics receiving record](../devtools/data/import_and_composition_receiving_674_675_20261109.json).
These selections overlap existing coverage; they are not a full-suite count.
Public main **af46ea3f3** is independently verified across all **42** changed/
deleted paths; the four pre-existing human edits remain byte-exact. #567/#673/
#674/#675/#676 are independently verified closed and board/queues agree. See the
[public closeout record](../devtools/data/comparability_and_diagnostics_closeout_20261109.json).

The original baseline-comparability leaf now gains **1.25 points**: weighted
source milestones are **73.7664% (approximately 73.8%)**, with graphical intents
unchanged at **31/50**. Supplemental repairs add no bonus. This is operational
source progress, not publication readiness. Resource runs use 1 CPU/2 GiB each;
recorded peaks stay below 0.8 GiB, no own OOM/reserve stop, and observed host
availability stays above 11 GiB. No all-core or unlimited-worker execution.

Next incoming owners are #677's catalog count and #679's terminal-capping numeric
selection axis; PR #678 proposes existing PCA/refinement addon workflows and
requires its own review and actual GUI receiving. #680 tracks the inspected PDB hard-coded producer version;
uibcdf/pyunitwizard#144 owns the guide-cache example correction. Preserve
#666/provider143, #582 effective recipes, remaining #421 intents, #524/#615,
broader #256 and #334 installed/platform/exact-candidate requirements. Source
checkpoints use [skip ci]; no new remote CI, tag, package or Release is launched.

## Source CI, mechanics and advisory performance receiving — 2026-11-09

PR #668 is received with exact Viewer 346c3319 source. #669's controlled wheel
now stays outside the scientific checkout, with real Git and path-with-spaces
controls; #670's projection fixture declares its supported schema while strict
production validation remains unchanged. The observed legacy AllBonds/HBonds
translation in #582 is corrected through a shared private engine adapter.
The broader effective engine-neutral recipe contract stays partial.

Clean c37e42510 passes **5,711** addon/preflight cases, **251** affected mechanics/
projection/force controls and **107/107** registered scientific cases with strict
clean-source correspondence. These overlapping selections are not one full
suite. All fourteen fast gates and repository Ruff checks pass. Actual Jupyter
receives ten Chemistry and twenty Analysis checks on the new frozen host;
missing local tooling/harness attempts remain recorded. Four rendered guidance
pages are inspected; existing notebook code/metadata/outputs stay exact.
See the [receiving record](../devtools/data/pre1_ci_and_mechanics_receiving_669_670_582_20261109.json).

The original hosted run remains failed: Linux/Python 3.14 contains one fixture
failure among 32,901 cases, while macOS/Python 3.12 fails public download before
tests (#671). Source repair does not qualify that matrix or installed artifacts.
#672 is an administrative duplicate of #670, not another defect fixed.

The maintainer accepts [advisory efficiency observations](benchmarking/performance_policy.md)
under #567: keep correct tools available, investigate comparable repeated
slowdowns above 15 percent in improvement issues, and keep invalid evidence
unevaluable. Timing does not block implementation. Full workload/environment
comparability and reviewed reference renewal stay pending.
Clean d1cf23362 receives all **121** affected policy/evidence/preflight controls
and fourteen fast gates; the [policy receiving record](../devtools/data/advisory_performance_policy_receiving_567_20261109.json)
retains old/new behavior, raw diagnostic failures and unchanged reference bytes.

Accepted weighted progress stays **72.5164% (approximately 72.5%)** and **31/50**
existing graphical intents. Regression repairs, receiving a newer host and a
benchmark-policy decision add no artificial milestone credit. Continue #421's
remaining intents, #666/provider143, #524 installed floors, #615, broader #256/
#582 and #334 exact-candidate work. Source pushes use the authorized deferred-CI
route; no new hosted matrix, package, tag, Release or promotion is authorized.

## Current chemistry assessment receiving — 2026-11-09 (#421, #256)

Three additional read-only Inspect tasks now receive two existing Chemistry
assessment intents: exact-template coverage of whole selected source groups,
whole-system terminal OXT inspection and explicit-pH reference-rule protonation.
The tasks apply no repair/removal and retain no executable decision. Native
state/naming/terminal/fixed-pKa and unsupported/partial limits remain explicit.
Reference identifiers are available in a separate collapsed scientific disclosure.

Clean 0d7f5505b passes all **347** affected native/panel/hosted-inventory cases
and public assessment doctests. Native/backend/numeric-test and guide/course
bytes stay exact on dc8568446; that source receives all **10** actual Jupyter/
Mol*/popup checks and **14** fast gates. The guide and course HTML are inspected;
all twelve executed Module 12 code cells/metadata/outputs remain unchanged.
The [receiving record](../devtools/data/molsysviewer_chemistry_assessment_receiving_421_20261109.json)
preserves the launcher/fixture failures, the async empty-table failed attempt
and both passing graphical attempts. The final graphical correction moves long
reference IDs into a disclosure; it changes no science or deadline.

The [scorecard](../devtools/data/pre_1_0_progress_scorecard_20261107.json) records
**31/50** received graphical intents and **72.5164% (approximately 72.5%)** weighted
completion. Only the two original leaves gain credit; three task names, test/
defect counts and the independent client report add no extra bonus. Resource
ceilings remain bounded to 5 CPU/6 GiB aggregate, with no own OOM/reserve stop.

Separately, DockingMT's immutable 9b077fab source documents and authenticated
reader receipts receive its original portable-reference prerequisite and bounded
saved-pose E3 workflow on explicit H5MSM 0.6. See the [upstream receiving record](../devtools/data/docking_h5msm06_client_receiving_256_20261109.json).
This is inspected independent-client evidence, not a local molecular replay or
all P5/P6/installed acceptance. Literal F/farad observation is corrected in the
consumer; its original weaker seals/failures remain. Default 0.5 and explicit
experimental 0.6 remain unchanged.

Next: remaining #421 PCA/sequence/property/interaction/mechanics, repairs,
construction/refinement and complete sessions; broader #256 P5 plus final stable
schema/default freeze; #666/provider143 scientific cutoff review; #524 floors,
#615, human/installed/platform and #334 exact-candidate gates. Viewer e4dd58cf
remains the exact retained host, not a newly qualified client artifact. #421
and #256 stay open. No tag, package, Release or remote matrix is authorized.


## Current vector/angular source receiving — 2026-11-09 (#421)

Three existing geometric-analysis intents are now source-qualified: directed
vectors, explicit triplet angles and explicit quartet torsions. Native 6302af9d6
passes 228 selected cases, including analytical signs/MIC/units and the public
get_angles doctest. Identical product/docs/numeric-test bytes on 6a8552850 pass
all twenty actual Jupyter/Mol*/popup checks, retaining all seventeen old checks.
Fourteen fast gates and four inspected HTML pages pass. Eighteen executed course/
tutorial code cells, metadata and outputs remain exact.

The [receiving record](../devtools/data/molsysviewer_vector_angular_receiving_421_20261109.json)
retains the three initial fixture failures and both incomplete 240-second GUI
attempts. Measured CPU throttling motivated four CPU with the same 4 GiB cap;
the expanded twenty-step scenario has a finite 300-second Node / 360-second outer
budget. Original scientific/scene assertions and other scenario deadlines remain.
Plain-Jupyter browser fingerprints are retained; no new fingerprints are admitted.
Actual host/cgroup resource evidence is distinct from synthetic tiny-budget test
warnings. No unsafe memory stress run is performed.

The [canonical scorecard](../devtools/data/pre_1_0_progress_scorecard_20261107.json)
now records **29/50** received intents; the weighted accepted milestone value is
**72.4028% (approximately 72.4%)**. Only those three existing leaves receive
credit; bug/test counts add none. Native angular eager storage is documented,
with post-1.0 chunking tracked by #667. Contact intent/#666 and
uibcdf/pyunitwizard#143 remain unresolved, with its prototype isolated.

Next: continue remaining #421 analysis/chemistry/construction/refinement/session
intents while resolving #666. Keep #256 independent client receiving/stable-root
freeze, #524 installed floors, #615 causality, human/installed/platform and #334
exact-candidate/publication exits explicit. Viewer e4dd58cf is the exact retained
host here; this does not qualify a newer host or installed pair. No tag, package,
Release, hosted matrix or final-candidate authority is added.

## New contact-boundary evidence and facade priority — 2026-11-09

The #421 contact prototype exposes native #666: an inclusive 0.5 nm decision
changes for equivalent 5 angstrom/500 pm cutoffs. Direct native dense/cell-list
and ordinary/trusted probes reproduce it. The [receiving record](../devtools/data/native_contact_unit_boundary_666_20261109.json)
retains all twenty-four observations and both original prototype selections.
The corrected selection has 152 passes/two failures; the local prototype c96d258b9
is isolated and unpublished. No graphical or milestone acceptance is added.
The general unit-conversion/comparison contract is requested in
uibcdf/pyunitwizard#143; no upstream defect or workaround is inferred.

New Viewer report #665 identifies missing native tools in the bound facade.
Reproduce and repair that public-inventory regression next, preserving native
signatures, independent results, explicit-input utility ownership and experimental
H5MSM controls. Independent #256 receiving, stable-format/candidate gates and
the publication pause remain unchanged.

## Modular encoding review and precision refusal — 2026-11-09

Clean `f03288768` receives #663's public option-boundary correction: 1,907
selected cases without skips/failures/errors, fourteen fast gates and six inspected
HTML pages. All 32 new controls pass, as do five unchanged legacy single/double
fidelity controls and the conversion doctest. The fourteen course code cells,
execution counts and outputs stay unchanged. Existing warning debt remains
explicit; no optional-ABI or complete-suite acceptance is claimed.

Explicit legacy `int_precision`/`float_precision` controls now refuse for modular
H5MSM through SMonitor `ArgumentConflictError`. They were previously accepted
without selecting the actual field dtypes. Ordinary writing retains float64
structural series and declared typed domains. Default 0.5, explicit experimental
0.6, units, scientific evidence, root/layer versions and old handler precision
remain unchanged. Source/target preservation, strict/report calls, mixed dtypes
and trusted-call refusal have public guards. See the
[receiving record](../devtools/data/h5msm_encoding_review_receiving_663_20261109.json).

Future field-specific precision/error budgets are recorded in #664 for post-1.0,
without another release blocker or placeholder API. #256 retains P5 independent
DockingMT receiving and P6 stable-root/default freeze; #334 retains exact source/
scientific/platform/installed gates. Original milestone weight is unchanged.

## Measured mechanics storage and nullable charges — 2026-11-08

Clean `990474db0` receives #662's shared stored-charge correction and the bounded
#256 storage tool: 1,869 affected cases without skips/failures/errors, fourteen
fast gates and four inspected HTML pages. Existing warnings are retained and
match the prior baseline. The eleven missing-value controls preserve detached
float64 elementary-charge arrays, NaN for mixed missing entries, None for absent/
all-missing columns, ordered/repeated/empty selections and unchanged native data.

The three preregistered 62 × 5,000 / 10,000 × 1,000 / 100,000 × 100 synthetic
workloads complete all six operations. The whole sequential campaign peaks near
698 MiB; measured file sizes are 3.42 / 77.37 / 85.12 MiB. These are warm-cache,
regular-data observations, not cold-disk/real-data compression or general memory
guarantees. File mechanical queries still load the whole static mechanical domain;
geometry queries avoid it. The User Guide includes the reusable command and
complete downloadable data. See the [receiving record](../devtools/data/mechanics_storage_and_nullable_receiving_256_662_20261108.json)
and [measurements](../devtools/data/h5msm_mechanics_storage_benchmark_256_20261108.json).

DockingMT #79/#88 have the exact portable provider handoff. P5 independent client
receiving and P6 final schema/default-writer/freeze stay open under #256. Default
writing stays 0.5, with explicit experimental 0.6. #334 installed/platform and
exact-candidate gates remain unaccepted. No native build, dependency, scientific
model, release or remote CI dispatch. Original weighted milestone completion
remains 72.4%; this extra storage/defect work adds no artificial milestone credit.

**Role:** operational audit and correction-tracking packet.  
**Owner:** [uibcdf/molsysmt#334](https://github.com/uibcdf/molsysmt/issues/334).  
**Audit source:** `4a80c22941090257d8ef78df09c944831413ee31`.  
**Last tracking review:** 2026-11-09.

## Experimental public mechanics persistence — 2026-11-08

Clean `69f938947` qualifies explicit public H5MSM 0.6: **1,843 affected cases
without omissions**, **14/14 fast gates** and fresh HTML, with five inspected
pages, the new API anchor and six unchanged baseline warnings. The
[receiving record](../devtools/data/public_mechanics_receiving_256_20261108.json)
retains original attempts, source/runtime inputs, twelve scientific-report refusal
controls and actual complete/projected/nonpolar-H-merged fresh readers.

`format_version="0.6"` is an explicit experimental write/convert option; default
output remains **0.5**. Supported public reads, scoped geometry/parameter queries,
metadata cardinalities, structural iteration, copying, selected extraction and
bounded topology-free append dispatch both modular roots. Native composition
preserves one mechanical provider, including report-only evidence. Calculation
projections are versioned too. Known assignments retain their existing science;
unknown/incomplete reports remain stored evidence but refuse scientific use or
atom remapping through SMonitor. No new model or force algorithm is introduced.

P4's bounded provider implementation is source-qualified and publicly delivered. **Next P5:** independent consumer/reference-workflow receiving, including
prepared persistence and original producer/unit/binding checks. **Then P6:**
bounded storage/memory measurements, final schema/default-writer qualification
and the first stable H5MSM 1.0 freeze. #256 remains open; no client, installed,
platform or release gate is accepted here. Original weighted progress remains
**72.4%**, with **59 source closures and 26/50 graphical intents**. The full
board snapshot remains 593 issues, 88 open and no PR, with no issue above #661.
Tests peak near 1.62 GiB and HTML near 1.26 GiB; all final jobs retain over
13 GB decimal host availability without pressure/OOM/reserve interruptions.

Public `52df76db2e9e29cc4812493e1cf3ca984e9fd57f` independently matches all
58 changed paths and preserves four human files. The
[delivery record](../devtools/data/public_mechanics_delivery_256_20261108.json)
and [owner handoff](https://github.com/uibcdf/molsysmt/issues/256#issuecomment-6732726967)
provide the exact source and opt-in invocation for independent P5 receiving.
No new package or minimum released package version is asserted.

## Private whole-file mechanics composition — 2026-11-08

Clean `b184e9d18` qualifies the #256 private whole-file root 0.6 orchestration:
**1,229 affected cases without omissions**, **14/14 fast gates** and fresh HTML.
The [receiving record](../devtools/data/mechanics_composition_receiving_256_20261108.json)
retains actual complete/projected/nonpolar-H-merged preparations in fresh readers,
original producer/assignment/history/maps, selected PDBQT bytes, another unit
policy, blocked preparation engines and actual edit invalidation. Resident
assembly requires explicit connected identity associations; independent maps
remain independently readable. Shared identity metadata avoids atom-sized index
arrays. A reusable atomic helper publishes only completed new files.

The new **#661** public uint64-overflow correction rejects invalid indices before
signed conversion/file creation, with twelve guards across all three axis kinds.
Its [resolved report](archive/resolved_bugs/unsigned_h5msm_axis_maps_wrap_out_of_range_indices_to_unknown.md)
is published and #661 is closed. The #660 absent-Structures
fixture is also corrected: original 1,111-case evidence did not exercise that
fifth branch; the dated archive/receipt correction preserves the original results.
The module-placement owner is #438; mistaken earlier #441 references are corrected
without changing executed evidence or reopening that unrelated distance bug.

The public default and supported reads remain H5MSM 0.5/0.3–0.5. P4 must integrate
version dispatch, conversion/query/selection/copy/append and source-preserving
migration; P5/P6 retain consumer and whole-format/default-writer qualification.
#256 remains open. Original weighted progress is **72.4%**, with **59 source
closures and 26/50 graphical intents**; no extra weight is credited for this
added format scope. The complete board snapshot is
593 issues, 88 open and no PR. Tests peak near 1.0 GiB, HTML near 1.25 GiB;
all final runs retain over 12 GB decimal host availability without resource stops.

Public source `1d033b65693dc0db84e594efccd2bf8651a19dda` independently matches
all 21 changed paths, with four human files preserved. The
[delivery record](../devtools/data/mechanics_composition_delivery_256_20261108.json)
and [owner response](https://github.com/uibcdf/molsysmt/issues/256#issuecomment-6731932749)
retain the private/public distinction. Next implement P4's supported public
operations before requesting consumer acceptance; #256/#438 remain open.

## Private mechanics-layer implementation — 2026-11-08

The bounded #256 field/type/unit catalog and private schema-1 codec are now
implemented locally. The 94-case directed selection passes, including 65 new
codec controls and the 29 existing refusal controls. Three actual prepared
system variants retain complete mechanical reports through fresh readers with
another unit policy and no preparation engines/Ackredit. Numeric arrays are
HDF5 datasets; UTF-8 labels use bounded fixed-width transfers. Source producer
metadata and original historical maps remain stored evidence, without rebinding.
The [owning plan](pending_proposals/h5msm_0_6_molecular_mechanics_persistence.md#p1-catalog-mechanics-layer-schema-1-draft)
records exact types/units, absent/empty semantics, malformed-data refusals and
original prototype failures. Clean `5c38a1022` now passes **1,178 affected cases
without omissions** (67 new codec guards) and **14/14 fast gates**. The
[receiving record](../devtools/data/mechanics_layer_receiving_256_20261108.json)
retains the initial layout failure and its AST-identical relocation to private
storage. Passing HTML from `d3e6b1ac7` is reused for an explicitly unchanged
scope, with three inspected pages and six unchanged warnings. The failed old
fast result is retained separately. Public `2cca126fe25ecf8f8d40e77acd8fb930e7e34f87`
independently matches ten changed paths and preserves the four human files;
[delivery](../devtools/data/mechanics_layer_delivery_256_20261108.json) and the
[owner response](https://github.com/uibcdf/molsysmt/issues/256#issuecomment-6731162300)
retain that bounded scope. The measured final test peak is 1,046,847,488 bytes,
with host availability above 13 GB decimal and no OOM/reserve/pressure stop.

This private layer does not yet make H5MSM 0.6 or 1.0 publicly writable/readable.
P3/P4 still need modular associations, public queries/conversion and persistence
operations; P5/P6 need consumer receiving and whole-format qualification. #256
remains open. Original weighted progress stays **72.4%**, with **58 source
closures and 26/50 graphical intents**; no new weight or closure is claimed.
The complete issue-board checkpoint still has 592 issues, 88 open and no PR.

## Current mechanics persistence work — 2026-11-08

The maintainer authorizes advancing **#256 before 1.0**, superseding the old
calendar restriction recorded in the checkpoint review below. The accepted
target is **H5MSM 1.0 alongside MolSysMT 1.0**, after schema qualification;
0.6 may be a development stage. Subsequent format versions evolve independently,
with incompatible changes requiring a new format major. The
[bounded plan](pending_proposals/h5msm_0_6_molecular_mechanics_persistence.md#revised-implementation-plan--2026-11-08)
defines P0–P6, model requests versus completed assignments, typed units/tables,
original reports, atom/state binding, partial-domain refusals, public operations,
fresh-reader/client gates and the default-writer/freeze decision.
No new format, tag, release or package is implemented or published by this plan.

**#660 is source-qualified:** a shared presence check catches report-only and
present-empty stored mechanics in all five H5MSM branches and MolSysDict 0.2.
Clean `272745fc8` passes **1,111 cases without omissions**, fourteen fast gates
and HTML. Three rendered pages are inspected; six existing HTML warnings and
course code/outputs are unchanged. The
[receiving record](../devtools/data/mechanics_presence_receiving_660_20261108.json)
retains the original failure, 29 new guards, runtime versions and resource limits.
The 0.5 schema and parameter-only dictionary projection are unchanged. Tests
peak at 542,543,872 bytes; final runs retain over 14 GB decimal host availability
without resource stops. Public delivery is independently verified at
`af71a6d29a334d2ae9d102be8ea6647f9f5ff1b3`: all 17 changed/deleted paths agree,
and the four human root files are preserved. **#660 is closed**; see
[delivery](../devtools/data/mechanics_presence_delivery_660_20261108.json).
Formal progress remains 72.4%, with **58 source closures and 26/50 graphical
intents**. The complete board has 592 issues, 88 open and no open PR.
#256 is now assigned to the 1.0.0 milestone; the
[owner decision](https://github.com/uibcdf/molsysmt/issues/256#issuecomment-6730428162)
keeps its portable client gate open. Next complete P1's exact field/type/unit and
axis catalog, then the codec and public/client receiving. New #256 work does not
receive artificial completion credit; no 0.6/1.0 codec is available yet.
The earlier post-1.0 statements below retain their dated review context and are
superseded by this maintainer decision.

## Maintainer follow-up queue — 2026-11-08

The bounded **#256 existing-public-composition review is complete** on public
`89b492e0f9c54702a3650dd95a47b517c2c7a17a` (11 verified paths; human files
preserved). Its future H5MSM 0.6 proposal remains open/post-1.0. No runtime
implementation changed: clean `e02ed4deb` passes 235 affected cases without
omissions, fourteen fast gates and HTML. Six valid and four adverse fresh readers
receive the existing native Python checkpoint under compatible trusted conditions;
[receiving](../devtools/data/native_checkpoint_receiving_256_20261108.json) and
[delivery](../devtools/data/native_checkpoint_delivery_256_20261108.json) keep
original reports, unit/association/history checks, selected public export,
invalidation and all scope exclusions. This is a local checkpoint option,
not the client's original complete H5MSM acceptance.

Clustering-unit defect **#659 is closed** and public at
`61b072b46b1c8bb1cba84b3ed42ca1e23dc287d9` (14 verified changed/deleted paths,
four human root files preserved). Clean `68350e0b2` passes 210 affected cases
with published PyUnitWizard 0.28.1 and the same guards with the exact clean
`f82b618` source used by DockingMT. Fourteen fast gates and five rendered pages
pass; original failures, literal/adjacent cutoffs and unchanged source/provider
hashes are retained in [receiving](../devtools/data/distance_clustering_unit_policy_receiving_659_20261108.json)
and [delivery](../devtools/data/distance_clustering_unit_policy_delivery_659_20261108.json).
The fix removes a presentation-unit round trip without adding fuzzy tolerance;
DockingMT's complete rerun and #256 hold remain independent.

Producer-version **#657 is closed** and public at `c35a342143a2de8205e74438f3787b07b9b7f5d3`
(15 independently verified changed/deleted paths, four human root files preserved).
Clean `bbb5eb7c7` passes 172 affected cases and fourteen fast gates; four rendered
pages, six unchanged warnings and preserved course code/outputs are retained in
[receiving](../devtools/data/runtime_version_receiving_657_20261108.json) and
[delivery](../devtools/data/runtime_version_delivery_657_20261108.json).
Unmatched unstamped source reports `0+unknown`; original producer metadata is
preserved. Build labels and exact mutable-source identity remain distinct.

Native correctness issues **#656/#658 are closed** and public at `a450529c3`
(13 verified changed/deleted paths, four human files preserved). Clean
`35ad4bc59` passes 247 cases, fourteen fast gates and HTML. Five rendered pages,
37 new selected-value/coordinate-edit controls and all prior failures are retained
in [receiving](../devtools/data/native_composition_receiving_656_658_20261108.json)
and [delivery](../devtools/data/native_composition_delivery_656_658_20261108.json).
The atom-to-coordinate integrity fix introduces no new snapshot or model.

Provider **#604 is also delivered and closed** at `261967eaf`; DockingMT #79
receives its supported pairwise/clustering composition, with independent E3 and
#256 persistence holds preserved. This changes no H5MSM 0.6 post-1.0 decision.

Accept no additional graphical intent or weight: **26/50**, all four fitting
intents, **72.35035797535798% (approximately 72.4%)**. Separate source closures
are now **57**. #421 remains partial. **Next finite correctness work: #660**,
the report-only mechanical provenance refusal gap reproduced during the review.
A synthetic invalid/stale report with no parameter values currently disappears
on accepted H5MSM/MolSysDict round trips; no valid client artifact loss is claimed.
Fix the rejection without adding mechanics storage. Keep #654 intake, remaining
graphical requirements and the planned OpenMM/openmmtools comparison. Complete
board: **592 issues / 89 open / no open PR**. Installed/platform/human/exact-candidate
requirements and frozen scientific gates are unchanged. The #256 review changes
no weighted leaf or closed-issue count.

Before publication, sequence-fit completed clean local receiving on `63fc27883`: 113 affected source
passes, two real Jupyter guards / sixteen checks, fourteen fast gates and HTML.
The [receipt](../devtools/data/molsysviewer_tools_sequence_alignment_receiving_421_20261108.json)
retains the broad partial failure, test-only repairs, unchanged runtime reuse and
reference memory boundary. That local checkpoint carried no public-source
acceptance, new score weight or closure count. #656 is a separately reported copy-policy bug;
#604 was queued at that preceding checkpoint and is now delivered above; the
OpenMM/openmmtools comparison remains planned.

The #655 prerequisite is source-qualified in `10d43b2a9`: 1,181 passing tests,
including conversion doctests, fourteen fast gates and inspected HTML. Its
[resolution](archive/resolved_proposals/h5msm_static_topology_conversion_reads_coordinate_payload.md)
retains the negative attempts and legacy reconstruction boundary. Public delivery is independently verified at `ca96894ea` (20 changed paths),
and #655 is closed. No weighted leaf is added; progress stays 72.3%, with
52 separate source closures and 25/50 accepted graphical intents.

The completed sequence-fit intent uses the received #655 static-topology
conversion prerequisite. #604 then supplies the bounded provider operations
recorded above. Record new incoming #654's GHECOM nonnumeric-REMARK
compatibility question without claiming reproduction or a policy decision.
At a forthcoming deliberate pause, audit available OpenMM/openmmtools analysis
and system-manipulation tools against existing MolSysMT capabilities. Preserve
form-agnostic/engine-neutral boundaries and attribution; distinguish reusable
molecular tools from Praxis/Nextia protocol/sampling orchestration. The study
and queued issues do not add scorecard leaves or alter frozen release gates.

## Dedicated periodic-origin source delivery — 2026-11-08

Public checkpoint `be11ef8f5c32008e4299e3b406062f8d587f323c` independently matches
all fourteen delivered paths and preserves four human root files. The
[origin receipt](../devtools/data/small_origin_gui_receiving_421_20261108.json)
retains 264 clean native/request passes, the first failed pm fixture, corrected
two-probe receiving and stronger four-probe nm/pm Jupyter receiving. The latter
passes fourteen checks on clean `d2918aa6c`, distinguishing zero-origin and
ignored-input-unit counterfactuals by complete cells. Exact stored boxes/units,
all native coordinates and actual Mol* images remain guarded. Source/export
fingerprints agree; runtime/Rust behavior and all deadlines are unchanged.
Fourteen fast gates and HTML pass with six unchanged title warnings, validated
rendered links and unchanged course code/outputs. The board is unchanged at
585 issues / 88 open / no open PR, with local queue agreement.

Progress remains **approximately 72.3%**, **25/50 graphical intents** and
**51 audit-related source closures**; this dedicated receiving adds no intent
or closure bonus. Continue the accepted sequence-fit intent and remaining
families, retaining #615 uncertainty, #567 policy, #582 effective recipes and
all human/installed/platform/exact-candidate requirements. No tag, package,
Release, promotion or hosted matrix is launched.

## Cell-assignment source delivery — 2026-11-08

Public checkpoint `dae961200c2c855cdf24f50fb2806ecabef8aaa6` independently matches
all 22 changed paths. Clean `7ba4f2ed5` passes 550 affected source cases and two
actual-Jupyter guards / sixteen checks, without skips, failures or errors. The
[cell receipt](../devtools/data/cell_assignment_gui_receiving_421_20261108.json)
keeps source fingerprints, current/independent effects, selected-structure
coverage, unchanged Cartesian positions/chemistry, physical units, factory
validation and actual popup authorities explicit. Fourteen fast gates and HTML
pass on `dae961200`; six existing title warnings are unchanged. Course code and
saved outputs are preserved. Four unrelated owner-formatting corrections keep
identical complete ASTs; whole-tree Ruff passes. Human root edits are untouched.

The existing cell-assignment leaf advances the unchanged scorecard to
**approximately 72.3%**, with **25/50 graphical intents accepted** and still
**51 audit-related source closures**. No defect-closure bonus or new intent is
introduced. Dedicated tiny-boundary-origin cross-policy graphical receiving
precedes the remaining accepted task families; #421 is partial. #615 uncertainty,
#567 policy, #582 effective recipes, installed/platform/human and exact-candidate
qualification remain due. The complete board is 585 issues / 88 open / no open
PR. No public artifact or hosted matrix was created.

## Fixture ownership and bounded scientific claims — 2026-11-08

#649/#650 are published on main checkpoint `a5fc92a23` and independently verified
closed. Their actual fixture fix is `242cbb98e`; qualified source `a2993b8f0ec0bbf34b95966891f9b783f61dbe85`
passes **525 parallel cases**, zero skips/failures/errors, alongside fourteen
fast gates, incremental HTML and applicable Ruff checks. The
[fixture receipt](../devtools/data/conversion_fixture_receiving_649_650_20261108.json)
retains the original six-failure/seven-pass serial diagnosis and 518-case
serial receiving. Positive water fixtures explicitly declare order-one O–H
bonds; unknown orders still fail. Fresh children select the real owner test
package from an unrelated working directory, with every blocked-engine case
retained. Package discovery excludes tests; no installed artifact is claimed.

The same source receives **43 Collantes/reference/unit/tutorial/doctest cases**
under normal and nondefault unit policy. Its
[claim receipt](../devtools/data/collantes_public_claims_receiving_473_475_20261108.json)
accepts only the audit's bounded experimental disposition: provisional ISA area
and retained legacy ECI wrapper/sums. Misleading physical-charge introductions
and the validation-index row are corrected. #473/#475 remain open for original
formula/table/unit and justified aggregation review; no scientific classification
is promoted. The Tool/Common Core retain unchanged executable cells and outputs.

Progress is **approximately 65.3%**, with **43 audit-related source issues
closed** and **23/50 graphical intents accepted**, under the unchanged weights.
The complete issue inventory contains **582 issues, 93 open**; no open PR was
present at the latest complete PR acquisition. This accepts one existing
scientific-claim leaf; supplemental fixture repairs add no bonus.

#612 remains active. The serial full attempt is deliberately interrupted after
1,544 passes. A later four-worker/6-GiB attempt reaches its 128-task cap and is
stopped; pytest/Receptor finalization and ending Git metadata are incomplete.
There is no OOM. The [resource record](../devtools/data/source_suite_resource_adjustments_612_20261108.json)
separates task-starvation errors from the two real fixture defects. The corrected
525-case pilot peaks at 3.07 GiB and 32 tasks, with no limit events. Next run the
complete exact-source suite with four workers, 6 GiB maximum/5 GiB high, no swap,
512 tasks and one native thread per worker; preserve the maintainer's 2 GiB
absolute host floor with earlier monitored stopping. Other graphical,
scientific-contract, installed/platform and exact-candidate exits remain due.
No new remote matrix, artifact, tag or release follows from these source gates.

## Public graph/XYZ examples received — 2026-11-08

#648 and #610 are published on public main `0aa9d853418f5c7061bd26ff71b16976b87656f4`
and independently verified closed. Qualified source `d2ce182a46cf247fa466f31606402cf3734ba8d4`
passes **89 cases**, including twenty new public-example/axis controls, literal
README graph-analysis and graph/XYZ recipe blocks, and the public getter
doctest. Fourteen fast gates and incremental HTML pass on the same source.
The [receiving record](../devtools/data/public_graph_xyz_receiving_648_610_20261108.json)
retains original failures, authoring corrections, checksums, notebook preservation
and resource observations. Tests peak at about 526 MiB, fast gates at 382 MiB
and incremental HTML at 380 MiB under the verified serial 2 GiB/one-CPU/no-swap
route. There is no OOM event or host-reserve violation. Four human documentation
edits and the native binary remain unchanged.

The rigid-fragment example now uses public ChemicalStates and explicitly typed
complete connectivity. XYZ retains its documented atom-level query and direct
quantity assignment; default system-coordinate delivery remains unsupported.
README quartets use chemical_states. #378 receives its bounded pre-1.0 example
contribution; its broader discoverability proposal stays partial and open.

The original #378/#610 milestone is now accepted. Progress is **approximately
63.9%**, with **41 audit-related source issues closed** and **23/50 graphical
intents accepted**, retaining all six original weights. The complete paginated
board contains **580 issues, 93 open and no open PR**. Next is #612's complete
exact-source receiving through the bounded serial route; continue the remaining
graphical and scientific-contract work without losing installed/platform or
final-candidate exits. No new artifact, remote matrix, tag or release is claimed.

## Indexed-H policy source closeout — 2026-11-08

#645 is published and independently verified closed. The experimental public
`chemical_states.normalize_indexed_hydrogen_policy` owns explicit admission,
canonical assignment and typed transformation evidence; strict correspondence
is unchanged. Qualified implementation `4f7c7e4c278a9995909c2f4d9bec917d03729a63`
passes **247 clean-source cases**, including 57 new contracts and its public
doctest, with zero skips/failures/errors. Fourteen fast gates pass on
`6e3c8d23e440c703632bed55cbe39e2a03244406`; corrected HTML and rendered
Tool/Cookbook/API/course links pass on `718576353997d86ea877c887c291fb6a5bd3b2b4`.
Their hashed runtime/test/fixture inputs are identical. The generated scientific
inventory adds no independent validation or coverage claim.

Public main checkpoint `4cafe7af25d626729c58df67adf30a788d2e0630` retains
all thirty-one verified changed/deleted paths. The
[owner receipt](../devtools/data/indexed_hydrogen_policy_receiving_645_20261107.json)
and [archived report](archive/resolved_proposals/normalize_stored_hydrogen_policy_for_correspondence.md)
retain every actual attempt, admission rules and scope. DockingMT #79 received
the supported contract and exact source handoff (6718020308). Its different
provider/RDKit prefix, complete workflow and installed artifact remain separate.
Native-copy future qualification #408 records this additional client case
(6718035629), without making it a new 1.0 client gate.

Tests peak at about 403 MiB. Full HTML peaks at about 1.50 GiB under the 2 GiB
bound, with high-memory throttling and no max/OOM event or swap. Corrected
incremental HTML peaks at about 477 MiB. All campaigns use one CPU, preserve
the host reserve and terminate normally. Native coordinate/box sharing and
later edit isolation are tested; other mutable metadata keeps its native-copy
allocation rules. No realistic 100,000-atom by 10,000-structure benchmark is
claimed. Twelve course code cells, saved outputs, IDs and metadata remain
unchanged; the new Tool/Cookbook examples execute under both unit policies.

The refreshed complete board contains **580 issues, 95 open and no open PR**.
New #648 records an inspected
[stale rigid-fragment tutorial](archive/resolved_bugs/rigid_fragment_tutorial_uses_retired_topology_chemical_attributes.md)
that still uses retired Topology chemistry. Reproduce and repair that bounded
example next, then receive #610 public XYZ coordinate delivery. Preserve the
broader #378 discoverability work and every other audit requirement.

The accepted score stays **approximately 62.5%**, with **39 audit-related source
issues closed** and **23/50 graphical intents accepted**. Supplemental capability
work adds no bonus to the frozen milestone weights. #612's complete source suite,
every remaining graphical, scientific-contract, installed/platform and exact-
candidate exit remain due. No new tag, package, remote matrix or release follows
from this source closeout.

## Previous scalar-ID closeout and next policy work — 2026-11-07

#647 is published and independently verified closed. Qualified source
`d020ff4a4e005c1e6076a9f417446685465fdf71` passes **279 clean-source cases**,
including **138 new setter controls**, all 54 comparison controls, existing
chemical-component/recovered-append tests and the public MolSys setter doctest.
The fourteen fast gates and applicable Ruff checks pass. Public main checkpoint
`d04d413d77a7fa1b745dd5c4ad31565373b0de73` retains all eighteen verified
changed/deleted paths and the preceding #644/#646 source repairs. The
[receipt](../devtools/data/component_id_assignment_receiving_647_20261107.json)
and [archived report](archive/resolved_bugs/scalar_string_component_id_is_rejected_by_the_molsys_assignment_adapter.md)
retain the original twenty-failure baseline and receiving scope. DockingMT
#33/#49 received the source and separate #645 study handoff (6717492396).

Tests peak at about 237 MiB, and fast gates at about 381 MiB, under serial
execution, one CPU, an enforced 2 GiB process-tree limit and zero swap. No OOM
or resource interruption occurs. No native kernel, dependency, storage schema
or scientific model changes. Both documentation notebooks retain all code
cells, outputs, IDs and metadata; their edits are Markdown only.

The refreshed complete board contains **579 issues, 95 open and no open PR**.
Next is #645's [explicit stored-H policy decision](archive/resolved_proposals/normalize_stored_hydrogen_policy_for_correspondence.md):
the real-input normal/nondefault-unit and H5MSM feasibility study is measured,
but a supported admission/rejection policy and transformation evidence remain
open. Keep #610's public XYZ delivery and the broader #378 work in scope.

The accepted score stays **approximately 62.5%**, with **38 audit-related source
issues closed** and **23/50 graphical intents accepted**. Supplemental bug
repairs and a private feasibility study add no milestone points. #612's complete
source suite remains pending; preserve every graphical, scientific-contract,
installed/platform and final-candidate exit. No new tag, package, remote matrix
or release is authorized by these source deliveries.

## Previous comparison closeout and stored-H feasibility — 2026-11-07

#646 is independently verified closed after publication of qualified source
`ad67e0e915ba23d90cb9d6331c063c342852d67a` on public checkpoint
`4f642256996bd25a21a9b204d7a684207e589974`. Receiving passes **220 cases**,
including **54 new controls**, the public compare doctest and fourteen fast
gates; applicable Ruff checks pass. All fifteen changed/deleted paths match
the public tree. Tests peak at about 300 MiB under one CPU, a 2 GiB process-tree
bound and zero swap. The [receipt](../devtools/data/component_comparison_receiving_646_20261107.json)
and [archived report](archive/resolved_bugs/compare_component_type_boolean_flag.md)
retain failures, output/metadata semantics and limits. DockingMT #33/#49 received
the source handoff (6717397158); its complete workflow/artifact gates remain separate.

The complete board contains **579 issues, 96 open and no open PR**. #647 owns
the separate scalar string-ID setter rejection found by the original controls.
Its [record](archive/resolved_bugs/scalar_string_component_id_is_rejected_by_the_molsys_assignment_adapter.md)
retains that failure; this bounded repair is next. For #645, a
[real-input study](archive/resolved_proposals/normalize_stored_hydrogen_policy_for_correspondence.md)
reproduces zero strict maps, then two maps after a private explicit-copy/set
policy experiment, under both unit policies and after H5MSM. This is feasibility;
no supported normalization policy or scientific equivalence is accepted.

The accepted score stays **approximately 62.5%**, with **37 audit-related source
issues closed** and **23/50 graphical intents accepted**. Supplemental repairs
and the study add no milestone points. Preserve #612's complete-source suite,
#610/#378 and every remaining graphical, scientific-contract, installed/platform
and final-candidate exit. No release or new remote matrix is authorized.

## Previous formal-charge closeout and incoming comparison flag — 2026-11-07

#644 is published and independently verified closed. Qualified source
`64f8c955ac8b93198f4926642d4f3d257a1d0c27` passes **474 focused cases**, with
zero skips, failures or errors, the updated public setter doctest, fourteen fast
gates and applicable Ruff checks. Public checkpoint
`f271a431d3c8b1f97261b1af573fb48ccc442d1f` retains all thirteen verified
changed/deleted paths. The [owner receipt](../devtools/data/formal_charge_boundary_receiving_644_20261107.json)
and [archived report](archive/resolved_bugs/formal_charge_nonquantity_error_leak.md)
retain the original failures and exact scope. DockingMT #33/#49 received the
source handoff (6717288667); its whole-provider/workflow qualification is separate.
The final tests peak at about 380 MiB under a 2 GiB process-tree bound, one CPU
and zero swap. No native backend, dependency or scientific method is changed.

The complete refreshed board contains **578 issues, 96 open and no open PR**.
New #646 reports rejection of a supported `component_type` Boolean comparison
flag. Its [owner record](archive/resolved_bugs/compare_component_type_boolean_flag.md)
starts with source inspection; bounded reproduction and repair take priority
before the separate #645 [stored-H policy study](archive/resolved_proposals/normalize_stored_hydrogen_policy_for_correspondence.md).
Strict chemical matching remains unchanged.

The accepted score stays **approximately 62.5%**, with **36 audit-related source
issues closed** and **23/50 graphical intents accepted**. This supplemental
boundary repair adds no milestone points. Preserve #612's complete-source gate,
all remaining graphical, scientific-contract, installed/platform and final-
candidate requirements. Shared resource feedback remains owned by
uibcdf/uibcdf-infrastructure#1 and uibcdf/moli#96. No release, candidate or new
matrix is authorized by this source closeout.

## Previous naming-contract owner closeout — 2026-11-07

#549 is independently verified closed after D0–D7 source acceptance. Qualified
source `d7c7b7e927824a45f806aca040199a2aa7d84d03` passes **545 focused cases**,
the public scalar-helper doctest, the canonical **ten-cell tutorial**, fourteen
fast gates and applicable Ruff checks. Public main checkpoint
`8f8b2e6646b0c7089e2b04d13d2d02e1fe6aff80` retains all eleven independently
verified changed/deleted paths. The
[owner receipt](../devtools/data/group_naming_owner_receiving_549_20261107.json)
and [archived report](archive/resolved_bugs/reconcile_legacy_amino_acid_name_mappings_with_native_protonation_labels.md)
retain the exact source, original outcomes, semantic boundaries and authorized
Viewer #315 handoff (6716685189).

Three new cases cover complementary domain order, selected source axes and
foreign declared chemistry. The namespace and bounded native/client naming
contract are accepted; profile coverage and stability remain experimental.
No values, scientific references, runtime algorithm or dependency are changed.
The final tests peak at about 454 MiB under an enforced 2 GiB process-tree
bound, one-CPU quota and zero swap. The preceding private selector mistake
and protective stop are preserved; it is not product failure or passing
qualification. Serial plans now reject parallel worker arguments before launch.

The existing #549 phase-five leaf adds 10/7 points with unchanged phase weights:
**approximately 62.5%**, **35 audit-related source issues closed**, and
**23/50 graphical intents accepted**. #612's complete source suite remains
pending; its one-case bounded pilot does not clear that gate. Continue its
safe exact-source route and independent #610 composition review while retaining
all remaining graphical, #473/#475, contract, installed/platform and final-
candidate requirements. No publication is authorized by this source closeout.

## Previous alternate-location qualification — 2026-11-07

#612's strengthened PDB fidelity guard is committed at
`2465d6b0cb137446f9917c971572a921003a9b89`: primary/alternate coordinates,
occupancies, B factors and string IDs are checked against literal fixture
values while preserving stable-ID atomicity. The affected 103-case battery
and all fourteen fast gates pass. The historical inconsistent test still fails
at the native refusal, as expected.

The complete default local suite was interrupted by the maintainer after
shared-host RAM exhaustion. The outer process exits 143 without finalized
JUnit/pytest results; the partial Receptor stream is incomplete. The
[receiving record](../devtools/data/alternate_location_owner_receiving_612_20261107.json)
preserves the exact source, command, passing focused controls and interruption.
This is not complete-suite acceptance. No heavy retry is launched; remaining
qualification needs a measured, resource-bounded execution route.

#612 remains open. Progress stays **approximately 61%**, with **34 audit-related
source issues closed** and **23/50 graphical intents accepted**. All graphical,
contract, installed, platform and final-candidate requirements remain. Continue
lightweight development while this resource-sensitive gate is deferred.

## Previous pagination owner closeout — 2026-11-07

#587 is accepted and independently verified closed. The implementation and
regression guard from `96191e07e6c0ba755b53e14c785ad953e7aa55f3` are unchanged
on public main `e84b8a99bd8aae8d1f92cbea72574b443ed2d57e`. Its historical
capped function fails the existing guard; current receiving passes **103 cases**,
including **five pagination controls**. Actual complete acquisition finds
575 issues, while the old 500-entry command loses #22 and #25; independent
issue views confirm their correct states. These are transport/fidelity controls,
not a new complete molecular test suite.

The [owner receipt](../devtools/data/devguide_pagination_owner_closeout_587_20261107.json)
retains the original failure, current execution, source correspondence, verified
closure and authorized handoffs to uibcdf/molsyssuite#171 (6714393150) and
uibcdf/moli#85 (6714393717). Their adoption remains separate. The
[archived report](archive/resolved_bugs/devguide_board_sync_truncates_issue_history.md)
records the local resolution.

There are now **34 closed audit-related source issues**. Milestone progress
remains **approximately 61%**, with **23/50 graphical intents accepted**. The
joint #612/#587 milestone is still pending: #612 requires its own affected
fidelity and exact-head full-suite acceptance. Continue that work, preserving
every remaining graphical, contract, installed, platform and final-candidate
requirement. Source closeout does not authorize publication.

## Previous external-reference source delivery — 2026-11-07

The #421 external-file fitting intent is accepted in sources on main at
`b3f4fd4cb38f98eb5d96d2617f6f1977c91717e1`. All fifteen changed paths match the
complete public tree. Receiving passes **5,297 integrated cases**, the original
provider read-window guard and both actual external/same-system Jupyter/Mol*
scenarios (**eight steps each**). Clean exact-source scientific execution passes
**107 cases / 68 nodes**, with zero skips/failures/errors. Fourteen fast gates
and HTML pass; six existing title warnings and baseline-matching page errors
remain recorded. The
[delivery receipt](../devtools/data/molsysviewer_tools_external_reference_delivery_20261107.json)
retains the public correspondence, scientific source and authorized Viewer #315
handoff (comment 6714264760). The receiving record preserves all attempts,
including premature blank captures and the stronger explicit focus/render check.

Progress is **approximately 61%**, now **23/50 graphical intents accepted** and
**33 audit-related source issues closed**. The existing external-reference leaf
adds about 0.057 weighted points; this is not a new weight or issue-count bonus.
The addon remains partial. Next: reconcile the already-delivered #587 pagination
closeout and #612's owning evidence, while retaining every remaining sequence/
cell/task/session and contract/installed/platform/human/final-candidate exit.
No new tag, candidate, artifact, remote matrix or publication is authorized.

## Previous modular-query delivery — 2026-11-07

#643 is fixed on public main at `71a2c2b8ef807f9ddce300cfd3917c5a51f56a1a` and
independently verified closed. All thirty changed paths match the complete
public tree. Receiving passes 1,921 integrated cases (eighty new provider
cases), three doctest nodes, fourteen fast gates and HTML with six retained
existing title warnings. Clean exact-source scientific execution passes
107 cases / all 68 registered nodes, with zero skips/failures/errors.

The unchanged external-reference prototype now passes **341 directed cases**,
including its original 5,000-structure read-window guard. The
[delivery receipt](../devtools/data/modular_h5_query_delivery_643_20261107.json)
records the public blobs, exact scientific source, unchanged prototype/test
bytes, closure and authorized Viewer #315 handoff (comment 6713930007).
[The archived report](archive/resolved_bugs/h5msm_0_5_queries_read_full_coordinate_series_before_applying_selection.md)
retains all failed attempts and the explicit static/map/external-backend limits.
Next: actual external-reference Jupyter/Mol*/popup receiving, then the remaining
agreed fitting/cell/task/session intents. The prototype remains local/unmerged;
its graphical leaf is not accepted yet.

Progress remains **approximately 61%**, **22/50 graphical intents accepted**,
and **33 closed audit-related source issues**. The closure adds no milestone
bonus. All contract/installed/platform/human/final-candidate requirements and
nightly/full-matrix backlog remain due. No release candidate, tag or artifact
is selected or authorized by this source checkpoint.

## Previous external-reference prerequisite — 2026-11-07

The next #421 graphical slice has a local, unmerged external-reference
prototype (`ca59736a4`). Its explicit ordered atom pairs and physical-unit
snapshot pass 339 directed cases, but a strengthened HDF5 I/O guard refuses
unrequested full-series reads (340 passes/one failure). The public query layer
materializes H5MSM 0.5 before applying even scalar/selected requests. The
[owning #643 report](archive/resolved_bugs/h5msm_0_5_queries_read_full_coordinate_series_before_applying_selection.md)
and [independent baseline](../devtools/data/modular_h5_query_baseline_643_20261107.json)
record a 5,000-structure primitive probe and eighteen failing standalone form
regressions on runtime bytes matching public `07f04d9e8`. The original source
and failed assertions are retained. A 120-byte stored reference snapshot is
not evidence of bounded I/O or peak RAM.

Correct the general H5MSM file/query route first, preserving schema, axes,
chemical context, units and lifetime contracts. Reuse its metadata, typed layer
readers, projected iterator and validated query delegation. The GUI continues
to call public MolSysMT tools; no GUI-only HDF5 reader or weakened window guard
is accepted. The prototype is not merged or source-accepted. Actual external
reference Jupyter/Mol*/popup receiving remains pending after provider repair.
The board has 575 issues, 97 open, through new #643; the preceding complete
acquisition had no open PR. Scope and the next remaining sequence/cell/task/
session families are unchanged.

Progress remains **approximately 61%**, **22/50 accepted graphical intents** and
**32 closed audit-related issues**. This is a required discovered prerequisite,
not bonus progress or a selected candidate. Installed/platform, contract,
human/Qt and final exact-artifact gates retain their independent requirements.

## Previous native diagnostic delivery — 2026-11-07

The native #640/#641 corrections are published on main at `49d1a720f` and
independently verified closed. Degeneracy now names
both the molecular-system structure index and selected-array position; shared
structural hints retain the reason and use conditional comparison advice for
all four SMonitor audiences. The
[receiving receipt](../devtools/data/native_structure_diagnostics_receiving_640_641_20261107.json)
records the final original-source baseline (60 diagnostic failures, two passing
invalid-scope controls), 701 integrated passes, one doctest and two actual
Jupyter scenarios (axes8/error-lifetime5). All fourteen fast controls and HTML
compilation pass; six existing underline warnings and baseline-matching page
errors remain visible. Four initial fixture/API/scope authoring attempts are
retained separately. No runtime API or scientific criterion was weakened.

Both owning records are archived with executable guards. All twenty changed/
deleted paths independently match the complete public Git tree. The
[delivery receipt](../devtools/data/native_structure_diagnostics_delivery_640_641_20261107.json)
records clean exact-source scientific execution (107 cases/68 nodes), verified
closures and the MolSysViewer #315 handoff (comment 6712967862). The last complete
board acquisition before these two closures has 574 issues, 98 open, through
#642, and no open PR. No newly numbered report changes the work order. Next is the accepted
#421 external-reference workflow, followed by sequence-derived fitting, cell
editing and the remaining task/session families. Native/expert external
references already exist; the current fit panel still fixes its reference to
the same molecular system, so expert availability does not close that GUI leaf.

Milestone progress remains **approximately 61%**, with **22/50 accepted graphical
intents** and **32 publicly closed audit-related issues** after this pair's
closeout. These two diagnostic repairs add no milestone bonus. The graphical
intent inventory has only 2.5 global weight points in the preserved hierarchical
formula; its counter is reported separately so small GUI deliveries stay visible.
Installed/public-host, contract, exact-candidate and human/Qt exits remain separate.
No new candidate, tag, Release or promotion is selected.

**Previous principal-axis checkpoint — 2026-11-07:** Align principal axes is
implemented and source-received on exact Viewer `e4dd58cf0`. The
[receiving record](../devtools/data/molsysviewer_tools_principal_axes_receiving_20261107.json)
passes **5,569 combined cases** and **seven actual Jupyter scenarios** (48
ordered steps): axes8, rejection5, System6, results7, Translate7, Center7,
Superpose8. Original failed test assumptions, unchanged registered source
inputs and baseline-matching page errors are retained. Native tensor/basis/
center validation, unit/rigidity truth, independent ownership, boxes/chemistry,
coverage and synchronization-only retry remain delegated unchanged.

#603 is source-received, archived and independently verified closed against
published source `96b73b3f3`. The [completion receipt](../devtools/data/molsysviewer_tools_principal_axes_completion_20261107.json)
records all 21 changed/deleted public paths and clean exact-source scientific
execution of 107 cases/68 nodes. All fourteen fast gates and HTML compilation
pass, with six retained underline warnings. Newly reported #640 and #641 own
native diagnostic index/context and vocabulary corrections; neither is hidden
inside the GUI. #642 now has a source-qualified evidence-catalog correction. Its owning
[report](archive/resolved_bugs/interactions_hdf5_readback_discards_evidence_catalog.md)
records 32 original failures/16 passing controls, 3,098 integrated passes,
eleven doctests and eight complete typed/two-analysis checks using the immutable
DockingMT carrier. The [receiving receipt](../devtools/data/interaction_evidence_catalog_receiving_642_20261107.json)
retains the exact input digests and historical failed outcomes. Complete catalogs,
codes, coverage and producer metadata survive standalone/full/layer/public
conversion routes under normal and pm/fs policies. Source `4d8af6c34` is published on main, all eighteen changed/deleted paths
independently match the complete public tree, and #642 is verified closed.
The [delivery receipt](../devtools/data/interaction_evidence_catalog_delivery_642_20261107.json)
records clean exact-source scientific execution (107 cases/68 nodes) and the
DockingMT #80 handoff (comment 6712753798). Continue with
#640/#641 messages and external-reference/sequence workflows,
cell editing and the other accepted families. The implementation is published
on main; these records retain its completed source receiving and pending exits.
No native scientific/Rust source or binary was changed by this GUI slice.

**Current audited implementation/source-delivery progress: approximately 61%.**
The [requirement-level scorecard](../devtools/data/pre_1_0_progress_scorecard_20261107.json)
recognizes verified partial milestones with the original six phase weights.
The [method and phase breakdown](#progress-estimate-for-the-authorized-execution)
explain the change from the retired 40% phase-exit count. This is a remeasurement
of delivered work; candidate/installed/platform/sign-off gates remain pending.
Audit-related source closures at that checkpoint were **30**. The last complete board acquisition
before closeout has 574 issues, 99 open, through #642; #642 is now independently
verified closed. Scope and publication authority are unchanged.

**Previous Rotate checkpoint — 2026-11-07:** the accepted #421 Geometry/Rotate
slice is implemented and locally received on exact Viewer `e4dd58cf0`.
Native axis-angle/rotation/center tools retain their scientific ownership;
the GUI adds explicit signed angular units and per-structure selection,
origin or fixed-point centers. The
[rotation receipt](../devtools/data/molsysviewer_tools_rotation_receiving_20261107.json)
records 5,091 addon cases, 551 overlapping directed/native/route cases and one
actual seven-step Jupyter/Mol*/popup guard. It preserves the test-only original
request-sequence failure and baseline-matching page errors. Source `c16b970a9`
is published on main and all seventeen changed paths match the complete public
tree. The [completion receipt](../devtools/data/molsysviewer_tools_rotation_completion_20261107.json)
records clean exact-source scientific execution (**107 cases/68 nodes**), all
fourteen fast gates, HTML compilation with six retained underline warnings and
preserved human edits. Human visual/Qt and installed/candidate gates remain
independent. The existing #334 remote full-suite recovery backlog is not waived. Accepted progress is **40%**; audit-related closures remain
**28**. The complete board remains 571 issues, 97 open, through #639.

**Next after this slice:** the other accepted #421 graphical families, beginning
with reference/principal-axis workflows and explicit cell editing. Property,
sequence, interaction/mechanics and complete scientific-session GUI remain in
scope. #524's actual public-host/installed gates remain separate. No release
candidate, tag, Release or promotion is selected.

**Previous delivery checkpoint — 2026-11-07:** contribution #543 is merged and verified
closed, with exact merge `0ddb99c2b` and public checkpoint `45e69bb10`.
#635/#639 are independently verified closed; all thirty changed paths match the
complete public tree. Audit-related closures are **28**, accepted phase progress
remains **40%**, and the latest complete board has 571 issues, 97 open, through
#639. Human source edits and immutable #632/#637 archives remain unchanged.

Owner receiving on exact Viewer `e4dd58cf0` passes **5,428 combined source
cases**, all four actual Jupyter scenarios together (**17/6/8/8** steps),
**107 molecular cases/68 nodes** with `--require-clean`, fourteen fast gates and
HTML compilation with six retained underline warnings. Source fingerprints
stay unchanged during receiving. Page errors match plain-Jupyter controls;
this does not establish causal repair of the original #615 observation. The
[source](../devtools/data/bound_tools_newer_host_source_receiving_635_639_20261107.json),
[completion](../devtools/data/bound_tools_newer_host_completion_receiving_635_639_20261107.json)
and [delivery](../devtools/data/bound_tools_newer_host_delivery_635_639_20261107.json)
receipts preserve the original failed smoke omission, expected route mutation,
exact source/backend identities and independent board/public verification.
Counts overlap; no installed/platform/human/candidate approval is inferred.
Earlier #602/#632/#633/#634/#636/#637/#638 deliveries remain in their receipts
and the dated progress log below.

**Previous next step (now implemented locally above):** Geometry/Rotate using
the delivered native constructor and its actual center/handedness/unit/selection
geometry and popup receiving. Principal-axis/
reference workflows, cell editing, further property/sequence/interaction/
mechanics and full scientific-session GUI retain their agreed scope. #524's
actual public-host/installed and exact final-candidate exits remain separate.
No candidate is selected and no family is dropped. Earlier checkpoints below
are dated history, superseded by this latest delivery where stated.

**Earlier execution checkpoints:** phases 1 and 2 are published/closed. Phase-two source
`3eb720444b97f77f9325acf52f55114ece0b5f9e` corrects #605/#607/#606/#608/#619;
independent public-file and closed-board receiving is recorded below. Joint
receiving passes 5,435 cases, final directed/documentation receiving passes
1,195, and the scientific certificate passes 97 cases across 64 nodes. These
scopes overlap. Accepted progress is 40%; #613 and #620 are published and closed.
The #620 precision correction and #524 default-renderer declaration are delivered
in public checkpoint `8d466268c`, with all 43 checked blobs independently matched. Remaining
#524 review and the actual Viewer floor still prevent phase-three credit.
No replacement candidate is selected. Public checkpoint `82bfa1c82` independently
matches all 58 checked blobs; #627/#628/#629 are verified closed, bringing the
audit-related closed count to 17. The MDAnalysis and ParmEd paired profiles pass
155 and 185 cases respectively without omissions; joint receiving passes 1,271
and scientific execution 97. Counts overlap. Existing phase weights are unchanged.

Current phase-three work closes the optional-provider review under #524.
Biopython's minimum/newer consumer profiles now each pass 385 without omissions;
OpenFF pairs each pass 86. PyTraj acquisition/engine/diagnostic/auditor receiving
passes 146. The revised floor profile retains actual auxiliary payloads rather
than dropping the original four failed/two skipped cases. New included-operation
NGLView defects #630/#631 are admitted: validation-keyword forwarding is locally
corrected in `e5d1dd0f8`; independent molecular widget state in HTML export is
being corrected and qualified. Their guards and provider boundary review add no
new method or progress weight. These optional profiles now qualify sources
`d850f6cc1`/`5cd744ebf` and corrections `e5d1dd0f8`/`fae9ab557`. Final OpenFF
profiles pass 199 and NGLView profiles 104 without omissions; joint receiving
passes 798, scientific execution 97/64 nodes and all 14 fast gates pass. HTML
compilation exits zero with four retained title-underline warnings. Source
delivery/board closeout and actual host/installed closure still prevent
phase-three credit. Public checkpoint `7e61fcc5c` now independently matches all
39 changed blobs; #630/#631 are verified closed. The audit-related closed count
is 19; accepted progress remains 40%. Optional-provider source review is
delivered, with the compatible public Viewer/clean installed exit still open.

Phase four now has isolated source merge `653ed8e0` over owner `030c201a5` and
PR #543 head `8ab2f5474`. Exact Viewer source `25061d9e9` passes import/API
preflight and **5,009 Python cases without failures or omissions**. The five
controlled workflows and dependency inventory now pin that received host. This
is separate-branch source receiving; actual Jupyter/popup, remaining graphical
families, installed and human acceptance remain due. The
[source receipt](../devtools/data/bound_tools_owner_source_receiving_20261107.json)
retains the limits. Accepted progress remains **40%** and no candidate is selected.

The subsequent #524 support-floor review qualifies the five retained required
providers and optional public Ackredit without changing their floors. Native
placement drops redundant deprecated sorting. A missed consumer of the phase-two
MIC signature is recorded as #621 and corrected locally in `2804f7954`; it adds
no weight or new method. Public checkpoint `ad6b71e97` independently matches all
14 checked source/record blobs, and #621 is verified closed. Accepted progress
stays 40%; remaining optional-provider and actual Viewer/installed closure remain.
The later MDTraj/NumPy and OpenMM checkpoints below supersede those parts of
the initial dependency-review queue.

The maintainer requests a durable record of the new audit, its reasoning, the
remaining work and the order in which to strengthen MolSysMT before 1.0.
Individual issues own their defects and acceptance criteria. This packet connects
them into bounded work blocks and records the evidence needed to advance.

The [release ledger](release_1_0_status.md) remains the authority for overall
execution, selected candidates and publication state. The
[scope decision](release_1_0_scope.md) governs admission, and the
[release gate](release_gate.md) owns mandatory qualification. This packet selects
no new candidate, changes no stability classification and authorizes no tag,
Release, artifact replacement or promotion. Preparing the record implements none
of its proposed runtime corrections.

## How to resume and maintain this packet

1. Read the current release ledger and the owning issue for the selected item.
2. Refresh its actual source, PR and receiving state. The audit snapshot below
   is dated evidence, not a live GitHub mirror.
3. Work in the sequence below unless a newly reproduced correctness or
   data-integrity defect warrants a documented change of order.
4. Keep correction details in the owning report. Update the affected work block
   here with the source commit, addressable guard, observed result and next exit.
5. Add one dated row to the progress log at a meaningful checkpoint, and update
   the release ledger with the resulting overall next step.

Do not overwrite the dated findings or old unsuccessful results when a fix
arrives. Append a dated correction if an audit statement was wrong. Record
source implementation, local qualification, consumer receiving, publication and
issue closure separately. A passing local case does not complete an installed
pair or final-candidate gate. Do not derive a release percentage from issue
counts, test counts or the historical weighted campaign.

Each correction checkpoint records its implementation and published-source
commits, an addressable regression, the executed result, remaining dependencies
and consumer acceptance when applicable. The portable receipt preserves audit
observations; a cached probe is not a maintained regression. Promote its minimal
counterexample into the owning test suite when implementing the correction.

The earlier fifteen-issue goal through #601 is complete. Its archived evidence
remains intact; this is a subsequent audit and work sequence.

## Dated audit: scope, evidence and limits

This was a directed maintainer review of architecture, critical native
composition, periodic geometry, configuration, persistence, scientific evidence,
dependency contracts, public documentation and the complete issue/PR inventory.
It was not a line-by-line inspection of every module, independent external
certification, full platform matrix or clean installed-artifact qualification.

The [portable audit receipt](../devtools/data/pre_1_0_robustness_audit_20261106.json)
retains the source identity, selected observations, scientific certificate,
test-result identities and evidence limits. Original local acquisitions and
logs are under `.pytest_cache/pre1-review-20261106/`; their digests are recorded
in the receipt. They are local evidence, not published attachments. No raw
GitHub inventory or unrestricted log is required to interpret the findings here.

| Observation at the audit checkpoint | Evidence and scope |
| --- | --- |
| Complete initial board | Seven paginated issue pages: 549 issues, 103 open, excluding PR entries. One open PR, #543. |
| New defect recorded | #618 was opened after independent reproduction and a search of the complete inventory. A fresh two-page open inventory then contains 104 issues and one PR. These counts describe that capture only. |
| Registered scientific execution | 83 cases pass for 61 registered nodes, with zero failures, errors or skips. The executor deliberately runs serially. |
| Addition and alternate-location receiving | 51 cases pass under 12 workers, including the exact #612 selector. The new #618 counterexample is outside those existing assertions. |
| Board acquisition regression | All five pagination controls pass under 12 workers; old issues beyond the former limit remain visible. |
| Conversion execution plan | Static audit of `resident-files-v12`: 220 of 620 declared edges are selected; 400 remain explicit debt outside that profile; zero plan errors. This audit does not execute those edges. |
| Main CI | Smoke 42295589104 succeeds at the audited source. Its four other ordinary push checks also succeeded at receiving. This is not the release matrix. |
| PR #543 | Reviewed head `8ab2f5474b2e04c68d31ef2854a238984b645fc8`: 99 changed files, 14,970 additions and 531 deletions. GitHub reports conflicts; its smoke succeeds. Full run 42291734556 remains pending at inspection, with four Linux jobs active and four macOS jobs queued. |

Execution uses the existing Linux/Python 3.14.7 development environment and
published Pytest Receptor 1.2.1. The existing controlled Viewer source is
`42234de839ed047016f8f241ea5eb717cfeb07be`; that development input does not
qualify the different Viewer source in PR #543. GH Run Receptor 1.1.1 supplies
the first full-run inspection, with native GitHub facts used for subsequent
status updates. No environment or dependency was installed or replaced.

Four pre-existing human autosummary edits remain unchanged. The scientific
certificate therefore correctly records `tracked_source_dirty=true` and
`release_eligible=false`. The unchanged native extension has SHA-256
`f32ed73f7ef3cf3225e12fbc56b9c4236a4452d758c94661f41860ad00d82c1c`.
Passed development checks must not be described as a clean release certificate.

The first scientific-executor invocation incorrectly supplied xdist options to
its intentionally serial runner. It executes zero tests and produces a usage
failure. That original certificate/log is retained separately; the corrected
invocation supplies the 83-case result above. Test durations are not benchmarks.

### Architectural assessment

The architecture is a sound basis for 1.0:

- Stable inventory, chemical assignments/connectivity, structures and calculated
  interactions have explicit, independent owners.
- Form-agnostic entry points and direct native queries share contracts while
  serving different interoperability and repeated-query workloads.
- Sparse interaction relations/occurrences, compound participants, coverage,
  provenance, source maps and typed H5MSM persistence are appropriate foundations.
- ArgDigest, DepDigest, SMonitor, PyUnitWizard and optional Ackredit have clear
  responsibilities. Their actual behavior at a boundary still needs testing;
  decorators and passing static validators are not scientific evidence.

The immediate improvement is stronger composition and numerical guarantees for
existing operations. Preserve these owners while correcting the failures below.
Additional Rust work requires a measured need; an index-map or metadata defect
does not become a kernel-performance problem merely because it affects a large
system.

### Completeness review and evidence boundaries — 2026-11-06

This is a sufficiently broad stabilization plan for the accepted release scope,
not an exhaustive scientific audit of MolSysMT. Its strongest evidence concerns
native composition, persistence continuity and the reproduced periodic defects.
Architecture inspection and registered-test execution do not establish equivalent
depth across every domain. Use this map to identify the remaining review instead
of interpreting an overall passing count as library-wide certification.

| Domain | Evidence available to this packet | Remaining acceptance boundary |
| --- | --- | --- |
| Native inventory, chemistry and composition | Independent selected-add and recovered-append counterexamples; published phase-one guards and receipt. | Receive affected consumer workflows and the exact installed candidate. Preserve partial-domain, state-association and failure-atomicity contracts. |
| Structure and periodic geometry | Governed analytic/external controls and directed rotated/changing-cell/unit regressions; phase-two source is still local. | Complete combined receiving and publication. Numerical conditioning, exact-boundary equivalence and the temporal sampling assumption must remain explicit. |
| Interactions | Sparse container, query, coverage, occurrence identity and persistence contracts; existing detector and curated tests. | Under #250/#254, assess container reliability separately from each offered method's scientific claim, chemical scope, parameters, units, provenance and periodic conventions. Existing tests are not absent merely because a method is outside the governed registry. |
| Physicochemical and secondary-structure observables | The generated [scientific evidence matrix](scientific_evidence_matrix.md) identifies bounded reference evidence and remaining gaps. | #473/#475 retain their scientific dispositions. The registered secondary-structure assignment gap must also remain visible: backend agreement/vocabulary checks do not independently validate assignment accuracy. This review does not admit a new predictor. |
| Forms, parsers and H5MSM | Declared conversion-profile audit, phase-one persistence receiving and existing schema/version rejection tests. | Execute the affected supported routes, quantity/map preservation and negative persistence controls on the combined source. A declared edge or one successful round trip is not universal format coverage. |
| Configuration and dependencies | Reproduced #613 leak, installed-runtime evidence under #524 and published dependency contracts. | Qualify actual decorated concurrent calls and a minimal installed dependency closure. Editable siblings and successful dependency metadata checks cannot substitute for either. |
| Mechanics and preparation | Existing bounded engine/preparation recipes, explicit experimental scope and earlier receiving. | #582 must distinguish requested/effective controls. Preserve unsupported chemistry, state and correspondence outcomes; no general force-field or preparation accuracy claim follows. |
| Viewer and distribution | Contribution/source inspection and historical host/artifact evidence. | Receive the agreed workflows against exact combined sources, then qualify exact artifacts through the existing release gate. Rendering, sessions, package installation and scientific accuracy are distinct conclusions. |

The generated registry remains the authority for scientific classifications;
this table does not create a second symbol inventory or change API stability.
For the nine offered interaction families, reuse the existing method profiles,
curated fixtures and attribution records during #250 acceptance. Record which
claims have independent evidence, which have provider/contract parity only,
and which remain explicitly unqualified. Resolve misleading public claims before
qualification; broader scientific benchmarking remains separately scoped.

Two execution details need stronger controls:

- **Finite graphical acceptance:** before phase-four receiving, pin the agreed
  #421 workflow inventory and named Viewer source. For each accepted workflow,
  identify its expert/notebook/popup modes, owner, numerical expectation and
  observable completion or rejection. Record exclusions and their reasons. Use
  the existing catalogue/design and receiving tools; neither add a GUI for every
  expert operation nor silently reduce the agreed set to obtain a green result.
- **Observed test completion:** a receiving record needs the exact command,
  source/backend identity, expected selection, actual collected/executed scope,
  native process exit and result artifact. At this review, the original local
  `phase2-integrated.xml` contains zero tests and supplies no successful combined
  receiving evidence. Investigate its command/collection outcome before crediting
  that exit. A zero-failure XML file, missing terminal output or a lost process
  handle cannot establish success. Do not repeat a still-running suite merely
  because its observation was interrupted.

These are acceptance and traceability improvements under #334, not permission
for another implementation expansion. The immediate order remains finishing
phase two, then #613 and the independently actionable portion of #524. Host
coordination and already-satisfied issue closeout may proceed alongside that
work. Keep the qualified Viewer-floor dependency explicit until its actual
artifact exists.

### Reproduced defects on the audited source

| Issue | Observation | Consequence |
| --- | --- | --- |
| [#618](https://github.com/uibcdf/molsysmt/issues/618) | Adding a three-atom source to a one-atom target with `selection=[2,0]` yields names `[L0,R0,R2]`, x coordinates `[0,2,0]` nm and formal charges `[0,2,0]`. The three-atom result retains four mechanics rows. | Coordinates/assignments can refer to different atoms from the stable inventory, and the mechanics axis is inconsistent. |
| [#616](https://github.com/uibcdf/molsysmt/issues/616) | A fresh 3,818-atom TcTIM control accepts an additional structure. Its H5MSM-recovered counterpart rejects the same source. Component names/types change from object-backed strings to canonical nullable strings. | Persistence changes compatibility despite equivalent represented chemical fields. Rejection remains atomic in this probe. |
| [#605](https://github.com/uibcdf/molsysmt/issues/605) | The box factory accepts zero/negative lengths; `[10,10,170]` degrees produces nonfinite cell entries. | Invalid physical cells reach downstream periodic consumers. |
| [#607](https://github.com/uibcdf/molsysmt/issues/607) | For row vectors `[[0,3,0],[-4,0,0],[0,0,5]]` nm and position `[5,6,7]` nm, both wrapping routes return `[5,6,2]` nm. Primary and nearest images are respectively `[-3,0,2]` and `[1,0,2]` nm. | Geometric orthogonality is incorrectly treated as Cartesian alignment. |
| [#606](https://github.com/uibcdf/molsysmt/issues/606) | An orthogonal-to-triclinic sequence unwraps the final atom to `[-1.1,-0.2,0]` nm instead of the independent lattice result `[-0.1,-0.2,0]`. | The first cell's classification is reused after the cell changes. |
| [#608](https://github.com/uibcdf/molsysmt/issues/608) | An origin of `[1e-5,0,0]` nm gives x=0 under nm/angstrom policies and x=3 nm under pm policy. | A numerical near-zero threshold changes the physical image with application units. |
| [#613](https://github.com/uibcdf/molsysmt/issues/613) | Deterministically overlapping contexts start with GPU aliases `('auto','auto')` and finish at `(False,False)`. | Temporary configuration leaks into the application after both contexts exit. This probe evaluates no GPU calculation. |

For #618, `native/molsys.py` passes the original selected indices to several
owners. `Topology.add()` extracts/sorts the inventory, structures and chemical
union retain the original order, and mechanics receives the full source.
Matching cardinalities alone cannot protect identity. Bioassembly chain
references need review under the same selected-source correction; no separate
bioassembly failure was executed in this audit.

For periodic operations, `rust/src/pbc.rs` retains assumptions distinct from
the general reduced-cell machinery in `rust/src/mic.rs`. Review reuse of the
existing primitives and their applicable conventions. Do not copy another
unqualified wrapping formula into a consumer or private parallel implementation.

### Other important findings

- **Installation (#524):** default `basic.info()` and native `.info()` use pandas
  Styler, but the declared runtime does not require Jinja2. The issue retains
  installed receiving that fails despite a successful dependency check. Resolve
  the dependency/output contract, actual public Viewer floor and justified
  provider restrictions without guessing versions or hiding optional-tool
  conflicts. Existing core-floor work is already delivered.
- **Closeout candidates:** the exact #612 test now passes and protects atomic
  stable-ID rejection, explicit valid resolution and PDB persistence. #587's
  paginated implementation and transport guards also pass. Reconcile their
  remaining owning acceptance before closure; do not reimplement corrected code.
- **Naming (#549):** implementation and extensive source evidence exist. Remaining
  producer/composite, consumer and final-candidate receiving must be distinguished
  from the original vocabulary defect.
- **Documentation (#378):** README still calls
  `msm.topology.get_dihedral_quartets`; the supported owner is `chemical_states`.
  The long release ledger also contains historical resume instructions that need
  a clearly identified current route. This does not authorize rewriting archived
  evidence or requiring a complete documentation redesign.
- **Scientific meaning (#473/#475):** the surface-area convention is explicitly
  provisional; Collantes ECI dimension/aggregation remain unqualified. Typed
  units and regression parity do not establish the original scientific meaning.
- **Mechanics (#582):** distinguish stored requests from controls applied by an
  engine. The bounded standard recipes do not certify arbitrary stored tuning.
- **Public XYZ use (#610):** explicit atom-level querying and direct quantity
  assignment already have receiving. Settle the omitted-element diagnostic and
  documentation before proposing another coordinate API.

## Action plan and initial progress

The following order is the proposed implementation route recorded at the
maintainer's request. Individual API/scientific decisions still require their
owning review. Existing admission and publication rules remain unchanged.

The phases express priority and acceptance dependencies, not an obligation to
serialize unrelated work. #612/#587 closeout can proceed at an earlier checkpoint
once its criteria are met. UI receiving fixes can advance independently of a
native scientific correction, while keeping affected GUI modes bounded. The
public Viewer floor in phase 3 depends on the host decision/receiving in phase 4
and artifact delivery in phase 6: retain that named dependency rather than
inventing a published version or treating the whole dependency review as done.

### Release relevance and responsibility

| Work class | Reports | Required disposition and owner |
| --- | --- | --- |
| Demonstrated correctness within included behavior | #618, #616, #605–#608, #613, subsequent #619/#620/#621/#622/#623/#625/#626/#627/#628/#629 | Correct the reproduced behavior and retain valid positive controls in the native, PBC or configuration owner. An experimental label does not excuse incorrect atom correspondence or numerical results. |
| Declared installed runtime | #524 | MolSysMT owns its manifests, default-output contract and installed receiving. A Viewer minimum depends on an actual qualified host artifact; provider limitations stay with their providers. |
| Public scientific meaning | #473, #475, #582 | Review the exposed claim and evidence. Correct a misleading contract or agree an explicit bounded disposition; an unavailable paper does not justify invented units, and a stored request must not be advertised as an effective engine control. Wider models or tuning are not automatically required. |
| Implemented contracts awaiting acceptance | #549, #250, #254 | Complete the remaining owning criteria and final-candidate/client receiving. Source delivery, scientific validation and public stability are separate decisions. |
| Accepted bound-tool workflows | #421, PR #543 and linked host reports | MolSysMT owns the bound scientific adapters; Viewer owns rendering, presentation, navigation authority and sessions. Receive their agreed workflow inventory together. Source-path exposure alone does not complete graphical or scientific acceptance. |
| Already corrected behavior | #612, #587 | Reconcile the addressable guard and remaining owning criteria, then close promptly. Do not hold an otherwise completed bug open solely until release. |
| Remaining extensions | Follow-up table below | Keep the remaining scope deferred unless the maintainer admits it or an included-workflow defect is demonstrated. An open issue is not evidence that its delivered subset is absent. |

Labels and milestones aid navigation; they do not determine correctness or
readiness. The refreshed open inventory still has 104 issues and one PR. Only
#549, #334, #254 and #250 have the exact `1.0.0` milestone at this review; the
newly reproduced bugs still require disposition under the admission rule.
Refresh these dated facts before relying on them at a later checkpoint.

### Progress estimate for the authorized execution

The maintainer now authorizes execution and requests periodic percentages.
Use the planning weights below for this new work only, starting at **0%** on
2026-11-06. They are estimates of work distribution, not measurements of library
quality, elapsed time, scientific coverage or readiness to publish. Earlier
completed campaigns retain their results and are not reset by this baseline.

| Block | Planning weight | Completed contribution at execution start |
| --- | ---: | ---: |
| Phase 1: selected composition and recovered append | 20% | 0% |
| Phase 2: periodic construction, images, continuity and units | 20% | 0% |
| Phase 3: configuration and installed-runtime closure | 10% | 0% |
| Phase 4: addon integration and required graphical receiving | 25% | 0% |
| Phase 5: contract closeout and scientific/public claims | 10% | 0% |
| Phase 6: exact candidate, required qualification and publication decision | 15% | 0% |

**Current operational measure — 2026-11-07: approximately 61%.**
The maintainer correctly identified that the former all-or-nothing measure
kept reporting 40% while phases 3 and 4 delivered substantial accepted source
work. The [milestone scorecard](../devtools/data/pre_1_0_progress_scorecard_20261107.json)
now owns the detailed requirement tree, acceptance evidence and arithmetic.
The six weights above remain **20/20/10/25/10/15**. Scope, scientific criteria
and mandatory publication gates are unchanged. This is an accounting correction
that recognizes earlier delivered work, not 21 newly implemented points in this
turn. The catch-up result was about 60.99; external-reference delivery now gives
about 61.05. Report it as **approximately 61%**
to avoid implying an effort estimate with decimal precision.

| Phase | Preserved weight | Verified milestone credit | Main remaining exit |
| --- | ---: | ---: | --- |
| 1 | 20 | 20.0 | Closed native corrections; retain guards. |
| 2 | 20 | 20.0 | Closed numerical corrections; retain guards. |
| 3 | 10 | 6.7 | Actual public Viewer floor and clean installed closure. |
| 4 | 25 | 14.4 | Remaining GUI/reference/cell/property/session families and owning acceptance. |
| 5 | 10 | 0.0 | Requirement-level contract/scientific-claim closeout. |
| 6 | 15 | 0.0 | Exact candidate, artifacts, mandatory gates and publication authorization. |

Credit verified leaves, not entire unfinished phases. Within a phase, the named
requirement packages have equal shares; nested GUI families have equal family
shares and explicit intent/task leaves within that family. A verified-source
leaf scores one, a pending leaf zero; parent values average their children.
For example, phase 3 receives two of three packages (configuration/precision
and non-Viewer provider-contract receiving); actual installed/public-Viewer
closure remains zero. Phase 4 receives integration, delivered native/endpoint
prerequisites and actual navigation truth, plus qualified portions of outcomes
and the explicit graphical inventory. Complete source tasks do not claim that
an entire family or publication exit is satisfied.

The scorecard makes the accepted GUI intents finite and reviewable. It does
not require a field for every expert argument, invent another scientific
algorithm or silently omit external references, sequence matching, broader
periodic/cell handling, preparation/assignments/construction, remaining
observables/mechanics or a complete scientific session. Source qualification
and pending human/installed acceptance stay separate. A pending leaf can have
existing code: it has not yet met this audit's requirement-level acceptance.
In particular, phase 5 receives no credit merely because older implementation
exists; its closeout and scientific-claim review still needs completion.

Every credited source package links its relevant executed receiving and public
source evidence. File existence, a green unrelated gate, raw test counts or
issue counts are insufficient. Supplemental bugs add no bonus; if new evidence
invalidates a credited claim, reopen its affected leaf until corrected. #640/
#641 retain their required native diagnostic dispositions. This planning index
is neither a scientific quality/coverage measure, a time prediction nor a
probability of publication readiness. Phase 6 remains zero, and the existing
publication pause and exact-artifact gates remain fully applicable.

### Reporting progress during execution

This percentage describes this audit's accepted work packages, not the fraction
of the entire MolSysMT library implemented or an estimate of remaining hours.
At each delivery checkpoint, report separately (1) newly accepted milestone
leaves and their weighted change, (2) supplemental correctness repairs delivered,
and (3) pending acceptance owned locally or by another component. Name the next
finite package. A supplemental repair can remove a real release risk while
leaving this milestone percentage unchanged. Do not count more tests, repeated
checks or metadata closeout as extra implementation. Phases 5 and 6 retain 25
points of genuinely pending work; source fixes do not silently receive those
contract/candidate/publication points. Prefer relevant affected checks and reuse
valid evidence; broaden a passing campaign only for a new change, failure or
unresolved concern.

To reproduce the arithmetic from the canonical snapshot:

```python
import json
from fractions import Fraction

with open('devtools/data/pre_1_0_progress_scorecard_20261107.json') as stream:
    scorecard = json.load(stream)

def fraction(item):
    if 'children' in item:
        return sum((fraction(child) for child in item['children']), Fraction()) / len(item['children'])
    return Fraction(item['state'] == 'verified_source')

points = sum((phase['weight'] * fraction(phase) for phase in scorecard['phases']), Fraction())
print(f'Approximately {round(float(points))}%')
```

**Preserved legacy phase-exit baseline:** the former 40% credited the two
phase-one corrections at ten points each and the four phase-two numerical
milestones at five points each. #619 shares #608's unit-invariance milestone
without adding weight. The [phase-two delivery](../devtools/data/pre_1_0_robustness_phase2_delivery_20261106.json)
retains all 27 verified public blobs and five closed issues. Subsequent dated
40% observations below remain historical evidence under that retired accounting
rule. The release ledger links this current measure rather than maintaining
an independent progress definition. Update the scorecard and this derived
snapshot together when accepting another milestone; retain its original
source/guard and any resulting remeasurement rationale.

### Phase 1 — Native composition and persistence continuity

**Initial position:** both defects reproduced; corrections not yet implemented
under this packet. **Order:** #618, then #616.

| Work | Required outcome and acceptance evidence |
| --- | --- |
| #618 selected addition | Choose one canonical selected-source map consistent with native extraction semantics, including the existing repeated-index policy. Apply it to inventory, coordinates and structural fields, chemical assignments, bonds/components, mechanics and relevant assembly references. Cover reversed/nonconsecutive, empty and full selections, both in-place modes and relevant form routes. Compare actual identities and values; retain source independence, explicit unsupported-state policies and atomic rejection. Do not impose global sorting on unrelated queries to hide this mismatch. |
| #616 recovered inventory | Resolve canonical storage versus semantic inventory equality in the owner. Cover compatible null/string representations and optional fields, full input preservation and structure/state associations. Keep rejection of real differences in bonds, assignments, state/reference ordering, completeness and correspondence; do not reduce compatibility to counts or names. |

**Exit:** public compositions preserve all represented axes, and continued work
after H5MSM recovery behaves consistently with the qualified native control.

**Execution checkpoint — 2026-11-06:** the selected-add and recovered-append
corrections are implemented in `19d6d55c1663bf3c6c7adfb9433fc775326292b5`.
The final joint native/composition/H5MSM/named-interaction selection passes
2,748 cases, with zero failures/errors/skips. The separate expanded
string/append/doctest selection passes 40 cases. These profiles overlap.
Ruff, dependency and course checks pass; original failures and 746 final-profile
warnings remain recorded. See the
[#618 closeout](archive/resolved_bugs/native_add_misaligns_selected_atom_domains.md),
[#616 closeout](archive/resolved_bugs/h5msm_component_dtype_append_rejection.md)
and [phase-one receipt](../devtools/data/pre_1_0_robustness_phase1_receiving_20261106.json).
Source publication/board closure must follow actual origin verification. This
source receiving does not complete platform/installed-pair/release gates.

The #616 record receives and preserves PR #543's existing consumer report.
During integration, retain this resolved record and its native guard rather
than reintroducing that PR's pending copy as a second active report.

### Phase 2 — Periodic geometry and unit invariance

**Initial position:** all four reports reproduced; correction receiving pending.
**Order:** #605, #607, #606, #608, with shared geometry reviewed together.

| Work | Required outcome and acceptance evidence |
| --- | --- |
| #605 cell construction | Validate finite positive lengths and physically meaningful, mutually compatible angle triples. Verify finite nonsingular output under the documented rounding convention, with a unit-invariant degeneracy/conditioning policy. Preserve valid orthogonal/triclinic, shared/per-structure angles, units and supported empty axes. Review the other public cell factory; keep arbitrary raw-vector conventions separate. |
| #607 oriented bases | Correct general admitted row-vector bases. Exercise primary, centered and MIC routes, compound and isolated selections, origin translations, canonical/rotated/skewed cells and both in-place modes against independent lattice truth. Narrowing an existing supported geometry requires a separate reviewed contract decision; rejecting all rotated cells is not equivalent to repairing this defect. |
| #606 temporal continuity | Define the previous/current transition-cell convention. Classify and apply the actual transition cell. Cover both classification changes, changing lengths, explicit structure traversal/order and atomicity. Document the sampling assumption: nearest-image continuity cannot uniquely recover physical winding after an undersampled large jump. Keep temporal continuity distinct from within-structure reconstruction. |
| #608 physical origins | Preserve explicit reference quantities without an application-dependent zero replacement. Cover exact zero, small signed origins, boundary positions, nm/angstrom/pm policies and input-unit variants across applicable wrapping routes. |
| Subsequent #619 raw-cell admission | Remove the dimensional determinant cutoff without bypassing genuine singularity, finite/shape/count or handedness conventions. Cover ordinary and small cells under nm/angstrom/pm/m application policies. Its separate mechanism and report share #608's five-point unit-invariance milestone; do not award additional progress weight. |

**Exit:** independent lattice/image controls pass, presentation units preserve
physical results, and unsupported geometry fails before molecular publication.
Include rotated and changing-cell cases in governed scientific evidence where
they protect a declared claim; retain existing valid analytic cases.

**Execution checkpoint — 2026-11-06:** #605 is corrected locally, with 430
PBC/scientific cases passing after 49 original guard failures. Its
[owning report](archive/resolved_bugs/box_factory_physical_domain.md) records the shared
physical-domain checks, unchanged numerical kernels and post-rounding policy.
Finish doctest/governance and public source receiving before crediting its five
percentage points. #607/#606/#608 remain uncorrected under this packet.

**Subsequent local checkpoint — 2026-11-06:** #605/#607/#606/#608 and
[#619](archive/resolved_bugs/periodic_box_nonsingularity_uses_a_dimensional_volume_threshold.md)
now have local implementations and directed receiving. The expanded PBC profile
passes 692 cases; the native backend was deliberately rebuilt for the general
cell/temporal corrections. The audit's original backend identity above remains
historical, not the identity of this subsequent execution. The working tree is
not a release candidate. Complete the combined receiving and portable receipt,
retain failed numerical-boundary attempts and their scientific interpretation,
then publish/verify the source and synchronize the five owning reports. Do not
infer that broader receiving passed from the zero-test integrated XML noted in
the completeness review. Accepted progress remains 20% until these exits hold.

**Final local source checkpoint — 2026-11-06:** implementation
`3eb720444b97f77f9325acf52f55114ece0b5f9e` passes 5,435 joint cases and
1,195 final PBC/docstring/documentation/evidence-runner cases. The latter receives
the final strengthened fixtures for both actual classification changes and
both nonconsecutive traversal orders. The scientific registry now includes
literal rotated images, changing-cell displacements and small-origin results
under non-default application units: **97 cases across 64 nodes pass**, with
zero failures/errors/skips. All 82 Rust unit tests pass. Counts overlap.
The [phase-two receipt](../devtools/data/pre_1_0_robustness_phase2_receiving_20261106.json)
binds source/backend identities, commands, native exits, original failed and
unobserved attempts, warnings and receiving chronology. The original zero-test
run selected a nonexistent directory; a controlled diagnostic exits 4 and the
corrected-path integrated run exits 0. This repairs the evidence gap, without
retroactively declaring the original run successful. Public delivery/issue
closeout is next; installed/platform, Viewer and exact-release gates remain due.

**Public closeout — 2026-11-06:** checkpoint
`27bc4d3c5ce67235d07c68f4a195b727a176eefd` publishes the implementation and
receiving record. Independent GitHub retrieval matches all 26 implementation/
test/documentation blobs and the receiving JSON. #605/#607/#606/#608/#619 are
independently verified closed with the public source commit and their owning
regressions. Phase 2 now contributes its original 20 points: total **40%**.
Installed/platform, graphical and final-candidate obligations remain due.

### Phase 3 — Configuration authority and installed runtime

**Initial position:** #613 reproduced; #524 remains partially implemented.

**Current receiving decision:** #613 source contradicts the existing
process-global writer-serialization contract in
[performance guidance](performance_and_jit.md#cpu-parallel-execution).
Restore that accepted owner contract: reentrant serialization for the full
context lifetime, atomic key/alias validation and restoration on exceptions.
Keep the separate CPU per-call ContextVar authority and no-override concurrency.
An unrelated observer can see temporary process-global values; neither the
correction nor the documentation may promise thread/task-local isolation or
protection from unsynchronized direct assignments. Verify this documented
limitation alongside the behavior rather than silently redesigning configuration.
Actual implementation and receiving remain pending at this checkpoint.

**Subsequent local execution:** #613 now has owner code and maintained guards;
first corrected receiving passes 25 cases, including the same cases on controlled
source from public ArgDigest 0.14.0. The implementation uses its supported
key-domain contract without adopting a newer provider API or raising a floor.
The independent public-call probe also discovers
[#620](archive/resolved_bugs/rust_cpu_kernel_inputs_follow_an_unsupported_single_precision_setting.md):
the global single-precision request sends float32 inputs to float64-only CPU
bindings. This serially reproduced boundary defect needs disposition within
phase 3 after #613; it does not require another precision backend or additional
progress weight. Final broader receiving and source closeout remain pending.

**Final #613 source checkpoint:** implementation
`f60e25b7edad28f035429563fd8b46f4d93395f2` passes 4,438 integrated cases,
32 final source-floor/docstring cases, 500 documentation cases and the
97-case/64-node scientific certificate, all without failures/errors/skips.
Counts overlap. The [owning closeout](archive/resolved_bugs/concurrent_configuration_contexts_leak_gpu_policy.md)
and [receipt](../devtools/data/configuration_serialization_receiving_613_20261106.json)
preserve original authoring/runtime failures, domain-bootstrap correction,
actual source-floor limits and unchanged environment/backend. Public delivery
and board closure follow. #620 and #524 remain unresolved; this checkpoint
does not yet credit phase 3 or raise accepted progress above 40%.

**#613 public closeout:** checkpoint
`1b1cc42e0c88de0df507e02f9349658e223369ef` publishes the implementation and
records. All 12 checked implementation/receipt/report blobs independently match
GitHub, and #613 is verified closed with its regression and source commit. The
[delivery receipt](../devtools/data/configuration_serialization_delivery_613_20261106.json)
also records all four ordinary workflows successful at the earlier PBC head
`16ecaae01`. These results do not qualify the new configuration source or an
installed candidate; finish this source block with its own unskipped head.
Next: #620 precision-boundary disposition and #524 installed-runtime closure.
Phase-three credit remains pending and total accepted progress remains 40%.

**Precision and default renderer qualified locally:** #620 implementation
`cb07e54af2a9be545b36d3fe8c64de34e0a0b132` preserves supported single-coordinate
publication while retaining float64 CPU working values and emitting the typed
`MSM-WARN-PRECISION-001` diagnostic. #524 implementation
`44fd0acf0788f1c9d06fe2a3a7446ad52c9e2550` declares Jinja2 >=3.1.2 because
default public/native `info()` consumes the supported Pandas renderer. Joint
receiving passes 4,592 cases, documentation/public doctests 599, directed
precision 39, and registered scientific execution 97 across 64 nodes. The
renderer also has 35 exact-Jinja2-minimum cases and seven isolated actual API/ABI
probes with selected provider minima on existing Python 3.11. Scopes overlap.
The [precision receipt](../devtools/data/native_precision_receiving_620_20261106.json)
and [renderer receipt](../devtools/data/runtime_renderer_receiving_524_20261106.json)
retain source/backend identities, commands, original failures, warnings,
unchanged notebook code/outputs and source-versus-installed limits.

Public delivery and #620 closure follow independent source verification.
#524 stays partial: suite/optional-provider APIs, NumPy restriction disposition,
actual public Viewer acquisition/floor and installed closure remain explicit.
Do not guess a Viewer minimum from a controlled source SHA; the last observed
GitHub Release is still 0.24.0. Own the independent review while preserving the
host dependency and later graphical/installed receiving.

The maintainer renews the working-commit policy under #334: every development
commit uses `[skip ci]`, pushes are batched and remote execution is reserved
for agreed qualification checkpoints. Root AGENTS.md records it. This direction
supersedes the automatic unskipped-head next step in the preceding dated
checkpoint, without waiving any final exact-candidate gate. Existing #613 smoke
42314744961 at `60ded0f7c` now concludes successfully; it does not qualify these
new sources. Accepted plan progress remains **40%** until phase 3 reaches its exit.

**Public precision closeout and partial renderer delivery:** checkpoint
`8d466268c3750aafe3fb1eac19fa03f1dc6df144` publishes both corrections and their
records. Independent GitHub retrieval matches all 43 checked blobs, and #620 is
independently verified closed as completed. All fourteen final fast gates and
the regenerated queue-index check pass; the initial stale-index failure remains
in the receipt. The [delivery record](../devtools/data/precision_renderer_delivery_620_20261106.json)
preserves this public receiving separately from scientific/platform/installed
qualification. #524 remains partial and is the next independent review. Accepted
progress stays **40%**; no new remote workflow, candidate or publication is selected.

The complete boundary inventory now contains 552 issues, 97 open, and the one
open PR #543 at the unchanged `8ab2f5474b2e04c68d31ef2854a238984b645fc8`.
There is no newly numbered issue after #620 in this acquisition. The delivery
record retains the inventory digest and selected observations; no new report
changes the #524 next step.

**Support floors and preparation receiving:** the retained public PyUnitWizard
0.28.1, mmCIF 1.1.1, ArgDigest 0.14.0, DepDigest 0.15.1 and SMonitor 0.16.0
payloads match independent Anaconda main-channel identities. Source receiving
passes 581 cases, with 14 explicit optional ownership-study omissions at the
older ArgDigest floor; a separate 133-case CCD/preparation/doctest profile has
no omissions. Public Ackredit 0.9.0 is imported from a separately verified
archive; its 62 Python files also match the older local-build cache despite
different archive hashes. Do not confuse source parity with canonical artifact
identity or the source floor profile with installed-runtime qualification.

The #524 placement correction `4f8b03364` removes duplicate build-level bond
normalization in favor of the existing ChemicalStates setter. Six warning-strict
public native/dictionary controls cover two structures and old atom/bond/coordinate
preservation. Combined exact-Pandas-3.1.0 receiving passes 965 cases; thirteen
additional owner/placement controls pass without warnings. The original failed
attempts remain in the [support-floor receipt](../devtools/data/runtime_support_floor_receiving_524_20261106.json).

The broader selection also reveals a missed phase-two consumer signature:
[#621](archive/resolved_bugs/periodic_fixed_state_hydrogen_addition_calls_a_retired_mic_helper_signature.md)
breaks fixed-state H preparation with a periodic box. Source `2804f7954` updates
that caller without a new geometry formula, backend or private compatibility
shim. Three existing failures and twelve new rotated/skewed compact/split unit
controls protect it. Directed receiving passes 60 cases, affected documentation
543, and scientific execution 97 across 64 nodes. These scopes overlap the
combined/provider selections. The [#621 receipt](../devtools/data/periodic_fixed_state_hydrogens_receiving_621_20261106.json)
retains exact source/backend identities and unchanged course code/outputs.
Public delivery and closure follow. Remaining optional-provider, NumPy-bound,
actual Viewer and installed-runtime work still prevents phase-three credit.

**Public preparation closeout:** checkpoint
`ad6b71e97626e01f67197b76f34cd6a031abe916` delivers the #621 correction and
#524 placement/support-floor records. Independent GitHub retrieval matches all
14 checked blobs; #621 is independently verified closed as completed. All
fourteen fast gates pass. The [delivery receipt](../devtools/data/support_preparation_delivery_621_20261106.json)
keeps this separate from installed/graphical/platform qualification. A fresh
complete inventory contains 553 issues, 97 open, and the unchanged PR #543 head;
no newly numbered issue after #621 changes the next work. Continue the remaining
#524 optional-provider and NumPy review while preserving the actual host/artifact
dependencies. Accepted progress remains **40%**, without extra regression points.

**Native extraction counterexample during optional receiving:** #524's MDTraj
review establishes that the native charge-export API requires at least 1.10.3;
its existing unbounded declaration is not yet corrected or qualified here. The
same work exposes [#622](archive/resolved_bugs/topology_extraction_accepts_invalid_atom_subsets_as_the_complete_source.md):
native Topology treated any full-length atom list as complete coverage, even
with duplicates or invalid positions. Source `35a0457f0` validates the owner
before that shortcut and retains sorted unique subsets, copy/alias semantics,
hierarchy, empty results and repeated attribute queries. The original 27 failing
rejection cases are retained; final integrated receiving passes 1,971 cases
without omissions, including documentation and doctests. The
[receipt](../devtools/data/topology_extraction_receiving_622_20261106.json)
separates authoring mistakes, overlapping runs and source/installed evidence.
The correction shares native-integrity scope without extra percentage credit;
public delivery/board closeout follow. Continue #524 after this bounded repair.

**Native extraction delivered:** checkpoint
`b206781edfb2dfd4f8120de4930cf82725fb1ad7` independently matches all twelve
checked source/record blobs. #622 is verified closed as completed, with its
source commit and addressable guard. The
[delivery receipt](../devtools/data/topology_extraction_delivery_622_20261106.json)
records that separate acceptance. All fourteen fast gates pass; work commits
carry `[skip ci]` and no remote workflow is dispatched. Continue #524's actual
optional-provider floor receiving, then the remaining NumPy/Viewer/installed
closure. Accepted plan progress remains **40%**.

**MDTraj and optional-contract source checkpoint:** #623 in `0ea1e04d7` repairs
the external topology subset's lost charges/labels and sparse hierarchy indices,
preserving source order, unknown assignments and source independence. Its
[record](archive/resolved_bugs/mdtraj_topology_subsets_lose_chemical_metadata_and_retain_sparse_hierarchy_indic.md)
and [receipt](../devtools/data/mdtraj_subset_receiving_623_20261106.json)
retain eight original failures, positive controls and metadata-preserving
documentation edits. Final receiving passes 1,191 cases each on public
MDTraj 1.11.0/Python 3.13 and 1.11.2/Python 3.14, without omissions.

Partial #524 in `962b2c68e` selects the API-grounded optional floor >=1.11.0
after rejecting 1.10.3's copy behavior. Its route auditor now checks public
optional constraints/required coverage and rejects conditional pip overrides,
without duplicating executable OpenFF version constants. A 654-case profile
receives routes, real provider operations, workflow contracts and documentation.
Paired PyParsing controls pass 72 on 3.3.2 and fail 28 on 3.3.3, preserving the
exact exclusion and #486 follow-up. The NumPy `<3` ceiling is removed: the
unchanged bridge has an explicit ABI boundary, without evidence for a version-
major ban. The [optional-runtime receipt](../devtools/data/optional_runtime_receiving_524_20261106.json)
retains public wheels, actual imports, failed attempts, independent review and
source/installed limits. Other optional-provider floors and actual Viewer/
installed closure remain due. Public delivery and #623 board closure follow;
accepted progress remains **40%**, with no bonus for supplemental regressions.

**Optional-runtime/subset public closeout:** published checkpoint
`f5c909e75d786a20d92f4b57e6fa2875a3ba651e` independently matches all 32 changed
public blobs. #623 is independently verified closed; #524 stays partial. All
fourteen fast gates and whole-tree Ruff lint/format pass. The
[delivery receipt](../devtools/data/optional_runtime_delivery_623_20261106.json)
retains the verified central #137 handoff and its still-pending graph refresh.
The fresh complete board contains 556 issues, 98 open, with unchanged PR #543.
New #624 is a heterogeneous small-molecule collection capability proposal for
PharmacophoreMT, explicitly requesting no immediate priority or closure; it
demonstrates no new correctness blocker. Retain that design review alongside
the growth backlog while continuing #524's remaining optional-provider and
actual Viewer/installed work. No remote workflow, package or release is selected;
accepted progress remains **40%**.

- For **#613**, choose the supported concurrency model at the configuration
  owner. Protect aliases, nesting, exceptions, unrelated observers and all
  applicable per-call overrides, including real decorated calls. Distinguish
  process serialization from thread/task-local isolation. A Viewer-local lock
  cannot protect direct MolSysMT callers.
- For **#524**, settle styled-output/Jinja2 requirements, complete API-grounded
  provider review and coordinate a real published Viewer minimum. Keep manifests,
  recipes and runtime-bearing environments aligned. Qualify the actual minimum
  installed closure and representative default operations, alongside newer
  published-provider compatibility. Preserve optionality and owning exceptions;
  source pins and development extras are not public release floors.

**Exit:** calls respect their declared configuration authority, and default
supported operations work in the declared installed runtime.

**OpenMM and constructor-boundary receiving:** optional OpenMM >=8.2.0 is
implemented in `3325cda9526fa1cdaa3daca90fbd03687fb14208`. Actual public
8.2.0/Python 3.12 and 8.6.1/Python 3.14 each pass the same 2,098 selected
provider cases without omissions. The first supplies the public support floors;
the second retains the ordinary SMonitor bridge. Original older-wheel ABI,
metadata, copy and fixture failures remain in the
[receipt](../devtools/data/openmm_runtime_receiving_524_20261106.json).

The review also repairs #625's unguarded PDBFixer file/text constructors in
`80590ef769cf9336b9f4fd45f452b453f1fe72c0` and #626's OpenMM copy/extraction
metadata and structure-dispatch defects in
`207d054cbc3281e43a291d759d9160ebadf61c9d`. Their maintained guards preserve
absence/transitive-failure distinctions, known/unknown chemistry, periodic boxes,
empty inventory parents, source identity and copy policy. Ordinary joint
receiving passes 1,060 cases; its two new invalid legacy-fixture labels are
corrected and all four fixture cases pass separately. Notebook code, outputs,
IDs and metadata are preserved. Public receiving/board closure follow; these
supplemental repairs add no progress weight. Remaining optional-provider,
actual Viewer and clean installed closure keep phase 3 open at **40%**.

**OpenMM block delivered:** public checkpoint
`4d1d5949aa6a717000ac5d01a6a818f0cc99aa5d` independently matches all 24
changed source/test/documentation/receipt blobs. #625 and #626 are verified
closed as completed. The
[delivery record](../devtools/data/openmm_runtime_delivery_625_626_20261106.json)
retains that state and a complete board checkpoint: 558 issues, 98 open, and
unchanged PR #543. Fourteen audit-related issues are closed; supplemental
regressions do not change the accepted 40% milestone. All 14 fast gates pass;
no new remote full-matrix or installed-artifact evidence is claimed.

**PDBFixer and runtime/docs distinction qualified:** `fac0d8706` selects
optional PDBFixer >=1.11 from the actual cap-completion counterexample. Both
1.11/OpenMM 8.2/Python 3.12 and 1.12/OpenMM 8.6.1/Python 3.14 pass the same
172 selected cases without omissions. The
[receipt](../devtools/data/pdbfixer_runtime_receiving_524_20261106.json)
retains the 1.10 failure, first network setup error, corrected harness artifact
collision, exact origins and final complete receiving. It qualifies the existing
pH route, not general H orientation, protonation or fixed-state PDBFixer support.

`0a06a01c2` retires unsupported OpenMMTools runtime declarations and places
Plotly with its real documentation-only consumer, preserving local regeneration.
All 625 dependency/registry/controlled-route/docs controls and 14 fast gates pass.
Public delivery follows. Remaining MDAnalysis/RDKit/OpenFF/ParmEd/PyTraj/NGLView/
Biopython APIs and actual Viewer/installed closure keep #524 partial and the
accepted phase progress at 40%. RDKit's consumed SetPositions API is now under
source/artifact study; no unqualified new floor is declared.

**RDKit receiving; new concrete data-operation defects:** `883e4e45a`
declares the API-grounded optional 2024.3.4 floor; `13b82905c` repairs #627's
malformed descriptor fixtures. Both exact public RDKit profiles pass 541 with
one conditional SMILES-negative omission; positive CCO conversion and all eight
native API/unit/CIP/chemistry guards pass. Seven fixture guards retain strict
VAL handling and all prior score/state assertions. The
[receipt](../devtools/data/rdkit_runtime_receiving_524_627_20261106.json)
separates native contiguous-storage protection from an unexposed provider
stride limitation. Publication and #627 board closeout follow.

Parallel studies independently reproduce #628 (MDAnalysis copy/subset bond
annotations/forces; baseline: 26 failed/four passed) and #629 (ParmEd native export
charge/coordinate/ID loss; valid baseline: 15 failed/two passed). They are admitted
correctness work in phase 3, with no new weighting or feature scope. Those
repairs are now qualified in f81ba2025/e270eda9b: 155/185 cases per public-provider
profile, plus 1,271 joint and 97 scientific cases in overlapping scopes. Public
delivery/board closeout follows; floors alone do not repair consumer omissions. Remaining provider/host/installed
acceptance keeps progress at 40%. PDBFixer source/dd60ee7d6 and all 16 public
blobs plus the central #137 handoff are independently received in the
[delivery record](../devtools/data/pdbfixer_runtime_delivery_524_20261106.json).

### Phase 4 — Bound-tool contribution and graphical receiving

**Initial position:** #421 partial; PR #543 open with conflicts at the audit
snapshot. Its successful smoke and pending full matrix are separate evidence.

| Work | Required outcome and acceptance evidence |
| --- | --- |
| #543/#421 integration | Reconcile the contribution with the corrected native source and a named Viewer source. Review expert mirrors, edits, detached results and graphical actions separately. Keep scientific algorithms and units with their native owners. |
| #602 rotation constructor | Review the smallest reusable public boundary over existing mathematical kernels for the agreed Rotate task. Specify axis validation, explicit angular units, handedness and row-vector active-rotation convention. Require analytic signed rotations, scaling/degeneracy and unit controls. No new algorithm/backend is implied. |
| #638 XYZ representation | Correct accepted rank-one/two/three publication and integer coordinate arithmetic without silent fractional truncation. Test supported quantity libraries, selections, unit policy, readonly and in-place failure atomicity at the coordinate-owner boundary. |
| #635 newer-host panel receiving | Use actual primary endpoint identity while preserving popup routing and rejecting another view's endpoint. Receive exact newer Viewer bytes separately; never transfer older-host evidence. |
| #590/#591/#603 outcomes and layout | Receive durable completion/rejection messages and actual Jupyter layout. Refresh must not replay science, revive a consumed token or erase the relevant native diagnostic. Distinguish already implemented contribution fixes from owner integration and graphical acceptance. |
| #609/#614 asynchronous receiving | Follow acknowledged presentation and actual attached/current panel identity. Retain exact title, numerical, lifetime and popup assertions; sleeps, forced clicks and accepted placeholders are not repairs. |
| #615 initial canvas | Preserve the original intermittent failure and early stack/timing instrumentation. Establish its causal stage on recurrence or an evidenced bounded environment disposition. A later passing run alone does not establish repair. |
| Viewer #314 navigation authority | Receive the Viewer-owned correction and rerun the conformational workflow that exposed it. A plot-selected structure must agree between canvas and Python authority across the admitted notebook/popup paths. Keep this host dependency explicit; do not patch native scientific coordinates to compensate. |
| #611/#567 gate semantics | Retain complete test tiers with a finite budget justified by their real workload. Preserve failed/cancelled attempts. Define comparable performance baselines and third-party/control roles, retain result artifacts and review policy changes rather than weakening a failing assertion. |

The plan review confirms [Viewer #314](https://github.com/uibcdf/molsysviewer/issues/314)
is open: actual Jupyter receiving observes a plot-selected canvas structure
without the required Python current-structure agreement. The PR explicitly
keeps that receiving and broader Geometry, Chemistry, Analysis/property,
sequence/mechanics/plot and scientific-session families pending. Use the
[owning #421 record](pending_proposals/molsysviewer_tools_addon.md),
[GUI design](molsysviewer_tools_gui_design.md) and linked receiving issues to
identify the accepted workflows. Neither the dated 246/248 source-path count nor
the initial task subset replaces that inventory. Do not silently drop an accepted
workflow to pass qualification or demand a GUI for every expert API path.

**Next source-integration route, reviewed 2026-11-06:** PR #543 remains at
`8ab2f5474b2e04c68d31ef2854a238984b645fc8`. A read-only comparison against
owner `e5d1dd0f8` identifies 99 contributed paths, seven owner overlaps and two
textual conflicts in the queue index/release ledger. Reconcile the contribution
in isolation, preserving the owner repairs and archived #605/#606/#607/#608/
#613/#616 records rather than reintroducing their pending copies. Refresh the
comparison against the final owner checkpoint before modifying it.

Published Viewer source `25061d9e99baf07fa0dcb4021897958a226f0152` supplies the
causal #314 correction and the host APIs needed by the Analysis panel. Its
public owning record is still partial: it reports 17 Jupyter R4 checks and
44/44 browser-core suites, while hosted/installed/human acceptance remains due.
Receive an exact snapshot rather than the dirty sibling working tree. Align
the five affected workflow routes/inventory to one actually received host SHA;
the older 42234de8/239c8dd7 pins are not evidence for that new combination.
Run the complete bound-tool selection and its inventory/native-viewer guards,
then the admitted Jupyter/popup cases. This can advance locally without
inventing a public package version or closing #421/#314 prematurely.

**Exit:** the agreed expert and graphical workflows receive the exact combined
sources, with full applicable tests, actual Jupyter/popup acceptance and explicit
remaining host/Qt limitations. Review/integration does not qualify installed
packages or make experimental scientific profiles stable. Do not dispatch a
duplicate matrix merely to monitor an existing run.

**Source receiving — 2026-11-07:** isolated merge `653ed8e0b48020a6b6ccf7aeeb186290784eee71`
preserves owner native science/tests/archives and the contribution's addon
runtime/guards. The refreshed comparison has eight overlaps and the same two
textual conflicts; the earlier seven-overlap count used an older owner. The
exact published Viewer snapshot `25061d9e9` passes import/API preflight and
5,009 Python cases (4,974 addon, 35 preflight), zero skips/failures/errors.
Only after receiving were six pin-bearing files aligned to that host; four
static checks pass. The [receipt](../devtools/data/bound_tools_owner_source_receiving_20261107.json)
retains the original uncommitted tested tree, committed merge, native exits and
unsuccessful nonproduct attempts. No actual Jupyter node was selected and main
has not received this branch. Next: complete #602 and rerun admitted graphical
workflows, retaining #609/#614's assertions and #615's original uncertainty.
No phase-four credit or host #314 closure follows from Python receiving alone.

**Explicit graphical receiving — 2026-11-07:** Preparation, pending chemistry
and periodic geometry pass with six/eight/eight steps. Analysis separately
passes its twelve-step wrapper after correcting the root-prepared test
auxiliary to the exact host build. The original four-case campaign has three
passes and one server-readiness failure; a diagnostic Analysis run then reaches
nine steps and fails on the incorrectly built auxiliary. All attempts and
source/asset identities are retained in the
[GUI receipt](../devtools/data/bound_tools_owner_jupyter_receiving_632_20261107.json).
New #632 owns the stale seven-step wrapper, now locally corrected and received.
No driver assertion or deadline is removed. These four implemented scenarios
do not replace the remaining accepted GUI families, full Jupyter campaign,
conformational #314, installed or human acceptance. #615 remains uncertain.
Accepted progress remains **40%**, with 19 audit-related issues closed.

### Phase 5 — Reconcile acceptance and public scientific claims

**Initial position:** mixed implementation, closeout and scientific-disposition
work; no blanket closure is justified.

| Work | Required outcome and acceptance evidence |
| --- | --- |
| #612/#587 | Receive the current corrected source and addressable guards, satisfy remaining owning criteria, archive/synchronize through the reporting protocol and close with the actual public commit. |
| #549 | Complete the remaining producer/composite and consumer receiving. Preserve original labels, explicit naming schemes, unknown context and ChemicalStates ownership. Separate delivered lookup/storage behavior from final-candidate acceptance. |
| #250/#254 | Reconcile implemented interaction/native-domain contracts with final-candidate and Viewer feedback. Decide public stability by surface; scientific detector evidence and container/persistence reliability remain separate questions. |
| #473/#475 | Establish the original physical meaning, units and justified aggregation, or record an explicit bounded experimental disposition. Keep ISA distinct from conformational SASA and ECI distinct from independently verified physical charges. Do not guess dimensions, sums or a replacement model. |
| #378/#610 | Correct the stale README namespace and affected examples; explain supported XYZ composition/default-element behavior. Check API/User Guide/Cookbook/course where affected. Broader SEO work remains separate. |
| #582 | Make requested versus effective mechanical recipes and unsupported controls explicit. Retain engine-neutral physical language and adapter ownership; wider tuning support needs separate execution evidence. |
| #334 status | Keep one concise current next-step entry in the release ledger. Preserve dated checkpoints and original candidate identities; reorganize history only with retained links and evidence. |

**Exit:** public claims match implemented and qualified scope; unresolved
scientific meaning is visible; source completion is not confused with release
qualification. Close only the issues whose actual acceptance criteria are met.

### Phase 6 — Exact candidate and publication decision

**Initial position:** replacement candidate selection and qualification are not
performed by this audit. The existing publication pause and immutable historical
artifact identities remain in force under #334.

After the accepted correction and receiving blocks are complete:

1. Agree exact compatible MolSysMT/Viewer sources, versions, builds and the
   affected qualification scope with their owners.
2. Freeze a clean candidate and execute the mandatory fast, scientific,
   full-source, native wheel, Conda/installed-pair and documentation gates in
   [release_gate.md](release_gate.md). The specified eight source cells and
   sixteen installed-pair cells retain their actual platform obligations.
3. Receive immutable artifact names, digests, dependency closure and actual
   import origins. Qualify client/session behavior separately from install smoke.
4. Return a failed gate's affected scope to stabilization. Preserve failed and
   incomplete attempts; do not reuse an older candidate's verdict for new bytes.
5. Obtain the existing final publication authorization, then perform the required
   public-artifact and Zenodo verification under
   [release and citation](release_and_citation.md).

**Exit:** the exact candidate satisfies the release contract and owner sign-off.
A passed development audit, source smoke or superseded installed pair is not
that exit.

## Cross-operation acceptance

Single-function guards need a small set of composed workflows because #618 and
#616 survive existing passing suites. Reuse existing fixtures and acceptance
tools; this is no new test framework or exhaustive Cartesian-product matrix.

| Workflow | Required evidence within the supported contract |
| --- | --- |
| Selected composition | Add a reversed/nonconsecutive source selection and compare names/source maps, coordinates, chemical fields, connectivity and selected mechanics against the expected identities. Exercise independent/in-place behavior and rejection before partial publication. |
| Native domains and persistence | Use a system with a named analysis; apply supported selection/permutation, write/read H5MSM 0.5, and check domain/source maps, producer metadata and documented occurrence identity. Compare a compatible structure append with its native control, including newly unevaluated coverage. Check supported coordinate/chemical edits and the affected interaction invalidation. H5MSM 0.5 does not persist nonempty MolecularMechanics: retain its explicit rejection rather than demanding that round trip. |
| Periodic observations | Check admitted image vectors/geometries against row-vector boxes and physical coordinates under changed application units. Receive the affected Viewer workflow on those same conventions where graphical consumption is required. |
| Installed default workflow | Outside checkouts, exercise representative default `get`/`info`, geometry and save/read operations with the declared dependencies. Verify real import origins and actionable optional-provider absence; development extras must not supply a missing runtime requirement. |

For each affected operation, select meaningful combinations from these axes:
ordered/nonconsecutive/empty/repeated selections under its own policy;
native/recovered logical string and null representations; valid/invalid and
changing cells; input and application units; independent/in-place ownership;
supported eager/chunked paths; and evaluated-empty versus unevaluated coverage.
Include unchanged-source and failure-atomicity checks where mutation is involved,
including warning-as-error behavior when the operation can emit one. A numerical
or identity regression needs an independent oracle and a valid positive control;
parity between two routes sharing the same bug is insufficient.

### Resource impact of the corrections

Review allocations on changed selection, composition, remap and persistence
paths. A small selected addition should not acquire an avoidable full-trajectory
copy merely to repair its index map. Reuse the existing native-copy/H5MSM
workloads when a correction changes resource behavior; record selected data,
resident outputs, first-index and repeated-query costs as applicable. Measure
peak memory when the allocation change warrants it. Do not infer process-RSS
bounds from array sizes, launch an unbounded stress test on this machine or add
an arbitrary performance gate. #567 owns baseline comparability; #336's general
streaming/editor work remains separately scoped.

## Cross-cutting requirements for every correction

- Reuse meaningful general tools in their owning modules. Keep selection/remap
  contracts shared; chemical connectivity belongs in `chemical_states`, stable
  inventory in `topology`, geometric primitives in `structure`, periodic rules
  in `pbc` and detector criteria in their interaction family.
- Validate at the public boundary with ArgDigest. Use trusted delegation only
  for values already satisfying the complete callee contract. Keep private
  helpers undecorated.
- Use DepDigest for applicable optional/backend availability and SMonitor for
  actionable diagnostics. Preserve absence, operational failure and unsupported
  scientific scope as distinct outcomes.
- Preserve PyUnitWizard quantity meaning through kernels, storage and outputs;
  test a non-default application policy. Use optional Ackredit for the executed
  scientific method when applicable, retaining original producer attribution.
- Test identities and values, not only counts/shapes or agreement between paths
  sharing an implementation. Add failure/unknown/empty cases and independent
  truth; review every gate for conforming output that could pass without doing
  the intended work.
- Check relevant form/native and eager/chunked parity within supported scope.
  Input streaming does not establish resident-output or process-RSS bounds.
  Reuse bounded existing workloads before commissioning another benchmark.
- Complete docstrings, User Guide, Cookbook and affected course lifecycle.
  Run applicable local checks, batch meaningful pushes and retain exact-head CI
  conclusions through the existing checkpoint policy.
- Revisit incoming issues/PRs at phase boundaries, recording why any new defect
  changes the order. Providers and consumers retain their own implementation
  and scientific acceptance responsibilities.

## When to stop stabilization and qualify

Declare **ready to qualify** only when reproduced included-profile defects have
their corrections/guards, accepted workflows have their required source receiving,
and exposed scientific claims have an agreed evidence or limitation disposition.
Identify exact counterpart sources and outstanding artifact gates in the release
ledger. Unresolved required host receiving remains an explicit dependency, not a
MolSysMT-native defect or a passing gate.

The **ready to publish** decision additionally requires the exact artifacts and
all applicable qualification/sign-off in the existing release gate. Keep that
single authority rather than maintaining another independent release checklist.
New extension requests do not restart completed stabilization blocks; a newly
demonstrated included-profile defect returns its affected block to correction
under the admission rule. No passing result here certifies untested optional
engines, GPU execution, chemical models or larger workloads.

## Preserved subsequent scientific and engineering work

These are valuable follow-ups, not missing implementations automatically added
to the initial release. Delivered subsets still ship and need their applicable
receiving; the table concerns each issue's remaining extension scope.

| Direction | Owning issues | Preserved boundary and reassessment trigger |
| --- | --- | --- |
| Environmental H refinement and broader site directions | #323, #375 | Keep fixed-state geometry, movable/frozen populations, model/environment coverage and correspondence explicit. Reusable operations belong in MolSysMT; composite protocol registration/orchestration is coordinated with Praxis. Publish/receive already implemented site-direction subsets separately from broader acceptor-model work. |
| Molecular identity and read-only plausibility | #447, #555 | Explicit chemical-state/stereo/isotope and geometry-rule policies, maps and unsupported outcomes. Keep dataset/docking/pharmacophore interpretation in consumers. Reassess on an admitted concrete workflow. |
| Recognition/model breadth | #262, #337 | Delocalized charge and chemically specific metal criteria need independent chemical evidence. Geometric candidates are not physical coordination certification. |
| Interaction editing and scale | #335, #336 | Preserve existing replacement/invalidation/compaction and bounded serialization. Individual observation editing, direct detector-to-file streams and general resumable append need separate contracts and recovery/measurement work. |
| Mechanical storage and runtime copies | #256, #592 | H5MSM 0.6 mechanics and faithful OpenMM runtime/State copies remain separately scoped. Do not invent complete runtime clones or persist the experimental mechanics model implicitly. |
| Preparation, states and pose analysis | #219, #220, #229, #230, #366, #604 | Explicit transformations/correspondence and declared clustering rules require their own scientific/API review. Existing partial or unsupported chemistry remains visible. |
| Wider forms and internal layout | #519, #438, #181 | Resource-owning FASTA, H5MSM module-location review and broader conversion profiles remain bounded independent work. Prioritize actual included-workflow defects without requiring every declared edge before 1.0. |
| Provider/performance follow-up | #403, #486, #530, #128, #382 | Retain qualified compatibility protections until actual replacement receiving. Profile additional query/startup/storage work before redesign; no unmeasured speedup or automatic provider upgrade. |

### Scientific source correspondence — #636

The original `3f66f5931` runner admitted a real temporary Git checkout whose
untracked `conftest.py` demonstrably ran: its one tracked test passed and the
certificate incorrectly reported release eligibility. The earlier #602/#638
molecular certificates were already dirty/ineligible and did not use that gap.

Correction `970cf51b7` now checks tracked state, all nonignored untracked inputs
and identical known commits before/after execution, retaining four exact
reserved workflow outputs. Its 23 controls pass, including loaded/self-deleting
hooks, restored tracked source, changed commits and clean/artifact positives.
Actual molecular execution passes 107 cases across 68 nodes with
`--require-clean` on that clean development commit. This narrow scientific/source
eligibility is distinct from a final candidate, ignored native/provider identity,
installed-pair/platform qualification and publication. The owning
[report](archive/resolved_bugs/scientific_certificate_ignores_untracked_python_inputs.md)
and [receipt](../devtools/data/scientific_source_correspondence_receiving_636_20261107.json)
retain the original failed outcomes. Final candidates must rerun their own
exact-source gate; this development checkpoint does not waive it.

## Progress log

Add rows rather than replacing earlier measurements. A completion row names the
implementation/publication commit, guard or receipt, consumer scope when needed,
issue state and next unresolved exit. Do not copy complete issue bodies here.

| Date | Scope | Verified position | Next step |
| --- | --- | --- | --- |
| 2026-11-06 | Audit at `4a80c2294` | Seven current defects reproduced, #618 reported; 83 scientific, 51 directed and five pagination cases pass in their stated scopes. Source and existing human edits are preserved. | Record the bounded plan, then begin #618 followed by #616 when implementation proceeds. |
| 2026-11-06 | Tracking packet | The maintainer requests this new document to retain the audit and track corrections. No runtime correction, new candidate or publication is made by this documentation step. | Append implementation/qualification evidence to the relevant phase and owning report as work advances. |
| 2026-11-06 | Plan review | Rechecked the full open inventory and PR #543's receiving scope. Added release relevance/owners, the open Viewer #314 dependency, composed-workflow and resource acceptance, and distinct qualification/publication exits. Dated audit results are unchanged. | Keep #618 → #616 as the immediate order; record the implementation guards in their owners when correction begins. |
| 2026-11-06 | Execution authorized | The maintainer requests execution, durable checkpoints and periodic progress estimates. The new-plan baseline is 0%; #618 implementation/receiving starts. All earlier audit observations and failed attempts remain evidence. | Qualify and publish #618, then continue #616. No tag, Release or promotion is made by this execution start. |
| 2026-11-06 | Phase 1 source checkpoint | #618 and #616 implemented in `19d6d55c1`, with 2,748 joint and 40 overlapping directed/doctest passes. Owning records are resolved/archived; original failures, warnings and limitations are retained. Planned completed contribution: 20% after origin/board receiving. | Verify public delivery and close #618/#616, then #605 → #607 → #606 → #608. No installed or release qualification is implied. |
| 2026-11-06 | Phase 1 delivered; phase 2 begins | `a91a4fd1b` is public on main; all nine implementation/test blobs independently match. #618/#616 are verified closed. Four remote checks pass; smoke 42305861858 is still active at inspection. Accepted progress: 20%. #605 additionally passes 430 local PBC/scientific cases. | Complete #605 documentation/source delivery, then #607. Preserve the actual smoke conclusion; do not treat an active run as passing or start another solely to monitor it. |
| 2026-11-06 | Completeness and execution review | Reconfirmed #618/#616 closed and #613/#524/#619 open. Added a domain/evidence map, explicit scientific-claim and finite GUI acceptance boundaries, and #619 without changing the phase weights. Directed local PBC receiving has 692 passes; the integrated XML contains zero tests and is not a passing receiving. Accepted progress remains 20%. | Resolve combined receiving, record the phase-two backend/receipt and deliver its source/closeout; then #613 and independently actionable #524 work. No new API, scientific method or publication is authorized by this review. |
| 2026-11-06 | Phase 2 source qualified | `3eb720444` implements all five PBC corrections. Corrected-path integrated receiving passes 5,435 cases; final directed/documentation receiving passes 1,195; the scientific certificate passes 97/97 for 64 nodes; 82 Rust unit tests pass. Counts overlap. The receipt retains original failures, zero-test/unobserved attempts and exact rebuilt backend identity. Phase-one smoke 42305861858 is now verified successful. | Publish and independently verify the source, synchronize/close #605/#607/#606/#608/#619, then credit the existing phase-two 20 points and continue #613/#524. No extra points for #619 and no installed-release claim. |
| 2026-11-06 | Phase 2 delivered and closed | Public checkpoint `27bc4d3c5` independently matches all 27 checked blobs. #605/#607/#606/#608/#619 are closed with source `3eb720444` and addressable guards. Accepted plan progress is 40%; #619 shares the existing unit milestone. The receipt preserves original failures and local/installed evidence boundaries. | Finish this checkpoint's ordinary unskipped CI and begin #613 under the accepted process-global serialization contract; continue independently actionable #524 runtime work. PR #543 remains open at the same reviewed head. |
| 2026-11-06 | Phase boundary board refresh | Complete paginated open inventory contains 98 issues and one PR after PBC closeout. No newly numbered open report changes the selected #613 next step. PR #543 remains open at `8ab2f5474b2e04c68d31ef2854a238984b645fc8`; its qualification remains separate. | Continue configuration correctness and installed-runtime closure, preserving the existing graphical and final-candidate dependencies. |
| 2026-11-06 | Configuration source qualified | #613 correction `f60e25b7e` passes 4,438 integrated, 32 source-floor/doctest, 500 documentation and 97 scientific cases in overlapping scopes. Its receipt retains all failed attempts and process-global limitations. Independent serial precision mismatch is reported as #620 after complete seven-page acquisition; no new backend is required. Accepted plan progress remains 40%. | Publish/verify and close #613; resolve #620 and independently actionable #524 before phase-three credit. The existing phase-two smoke remains active in its bound-tool receiving step at inspection. |
| 2026-11-06 | Configuration delivered; PBC CI terminal | Public checkpoint `1b1cc42e0` matches all 12 checked implementation/receipt/report blobs. #613 is independently verified closed. All four observed ordinary workflows at PBC head `16ecaae01`, including smoke 42312538781, conclude successfully. Accepted plan progress remains 40%; source and installed-release qualification stay separate. | Finish the configuration checkpoint with an unskipped head and inspect its applicable CI, then continue #620 and independently actionable #524. |
| 2026-11-06 | Precision and default renderer qualified | #620 `cb07e54af` and partial #524 `44fd0acf0` pass 4,592 joint cases, 599 documentation/doctests and 97 scientific cases; scopes overlap. Directed precision has 39 passes; exact-Jinja2 receiving has 35 and isolated minimum-provider receiving seven. Seven notebook edits preserve code/outputs. #613 smoke 42314744961 succeeds at `60ded0f7c`. The maintainer renews `[skip ci]` on all work commits and batched pushes, superseding automatic unskipped heads for small work blocks. | Publish and independently verify the source and receipts, close #620, and finish independently actionable #524 review without inventing a public Viewer floor. Installed/graphical/final-candidate qualification remains separate. Accepted progress remains 40%. |
| 2026-11-06 | Precision delivered and closed | Public checkpoint `8d466268c` independently matches all 43 checked source/record blobs. #620 is verified closed as completed. Final fast gates pass 14/14; the queue-index check passes. No new remote run was dispatched; all three work commits carry `[skip ci]`. Accepted plan progress remains 40%. | Continue the remaining #524 provider/restriction review, preserving actual public Viewer-floor and installed closure dependencies; then the agreed addon/graphical receiving and contract closeout. |
| 2026-11-06 | Support floors and periodic preparation qualified | Five required public support floors and optional Ackredit receive 581 passing consumer cases with 14 explicit optional study omissions, plus 133 parser/preparation/doctest passes. #524 `4f8b03364` removes duplicate deprecated sorting; #621 `2804f7954` corrects the missed MIC consumer. Exact-Pandas-3.1.0 combined receiving passes 965, documentation 543, scientific execution 97; scopes overlap. The original failures and unchanged notebook code/outputs are retained. Accepted progress stays 40%. | Publish and independently verify the sources/receipts, close #621, then continue optional-provider/NumPy-bound review and actual Viewer/installed closure. No additional progress weight or publication authorization. |
| 2026-11-06 | Support/preparation delivery verified | Public checkpoint `ad6b71e97` matches all 14 checked source/record blobs. #621 is independently verified closed. All fourteen fast gates pass; complete board acquisition contains 553 issues, 97 open, and unchanged PR #543 at `8ab2f5474`. No newly numbered report changes the order. Accepted progress stays 40%. | Continue the remaining optional-provider minima/exclusion and NumPy ABI-bound review under #524, then actual Viewer acquisition and installed/graphical receiving. Work commits retain `[skip ci]`; no new remote workflow or release is selected. |
| 2026-11-06 | OpenMM and optional constructor receiving | Source 80590ef76 repairs #625, 207d054cb repairs #626, and 3325cda95 declares optional OpenMM >=8.2.0. Both actual public OpenMM profiles pass 2,098 selected cases; ordinary joint receiving and four corrected legacy controls qualify diagnostics/docs/native routes. Original failures remain in the receipt. Accepted progress stays 40%. | Independently receive the batched source and close #625/#626, then continue PDBFixer and remaining optional-provider/Viewer/installed work under #524. |
| 2026-11-06 | OpenMM block published and closed | Public checkpoint 4d1d5949a matches all 24 checked blobs; #625/#626 are verified closed. The full board has 558 issues, 98 open and unchanged PR #543. Fourteen audit-related issues are closed; accepted progress remains 40%. | Finish PDBFixer minimum receiving, distinguish unused runtime declarations from docs dependencies, then continue remaining optional APIs and actual host/installed closure. |
| 2026-11-06 | PDBFixer and runtime/docs separation qualified | Source fac0d8706 selects optional PDBFixer >=1.11; final minimum and newer profiles each pass 172 selected cases. Source 0a06a01c2 retires unsupported/runtime-misclassified declarations; 625 route/docs cases and 14 fast gates pass. The original network/harness failures are retained. Accepted progress stays 40%. | Verify batched public delivery, continue RDKit and remaining optional APIs, preserve actual Viewer/installed closure under #524. |
| 2026-11-06 | RDKit API and fixture qualification | Source 883e4e45a selects optional RDKit 2024.3.4; 13b82905c repairs #627 reference fixtures. Minimum/newer profiles each pass 541 with one documented conditional omission; literal chemical/score assertions are retained. New #628/#629 data-loss baselines are reproduced and admitted as correctness work. Accepted progress stays 40%. | Deliver/close #627, finish MDAnalysis/ParmEd owner repairs and actual-provider receiving, then remaining optional and host/installed scope under #524. |
| 2026-11-06 | MDAnalysis/ParmEd consumer repairs qualified | #628 source f81ba2025 and #629 source e270eda9b preserve represented metadata/geometry/chemistry and explicit target limits. Final actual-provider pairs pass 155 and 185 per profile without omissions; joint receiving passes 1,271, scientific execution 97/64 nodes. Source 33a702bfa aligns optional floors. Original failures and failed harness attempts remain in portable receipts; scopes overlap. Accepted progress stays 40%. | Independently receive the batched public sources and close #627/#628/#629, then finish OpenFF/Biopython/NGLView/PyTraj and actual host/installed closure. No new tag, candidate or remote workflow. |
| 2026-11-06 | Consumer repair block delivered | Public checkpoint 82bfa1c82 independently matches all 58 changed blobs. #627/#628/#629 are verified completed; audit-related closed count 17. Complete acquisition has 561 issues/98 open and unchanged PR #543 at 8ab2f5474. Fourteen fast gates pass. Accepted progress remains 40%. | Finish remaining optional providers and actual host/installed closure under #524; keep graphical, installed-package and final-candidate qualification separate. |
| 2026-11-06 | Final optional-provider source block qualified | d850f6cc1 uses public alignment rows; 5cd744ebf declares supported optional acquisition/floors; e5d1dd0f8/fae9ab557 repair #630/#631. Final profiles pass Biopython 385 each, OpenFF 199 each and NGLView 104 each with no omissions; joint 798, scientific 97/64 nodes and fast gates 14/14 pass. HTML compilation exits 0 with four retained source-title warnings. Counts overlap; accepted progress stays 40%. | Publish and independently verify the block, close #630/#631, then receive the newer exact Viewer source and reconcile PR #543 while keeping public-host/clean installed closure explicit under #524. |
| 2026-11-06 | Optional-provider block delivered | Public 7e61fcc5c matches all 39 checked blobs; #630/#631 are verified completed. Audit closed count 19, progress 40%. The complete board has 563 issues/98 open and unchanged PR #543. The central graph notice is independently received; refresh is not claimed complete. | Receive isolated owner+543 with exact newer published Viewer source; retain #524 public-host/clean installed closure and distinct graphical/release gates. |

| 2026-11-07 | Isolated bound-tools source received | Merge `653ed8e0` reconciles owner `030c201a5` with contribution `8ab2f5474`; exact Viewer `25061d9e9` passes import/API preflight and 5,009 Python cases with zero failures/errors/skips. Owner source/test/archive and incoming runtime/guard preservation are checked. Five workflows plus the inventory now pin the received host; four static checks pass. | Complete #602 and actual Jupyter/popup/navigation receiving. Main, installed and human acceptance remain separate; progress 40%, closed audit issues 19. |

| 2026-11-07 | Four implemented GUI scenarios received | First campaign: three passes (Preparation6/Pending8/Periodic8), Analysis failed before browser at server readiness. Diagnostic Analysis completed nine steps before a root auxiliary-build error; exact-build correction plus preflight permits all twelve Analysis steps and the #632 wrapper to pass. Portable receipt retains all three executions and failed outcomes. | Finish source delivery/closeout of #632, then #602 and remaining agreed graphical families/full Jupyter/conformational receiving. Original readiness and #615 uncertainty remain; progress 40%, closed issues19. |

| 2026-11-07 | Rotation/documentation block locally qualified | #602 native/expert constructor and #633/#634/#637 corrections pass 7,764 integrated cases; minimum providers 76, scientific 107/68 nodes, five notebooks across two campaigns and fast gates 14/14. Scopes overlap; scientific certificate explicitly ineligible; original failures and six HTML warnings retained. | Deliver the combined source and close only verified owner issues. Then correct #638 and #636 and receive #635 on its actual newer host. Progress 40%, public audit closures 19; no candidate or installed/human closure. |

| 2026-11-07 | Rotation and guard block delivered | Main source `684a5b0cb` and archive `2499dc53b` match complete public API trees. #602/#632/#633/#634/#637 are verified closed, taking audit-related closures to 24; progress remains 40%. | Correct #638 and #636, receive #635/new exact host, and retain all broader graphical/installed/human/final-candidate exits. |

| 2026-11-07 | XYZ coordinate representation qualified | #638 preserves original ranks/units/quantity owners, promotes independent integer storage and rejects unsafe integer publication. Minimum-provider/ownership/doctest receiving passes 269, scientific 107/68, all six notebooks and fast gates 14/14. Broad native-1 record retains 7,977 passes/two corrected fixture import errors; six HTML warnings remain. | Publish and independently verify/close #638, then correct #636 and receive #635/newer host. Public closures 24, progress 40%; no candidate. |

| 2026-11-07 | Scientific source correspondence qualified | #636 source `970cf51b7` rejects unsafe starting/ending source while retaining reserved outputs; all 23 real-execution controls pass after nine original failures. Actual molecular `--require-clean` passes 107/68 nodes on the clean development commit. | Deliver and independently verify/close #636, then receive #635 and the newer exact host. Public closures 25, progress 40%; narrow source eligibility does not select a candidate. |

| 2026-11-07 | Scientific source correction delivered | Public `6d9f8b07a` matches all ten changed paths and #636 is verified closed. Audit-related closures 26; complete board 570 issues/98 open. The narrow clean scientific/source certificate binds implementation `970cf51b7`; no candidate is selected. | Receive #635 and #543 head `42f5ed3bc` on its exact newer host, then remaining accepted graphical/installed/human exits. Progress remains 40%. |

| 2026-11-07 | Newer-host contribution delivered | Public `45e69bb10` matches all thirty changed paths; #543 is verified merged at `0ddb99c2b`; #635/#639 are verified closed. Owner receiving passes 5,428 source cases, all four actual Jupyter scenarios (17/6/8/8), clean scientific 107/68, fast gates 14/14 and HTML native0 with six retained warnings. Complete board 571 issues/97 open, audit closures28, progress40%. | Continue accepted #421 graphical families, starting Rotate with the delivered constructor, without dropping remaining session/host/installed/human/final-candidate exits. |

Once this work is complete, consolidate any lasting rules into their normative
owners and archive the dated packet through the owning release/reporting route.
Preserve the receipt, original outcomes and links so a future reviewer can recover
what was known, decided, implemented and qualified at each checkpoint.

| 2026-11-07 | Evidence-catalog correction source-qualified | #642 retains the complete stored label table and numeric codes through the typed constructor. Original reader: 32 failed/16 passing controls; correction: 3,098 integrated passes, eleven doctests, eight typed/two-analysis checks on the immutable real carrier. Historical consumer failures and producer metadata stay unchanged; no detector replay. | Public main `4d8af6c34` independently matches all eighteen changed/deleted paths; #642 is verified closed and DockingMT #80 receives comment 6712753798. Clean scientific execution passes 107/68 nodes. Continue #640/#641 and the next finite accepted GUI package. Supplemental repair adds no milestone bonus: approximately 61%; installed and candidate exits stay separate. |

| 2026-11-07 | Native diagnostic corrections locally qualified | #640 maps source structure indices separately from selected positions. #641 preserves reason/code/type and general conditional guidance across all four audiences. Original baseline: 60 failed/2 controls; receiving: 701 cases, one doctest, two actual Jupyter scenarios, 14 fast gates and HTML with six retained warnings. | Public main `49d1a720f` independently matches twenty changed/deleted paths; both issues are verified closed. Clean scientific execution passes 107/68 nodes. Viewer #315 receives comment 6712967862. Continue the accepted #421 external-reference GUI workflow. Progress approximately 61%; graphical intents22/50. No installed/candidate or human acceptance is inferred. |

| 2026-11-07 | External-reference prototype exposes provider I/O prerequisite | Local prototype ca59736a4 retains only selected unit-bearing anchors, but the stronger real HDF5 window guard finds full-series public-query reads. Initial/expanded 324/339 passes and final 340pass/1fail scopes overlap. Independent #643 probe and eighteen provider failures match public runtime 07f04d9e8. | Repair the general H5MSM query route, then finish the original graphical acceptance without a private reader or relaxed guard. Progress61%, graphical22/50, source closures32; no candidate or installed acceptance. |
| 2026-11-07 | Modular-query source fix delivered and consumer guard received | #643 published at 71a2c2b8e; all thirty changed paths match the public tree. 1,921 integrated, three doctest nodes, fourteen fast gates and HTML pass. Clean exact-source scientific execution passes 107 cases/68 nodes. The original external-reference guard/prototype bytes remain unchanged; local composition ea410c573 passes 341 directed cases. | #643 independently verified closed; authorized Viewer #315 comment 6713930007. Continue actual external-reference Jupyter/Mol*/popup receiving and all remaining scope. Progress61%, graphical22/50, source closures33; no candidate/installed/publication acceptance. |

| 2026-11-08 | Placement and saved-benchmark-data receiving | #651 fix `51a3e1898` receives 598 cases, both unit policies, fourteen clean-source fast gates and HTML. Partial #567 fix `e21cd1341` receives 45 cases and fourteen fast gates, retaining original threshold and blocking scope. All later #612 incomplete attempts and #652 cache-review uncertainty are recorded. | Publish/verify and close only #651, then a fresh full-source run with four workers and enforced 8-GiB/4-CPU limits, preserving the 2-GiB host reserve. Progress stays 65.3%; no supplemental bonus or #567 policy acceptance. |

| 2026-11-08 | Complete local source and developer evidence received | Clean `03c59caef9` completes 32,039 default cases (32,014 pass/25 skip); all 23 Amber omissions pass separately on the same source. #612 source acceptance is complete. Current `12a6c6fc2` passes 104 directed developer/panel cases after #653 repairs the unchanged completeness guard failure; #611 finite-budget owner review is complete. #567 retains open comparability/role policy. | Publish/verify and close #612/#611/#653, then credit only the original owning milestones. Keep every interrupted/resource observation and bounded artifact detail; begin the nine existing Jupyter scopes for #590/#591/#609/#614. No installed or final-candidate waiver. |

| 2026-11-08 | Full-source block publicly received | Public `258702da0` is independently verified; #612/#611/#653 are closed and board/queues agree. Fourteen fast gates pass. Complete board: 585 issues/92 open/no PR. Accepted progress 68.0%, source closures 47, graphical 23/50; only original owning leaves receive credit. Provider detail-recovery request is uibcdf/pytest-receptor#51. | Begin the nine original Jupyter owner scopes with explicit CPU defaults and activated paths; preserve #615 uncertainty, #567 policy, remaining graphical/scientific contracts and installed/final-candidate gates. No release authorization. |

| 2026-11-08 | Existing graphical owner receiving begins | Public product checkpoint `425c16ba2` retains accepted 68.0%, 47 source closures and 23/50 intents. The next declared campaign selects the nine original actual-Jupyter guards for #590/#591/#609/#614, sequentially, with the exact Viewer/provider route, explicit CPU default and activated tool paths. Planned process-tree cap 4 GiB/2 CPU/no swap; the host reserve and finite stop route remain monitored. | Receive real layout/outcome, all five original acknowledgement drivers and all three navigation consumers. Keep every source/geometry/title/lifetime/deadline assertion and #615 causal uncertainty; no provisional policy or AGENTS edit. |

| 2026-11-08 | Four graphical owner defects publicly closed | Clean `68323539e` passes all fourteen actual-Jupyter guards / 109 browser checks; all 8,560 owner and 2,463 verified-export inputs agree before/after. Fourteen fast gates pass on public `9a27cc1bea`. #590/#591/#609/#614 are independently verified closed; complete board 585 issues/88 open/no PR and queue sync pass. Accepted milestones 72.2%, 51 source closures, graphical intents still 23/50. | Continue the existing general-orientation/changing-cell periodic GUI intent and remaining agreed families. Preserve every failed/stopped attempt, #615 uncertainty, #567 policy, #582 recipe work and all installed/platform/final-candidate requirements. No release authority. |

| 2026-11-08 | General periodic graphical intent publicly received | Public `1659a1515` delivers clean `2f0eeb1c1`: 336 source cases, fixed/general real-Jupyter guards (sixteen browser checks), shared physical-box validation and previous-selected transition cells. Fourteen fast gates, course structure and HTML pass; six old heading warnings remain. Code/outputs in four course modules are preserved. | Credit only the existing general-periodic leaf: 24/50 graphical intents, 51 source closures, weighted 72.2367%. Continue cell assignment, tiny-boundary-origin graphical receiving and all other original/external/final-candidate requirements. No full-family, installed, human or release acceptance. |

## Planned OpenMM/openmmtools capability comparison

At the requested deliberate pause, inspect the local source repositories and
record their exact revisions and local modifications before drawing conclusions.
Currently observed heads are OpenMM `ba0aa236ac4d07241382869604c4d2ea58c4f3f5`
and openmmtools `a42cbdc862a0a4fe996a579dd1b04611ce9916a4`; these are inventory
observations, not yet reviewed or qualified sources. Do not implement anything
merely because another package exports it.

Build an evidence table with one meaningful operation per row: scientific
purpose; source API/implementation and reference; existing MolSysMT equivalent
and real gap; prospective users; domain owner; reusable public contract; units,
atom/group/structure/state axes and PBC assumptions; optional-provider boundary;
licensing/attribution; independent tests and estimated resource cost. Distinguish
an existing but undiscoverable tool from a missing capability.

Rank the findings as reuse/document now, investigate/implement later, provider
request, or outside MolSysMT's remit, with explicit reasons. General tools must
retain engine-neutral, form-agnostic boundaries and use the appropriate owning
module. Protocol orchestration and sampling strategies require an explicit
Praxis/Nextia ownership decision. Reuse compiled primitives first; justify any
new Rust work by measurement. Compare representative cases against independent
or analytical controls before proposing a scientific-equivalence claim.

The deliverable is a dated comparative report and prioritized proposals, with
owning issues where needed. This records the user's requested study without
changing frozen 1.0 gates, adding a scorecard weight or promising unreviewed
scientific functionality. #604 was the next finite block after sequence-fit and is now delivered above;
the subsequent #656/#658 fixes are also delivered above. Continue with #657
and the existing-composition question under #256.


## Native addon additions received — 2026-11-09 (#665)

Source 46ed67b7e receives four real public wrappers and current H5MSM schema/
mechanics signatures. It preserves current-primary versus explicit-input
ownership, exact native contracts and experimental limits. The final affected
selection passes 398 cases; an explicit union of complete case outcomes covers
all 5,806 current cases in the reviewed scope. The original 600-second full
invocation and subsequent stale-namespace/help failures remain recorded, not
relabeled as passes. Fourteen fast gates pass; API/guide/course/Cookbook HTML
is inspected and fifteen executed notebook cells remain exact.

See the [archived report](archive/resolved_bugs/bound_addon_omits_newly_exported_native_tools.md)
and [receiving evidence](../devtools/data/bound_provider_admission_receiving_665_20261109.json).
This is source receiving with retained Viewer e4dd58cf, not qualification of the
newer reporter host, an installed pair or a final candidate. No graphical intent
or weighted-score bonus is added. #421's contact task remains held by native
unit-boundary review #666 / uibcdf/pyunitwizard#143. #256 handoffs, #524 floors,
remaining graphical work and #334 release gates remain outstanding.
