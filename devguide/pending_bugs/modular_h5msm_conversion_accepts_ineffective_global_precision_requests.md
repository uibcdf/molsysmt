---
summary: Modular H5MSM conversion accepts ineffective global precision requests
issue: uibcdf/molsysmt#663
status: active
opened: 2026-11-08
closed:
severity: medium
verification: reproduced
area: [convert, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Modular writing accepts ineffective precision requests

**Reported:** 2026-11-08, during the #256 P6 whole-format/default-writer audit.
**Status:** Reproduced; bounded option-validation correction under qualification.

## What

`msm.convert(molsys, to_form='file:h5msm', output_filename=path,
float_precision='single')` succeeds but stores float64 structural datasets.
`int_precision='single'` is also accepted without controlling the field encodings.
Either explicit `double` value instead raises the existing generic ValueError.
The same behavior occurs with default 0.5 and explicit experimental 0.6.

## How

The modular conversion shortcut discards precision keywords equal to their old
legacy defaults, then calls fixed-schema codecs. These write structural floating
series as float64, identity/reference vectors as schema-declared integers and
other typed domain payloads with their declared encodings. Global legacy
precision controls do not implement this behavior. Their silent acceptance is
therefore misleading; the issue is the public option boundary, not a request
to change the stored numerical values or mechanically cast assignment evidence.

## Why

A caller can believe it requested reduced storage/memory precision while the
codec never applied it. A whole-format freeze must describe actual stored types.
Global casts also cannot silently round coordinate-bound scientific evidence or
change nullable/typed chemistry and mechanical payloads.

## What is measured and what is assumed

On unchanged `c6ec38806`, thirty-two public controls produce 28 failures and
four passes. Twelve single-precision refusal guards instead create files;
twelve double controls encounter the old generic ValueError; four existing-file
controls reach FileExistsError instead of option refusal. Existing-file bytes
are not shown overwritten. Four no-override controls pass, preserving float64
geometry with sub-float32 increments, strict/report behavior, and a float32
mechanical column in 0.6. Original output and source/resource hashes are retained.

## What was refuted

The file does not have a global precision setting that this request selects.
Changing just the default label to double would leave mixed schema types and
scientific bindings unexplained. Implementing lossy global casts is not needed
to correct the false acceptance and would be a separate fidelity/schema decision.
The successful no-override controls refute a default-writer round-trip defect.

## Scope and exclusions

Reject explicit legacy `int_precision` and `float_precision` for modular 0.5/0.6
through the existing SMonitor ArgumentConflictError, with omission/fixed-encoding
guidance. ArgDigest retains value validation; trusted delegation cannot silently
ignore these keys. Keep compression's currently supported fixed defaults,
ordinary no-override output, typed payload values/dtypes, roots and units unchanged.
Legacy 0.3/0.4 handlers retain their separate precision contract. No storage
precision feature, new schema, scientific model or dependency is introduced.

## Acceptance criteria

Thirty-two original public guards pass for MolSys, Structures and complementary
inputs, ordinary/strict/report requests, unchanged existing files and trusted
calls. Relevant conversion/H5MSM regression, doctests, style and governance checks
pass. Foundations, file Toolbox, Cookbook and course describe field-specific
encodings and explicit refusal without claiming a stable 1.0 freeze. Deliver the
qualified source and record before owner closure; #256 remains open for its
independent client and final schema/default decisions.

## Provenance

Shared Linux x86-64 host; Python 3.14; original source `c6ec38806d5fd0a3ed77e8f5f1c52c5e738e9c18`
with only the new guards. One computational CPU, 2 GiB process-tree ceiling,
no swap and shared-host reserve/pressure monitoring. Exact runtime/import/version
and measured resource evidence belongs to the final receiving record.
