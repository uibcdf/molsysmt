---
summary: Freeze 1.0 scope and complete bounded stabilization
issue: uibcdf/molsysmt#334
status: active
opened: 2026-10-05
closed:
verification: inspected
area: [docs, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Freeze 1.0 scope and complete bounded stabilization

**Accepted:** 2026-10-05, following the maintainer's request to stop capability expansion and preserve deferred work in issues.

## What

Freeze feature scope at `d609187ae17af089ef976116252e5a64b6331210` and complete a finite stabilization queue. The normative [scope decision](../release_1_0_scope.md) owns the admission rule, included profiles, six exit packages and full issue classification. This record tracks its execution; it does not duplicate that inventory.

## How

Review the current public contracts and board, separate correctness/qualification from extensions, retain current experimental profiles, and place unimplemented editing/storage/scientific extensions in #335–#338. Use the existing `1.0.0` milestone for remaining release reviews and a dedicated `Post-1.0` milestone for extensions and accepted debt. Update the roadmap, execution plan and ledger to route future work to this boundary.

## Why

The recent #304 reader checkpoint delivers explicit engine selection and inspectable evidence but still has chemical/performance extensions. Continuing all of them before publication would keep moving the endpoint. The same distinction applies to already implemented interaction replacement/compaction versus arbitrary editors and streaming.

## What is inspected and what remains unknown

The 2026-10-05 board query returned 75 open issues:

```bash
gh issue list --repo uibcdf/molsysmt --state open --limit 200 \
    --json number,title,body,labels,milestone,url
```

The initial scope review inspected their requests, current active queues, native/H5MSM/interaction public code, existing qualification records and the release gate. It did not reproduce #25/#30/#112, execute a new full suite, certify published dependency closure or obtain new Viewer canvas feedback. S1 is now qualified as recorded below; the other unknowns remain explicit queue items. Historical receipts and the prior weighted 99% figure are not current release certification.

The resulting board classification was read back and checked against the entire
snapshot: 15 issues in `1.0.0` (the 14 review/qualification owners plus this
tracking issue), and 65 in `Post-1.0` (61 original issues plus four extensions).
No issue was closed. Existing lifecycle-label drift in #215/#250/#252/#254/#271
was corrected to their actual partial reports; #286's existing area metadata
was synchronized, including its missing `coverage` label. Milestone scheduling
does not replace those lifecycle states or turn the reviews into proven defects.

## What was refuted

Closing every open issue is not the release criterion: most are additional capabilities, older delivered requests awaiting reconciliation, or explicit accepted debt. Conversely, labelling a current-profile correctness failure experimental is not sufficient to defer it. Installed-source parity or an old green campaign cannot qualify a different candidate.

## Scope and exclusions

This accepts the local scope rule and tracking changes, without changing runtime methods, signatures, scientific tolerances, dependencies, format versions or platform obligations. Other client integrations remain outside the initial required Viewer integration. No tag, package upload or GitHub Release is authorized by this record.

## Acceptance criteria

- The normative scope owns a finite stabilization queue and an exhaustive classification of the inspected open issues.
- Previously discussed deferred work has an owning issue; no issue is closed solely for deferral.
- Board milestones, proposal cross-links, roadmap, plan and ledger agree.
- S1–S5 reach their documented exit conditions; S6 follows the unchanged exact-candidate publication/sign-off policy.
- Close this operational tracking issue only with the final candidate/evidence and normative scope/release references. Creating this document alone does not close qualification.

## Dependencies and risks

Provider lifecycle and result qualification remain #250/#251/#252/#254; Python/dependency review remains #237/#244/#245. Viewer-owned feedback and product gates stay in uibcdf/molsysviewer#114/#112. Do not create a second scientific or release-gate checklist.

## Provenance

2026-10-05; read-only GitHub board and source inspection at `d609187ae`. Repository-facing changes in this checkpoint are documentation and issue tracking only.

## Documentation and board checkpoint

`validate_devguide.py`, `devguide_index.py --check`, the 263-symbol API registry
check and `git diff --check` pass. The read-only `devguide_issue.py sync --check`
also confirms that the open board agrees with the queues after label alignment.
No runtime code or notebook executable cell changed; no new scientific/full
suite was run or release gate declared complete.

## S1 checkpoint

The [execution ledger](../release_1_0_status.md) records the complete S1 triage:
#30's supported conversion now reuses native inference, #112's existing absence
behavior has an additional public guard, and #25's external-enrichment remainder
is a post-1.0 proposal. The scoped Python 3.14 selection passes 819 tests and
converter doctests; this is not the full release suite. The source fix, user
documentation and unchanged executable notebook cells are recorded in the
owning reports rather than a second acceptance list.

The previous head's devguide and policy runs did not acquire hosted runners;
they failed without executing steps. Applicable hosted evidence is still
required at the next checkpoint. Sphinx builds in the existing 3.13 documentation
environment; completing 3.14 documentation tooling remains #237. Continue
with S2, retaining S3–S6 and final publication approval.
