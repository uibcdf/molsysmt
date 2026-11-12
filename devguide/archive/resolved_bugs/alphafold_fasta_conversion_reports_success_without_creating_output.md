---
summary: AlphaFold FASTA conversion reports success without creating output
issue: uibcdf/molsysmt#732
status: resolved
opened: 2026-11-12
closed: 2026-11-12
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


## Resolution — 2026-11-12

The functional correction is delivered in ed12b039a, with documentation on
clean 4b280fdcb. The final combined cohort passes 254 cases without warnings
or omissions, including 44 actual native/file/string article controls, existing
sequence/native/PDB examples, both repaired adapter boundaries and doctests.
The seven-page strict HTML build has zero warnings and unchanged inputs.
The [receiving record](../../../devtools/data/string_form_reference_receiving_727_731_732_20261112.json)
retains failed attempts, independently matched published source files, notebook
preservation and bounded resource controls. Common/lifecycle receiving follows
separately in the same receipt; this is not complete-source or installed
qualification. Source/native binary and provider-adoption scopes stay explicit.


### Common-check closeout — 2026-11-12

Fifteen common fast gates, generated-index checks and whole-repository Ruff
lint/format pass with unchanged checked inputs. All nine exact task-owned
services are terminal/retired after MainPID-zero checks; no foreign process
is signalled. The receiving record retains resources and native exits.
Source, nightly, client, installed and publication obligations remain separate.
