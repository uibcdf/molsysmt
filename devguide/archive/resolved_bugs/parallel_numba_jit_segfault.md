# Intermittent Parallel Numba JIT Segmentation Fault

## Status

Resolved on 2026-07-22. The native crash was not caused by a
demonstrated Numba compilation race. Canonical element selection removed repeated
atom indices from an ordered group relation, while the group-size array retained
the repetitions. The compiled center kernel consequently read beyond the supplied
coordinate array. The deterministic reproducer, an affected-surface gate of 1,819
tests, and the complete 9,417-test suite all pass after the correction.

The investigation hypotheses below are retained as historical reasoning. The
root-cause and final-validation sections supersede their provisional conclusions.

## Evidence

The command below was run with a cold or partially invalidated JIT state on
Python 3.13.12:

```bash
python -m pytest -q -n 12
```

Near 96% completion, three xdist workers terminated with `SIGSEGV`. Their Python
traces ended in `molsysmt/_private/jit.py` while executing compiled geometry
kernels through `get_center()` and `get_distances()`. The test suite then
continued with replacement workers. After the conversion-selection defect found
in the same run was corrected, two complete repetitions of the identical
12-worker command finished without a crash; the final repetition was fully
green.

At that point this was evidence only of a possible race or native-runtime
stability problem. The later deterministic reproducer demonstrated that this
initial interpretation was incomplete.

## Impact

- A cold parallel CI run may terminate workers nondeterministically.
- A worker crash can obscure ordinary assertion failures and lengthen diagnosis.
- The observation strengthens the existing motivation to reduce dependence on
  Numba warm-up, but it is not by itself evidence that Rust migration is the
  only solution.

## Investigation plan

1. Reproduce from a deliberately isolated empty Numba cache with 12 workers.
2. Repeat the same test order with one worker and with JIT disabled.
3. Capture the first native stack with `faulthandler` and, if reproducible,
   `gdb` or an equivalent native debugger.
4. Distinguish concurrent compilation from concurrent execution by warming all
   relevant kernels in one process before starting xdist.
5. Record Numba, llvmlite, NumPy, compiler, CPU, and Python versions with every
   reproduction.

## Acceptance criteria

- A deterministic reproducer identifies whether compilation, cache loading, or
  kernel execution is responsible; or a documented stress campaign completes
  repeatedly without a crash and provides enough evidence to close this report.
- Any fix has a focused stress test in addition to the ordinary full suite.
- Normal scientific geometry results remain covered by the existing serial and
  external-oracle tests.

## Investigation log — 2026-07-22 (NOT reproduced)

> **These experiments are expensive in wall-clock time (the campaign below took
> roughly 2 hours of near-full-CPU load). Do not re-run them casually.** They did
> not reproduce the crash; repeating them without a new, concrete lead is unlikely
> to add information and should not be a default step when touching the geometry
> kernels. Re-run only if the segfault is observed again *and* a fresh hypothesis
> (e.g. a specific dirty-cache state) motivates a targeted variant.

Environment matched the original observation: Python 3.13.12, numba 0.64.0,
llvmlite 0.46.0, numpy 2.3.5, pytest 9.0.2, pytest-xdist 3.8.0, Xeon E5-2630 v4
(10c/20t), Linux 6.17. Every run used an **isolated temporary `NUMBA_CACHE_DIR`**;
the global `.numba_cache` and source `__pycache__` were never touched. pytest was
the authority; `faulthandler` was enabled everywhere.

Controlled matrix over the geometry subset (`get_center`, `get_distances`,
`get_geometric_center`, `center`, `move_away`, `pbc`, `lib`; 185 tests) plus two
direct kernel stressors:

- serial cold cache — 185 passed, 0 crash;
- `pytest -n 12` cold cache — **15 reps**, 185 passed each, 0 crash;
- `pytest -n 12` warm cache — 5 reps, 0 crash;
- barrier-synchronised concurrent **compilation** race (12 processes, cold shared
  cache, only the `get_center.py`/`get_distances.py` kernels) — **200 iterations
  = 2400 concurrent cold compiles, 0 crash**;
- concurrent parallel **execution** under oversubscription (12 processes, warm
  cache, `parallel_mode=True`, 720k-element payload) — **30 iterations
  = 14,400 multithreaded calls, 0 crash**;
- JIT disabled, serial and `-n 12` — ordinary test failures only (numba-only
  constructs break under `NUMBA_DISABLE_JIT=1`), **no SIGSEGV** (a control:
  without native JIT code there is no segfault).

Aggregate: ~2,415 cold parallel compilations of the implicated kernels and ~14,400
concurrent multithreaded executions produced **zero SIGSEGV / SIGABRT / faulthandler
dumps**. For those kernels, the barrier stressor applied more simultaneous
compilation pressure than xdist's staggered startup normally does; it did not
reproduce the broader module-import and native-workload surface of the full suite.

**Conclusion:** not reproduced under a substantial (geometry-focused) campaign on
this exact environment. The campaign provides strong negative evidence against a
deterministic geometry-kernel defect and against a readily reproducible threading
failure. It does not identify the cause of the original worker crashes.

An audit of Numba 0.64.0's actual cache implementation corrects an important early
hypothesis: the kernels in one Python source file do **not** share one `.nbi` cache
index. `CacheImpl` builds the filename base from the module, qualified function
name, and source-line disambiguator. The local artifacts confirm names such as
`get_distances.get_distances_single_system-24.py313.nbi`. A collision between the
four or seven different kernels in the same file is therefore not a valid proposed
mechanism.

`IndexDataCacheFile.save()` still performs an unlocked read-modify-write of each
function's index, so a cross-process race remains possible when the *same function*
is compiled concurrently for different cache keys. However, these MolSysMT kernels
have fixed signatures and the workers in the observed run used the same host and
configuration. The existence and relevance of such a race are consequently
unproven here; the atomic temporary-file replacement alone is not evidence that it
caused the crash.

Leading hypotheses, without assigning unsupported probabilities, are now:

1. an unrecovered transient in Numba, LLVM, its threading runtime, or native cache
   loading during the wider full-suite run;
2. a dirty or incompatible persistent cache state, although no exact corrupt state
   was captured and the clean-cache campaign cannot test this;
3. an interaction elsewhere in the full-suite native workload rather than in the
   geometry-only surface;
4. a geometry-kernel memory-safety defect, for which the campaign provides strong
   negative evidence.

No fix is implemented or currently justified. Reopen active investigation if a
worker crashes again, preserving the cache directory and native crash evidence
before any cleanup.

### Conditional diagnostics (not yet implemented; never in the default gate)

1. **Cold parallel stress** (`@pytest.mark.stress`): the geometry subset under
   `-n <N>` with a fresh isolated `NUMBA_CACHE_DIR`, asserting no worker exits on a
   signal. Retain the harness for targeted manual use after a new observation; the
   two-hour campaign does not justify adding it to routine nightly work.
2. **Barrier compile-race harness**: a hardened, marked subprocess test that spawns N
   processes which cross a barrier and then force cold compilation of the
   `get_center.py`/`get_distances.py` kernels into one shared cache, asserting all
   child exit codes are 0 over K iterations. Use only if a future crash again points
   to concurrent compilation; the present version has already completed 2400 runs.
3. **Captured-cache reproducer**: if the failure recurs, preserve a copy of the exact
   cache and reproduce from that artifact in a subprocess. Synthetic deletion is
   not equivalent evidence: Numba treats a missing `.nbc` as a cache miss and
   recompiles. A deliberately truncated `.nbc` may still be useful for evaluating
   clean failure behavior, but it tests generic corruption handling rather than the
   cause of the observed crash.

### Defensive options (not implemented — cause not demonstrated)

The cause is not proven, so no library change is proposed. If future evidence makes
defensive CI hardening worthwhile, the actual guarantees and costs are:

- **A — Pre-warm registered kernels serially before xdist starts**: this can reduce
  concurrent compilation, but only for factories registered in modules imported by
  the controller. It does not validate or neutralize an already corrupt cache and
  therefore must not be presented as a fix for the original observation.
- **B — Per-worker isolated `NUMBA_CACHE_DIR`** keyed by `PYTEST_XDIST_WORKER`:
  eliminates cross-worker cache sharing; cost is up to N-fold compilation and it
  cannot be combined directly with one shared pre-warmed cache.
- **C — Per-run fresh shared cache**: set `NUMBA_CACHE_DIR` before Python starts,
  reuse it across the workers for that run, and discard it afterwards. This avoids
  persistent dirty state but does not eliminate same-run concurrent writes.
- **D — Pre-warm then use a read-only cache**: potentially provides the strongest
  CI isolation, but requires proving that every required kernel and cache key was
  warmed and that Numba behaves correctly when an unexpected key cannot be saved.

Historical recommendation before recurrence: keep the library untouched and
preserve exact cache/native evidence if the crash recurs. The recurrence and
deterministic reproducer below superseded this recommendation and justified the
targeted library correction.

## Recurrence log — 2026-07-22

The crash recurred during ordinary 1.0 consolidation work, without a synthetic
stress harness:

1. A focused 89-test command using `python -m pytest --receptor=llm -n 12`
   terminated multiple workers with `SIGSEGV`. A faulthandler trace ended at
   `molsysmt/_private/jit.py:167`, reached from `get_center()` inside
   `get_distances()`. The run finished with one worker reported as not properly
   terminated.
2. The same functional surfaces were then run serially with
   `python -m pytest --receptor=llm`. That process also exited with signal 11
   (`exit 139`) at the same `jit.py:167 -> get_center()` boundary.

No `NUMBA_CACHE_DIR` environment variable was set for either run and the active
SMonitor profile resolved to `user`. Under that profile, `_private/jit.py` does not
redirect the cache to the repository-level `.numba_cache`; Numba therefore used
its default source-adjacent cache. The serial recurrence after the parallel crash
is important new evidence: it is consistent with a persistent cache artifact
created or exposed by the parallel run, and is not explained by execution-time
thread oversubscription alone.

This recurrence does not yet prove cache corruption, but it changes the next
experiment. Preserve the source-adjacent cache, repeat the failing functional
selection with a fresh isolated `NUMBA_CACHE_DIR`, and compare it with a subprocess
that reuses the preserved default cache. Do not repeat the broad two-hour clean
stress matrix; it already answered a different question.

## Root cause and correction — 2026-07-22

The exact failing test was reduced to:

```bash
python -m pytest -vv \
  tests/structure/get_distances/test_get_distances_from_molsysmt_MolSys.py::\
test_get_distances_from_molsysmt_MolSys_groups_13
```

It crashed deterministically with both the existing default cache and a fresh,
isolated `NUMBA_CACHE_DIR`. This rules out dirty persistent cache state as a
necessary condition for the reproduced failure.

The test computes 21 distances between group centers. Atoms legitimately recur
across those groups. `get_center()` built `atoms_per_group` from the full ordered
relation, then requested coordinates through the canonical public selection path,
which sorted indices and removed repetitions. The Numba kernel therefore received
fewer coordinate rows than `sum(atoms_per_group)` and performed an out-of-bounds
native read.

The correction keeps the public selection contract canonical. Ordered relations
now read each unique atom once and reconstruct order and multiplicity with the
inverse index before invoking the kernel. The same mapping is applied in eager and
chunked execution. A Python-side native-boundary check now rejects any mismatch
among coordinate count, weight count, and summed group sizes before compiled code
can run.

The deterministic reproducer passes after the correction. Related ordered
relations in distance pairs, angle triplets, dihedral quartets, hydrogen-bond
donor/hydrogen pairs, and NGLView contact endpoints were audited and adapted to the
same distinction between canonical sets and ordered relations. The preserved cache
copy remains in `/tmp/molsysmt-numba-crash-20260722/` for the duration of this
development session, but it is no longer the leading causal artifact.

## Final validation

The following gates passed with a fresh isolated Numba cache:

- affected native, structural, PBC, scientific-truth, H5MSM, hydrogen-bond, and
  NGLView surfaces under 12 xdist workers: **1,819 passed**;
- complete repository suite under 12 xdist workers: **9,415 passed, 2 skipped**
  from 9,417 collected tests, with no worker crash or faulthandler dump;
- `ruff check molsysmt tests`: **all checks passed**.

The regression coverage includes the formerly crashing repeated-group case and
external geometry agreement against MDTraj and MDAnalysis. This satisfies the
acceptance criteria and the report can be archived as resolved.
