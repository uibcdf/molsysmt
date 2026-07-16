# Heavy Memory-Pressure Warning Flood

**Status:** resolved 2026-07-13

## Problem

`ChunkedExecutor._execute_heavy()` checks process RSS after every chunk and emits
a `MemoryPressureWarning` every time the configured threshold is exceeded. A
single run can therefore emit tens or thousands of nearly identical warnings.

The heavy heuristic integration test currently demonstrates this behavior: its
deliberately small RAM budget produces one warning for each processed chunk.
This obscures other diagnostics and adds avoidable overhead.

## Required resolution

- Emit once on threshold crossing, then rate-limit or report only meaningful
  pressure increases.
- Add a final summary with maximum pressure and affected chunk range when useful.
- Distinguish an intentionally tiny test budget from actionable production
  pressure in tests.
- Add warning-count and re-arm tests (for example, pressure drops below and later
  crosses the threshold again).

Memory pressure must never hide or replace the scientific failure that caused a
chunk to abort.

## Resolution

The executor now emits once when pressure crosses the threshold, remains quiet
while pressure stays high, and rearms after pressure returns to or below the
threshold. Tests cover continuous pressure and a high-high-low-high sequence.
