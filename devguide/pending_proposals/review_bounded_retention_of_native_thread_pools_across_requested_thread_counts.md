---
summary: Review bounded retention of native thread pools across requested thread counts
issue: uibcdf/molsysmt#652
status: open
opened: 2026-11-08
closed:
verification: inspected
area: [performance, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bounded lifetime of native thread pools

## Observation and limits

`rust/src/threads.rs` stores an Arc<ThreadPool> for every requested worker count
in a static HashMap. Entries are never evicted. Repeating one count reuses its
pool; distinct counts can retain the sum of their worker threads until process
exit. `RAYON_NUM_THREADS` does not override an explicitly supplied pool size.
The public session/per-call num_threads contract controls active calculations,
not a global count of every retained OS thread.

This is source inspection on `fbafc69a5`, not an isolated measured leak or proof
that this cache caused the shared-host pressure. #612's first full four-worker
attempt hits its 128-task cap; the corrected cap prevents those failures and
later observes more than 128 tasks. Other native providers, explicit parallel
controls and subprocesses also contribute; do not attribute all tasks to Rayon.
The ordinary source test corpus deliberately exercises different counts.

## Proposed study

Measure a finite fresh-process sequence of supported counts using the existing
native probe and real kernels, with live OS threads/RSS and repeated-count
controls. Compare bounded LRU/thread-budget policies and transient pools against
current reuse, preserving exact per-call/session semantics, concurrent/nested
calls and numerical outputs. Evaluate drop/join behavior outside cache mutexes,
no deadlock and performance for repeated and alternating sizes before changing
Rust. A bounded cache must not silently ignore the requested parallelism.

## Ownership and acceptance

MolSysMT owns its native cache; infrastructure-independent execution allocation
is coordinated with uibcdf/moli#96 and uibcdf/uibcdf-infrastructure#1. No copied
resource scheduler, fixed machine-specific public cap, new placeholder API or
backend-specific molecular state is proposed. Keep explicit inputs, observed
active/cached resources and process-wide limits distinct. Receive meaningful
lifetime/concurrency and numerical guards plus workload/time/memory evidence.

Priority remains an owner decision after isolated measurement. This inspected
optimization proposal is not a proven scientific defect or an automatically
added initial-1.0 gate. Existing bounded controllers protect the source campaigns;
no Rust implementation or scientific/performance qualification is changed here.

The current builder uses expect on pool-creation failure; an eventual revision
should also evaluate an ordinary structured resource error instead of a Rust
panic, using a finite subprocess stress control. This is inspected failure-path
behavior, not a newly executed exhaustion test. Do not stress the shared host.
