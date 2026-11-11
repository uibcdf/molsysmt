---
summary: Copying an open legacy H5MSM handler fails with an unstructured path TypeError
issue: uibcdf/molsysmt#712
status: active
opened: 2026-11-11
closed:
severity: medium
verification: reproduced
area: [form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Reporting the unavailable independent-copy route of a legacy handler

## What

`msm.copy(handler)` and `msm.copy(handler, output_filename=path)` on an open
legacy H5MSMFileHandler fail with TypeError from `stat`: the live handler is
passed as a path. Both outcomes are reproduced on `f0dbb58e0`; the source
remains open and unchanged and no destination is produced.

## How

The form copy adapter calls `shutil.copy(item, output_filename)`, although
`item` is a resource-owning H5MSMFileHandler rather than a filename. It does
not implement the advertised independent handler-copy protocol. Adjacent
legacy PDB/GRO handler copies already report an explicit unimplemented route.

## Why

Form recognition and an exported function do not establish independent-copy
support. A low-level path TypeError gives no useful capability boundary and
contradicts the public copy function's structured refusal contract. The older
#450 correction covers file paths, not this live-handler form.

## Decision and acceptance

Report this unavailable route with the existing NotImplementedMethodError and
native diagnostics, preserving the public signature/digestion boundary. Do not
invent a live-resource snapshot protocol during this correction. Explain the
supported alternative: finish a writer first, then use `msm.copy(filename)` for
an independent byte-preserving file copy; or convert to resident MolSys and
copy that object. Direct and universal calls must refuse without creating a
destination or closing/changing the original, under normal and trusted inputs.
Existing path-copy/lifecycle and generic-copy guards remain unchanged.

A future open-handler copy needs a separate contract for writer flushing,
read/write modes, retained cursors, file lifetime and failure cleanup. This
correction does not implement or certify that capability.

## Provenance

2026-11-11; Linux/Python 3.14.7, MolSysMT `f0dbb58e0`, frozen client/provider
composition matching the separate full run. The one-CPU/one-GiB probe uses only
an open bundled read handle and its own temporary destinations. Raw exceptions
and unchanged-input hashes are retained privately under #334.

## Local correction receiving

The original combined guards fail 20 cases and pass three positive controls.
The corrected expanded cohort passes 85 cases with no skips, including native
creation, direct/universal copy refusal, file-copy/lifecycle, legacy handler
conversion and a real public file-copy doctest. Original failures are retained.
Two actual documentation examples execute under nm/ps and pm/fs with unchanged
input bytes, physical coordinates, declared shapes and closed owned handles.
This is bounded source receiving, not full-suite or installed acceptance.
