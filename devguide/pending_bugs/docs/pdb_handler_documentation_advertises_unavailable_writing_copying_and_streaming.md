---
summary: PDB handler documentation advertises unavailable writing, copying and streaming
issue: uibcdf/molsysmt#714
status: active
opened: 2026-11-11
closed:
severity: medium
verification: inspected
area: [docs, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Reporting actual PDB handler capabilities

## What

The Foundations page calls PDBFileHandler a streaming writer. Its form notebook
advertises independent copy, subset extraction, add/merge/append, setters and
streaming iteration as implemented. The shown attribute type calls normalized
content a dictionary, although it is an object containing ordered models and
record collections. The example requires an unspecified protein.pdb file.

## How

On published 6acad4f35, native/pdb_file_handler.py eagerly reads text into a
StringIO buffer, fills normalized content and parses a separate entry. dump()
is empty. The copy/add/merge/append adapters and form-specific iterator advance
methods raise structured unavailable-route errors; set.py contains no field
setters. The old full-axis identity helper can return its borrowed handler;
it is not an independent snapshot or a general selected handler writer.

## Why

A file-backed class name and exported adapter functions do not establish
streaming, editing or writing support. Users may select an unsuitable route
for large inputs or assume that a copied handler is independent. Correcting
these claims is pre-1.0 instructional robustness, not a new parser capability.

## Scope and exclusions

Correct the Foundations and form pages, clarify raw PDB angstrom values versus
public PyUnitWizard quantities, and retain opaque-remark/naming-scheme limits.
Use a bundled example with deterministic closure. Distinguish registered native
conversions from unsupported hooks. Add the existing experimental PDBQT guide
to the handler portal without inventing a FASTA handler or new API page.
No runtime parser, serial decoder, iterator, copy implementation, scientific
model or dependency changes are included. Existing API docstring debt is not
certified by this bounded review.

## Acceptance

Execute the actual bundled example under nm/ps and pm/fs; verify nonempty parsed
models, the first atom's physical coordinates against the deposited ATOM record,
selected query shape and owned-buffer closure. Preserve notebook code, outputs
and execution metadata. Inspect actual generated articles and link destinations,
with zero unresolved references in this slice. Keep registered attributes/routes
aligned with their sources without claiming availability in every input.

## Provenance

2026-11-11; source 6acad4f35, Linux/Python 3.14.7. This defect is established by
source and documentation inspection; execution receiving is recorded separately.
The concurrent complete-source run uses its own clean frozen worktree and
unchanged qualified native binary. #713 remains independent.
