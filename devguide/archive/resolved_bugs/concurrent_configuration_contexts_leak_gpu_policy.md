---
summary: Concurrent configuration contexts leak GPU policy and restore the wrong state.
issue: uibcdf/molsysmt#613
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [configure, concurrency, structure, molsysviewer]
guard: tests/basic/test_configuration_context.py
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

## Owner correction in progress — 2026-11-06

The existing normative configuration contract already chooses process-global
writer serialization, not thread/task-local isolation. The current source lacks
that implementation. The owner correction introduces a full-lifetime reentrant
lock, restores nested/reused contexts on exceptions, validates the complete
name/alias declaration before any mutation and serializes public session setters.
CPU per-call ContextVars retain their separate authority. Decorated calls with
no global override bypass the global writer context so independent CPU calls do
not serialize unnecessarily. Outside observers and direct module assignments
retain their explicitly documented process-global limitations; synchronous
contexts must not span awaits in overlapping async tasks.

Both public context entry routes use ArgDigest's configuration domain. The domain
obtains the owner's data names lazily to avoid configuration/bootstrap recursion;
configuration values otherwise retain their consuming operations' contracts.
GPU aliases reuse the existing digester, and conflicts use SMonitor's structured
exception. Public ArgDigest 0.14.0 source supports this route; no provider floor
or environment change is required. Trusted skip preserves key/alias integrity.

Original receiving records 12 context failures and two passing public-call
controls. Earlier fixture attempts retain two invalid public-class references
and a separate real precision failure; they are not counted as context failures.
An initial owner implementation eagerly imported configure from its domain,
causing an unregistered-domain bootstrap cycle; the lazy domain fixes that
consumer error. First corrected receiving passes 25 cases locally, including the
existing parallel-control suite and the same 25 cases against controlled source
from public ArgDigest tag 0.14.0 (`0fa776af2d271065c60727c28480b20c3ce09aee`).
This is source-floor receiving, not an installed distribution qualification.

The independently reproduced precision mismatch is uibcdf/molsysmt#620 and remains
separate. Final broader receiving, documentation, source publication and owning
closeout are pending. No GPU numerical or Viewer acceptance is claimed.

## Final native source receiving — 2026-11-06

Implemented in `f60e25b7edad28f035429563fd8b46f4d93395f2`. Joint
configuration/parallel/heavy/structure/interactions/PBC receiving passes **4,438
cases**, zero failures/errors/skips. **32 cases**, including the context doctest,
pass against controlled source from public ArgDigest 0.14.0; **500 documentation
cases** and **97 scientific cases across 64 nodes** pass in their stated scopes.
Counts overlap. Ruff, dependency, 156-notebook course and API stability checks pass.
No provider floor, environment or native backend is changed in this block.

The [portable receipt](../../../devtools/data/configuration_serialization_receiving_613_20261106.json)
retains original authoring/runtime failures, the consumer bootstrap correction,
commands/scopes, exact source/backend hashes, warnings and evidence limits.
The minimal course-link receiving now copies the real maintained configuration
page header; its strict warning assertions were not weakened. Both changed
notebooks preserve code, outputs, IDs and metadata. Public source/board delivery
follows this prepared closeout; installed/graphical and release qualification
remain separate.

The accepted process-global contract is fulfilled, without claiming isolation
for outside observers, direct assignments or overlapping asynchronous contexts.
The independent precision mismatch remains uibcdf/molsysmt#620. #524 still owns
installed-runtime closure. Resolving this issue alone does not complete phase 3
or add its ten points to the currently accepted 40% plan progress.
