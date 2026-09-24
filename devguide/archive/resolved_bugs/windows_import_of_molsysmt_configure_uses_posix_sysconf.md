---
summary: Windows import of molsysmt.configure fails because os.sysconf is unavailable
issue: uibcdf/molsysmt#239
status: resolved
opened: 2026-09-24
closed: 2026-09-24
severity: high
verification: reproduced
area: [config, build]
guard: tests/test_configure.py::TestConfigVariables::test_physical_memory_uses_windows_api_without_sysconf
normative:
blocked_by: []
supersedes: []
---

# Windows import of molsysmt.configure fails because os.sysconf is unavailable

**Reported:** 2026-09-24, during the exact staged-pair gate for
uibcdf/molsysmt#195.
**Status:** resolved. The source correction, local regression tests and the
corrected staged Windows installed-pair gate all pass.

## What

All three Windows cells in hosted run `35961600369` installed the exact
MolSysMT 0.22.0 build 4 and MolSysViewer 0.23.1 build 1 pair. During the
offline BCIF check, importing `molsysmt.configure` raised:

```text
AttributeError: module 'os' has no attribute 'sysconf'
```

The converter and Viewer checks were not reached on Windows.

## How

`molsysmt/configure/__init__.py` calculated `max_ram_usage` at import time
with `os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")`. That API is
not present in Windows Python. The correction keeps `sysconf` on POSIX and
queries `GlobalMemoryStatusEx` on Windows, using `ullTotalPhys` for the same
50%-of-physical-RAM default. The Windows API structure and its initialization
follow the Microsoft `MEMORYSTATUSEX` contract.

## Why

The unconditional import failure blocks the public conversion path and all
other MolSysMT operations importing configuration on Windows. It is a code
defect, not a Conda solver or package-upload problem. It prevents an honest
Windows release claim.

## What is measured and what is assumed

**Measured:** all Windows Python 3.11, 3.12 and 3.13 jobs of run
`35961600369` reached the installed-pair validator and failed there; the
Python 3.13 traceback names `configure/__init__.py` and `os.sysconf`.
The local regression tests simulate both the POSIX and Windows branches
without depending on host OS.

**Measured:** targeted producer run `35963198451` published the additive
Windows ABI3 build 5 from commit `ec5cbd41bf121f595fbb88e16f9aa9f3728581ea`.
An independent channel inventory confirmed its staging label. Exact-pair
run `35964451004` then passed all three Windows Python jobs, including BCIF,
PDB-text, Viewer and explicit-environment checks; each job uploaded its
environment record.

## What was refuted

The failure is not caused by missing Conda support packages: the install step
completed. It is not caused by missing optional Biopython: the traceback
terminates at the configuration import before form detection.

## Scope and exclusions

This report covers portable default memory-budget discovery and its installed
Windows check. The separate evidence-export failure on ARM and macOS, where
`conda` is absent from micromamba-only runners, remains under
uibcdf/molsysmt#195.

## Acceptance criteria

1. Windows import of `molsysmt.configure` succeeds without `os.sysconf`.
2. POSIX retains the existing physical-memory budget semantics.
3. Regression tests cover both paths and the Windows API failure.
4. A clean installed staged pair passes the Windows cells of the exact-pair gate.

All four criteria are met. The guard named in front matter simulates the
Windows API without `os.sysconf` and fails if the POSIX-only import path
returns. The complementary POSIX and failure-path tests live in the same
module.

## Provenance

GitHub Actions run `35961600369`, Windows 2025 runners, Python 3.11--3.13,
MolSysMT 0.22.0 ABI3 build 4 and MolSysViewer 0.23.1 noarch build 1,
2026-09-24.
