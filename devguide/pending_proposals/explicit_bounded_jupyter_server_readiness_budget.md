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

## MolSysMT review of draft #706 — 2026-11-10

Reviewed exact head `66273e4d3ad722726336055b4bf38dc76761e35e` against its
declared base `9dff314f896238d8d9968c3c86b9b901adf6e81a`, already an ancestor
of MolSysMT main. The [draft](https://github.com/uibcdf/molsysmt/pull/706)
adds the #705 CLI and an opt-in prolonged-session harness. Its 25 focused
runtime-file/CLI cases pass from the exact test sources with pytest-receptor.
The first sandboxed attempt had 23 passes and two denied local-socket calls.
The permitted local repeat passes all 25. The browser script parses with
`node --check`. These checks do not start Jupyter or a browser campaign.

Two additional deterministic launcher controls expose unresolved behavior:

1. A simulated authenticated 200 response arrives at 0.2 s with a 0.1 s
   preparation budget. The recorded startup has `ready=true` and the browser
   launches. The loop checks time before the request, passes a fixed 1 s
   transport timeout, can sleep a further 0.5 s and accepts success without a
   post-response deadline check. Clamp the probe and sleep to remaining time,
   and refuse an otherwise valid response once the deadline is reached. Test
   in-budget and late 200 responses, timeout and early exit at the launcher
   boundary, with no late browser launch and owned-file retirement.
2. `--cycles 30 --active-seconds 90` passes CLI validation, but playback alone
   requires at least 2,700 s. The launcher gives the entire browser process
   2,400 s, including startup, edits, windows, session round trips and cleanup.
   Require a coherent finite process deadline for the selected profile or
   reject an impossible combination before output creation.

Each adverse control reaches the production launcher with a fake monotonic
clock and server/browser boundary. The initial reviewer double omitted the
node-version call and is superseded by the corrected reproducer. No actual
browser run or resource load is needed to demonstrate either condition. The
PR's reported fifteen completed cycles and shared-pressure stop at cycle 16
remain partial evidence. Retired-controller observations remain owned by
uibcdf/molsysviewer#356. A separately reviewable readiness change can close
#705 after its own tests and receiving. The extended campaign and #615 keep
their own acceptance conditions. Draft #706 stays open for revision.
