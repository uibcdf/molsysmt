# Configuration Context Is Not Thread-Safe

**Status:** Confirmed

## Problem

`molsysmt.configure.configure_context` and `with_configure_overrides` describe
their behavior as thread-safe, but they mutate shared module attributes and
restore them on exit. Overlapping contexts in different threads can observe or
restore each other's values.

The same mechanism controls parallel threads, GPU backend, precision, and cell
list selection, so the race can alter numerical execution policy.

## Evidence

- `molsysmt/configure/__init__.py` stores configuration as module globals.
- `configure_context.__enter__()` calls `setattr(module, key, value)`.
- `__exit__()` restores a snapshot without ownership or synchronization.
- Existing tests cover nested single-threaded restoration, not overlapping
  threads.

## Required resolution

Choose and document one concurrency model:

1. context-local overrides using `contextvars` with wrappers reading effective
   values through accessors; or
2. an explicitly process-global model with locking and a documented prohibition
   on overlapping contexts.

Add deterministic overlapping-thread tests for restoration and isolation. Audit
Numba's process-global thread count separately because context-local Python
settings alone cannot isolate `numba.set_num_threads()`.
