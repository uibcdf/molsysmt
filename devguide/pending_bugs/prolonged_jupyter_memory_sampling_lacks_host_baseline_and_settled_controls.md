---
summary: Prolonged Jupyter memory sampling lacks host baseline and settled controls
issue: uibcdf/molsysmt#723
status: open
opened: 2026-11-11
closed:
severity: medium
verification: upstream
area: [tests, diagnostics]
guard:
normative:
blocked_by: []
supersedes: []
---

# Qualifying prolonged Jupyter memory observations

## What

MolSysViewer reports memory growth in plain Jupyter controls without molecular
imports, and a difference between the receiver's raw same-task heap observation
and later settled/CDP samples. The receiver currently calls exposed GC, reads
performance.memory and dereferences weak controllers in one page evaluation.
Those values alone do not establish molecular retention or complete retirement.

## How

Source inspection confirms the same-evaluation GC/heap/WeakRef sequence in
prolonged_session_jupyter.mjs. The independent consumer reports plain-host
controls, default-host versus cell-toolbar diagnostic ablation, a separately
received JupyterLab wheel and three scientific diagnostic cycles. Those
experiments have not been independently rerun here. Their GC timing and heap
API comparison change two factors together; causal contributions remain open.
Original functional and raw measurement results retain their actual scope.

## Why

Receive the method before interpreting memory deltas. MolSysMT owns this
receiver; consumer lifetime attribution remains uibcdf/molsysviewer#315/#356.
This follows #718's corrected input readiness, without reopening its accepted
functional guard or explaining #615's original initialization timeout. Preserve
scientifically correct implementations and distinguish metrology uncertainty
from a proven molecular leak.

## Intended receiving and acceptance

1. Add a bounded plain-Jupyter control with actual package/application identity
   and extension settings; preserve default-host and diagnostic-ablation scope.
2. Observe post-retirement state through a defined asynchronous sequence with
   positive retained-witness and negative retired-object controls. Compare heap
   APIs at the same sampling point before attributing a difference to timing.
3. Keep scientific/window/session assertions, original deadlines and recorded
   resource limits. Receive a concrete owner-reviewed correction and actual
   GUI regressions before another comparable long campaign. No blind replay.
4. Preserve failures, raw/settled method labels, exact unchanged inputs, native
   identity and owned-process retirement. Do not disable routine user extensions
   or upgrade the shared environment to make a gate pass. External upstream
   publication retains its separate prior-authorization requirement.

## Scope and next action

Admitted under #334's P4 polishing intake. Review the concrete bounded receiver
proposal from the reporter; independently receive the measurement method before
selecting long-run inputs. #718 is a separate readiness/provenance closure.
No public molecular API, scientific algorithm, dependency floor or new score
weight is requested. Candidate construction, hosted qualification and
publication remain paused; installed/final-pair and human acceptance stay open.

## Provenance

2026-11-11 local intake. The owning issue records the reported c5115dff client,
matched aee7aa65 scientific Python bytes, canonical 4ffb82e4 native binary,
PyUnitWizard development copy, host controls and diagnostic scopes. Source
inspection alone does not independently validate all reported experiments.
