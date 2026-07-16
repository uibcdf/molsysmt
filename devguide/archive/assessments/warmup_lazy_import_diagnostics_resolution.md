# Warmup Swallows Lazy-Import Errors

**Status:** resolved 2026-07-13

**Severity:** medium — diagnostics, optional dependencies, and benchmarking

## Evidence

`molsysmt/warmup.py` loops over `_LAZY_ATTRIBUTES` when `modules=True` and wraps
each `getattr(molsysmt, attr)` call in `except Exception: pass`.

## Why this is a defect

- Programming errors and broken package imports are indistinguishable from
  unavailable optional capabilities.
- Benchmark warmup can appear successful even though part of the intended
  execution surface was not loaded.
- The behavior conflicts with the repository rule against silent diagnostic
  emission and broad exception swallowing.

## Proposed correction

Return a structured warmup report containing loaded modules, compiled kernels,
expected optional-dependency skips, and unexpected failures. Expected missing
soft dependencies may be recorded without failing the default user workflow;
unexpected exceptions should be surfaced and should fail strict QA mode.

## Acceptance criteria

- No broad exception is silently discarded in the warmup loop.
- User and strict/QA modes have documented behavior.
- The result reports partial warmup rather than only a kernel count.
- Tests distinguish an expected optional dependency miss from an injected
  internal import error.

## Resolution

`warmup()` preserves its integer return by default and optionally returns a
structured report. Missing optional dependencies are reported as skipped;
unexpected failures emit `WarmupFailureWarning`, and `strict=True` propagates
them for QA. Control arguments now pass through ArgDigest, and tests cover all
three outcomes.

The course and maintained guides now use `warmup()` rather than the deprecated
`warmup_numba()` alias. A separate Rust AOT exploration defines the evidence and
packaging gates for eventually making runtime JIT warmup unnecessary.
