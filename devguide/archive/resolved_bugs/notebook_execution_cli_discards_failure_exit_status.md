---
summary: Notebook execution CLI discards failure exit status
issue: uibcdf/molsysmt#260
status: resolved
opened: 2026-09-29
closed: 2026-09-29
severity: high
verification: reproduced
area: [docs, tests]
guard: devtools/tests/test_execute_notebooks_cli.py::test_cli_exits_nonzero_when_any_notebook_fails
normative:
blocked_by: []
supersedes: []
---

# Notebook execution CLI discards failure exit status

**Reported:** 2026-09-29, while executing the updated Luzard-Chandler tutorial.
**Status:** Resolved; the CLI aggregates failures and exits nonzero.

## What

`python docs/execute_notebooks.py -q
docs/content/user/tools/hbonds/get_luzard_chandler_hbonds.ipynb` reported
`PermissionError` when the sandbox prevented the Jupyter kernel from opening
local sockets. Its final summary said one notebook failed, but its process
exit code was 0. The same tutorial subsequently executed successfully with
the required local socket permission; this report concerns the CLI status,
not the tutorial or that sandbox restriction.

## How

`docs/execute_notebooks.py::main` returns the number of failed notebooks.
The CLI entry point discards the return value in every input branch and
terminates normally. Missing paths also only print a message. Consequently
an automation consuming the process exit code can accept failed execution.

## Why

Documentation validation and hosted jobs need a truthful failure signal.
Human-readable failure text is insufficient for a gate that accepts code 0.

## Scope and exclusions

Aggregate execution failures across requested files/directories and return a
nonzero exit code when any input fails or is missing. Preserve successful
execution, quiet reports, and code-fingerprint handling. This does not change
Jupyter kernel permissions, scientific code, or notebook contents.

## Acceptance criteria

A process-level test must run the real CLI with a controlled failing notebook
execution command and assert a nonzero exit status. A success control and a
mixed multi-input case must preserve success and failure aggregation. Missing
inputs must also fail. The guard must fail on the original entry point.

## Provenance

Observed on Linux x86_64, Python 3.13.14, on 2026-09-29. The exact local
failure was blocked socket creation during Jupyter startup; no network
download or missing scientific dependency was involved.

## Resolution

The CLI now sums failure counts across all requested files and directories,
counts missing inputs as failures, and exits with status 1 when any input
fails. Successful runs keep status 0. The function-level missing-path branch
also returns a failure count consistently.

The process-level guard runs the original CLI entry point in a subprocess,
controlling only the external Jupyter command result. It fails on the
original runner for one failing notebook and both mixed-input orders. The
missing-input test also fails on the original runner; its success control
passes. Together these produced four failures and one pass before the fix,
and five passes afterward. This checks the signal consumed by automation,
without requiring a live kernel or socket permissions. The scientific
Luzard-Chandler tutorial separately executed all six cells successfully.
