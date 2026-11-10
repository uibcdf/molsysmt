---
summary: Generated PDB provenance hard-codes MolSysMT version 1.0
issue: uibcdf/molsysmt#680
status: active
opened: 2026-11-09
closed:
severity: low
verification: reproduced
area: [form, diagnostics]
guard: tests/form/molsysmt_MolSys/test_pdb_producer_version.py
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


## Actual writer receiving — 2026-11-09

Three actual public PDB writes reproduce the old false producer version. The
writer now reads the imported package's cached __version__, splits long version
strings losslessly into <=80-column REMARK records and retains a separate dated
creation record. Scientific ATOM/HETATM/CONECT/CRYST1/MODEL records remain exact.
No runtime Git, distribution query or subprocess is added.

The owned benchmark normalizer accepts only the known leading writer block,
stores all original records and raw/prepared digests, and replaces that block
with two deterministic records. Its @2 metadata records both source/prepared
record counts, allowing exact reconstruction even with long continuation lines.
Scientific records and existing caller files remain untouched. Broader native
writer tests and actual tiny benchmark production remain due before closure.
