---
summary: Make real-Jupyter server-readiness budgets explicit and bounded.
issue: uibcdf/molsysmt#705
status: open
opened: 2026-11-10
closed:
verification: inspected
area: [tests, jupyter]
guard:
normative:
blocked_by: []
supersedes: []
---

# Explicit bounded Jupyter server readiness

## What / How / Why

The Viewer team reports an E2 pilot that exhausts the launcher's forty
half-second preparation polls while Jupyter is still initializing extensions.
Its retained server log subsequently reaches serving state during retirement.
The reported attempt failed before any browser or molecular cell; its external
28.30-second/215-MiB/three-retired-process observation has not been replayed
here. Source inspection confirms the fixed readiness loop.

The team proposes a finite positive CLI preparation budget, bounded above by
300 seconds, with the existing default of 20 seconds. Its separately declared
sequential two-CPU/four-GiB scale profile would request 90 seconds. This is
operational preparation control, not a scientific-operation, first-canvas or
frontend deadline change. Preserve the original failed default-budget attempt.

## Acceptance and ownership

The Viewer team prepares the contribution; MolSysMT will review and receive
its exact source. No implementation or runtime setting is changed by this
triage. Require deterministic validation of defaults/invalid/nonfinite/excessive
values, bounded monotonic readiness, authenticated endpoint success, early
process exit/timeout and actual elapsed/budget recording in server-startup.json.
Retain existing runtime-file/source nonmutation and owned-process retirement.
Do not publish token-bearing URLs, raw settings or server credentials.

Actual bounded receiving must separate the default 20-second control from
the explicitly selected scale profile. Changing a preparation profile does
not turn the earlier failed attempt green or establish #615 causality. No
scientific assertion, browser/cell timeout or missing-canvas acceptance may
be silently relaxed. The initial-canvas report remains separately owned by
[the #615 investigation](../pending_bugs/intermittent_jupyter_initial_canvas_timeout.md).

## Plan disposition

Add #705 to the existing pre-1.0 intake under #334 and #421, with no extra
original milestone weight. Receive the incoming contribution when supplied;
retain the complete local 5e7d65a66 session as evidence of its own unchanged
source. The [completion handoffs](../pre_1_0_completion_handoffs_20261110.md)
keep provider requests and publication/installed/human boundaries separate.
