# Technical handoff for the maintainer's 1.0 documentation review

**Role:** operational completion plan under uibcdf/molsysmt#334.
**Accepted objective:** maintainer decision of 2026-11-12.
**State:** target agreed; technical handoff not yet achieved.

## Destination and authority

Reach a technically qualified MolSysMT 1.0.0 / MolSysViewer 1.0.0 pair for
which the only outstanding substantive review is Diego's editorial and
scientific review of the documentation. Do not hand off unfinished engineering,
unclassified release blockers or unexecuted mandatory qualification as a
documentation-review task.

The [scope decision](release_1_0_scope.md#documentation-review-handoff-objective--2026-11-12)
owns admission rules. The [execution ledger](release_1_0_status.md#resume-from-here)
owns current status, next actions and evidence. This plan defines the route and
exit criteria, not a second progress register. The
[release gate](release_gate.md) remains the authority for exact-candidate checks;
the [publication contract](release_and_citation.md) owns release and archival
operations. No gate is waived and no existing source/package result is relabelled.

The current pause on new candidate construction, hosted qualification, tags,
promotion and publication remains in force. The goal does not lift it. Prepare
the concrete final-pair proposal and obtain the agreed resumption before those
operations; routine source correction and bounded local checks can continue.

## Finite work order

| Stage | Required work | Exit evidence and owner |
| --- | --- | --- |
| 1. Finish technical correction and documentation preparation | Finish admitted correctness/data-integrity repairs and misleading documentation, including #727's intended references. Reconcile docstrings, User Guide, Cookbook and course with actual contracts, units, domain ownership and scientific limits. Review relevant new issues and PRs at phase checkpoints. | Focused regressions, relevant executable examples and actual rendered-article/link receiving; strict full documentation build; no unresolved blocker in the promised stable scope. #334 / #727 and the existing polishing queue own evidence. |
| 2. Conclude the remaining investigations and contract decisions | Preserve the completed #723/#713/#615 investigations, #763/#766 reader corrections, #256 source/wire decision and #764/#765/#768 governance/notebook receiving. Retain their original limits and failures. Conclude #250/#254/#524 final compatibility, profile and artifact acceptance. | Linked owner conclusions, supported limitations and required maintainer/client acceptance. A deferral or uncertainty is not a passing result; outstanding blocking scope must be resolved or explicitly accepted through its applicable policy. |
| 3. Freeze and qualify the exact coordinated pair | Agree producer commits, unused builds, immutable filenames, channels and SHA-256 values with MolSysViewer. After the agreed resumption, run all mandatory exact-source/native/scientific/documentation and installed-pair gates. Qualify supported dependency bounds and retain the declared experimental-platform limits. | The complete evidence set required by release_gate.md: scientific certificate without skipped registered nodes, eight-cell full-source matrix, applicable native artifacts and sixteen-cell installed Conda pair. Source-only or earlier package results cannot substitute. |
| 4. Deliver the review packet | Present the qualified reference, reproducible documentation site, reader route, remaining documented experimental limits, evidence links and explicit deferred-work list. | Diego receives documentation to review with no separate unresolved engineering or client-acceptance task required to establish readiness. The live ledger explicitly records the handoff decision and qualified identities. |

Stages 1 and 2 may overlap while external replies arrive. Stage 3 depends on
the final MolSysViewer candidate and the agreed resumption. Stage 4 cannot be
declared complete merely because all currently selected local tests pass.
Record external prerequisites with owner and requested deliverable; do not
silently treat waiting as acceptance.

**Stage-2 receiving — 2026-11-15:** #256's finite BindingMT default-write/
migration return is accepted and its first-stable H5MSM 1.0 source/wire decision
is complete. The [owner receipt](../devtools/data/binding_default_h5msm_acceptance_256_20261115.json)
retains source/native limits and independent raw-file checks. Preserve that
conclusion; continue #524 and #250/#254/#421, then the exact coordinated gates.
This does not complete stage 2 or lift the stage-3 execution/publication pause.

The [finite contract closeout packet](pre_1_0_contract_closeout.md) supplies
the current stage-2 guarantee-to-guard mapping and exact owner returns. Its
presence is preparation, not evidence that client or candidate acceptance has
finished. Do not widen the work while those returns are pending.

## Independent MolSysMT work queue — 2026-11-16

**Owner:** uibcdf/molsysmt#334. **Planning basis:** `3b006f627`.
The maintainer requests productive local work while MolSysViewer completes its
own gates. The following queue executes stages 1, 2 and preparation for stage 4;
it does not depend on receiving a new consumer candidate. Stage 3 keeps its
existing dependencies and execution/publication pause.

This is a finite queue for already admitted documentation, correctness and
qualification preparation. It adds no release gate, scientific feature or
requirement to execute the entire historical notebook corpus. The live ledger
owns progress; this section owns the work order and exit criteria. Initial
states below describe planning, not completed execution or new scorecard credit.

| Block | Work and concrete deliverable | Exit evidence | Initial state |
| --- | --- | --- | --- |
| I0 — evidence and scope map | Inventory the existing review route below and corresponding course modules. Match relevant pages/examples to the actual source, code/input fingerprints and prior execution/rendering receipts. Freeze the local file/cohort list and identify native-only, consumer-dependent, optional-engine and external-input cases. | Every selected item has a reason, applicable evidence or unresolved gap, owning boundary and next action. Source rendering, actual execution and scientific validation remain separate. | Planned; prior receipts available. |
| I1 — technical and scientific reading | Review the frozen native documentation cohort against implemented contracts and scientific evidence. Produce a finite discrepancy list, with owning issues for actionable defects and explicit dispositions for existing limitations. | Names, signatures, defaults, axes, units, ownership, physical interpretation, method/attribution and public stability claims agree across the affected docstring, User Guide, Cookbook and course material. | Planned. |
| I2 — executable native examples and corrections | Run the examples whose admitted gap needs execution, in bounded batches using existing tooling/environment. Correct reproducible documentation or source defects through their proper reusable owners; update affected outputs and meaningful guards. | Actual command/exit, source/runtime/input identity, units, outputs and warnings are retained. Independent checks protect the intended numerical/mapping behavior. Every required selected case has valid receiving; a missing dependency or failed run remains unresolved. | Planned after I0; overlaps I1. |
| I3 — qualification-route preflight | Review existing build/staging/installed/citation inputs and offline guards. Keep the seven-surface dependency draft current, preserve the corrected kernel baseline and specify every final identity still needed from its owner. | Input-validation/identity/failure controls are exercised where needed. The final execution packet names real tools, required arguments, artifact custody and stop conditions. Missing final identities are explicit; no producer/build is invented or reserved. | Prepared in part: reciprocal minimum agreement and unapplied draft exist. |
| I4 — local documentation receiving and reader packet | After admitted local corrections, build the documentation strictly and inspect the affected articles, figures, links and downloadable examples. Consolidate the existing reading route, scientific limits and deferred-work list. | Reproducible local site and scoped content/link receiving tied to actual sources, with executable-example evidence distinct from stored rendering. The final-candidate rebuild remains due. | Planned after the correction batches. |
| I5 — local closeout and final-pair handoff | Reconcile the selected findings and issue/PR intake, update the existing contract packet and ledger, and return an explicit local-complete/external-pending disposition. | Locally admitted work has a verified conclusion; required unresolved cases and external owners remain visible. Exact final-pair qualification and Diego's content review are not marked complete. | Planned; intake also runs at block boundaries. |

### I0: select work from evidence, not from test counts

Start with the maintained reading route and these existing receipts:

- [Essential native/chemical/storage examples](../devtools/data/documentation_examples_receiving_334_20261114.json).
- [Geometry examples and actual figures](../devtools/data/geometry_documentation_receiving_334_757_20261114.json).
- [Peptide course execution](../devtools/data/peptide_course_receiving_759_761_20261115.json).
- [Form-reference coverage](../devtools/data/remaining_form_reference_receiving_727_20261113.json).
- [Complete stored-source documentation rendering](../devtools/data/complete_documentation_source_receiving_334_20261113.json).

A matching notebook filename, stored output or code hash alone does not prove
that its example passes with the present runtime. Review relevant library,
native, dependency and input changes before reusing earlier evidence. Conversely,
do not repeat a received campaign simply to obtain another passing count.
Record why a repeat is necessary or why its earlier bounded evidence applies.

Freeze the first cohort before execution. Review in this order:

1. Native model, get/info, selection, copy/extraction and declared axes.
2. ChemicalStates, named Interactions and H5MSM presence/maps/provenance/edit
   invalidation, including independent or partial systems.
3. Geometry/PBC/physchem and preparation/mechanics examples within their
   declared scientific and optional-engine limits.

This is a risk-based order, not a fixed number of examples standing in for
coverage. Corresponding course examples enter when they teach the same changed
or insufficiently received contract. Consumer-dependent examples keep their
own owner and future receiving; they do not delay unrelated native work.
Use metadata and per-file processing rather than loading all notebook outputs
or molecular inputs at once. A compact worklist using existing receipts is
sufficient; I0 does not commission a new audit framework or orchestrator.

### I1/I2: review and execution boundaries

Check scientific meaning as well as whether code runs: tabulated descriptors
versus geometric observables, aggregation, dimensions, precision versus output
dtype, periodic image conventions and applicable method definitions. Keep the
authoritative API-stability and scientific-evidence registries as their owners.
References and Ackredit statements must distinguish executed software, faithful
method reproduction and inspiration. Existing qualified uncertainty, including
the Collantes primary-source questions, is not silently promoted to validation.

Use the current development environment or an already received support
composition, recording actual import origins. A native-only example needs no
new MolSysViewer candidate or live canvas; this does not imply the absence of
installed support dependencies. Inspect input sizes and optional/network calls
before running. Prefer the original bundled/offline input where its scenario
already permits it; do not silently substitute another scientific problem.

Exercise the relevant non-default unit policy where it protects the actual
contract, retaining physical equivalence and correct index maps. Do not double
every execution mechanically. Preserve notebook scientific content, native
file inputs and expected failures; do not erase outputs or weaken an assertion
to manufacture a pass. A necessary software fix uses existing modular owners,
ArgDigest, DepDigest, SMonitor, PyUnitWizard and optional Ackredit at their real
boundaries. Public changes retain the full documentation lifecycle.

Record actionable defects in their owning issue before sustained correction.
Routine prose fixes need proportionate checks; reproducible numerical/data-loss
or supported-workflow defects need meaningful regression protection. New
algorithms, detectors, convenience APIs, #512 content-contract expansion and
#728 implementation remain deferred under the existing scope cutoff.

### I3: prepare existing routes without constructing a candidate

Inspect the existing producer and validators, including
[the Conda workflow](../.github/workflows/build_and_upload_conda_packages.yaml),
[installed-pair workflow](../.github/workflows/verify_installed_conda_pair.yaml),
[release-route guards](../devtools/tests/test_release_route.py),
[staging guards](../devtools/tests/test_validate_conda_staging.py),
[installed-runtime guards](../devtools/tests/test_installed_runtime_dependencies.py)
and [citation tools](../devtools/tests/test_citation_release_tools.py).
Run relevant existing offline controls when the review identifies an unreceived
or changed boundary; this is not a request to repeat every passing test.

The packet must distinguish exact producer SHAs, package versions/builds,
platform/interpreter scope, immutable files/hashes/channels, actual import
origins and receiving artifacts. Agreement on reciprocal >=1.0 floors is not
an applied or qualified public minimum. Keep the untagged source pin and its
real version label coherent until producer metadata is selected before freeze.

Existing staging build-only behavior and later installed qualification are
different phases. Preserve old artifacts and every failure; do not dispatch a
producer, solver, hosted matrix, promotion, tag or release from this preflight.
The existing pause and exact-candidate gate continue to own those operations.

### Execution, intake and stop rule

Apply the loaded operator policy and the accepted common resource rule to
each material run. Estimate whole-family RAM, CPU/native threads, scratch and
duration from its real inputs and existing measurements. Start with a small
bounded example when demand is unknown; choose further concurrency from measured
demand and current conditions. Use existing execution/monitoring tools, preserve
the host reserve and unrelated work, and confirm owned retirement. Available
capacity is not reservation or aggregate protection. Use Pytest Receptor for
pytest and GH Run Receptor where CI evidence inspection is needed.

At block boundaries, acquire the applicable issue/PR scope through complete
owner pagination and review correctness/data-integrity reports first. Known
unavailable identities remain unknown, with local records preserved. Do not
claim an empty backlog from a partial response. Routine consumer status messages
are consolidated at these checkpoints; a concrete new provider defect can
reprioritize this queue, while receipt-only updates do not replace its execution.

Finish this queue when the frozen locally admitted cohort, required corrections,
preflight and local reader packet have evidenced conclusions. Any mandatory
unexecuted item stays unresolved with its owner; classifying or deferring it is
not a pass. New concrete correctness findings use the existing admission rule.
Once the local cohort is complete, return its conclusion rather than enlarging
it merely because the consumer is still working.

Completion prepares the final handoff but does not establish it. MolSysViewer
must still return its final qualified source; exact pair construction and all
required source/native/scientific/documentation/installed gates follow the
agreed resumption. The original global scorecard and its weights are unchanged.

## Admission rule that keeps the destination reachable

- Continue fixing incorrect results, silent data loss, invalid units/maps,
  broken supported workflows, unsafe resource behavior and materially misleading
  scientific or user documentation in the admitted scope.
- Changes needed to satisfy an already required release gate or an agreed
  client contract remain necessary work. Reopen affected evidence when such a
  change invalidates it.
- New detectors, algorithms, public-API conveniences, redesigns and optional
  performance/maintainability improvements are tracked for after 1.0 by default.
  They enter this route only by an explicit maintainer scope decision or because
  evidence establishes that they are necessary to correct an admitted blocker.
- Performance differences alone do not make a correct implementation a release
  blocker. Preserve #567's measured-debt policy and report improvement work.
- Review new reports for severity and relevance; do not aim to close every open
  issue. Deferred items stay open with reason, owner and revisit condition.

In particular, #728's combined ProtOr radii/types/provenance proposal is not a
prerequisite for this handoff. Preserve its source study and consumer request;
defer implementation to the post-1.0 queue unless a later explicit admission
changes that decision. The existing supported public composition remains usable.

## Handoff acceptance checklist

- [ ] Every pre-1.0 engineering obligation has an evidenced conclusion; no known
      unresolved blocker is hidden as a documentation limitation.
- [ ] Stable H5MSM scope and consumer contracts are agreed, and scientific
      profiles retain their actual validation/experimental classifications.
- [ ] The exact final pair and its artifacts are identified, and every
      mandatory technical gate has passed at that reference.
- [ ] The complete documentation site and relevant examples have technical
      receiving; the remaining task is the maintainer's content review.
- [ ] The review packet contains evidence, known limitations and owned deferred
      work, with no unexecuted mandatory gate described as completed.

These are evidence criteria, not percentage credit. The original scorecard
keeps its weights and acceptance conditions; polishing does not manufacture
progress or establish a reliable completion date.

## Review packet and reader route

Prepare this packet as the preceding stages complete. Its presence does not
establish that the technical handoff has been accepted:

- Exact source and package identities for both libraries, including actual
  import origins, platform/Python scope and immutable artifact hashes.
- The corresponding documentation build and its reproduction route, with
  stored-notebook rendering, executed examples and actual browser receiving
  distinguished explicitly.
- Links to terminal technical evidence, accepted scientific/profile limits
  and the owned deferred-work list. Failed attempts retain their original
  outcomes; pending required gates remain visible.
- The reading sequence below, so the maintainer can review the public
  explanation before checking specialist API details.

| Review area | Starting pages and main question |
| --- | --- |
| Installation and supported scope | [Installation](../docs/content/about/installation.md) and [support](../docs/content/user/foundations/support/index.md): can the stated installation deliver the claimed platform, provider and form capabilities? |
| Molecular model and ownership | [Molecular systems](../docs/content/user/foundations/molecular_system/index.md) and [native domains](../docs/content/user/foundations/native_world/index.md): are stable inventory, chemical states, structures, mechanics and named analyses explained with their actual ownership and absence semantics? |
| Language and physical quantities | [Query language](../docs/content/user/foundations/language/index.md) and [units](../docs/content/user/foundations/governance/quantities_and_units.md): are indices versus IDs, groups, structure selections and configurable units unambiguous? |
| Everyday operations | [Basic tools](../docs/content/user/tools/basic/index.md) and [Cookbook](../docs/content/user/cookbook/index.md): do examples explain the relevant copy, extraction, mutation and conversion boundaries? |
| Geometry and scientific observables | [Structure](../docs/content/user/tools/structure/index.md), [PBC](../docs/content/user/tools/pbc/index.md) and [physchem](../docs/content/user/tools/physchem/index.md): do methods, units, periodic conventions, references and limitations support the stated interpretation? |
| Preparation and mechanical models | [Build](../docs/content/user/tools/build/index.md) and [molecular mechanics](../docs/content/user/tools/molecular_mechanics/index.md): are chemical-state assumptions, terminal/hydrogen policies, engine/model choices and assignment coverage explicit? |
| Interactions and persistence | [Interaction tools](../docs/content/user/tools/interactions/index.md) and [H5MSM 1.0](../docs/content/user/tools/form/file/h5msm_10.md): are sparse observations, coverage, provenance, maps and edit invalidation distinguished from scientific classification and format stability? |
| Learning path and public promises | [Four Paths course](../docs/content/course/index.md) and [API lifecycle](../docs/content/user/foundations/governance/public_api_and_lifecycle.md): do the teaching sequence and stability labels agree with the qualified release scope? |

Keep this route tied to the exact received site in the final packet. A local
source preview is useful during preparation; it does not identify the final
published documentation or qualified installed pair.

## Review, manuscript and publication

Diego reviews the documentation and develops the MolSysMT 1.0 manuscript. Paper
drafting can overlap the technical work; manuscript acceptance is not used as
evidence of software readiness. Publication follows the qualified software,
review and coordinated release decision, not an automatic consequence of this
plan or of paper submission.

A review may discover a real defect. Correct it and reopen the affected work
rather than protecting a checklist result. If review changes the candidate,
identify the new exact commit/artifacts and satisfy every mandatory gate on
that final reference as required by release_gate.md. Even documentation-only
edits do not authorize reusing a different commit's qualification as though it
belonged to the new one. Requalification is a controlled release step, not an
invitation to add optional capabilities.

After review and final qualification, obtain the final publication decision,
publish the coordinated release and complete the required public-installation,
Release/Zenodo and exact-version archival verification. Resume deferred
development with its existing issues and evidence after that release.
