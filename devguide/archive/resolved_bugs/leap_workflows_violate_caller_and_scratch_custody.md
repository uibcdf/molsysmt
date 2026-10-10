---
summary: LEaP workflows violate caller and scratch custody.
issue: uibcdf/molsysmt#373
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: reproduced
area: [build, tests, performance]
guard: tests/third_party/tleap/test_tleap.py
normative:
blocked_by: []
supersedes: []
---

# LEaP workflows violate caller and scratch custody

**Reported:** 2026-10-10 during uibcdf/molsysmt#371.
**Status:** Repaired; controlled child/workflow guards pass.

## What

The developer check runs its child in the caller directory, allowing a generated
`leap.log` to replace existing evidence. `TLeap.run()` allocates scratch before
input copying enters its cleanup scope and suppresses rmtree errors. The LEaP
peptide builder removes intermediate storage only after successful conversion.

## How

- `devtools/tleap/check_tleap.sh` now resolves the executable before changing
  directory and runs the child inside its generated scratch. The existing EXIT
  trap retires that directory; absolute/relative paths containing spaces work.
- `molsysmt/third_party/tleap/tleap.py` includes input copying inside its existing
  finally boundary and propagates directory-removal errors. Explicit directories
  and requested retention remain caller-owned. The original cwd is restored.
- `molsysmt/build/build_peptide.py` uses a managed directory around preparation,
  execution and conversion. The bridge still delegates to the existing TLeap tool.

## Why

Caller evidence must not be overwritten by a developer check, and failed optional
workflows must not accumulate unowned intermediates. These are existing contract
repairs; no force-field criterion, engine default or public signature changes.
Shared resource governance remains uibcdf/molsyssuite#104.

## What is measured and what is assumed

On source `70d1400b9514904fbf9b1a5ca126ddf4591e63dc`, four private real child
checks fail custody assertions. The runtime LEaP/builder selection records five
failures and eleven successful controls. Failures cover copy/setup/start/run/
conversion boundaries and an injected unlink denial. After repair the combined
memmap/LEaP resource scope passes 30 cases.

The Bash checks execute a private inert Python child and preserve its receipt
outside scratch. Runtime error guards use controlled child/converter substitutes.
No real AmberTools or scientific calculation executes in those reproductions.
The initial after-repair attempt also caught two test-receipt mistakes: child
error output belongs to stderr, and the injected PermissionError needed real
errno/strerror fields for shutil's error reconstruction. Correcting those retains
custody and visible-error assertions; neither changes the product contract.

## What was refuted

An EXIT trap alone is insufficient when the child writes outside its scope.
Cleanup after successful conversion does not cover preparation or parser failure.
Ignoring removal errors prevents the caller from knowing scratch remains.

## Scope and exclusions

Preserve returned diagnostics, explicit output files, working-directory retention,
parameterization and conversions. Process-global cwd use is documented but not
made concurrent. Generic converter/native-library exceptions are tracked separately
by uibcdf/molsysmt#374.

## Acceptance criteria and guards

- `devtools/tests/test_tleap_check.py`: real private child, both exits, absolute and
  relative executable paths, caller-log custody and retired scratch.
- `tests/third_party/tleap/test_tleap.py`: setup/child failures, explicit retention,
  restored cwd and a visible error from actual rmtree with injected unlink denial.
- `tests/build/build_peptide/test_leap_resource_lifecycle.py`: failure at preparation,
  execution or conversion, plus successful disposal after output conversion.

## Provenance and commands

Linux, shared development Python 3.14.7, 2026-10-10. Commands:

```bash
python -m pytest --receptor=llm -n 12 devtools/tests/test_tleap_check.py
python -m pytest --receptor=llm -n 12 \
  tests/build/build_peptide/test_leap_resource_lifecycle.py \
  tests/third_party/tleap/test_tleap.py
```

The [owner contract](../../temporary_resource_operations.md), public docstrings,
User Guide, Cookbook and affected course modules describe the lifecycle.

Final selected regressions pass 278 cases, both strict docstring renders pass,
and all 14 fast gates pass. Ruff, Bash syntax and parent-signature comparison
also pass. These are local source checks, not installed-package qualification.
