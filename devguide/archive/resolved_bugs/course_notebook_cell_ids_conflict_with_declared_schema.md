---
summary: Course notebook cell IDs conflict with the declared notebook schema.
issue: uibcdf/molsysmt#514
status: resolved
opened: 2026-10-27
closed: 2026-10-27
severity: medium
verification: reproduced
area: [docs]
guard: devtools/tests/test_documentation_notebook_schema.py::test_documentation_notebook_schema
normative:
blocked_by: []
supersedes: []
---

# Course notebook cell IDs conflict with the declared notebook schema

## What

Four Interaction Networks course notebooks declare notebook format 4.4 but
include a new markdown cell with an `id` field, supported only from 4.5.
The notebooks are invalid at their declared version. This was introduced by
24ee46486 while receiving the addon detector documentation.

## How

The strict parallel Sphinx command logs `Notebook JSON is invalid: Additional
properties are not allowed ('id' was unexpected)` for the Alzheimer, Antiviral,
Biophysics and Enzyme modules. Make nevertheless exits successfully; a successful
exit therefore did not establish valid rendered notebook content.

Raw `nbformat.validator.iter_validate` detects exactly the same four source
notebooks without converting, upgrading or normalizing their contents. A
focused raw-schema regression check fails against the original source (one
failed, one passed), including an independent rejection example. The existing
source-wide schema guard uses this same raw validator and is retained; no
duplicate scanner is introduced.

## Why

Retain the new scientific/API narrative but remove its unsupported cell metadata.
A schema upgrade would change the metadata contract of every existing cell and
is unnecessary for this prose addition. No code cell, output, heading or
scientific criterion changes.

## Acceptance criteria

All notebooks discovered by the real Sphinx source inventory must validate at
their declared schema without repair. The guard must reject an `id` added to a
4.4 notebook, and the strict full documentation build must contain no notebook
validation errors. This check complements Sphinx warning-as-error handling;
it does not claim notebook execution or visual qualification.

## Resolution — 2026-10-27

Removed only the four unsupported `id` keys, retaining nbformat 4.4 and every
cell's narrative, code and outputs. No format upgrade or content substitution
is needed. The pre-existing addressable guard named above checks the stored
source without normalization; it rejects this exact failure mechanism.
The full strict parallel Sphinx build exits zero with no warnings or notebook
validation errors after the repair. This is source-schema/render-build evidence,
not notebook execution, a deployed site or installed-package qualification.
