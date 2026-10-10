---
summary: Failed persistent-result construction leaks backing storage.
issue: uibcdf/molsysmt#372
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: reproduced
area: [build, tests, performance]
guard: tests/heavy/test_persistent_result.py::test_failed_mapping_retires_only_owned_storage
normative:
blocked_by: []
supersedes: []
---

# Failed persistent-result construction leaks backing storage

**Reported:** 2026-10-10 during the resource-owner review, uibcdf/molsysmt#371.
**Status:** Repaired; owned construction scratch is retired on failure.

## What

The result constructor allocates a backing file before opening the NumPy memmap.
A mapping error leaves that file without a returned handle or cleanup owner.
On original source `70d1400b9514904fbf9b1a5ca126ddf4591e63dc`, two mapping-error
cases retain the file, and the retirement-failure guard confirms cleanup is not
attempted. The other seven selected handle controls pass.

## How

The allocation in `molsysmt/_private/execution/persistent_result.py` now encloses
mapping construction in a failure cleanup boundary. It retires only its own
file and re-raises the original error. If retirement itself fails, that error
propagates with the mapping error as its exception context. Caller paths remain
caller-owned; requested write-mode mapping may still write to those paths.

## Why

Failed allocation can accumulate orphaned disk storage. This restores resource
custody without changing molecular calculations, dependencies or public APIs.
Shared policy coordination is uibcdf/molsyssuite#104.

## What is measured and what is assumed

Private mapping failures exercise ValueError and OSError without large allocation.
The combined initial handle/developer-check run reports 7 failures and 7 passes;
three failures are these handle cases. Context failure also checks successful
handle allocation and actual unlink. The final combined repair scope passes
30 tests. Injected retirement failure is control-flow evidence, not a real OS
permission-fault or Windows qualification claim.

## What was refuted

Cleanup after a returned handle already works; the missing boundary is construction.
Deleting caller-provided paths would be a second defect, not a repair.

## Scope and exclusions

Owned construction failure and visibility of removal errors only. No new lifetime
API, idempotent cleanup contract, memory estimator, flush policy or format change.

## Acceptance criteria

Mapping failure retires owned scratch, preserves caller files, and reports a failed
retirement with both exceptions. Existing handle/context controls remain passing.

## Provenance and commands

Linux, shared development Python 3.14.7 / NumPy 2.4.6, 2026-10-10. The original
source above was executed before repair with:

```bash
python -m pytest --receptor=llm -n 12 tests/heavy/test_persistent_result.py \
  devtools/tests/test_tleap_check.py
```

The maintained [owner contract](../../temporary_resource_operations.md) describes
ownership independently of the disposable local test receipts.

Final selected regressions pass 278 cases, both strict docstring renders pass,
and all 14 fast gates pass. Ruff, Bash syntax and parent-signature comparison
also pass. These are local source checks, not installed-package qualification.
