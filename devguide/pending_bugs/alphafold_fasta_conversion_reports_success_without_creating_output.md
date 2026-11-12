---
summary: AlphaFold FASTA conversion reports success without creating output
issue: uibcdf/molsysmt#732
status: active
opened: 2026-11-12
closed:
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/string_alphafold_id/test_fasta_refusal.py
normative:
blocked_by: []
supersedes: []
---

# AlphaFold FASTA export reports a nonexistent file

## What

Both the direct adapter and msm.convert return the requested FASTA pathname
without creating a file. With a pre-existing destination they report success
while leaving its unrelated content intact. A synthetic HTTP response reproduces
this without contacting AlphaFold or deleting caller-owned data.

## How

The converter reads and discards an entry response, then returns output_filename.
It has no implemented sequence parser or writer. The combined baseline has
eight failures/two passes: four missing-refusal cases and #731's four copy cases.
The correction raises the existing catalogued NotImplementedConversionError
before network or filesystem access. Validated public/direct calls and absent/
pre-existing targets are guarded.

## Why

A returned filename falsely promises an output artifact. The existing registry
entry is a compatibility route, not working scientific serialization. Safe
refusal fixes the false-success defect without inventing the scientific meaning
of the export. A model-aware writer and the choice between represented model
positions and a full source sequence are separate post-1.0 work under #733.
No model sequence is inferred from an unrelated full-accession sequence.

## Acceptance and evidence

The operation must fail through SMonitor before I/O, leave an absent output
absent and preserve existing bytes. The corrected combined cohort passes thirteen
cases, including changed docstrings and the copy guards. The source-reference
review must label this route unavailable. Common/HTML receiving and lifecycle
closeout remain due; real network/service and sequence export are not qualified.

## Provenance

Linux/Python 3.14.7; original probe uses published cd6f26523 with test-only
working changes. A one-CPU/1.5-GiB/no-own-swap controller preserves a 6.5-GiB host
reserve. Provider composition and the native binary remain unchanged.
