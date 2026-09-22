---
summary: Ruff cleanliness test passes while scanning zero Python files
issue: uibcdf/molsysmt#232
status: resolved
opened: 2026-09-22
closed: 2026-09-22
severity: medium
verification: reproduced
area: [ci, tests]
guard: devtools/tests/test_ruff_clean.py::test_ruff_clean_across_repo
normative:
blocked_by: []
supersedes: []
---

# Ruff cleanliness test passes while scanning zero Python files

**Reported:** 2026-09-22, while auditing the Ruff migration boundary.
**Status:** Resolved; the test now proves its selected file set covers the maintained
tooling and MolSysViewer add-on before accepting a clean Ruff result.

## What

The first test in `devtools/tests/test_ruff_clean.py` invokes Ruff over the repository
root with `--force-exclude`. It accepts a zero-file run as success:

```text
$ ruff check --no-cache --force-exclude .
All checks passed!
warning: No Python files found under the given path(s)
```

Without `--force-exclude`, `ruff check --show-files .` lists 69 Python files in this
checkout. The separate `test_core_critical_ruff_rules` explicitly targets the core
package and still exercises its narrow rule set.

## How

`devtools/tests/test_ruff_clean.py:9` passes `--force-exclude` with `.` as the sole
path. The configured `extend-exclude` contains `molsysmt`, which also matches the
repository root's basename when exclusion is forced. Ruff reports no selected Python
files but returns zero. The test checks only that return code, so it cannot distinguish
an actual clean scan from an empty one.

## Why

The test named `test_ruff_clean_across_repo` gives a false clean signal for the
maintained tooling and MolSysViewer add-on that the temporary Ruff boundary intends
to cover. A new lint violation there could evade this test. The critical-rule workflow
and the second test continue to protect their explicitly selected core rules, so this
is a gap in one control rather than an absence of all Ruff checking.

## What is measured and what is assumed

Measured on 2026-09-22 with Ruff 0.16.5 and Python 3.13.14:

- `ruff check --no-cache --force-exclude .` exited 0 and warned that it found no
  Python files.
- `ruff check --show-files . | wc -l` returned 69.
- `ruff check --no-cache .` exited 0 without that warning.

The path-component explanation follows from the configured `extend-exclude` and the
observed difference between the two commands; it does not depend on a proposed fix.

## What was refuted

The clean exit does not prove that the configured boundary is clean: Ruff itself
reports an empty selection. Removing the temporary core exclusion is a separate,
larger migration tracked by `uibcdf/molsysmt#212` and is not necessary to fix this
test.

## Scope and exclusions

This report concerns the zero-file success of the repository-wide cleanliness test.
It does not claim that the critical-rule test is empty, nor does it require the full
legacy-core migration to be completed now.

## Acceptance criteria

- The cleanliness test invokes Ruff on the intended currently maintained Python
  boundary and fails when Ruff selects no files.
- A regression test proves that the gate fails if the selected file set becomes
  empty; it must check coverage rather than merely a successful return code.
- The narrow core gate remains active until `uibcdf/molsysmt#212` is resolved.

## Resolution

The test now asks Ruff which files the configured `.` scan selects, requires one
representative file from each of the two currently maintained trees, and then runs
`ruff check --no-cache .` without forced exclusion. The same selected paths and
configuration apply to both commands. A zero-file result fails the set assertion,
so `devtools/tests/test_ruff_clean.py::test_ruff_clean_across_repo` guards this
failure mechanism. The separate critical-rule test still checks `molsysmt`.

## Dependencies and risks

The eventual fix must not accidentally enable the full legacy-core baseline before
its migration. Any explicit file-set check should follow later path-by-path changes
under `uibcdf/molsysmt#212` without becoming a frozen list of all current files.

## Provenance

Local Linux checkout, Python 3.13.14, Ruff 0.16.5, 2026-09-22.
