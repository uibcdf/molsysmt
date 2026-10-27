---
summary: Budget CI smoke for both native and bound scientific tiers.
issue: uibcdf/molsysmt#501
status: resolved
opened: 2026-10-27
closed: 2026-10-27
verification: measured
area: [ci, addons, testing]
guard:
normative: devguide/molsysviewer_addon.md
blocked_by: []
supersedes: []
---

# Budget CI smoke for both native and bound scientific tiers

**Reported:** 2026-10-27, exact-source addon qualification. Opened with the
principal maintainer's authorization.
**Status:** resolved; corrected-source hosted CI completes successfully.
Hosted completion is being verified without removing scientific tests.

## What

Increase the bounded `CI smoke` job budget from 15 to 25 minutes so that the current native scientific and bound MolSysViewer tiers can finish and publish an official terminal result without removing tests.

## Evidence

Exact source `ea9fff3395157389b3a245cf70f58517973e76b8`, fixed-ref run [40570840482](https://github.com/uibcdf/molsysmt/actions/runs/40570840482): pytest completed both tiers with `PASS exit=0` (2,807 native / 1,845 addon cases; four and three optional Ackredit skips). The workflow then ended officially `cancelled`, which remains non-success evidence.

GitHub check-run 122424282078 explicitly annotates: `The job has exceeded the maximum execution time of 15m0s`. The job ran from 19:37:54 to 19:53:05 UTC on 2026-10-27. Native tests took 367.59 s and bound tests 352.21 s, in addition to environment/toolchain/build/control setup and cleanup. This is measured budget exhaustion, not an inferred product failure or an unexplained cancellation.

## Decision and acceptance

Keep both scientific tiers and their guards. Use a finite 25-minute job maximum, document its native-plus-bound scope and preserve the original cancelled run, its completed pytest evidence and annotations. Qualify the corrected source with an officially successful applicable run. Do not relabel `cancelled` as success, infer installed compatibility, skip scientific tests, or claim a universal runtime/performance bound.

This operational budget policy will be absorbed in `devguide/molsysviewer_addon.md`; no brittle test mirroring the timeout literal is needed. Actual hosted execution and the existing workflow/contract controls remain the implementation evidence.

Related: uibcdf/molsysmt#421, uibcdf/molsysmt#500, uibcdf/molsysviewer#264.

Record: `devguide/archive/resolved_proposals/ci_smoke_budget_covers_native_and_bound_scientific_tiers.md`.


## Scope and exclusions

Finite development CI budget for setup, build, both scientific tiers and cleanup.
This is not a performance guarantee, installed qualification, release waiver or
permission to report an officially cancelled workflow as passing. The separate
fixture migration is uibcdf/molsysmt#500.

## Provenance

GitHub run 40570840482 and check-run 122424282078, source ea9fff339, Linux/Python
3.14. Original complete bundle/log/check annotations are retained with digests.
The conclusion is cancelled even though the two pytest processes report success.

## Resolution — 2026-10-27

Correction 4ad988584ec1409fb9f90e2e8ce2aab05a638473 passes fixed-source
CI smoke 40575948453, officially success including cleanup. Native pytest has
2,847 passes, four optional Ackredit skips and the one strict #499 xfail on that
frozen source. Bound pytest has 1,845 passes and three optional Ackredit skips.
All five additional applicable source controls pass. The original failed and
timed-out runs remain non-success evidence. The 210 directed fixture cases
pass; scientific assertions and selected tests are retained. The new budget is
finite, not a runtime guarantee. This closes #500/#501 for this source, without
claiming installed, all-platform or release qualification. The separate #499
owner repair ab165135e is not retroactively qualified by this earlier run.

Evidence: `devtools/data/molsysviewer_tools_descriptor_ci_closeout_20261027.json`.
