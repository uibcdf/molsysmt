---
summary: Legacy H5MSM creation truncates a destination before rejecting an unsupported schema
issue: uibcdf/molsysmt#711
status: active
opened: 2026-11-11
closed:
severity: high
verification: reproduced
area: [form, data]
guard:
normative:
blocked_by: []
supersedes: []
---

# Rejecting an unsupported legacy schema before opening a destination

## What

`H5MSMFileHandler(path, io_mode="w", format_version="1.0")` raises FormatError,
but creates a new HDF5 file or truncates an existing destination first. A small
private probe on source `f0dbb58e0` preserves its real exception and records that
caller-owned bytes no longer match after rejection. No bundled/user input is
modified by the probe; only its own temporary targets are used.

## How

`native/h5msm_file_handler.py::_new_msmfile` calls `h5py.File(filename, "w")`
before checking the requested version against the legacy 0.3/0.4 allowlist.
This is the low-level legacy writer; public default 1.0 writing has a separate
modular implementation and must not be routed through it.

## Why

An unsupported request can destroy an existing destination even though no
writer is returned. This is a data-integrity defect, not a reason to disable
valid legacy writes or change the public modular default.

## Decision and acceptance

Move the existing exact-version validation ahead of file opening. Keep the
same supported/default versions and structured FormatError. Unknown requests
must not open/create/truncate destinations, including an existing ordinary
file or valid HDF5 file. Positive 0.3/0.4/default writing and existing handler
read/boundary tests must still pass. This bounded change does not claim atomic
creation for every unrelated invalid option or interrupted HDF5 write.

## Provenance

2026-11-11; source `f0dbb58e0c0a2d29bdc74024a3f888c002a9a2f0`, Linux/Python
3.14.7, published PyUnitWizard 0.29.2 overlay and unchanged native ABI3 4ffb82e4.
The probe runs under a 1-CPU/1-GiB/no-swap scope after checking aggregate host
headroom while the separate full-source suite is active. Related #411/#256
read/schema boundaries remain separate. The owning source-polish work is #334.

## Local correction receiving

The original combined guards fail 20 cases and pass three positive controls.
The corrected expanded cohort passes 85 cases with no skips, including native
creation, direct/universal copy refusal, file-copy/lifecycle, legacy handler
conversion and a real public file-copy doctest. Original failures are retained.
Two actual documentation examples execute under nm/ps and pm/fs with unchanged
input bytes, physical coordinates, declared shapes and closed owned handles.
This is bounded source receiving, not full-suite or installed acceptance.
