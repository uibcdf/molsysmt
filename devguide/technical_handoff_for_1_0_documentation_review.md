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
| 2. Conclude the remaining investigations and contract decisions | Preserve #723's completed bounded memory campaign and #713's accepted closure, including their original limits and failures. Obtain #615's accepted disposition from the MolSysViewer audit lead. Finish #256's stable H5MSM decision and #250/#254/#524 compatibility, profile and dependency agreements. | Linked owner conclusions, supported limitations and required maintainer/client acceptance. A deferral or uncertainty is not a passing result; outstanding blocking scope must be resolved or explicitly accepted through its applicable policy. |
| 3. Freeze and qualify the exact coordinated pair | Agree producer commits, unused builds, immutable filenames, channels and SHA-256 values with MolSysViewer. After the agreed resumption, run all mandatory exact-source/native/scientific/documentation and installed-pair gates. Qualify supported dependency bounds and retain the declared experimental-platform limits. | The complete evidence set required by release_gate.md: scientific certificate without skipped registered nodes, eight-cell full-source matrix, applicable native artifacts and sixteen-cell installed Conda pair. Source-only or earlier package results cannot substitute. |
| 4. Deliver the review packet | Present the qualified reference, reproducible documentation site, reader route, remaining documented experimental limits, evidence links and explicit deferred-work list. | Diego receives documentation to review with no separate unresolved engineering or client-acceptance task required to establish readiness. The live ledger explicitly records the handoff decision and qualified identities. |

Stages 1 and 2 may overlap while external replies arrive. Stage 3 depends on
the final MolSysViewer candidate and the agreed resumption. Stage 4 cannot be
declared complete merely because all currently selected local tests pass.
Record external prerequisites with owner and requested deliverable; do not
silently treat waiting as acceptance.

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
