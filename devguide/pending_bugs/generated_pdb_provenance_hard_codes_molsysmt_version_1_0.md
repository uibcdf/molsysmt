---
summary: Generated PDB provenance hard-codes MolSysMT version 1.0
issue: uibcdf/molsysmt#680
status: open
opened: 2026-11-09
closed:
severity: low
verification: inspected
area: [form, diagnostics]
guard:
normative:
blocked_by: []
supersedes: []
---

# Reporting the actual PDB producer version

## What

The native MolSys to PDB-text writer writes `Created by MolSysMT version 1.0`
literally. The output therefore claims that producer even when the imported
runtime has another version or an explicit unknown version.

## How

Source inspection of molsysmt/form/molsysmt_MolSys/to_string_pdb_text.py finds
the hard-coded version in the REMARK immediately after the dated HEADER.
This surfaced while #567 normalized only benchmark-owned volatile records;
that benchmark now retains the actual cached runtime version separately.
This report is inspected, not a new full PDB round-trip qualification.

## Why

Producer provenance must describe the software used to write the observations.
The version-selection bootstrap was independently repaired in #657; this writer
still bypasses its cached result. No coordinate, connectivity or unit error
is established by this string defect.

## Acceptance criteria

Use the cached version of the imported package; do not query Git, distribution
metadata, network or an external process during scientific writing. Preserve
format-safe REMARK records for long local/unknown version strings, atom records,
units, timestamps and existing PDB readers. Add a real writer regression with
alternate cached versions. Review the benchmark-owned provenance normalization
if the writer record layout changes, so all volatile records stay accounted for.

## Scope

This is a bounded pre-1.0 provenance correction, not a new PDB parser or a change
to scientific data. It remains pending after the independently qualified
#567/#673/#674/#675/#676 checkpoint.
