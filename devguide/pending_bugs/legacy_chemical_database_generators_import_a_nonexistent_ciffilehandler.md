---
summary: Legacy chemical database generators import a nonexistent CIFFileHandler
issue: uibcdf/molsysmt#368
status: open
opened: 2026-10-10
closed:
severity: low
verification: inspected
area: [data, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Legacy chemical database generators depend on a nonexistent native CIF parser

**Reported:** 2026-10-10, final adapter-delivery audit for uibcdf/molsysmt#139.
**Status:** Open; deferred from the pre-1.0 runtime repair.

## What

The standalone regeneration scripts in `molsysmt/data/databases/amino_acids/`,
`ions/`, `saccharides/` and `small_molecules/` import
`molsysmt.native.CIFFileHandler`, a class that does not exist. Three call `parse()`;
the amino-acid script calls `read()` and `get_item()`. These scripts cannot use the
advertised legacy parser. Existing packaged database readers are separate.

## How

Each `make_*_db.py` contains the import. The absent native class and its placeholder
form registration are addressed in #139; retiring that registration does not
repair these independent regeneration scripts. A real `mmcif.io.IoAdapter` route
exists for public CIF conversion, but the scripts expect a different category
mapping interface and process the complete CCD rather than a coordinate system.

## Why

Future database maintenance needs a reproducible, usable regeneration path.
Keeping broken legacy scripts without a tracked owner would hide that debt.
This is tooling debt, not evidence that loading packaged chemical data fails.

## What is measured and what is assumed

Source-inspected on 2026-10-10: all four script imports and their downstream calls.
No script was executed: regeneration needs a downloaded CCD and writes database
files. No claim is made about newly generated scientific data or performance.

## What was refuted

The placeholder form adapter does not implement the missing native parser.
Keeping it registered cannot make these scripts work. Implementing a new public
handler is not required to use the existing mmCIF parser.

## Scope and exclusions

Post-1.0 data-tool maintenance. Restore or replace these standalone scripts using
an existing parser, after reviewing the complete multi-container CCD requirement.
Do not change packaged database data merely to remove an import failure.

## Acceptance criteria

- Provide a supported CCD regeneration route or explicitly retire each obsolete script.
- Verify multi-container/category parsing on a small local CCD fixture.
- Check deterministic output and category-specific chemistry requirements.
- Document inputs, provenance and invocation; add an addressable regression guard.

## Provenance

Inspected source based on d47b528dabc0a68bf0ce90660b6c3a71701e674c.
Related runtime repair: uibcdf/molsysmt#139.
