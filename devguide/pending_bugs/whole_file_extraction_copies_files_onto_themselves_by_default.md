---
summary: Whole-file extraction copies files onto themselves by default
issue: uibcdf/molsysmt#729
status: active
opened: 2026-11-12
closed:
severity: high
verification: reproduced
area: [form]
guard: tests/form/test_whole_file_extraction.py
normative:
blocked_by: []
supersedes: []
---

# Whole-file extraction loses the independent-output contract

## What

A valid one-atom GRO file passed to `msm.extract(filename)` raises
`shutil.SameFileError`. `copy_if_all=False` returns the unchanged source.
The default request should produce an independent result, rather than trying
to copy its source inode onto itself. The source remains unchanged in the
recorded failing GRO probe.

## How

At source 9fa845193, `file_gro/extract.py` replaces a missing output filename
with the input path, then calls shutil.copy because copy_if_all defaults to
True. Source inspection finds the same whole-file pattern in eighteen file
adapters. DCD/XTC already delegate to corrected identity routes; H5MSM/TRJPK
have separately documented identity behavior and are outside this correction.
Mol2's explicitly unavailable extraction is also excluded.

The first probe also uses standard chemical XYZ text, which is not the
coordinate-dump format implemented by file:xyz. Its IndexError is invalid-test
input, not evidence of a second software failure. Use the actual two-integer
structure/atom header in subsequent XYZ tests. Inspect supported XYZ/H5 subset
writers for source-alias safety before calling their destination behavior safe.

## Why

Default independent extraction is a supported basic workflow. Falling through
to a raw SameFileError breaks it and bypasses the existing managed-copy and
catalogued destination-validation machinery. A subset writer that resolves a
missing destination to its source must not overwrite that source.

## Scope and correction

Reuse the existing private copy_file/file_copy_destination tools, preserving
ArgDigest boundaries, optional-engine enforcement, raw bytes, file forms and
explicit copy_if_all=False alias permission. Do not add another temporary-file
registry or alter native extraction, chemical interpretation, H5MSM/TRJPK
identity contracts or unsupported Mol2 extraction. Preserve subset ordering,
quantities and source bytes; reject explicit aliases before writing. Update
public documentation/course guidance and the active #727 file-reference review.

## Acceptance criteria

- Whole-file adapter requests produce independent byte-equivalent managed
  output by default and preserve explicit no-copy behavior.
- Persistent destinations are honored, including when copy_if_all=False;
  attempted copying onto source aliases fails through the existing catalog.
- Actual public GRO/coordinate-dump XYZ workflows and supported subset output
  preserve the source, selected axes and values. Caller-owned sources and
  unrelated files are never registered for automatic deletion.
- Preserve original failures; qualify focused guards, affected doctests,
  documentation and common checks before closure. Do not claim file-format or
  installed qualification from raw-byte copy tests.

## Evidence and provenance

Bounded Linux/Python 3.14.7 probe, one CPU / 1.5 GiB / no own swap, on
9fa845193 with recorded dirty #727 test-only changes. Native 4ffb82e4 and the
existing controlled providers are unchanged. The private file-reference
receiving cache retains probe inputs, native exit, exceptions and source hashes.
The probe process exits successfully after recording the failing API call;
that process exit does not turn the API failure into success.


## Corrected receiving — 2026-11-12

The discriminating baseline has 80 failures and 52 passes. Eighteen default
adapter copies and explicit aliases expose SameFileError; two restart-style
adapters ignore a distinct destination with copy_if_all=False. Actual public
GRO and coordinate-dump XYZ requests reproduce the copy failure. Selected XYZ
output and its three aliases also demonstrate source-overwrite behavior on
synthetic caller-owned fixtures. Those source changes are failures, not accepted
in-place editing.

All eighteen whole-file adapters now reuse copy_file. Explicit no-copy aliases
retain their permission; distinct destinations work regardless of the flag.
XYZ subset output uses file_copy_destination and preserves selected axes and
values in an independent output. HDF5 subset output requires an explicit
independent destination and closes both owned reader/result handles; no
unsupported overwrite or automatic-writer capability is advertised. Original
H5MSM/TRJPK identity and unsupported Mol2 behavior are unchanged.

Corrected original receiving passes 132 cases. An expanded cohort passes 134,
including a real tiny MDTraj HDF5 subset with topology/time/order/source-byte
checks and pre-open destination refusal. No cases are omitted in this controlled
runtime. These are focused source controls, not complete scientific, optional-
provider, platform or installed qualification. Documentation integration and
final source/common checks remain due before closure.

The 136-case lifecycle receiving also executes the new cookbook example under
nm/ps and pm/fs. Original notebook code, outputs and metadata remain unchanged.
Initial lint exposes sixteen unreachable legacy returns after early-return
refactoring and one import-layout mismatch; those are corrected before source
publication. HDF5 automatic subset writing is deliberately not claimed: its
existing external writer requires a distinct explicit destination.
