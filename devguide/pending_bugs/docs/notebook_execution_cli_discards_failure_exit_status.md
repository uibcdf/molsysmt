---
summary: Notebook execution CLI discards failure exit status
issue: uibcdf/molsysmt#260
status: active
opened: 2026-09-29
closed:
severity: high
verification: reproduced
area: [docs, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Notebook execution CLI discards failure exit status

**Reported:** 2026-09-29, while executing the updated Luzard-Chandler tutorial.
**Status:** Active; notebook execution failure reported with successful CLI status.

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
