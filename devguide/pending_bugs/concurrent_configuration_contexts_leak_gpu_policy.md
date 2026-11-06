---
summary: Concurrent configuration contexts leak GPU policy and restore the wrong state.
issue: uibcdf/molsysmt#613
status: open
opened: 2026-11-06
closed:
severity: high
verification: reproduced
area: [configure, concurrency, structure, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Concurrent configuration policy restoration

## What

The context claims thread safety but mutates module-global configuration without
isolation or serialization. Overlapping overrides can leak to unrelated calls
and leave the wrong application policy after both contexts have exited.
`with_configure_overrides` uses this context for per-call GPU options, so direct
context use is not the only affected route.

## How

Reproduced independently of Viewer on native ed09f6453, Python 3.14.7. Two event-
coordinated Python threads enter use_gpu=False and then use_gpu=True. The first
exits before the second. Starting from use_gpu/gpu_mode auto/auto, both contexts
finish with False/False, not auto/auto. A separate observer reads another
thread's temporary False while its context is active. No GPU executes.

The complete deterministic reproduction, bounded waits and final explicit test
cleanup are in #613. A ContextVar already handles parallel settings separately;
that does not isolate the module-level GPU attributes. The complete paginated
544-issue inventory, including open/closed bodies, contained no equivalent report.

## Why

Independent native calculations or Views must preserve explicit per-call and
application backend policy. A per-View molecular edit lock does not isolate
process-global native configuration. This is discovered through #421 / PR #543
and uibcdf/molsysviewer#264; serial consumer receiving does not establish native
concurrent-call safety.

## Acceptance

Define and implement the provider's concurrency contract, including independent
observers, overlapping contexts, nesting and exception restoration. Test the
use_gpu/gpu_mode aliases and other relevant configure overrides through the
public decorated scientific calls. Do not add an addon-only mutex or numerical
fallback, and do not interpret this configuration observation as a verified GPU
numerical failure. No provider repair is included in this contribution.
