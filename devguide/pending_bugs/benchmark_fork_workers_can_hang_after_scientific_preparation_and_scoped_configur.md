---
summary: Benchmark fork workers can hang after scientific preparation and scoped configuration.
issue: uibcdf/molsysmt#676
status: active
opened: 2026-11-09
closed:
severity: medium
verification: reproduced
area: [performance, tests]
guard: devtools/tests/test_benchmark_worker_lifecycle.py
normative:
blocked_by: []
supersedes: []
---

# Benchmark workers inherit runtime state and may wait indefinitely

## What

The competitive harness forces fork after molecular/native/unit preparation and
holds scoped configuration in the parent. A real four-atom/three-structure
campaign never returns from its first timing worker. The outer service stops it
after 180 seconds: 7.309 CPU seconds and 291M displayed peak memory, no observed
memory pressure or reserve event. This is an incomplete attempt, not a numeric
failure, resource exhaustion or a successful benchmark.

## How

The retained attempt is benchmark-567-tiny-standards-directed. Systemd's native
Result=timeout and journal preserve its disposition; no final JUnit or complete
supervisor/source-after receipt exists. Do not manufacture those records. The
exact inherited-lock/native-runtime component remains unassigned; no PyUnitWizard,
Rayon or third-party defect is asserted. Python documents the problems of fork
with inherited multithreaded state and the fresh-interpreter spawn alternative:
https://docs.python.org/3.14/library/multiprocessing.html#contexts-and-start-methods

## Why and correction

Numerical validation before timing is required by #567/#673. It must not make
measurement hang by inheriting that initialized process. Competitive cases now
supply importable factories plus paths and scalar policy, construct their own
native objects in a fresh spawn worker, recheck the actual workload against the
parent declaration, and only then warm/time. No molecular object, live registry,
lock or prepared trajectory is pickled. Startup/preparation remain outside timed
samples. All workers drain their IPC before join, have a finite deadline and
clean up only their own process. Exceptions cannot become zero timings.

The existing arbitrary-closure/fork path remains explicitly legacy and bounded;
its completion/safety after arbitrary user preparation is not certified. New
competitive cases use factories. This does not change MolSysMT's molecular
execution API, global multiprocessing start method or computational backend.

## Receiving so far

The same two tiny full campaigns pass all 21 paths each under spawn: ten selected
controls pass in 116.68 seconds, measured service peak about 502 MiB, host
available memory stays above 13 GiB. These observations qualify evidence transport,
not a performance ranking. All earlier numerical/unit/timeout attempts remain.
Full clean-source receiving and the explicit worker-lifecycle guards are due.
