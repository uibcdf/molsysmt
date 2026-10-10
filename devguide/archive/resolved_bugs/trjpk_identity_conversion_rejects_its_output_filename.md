---
summary: TRJPK identity conversion rejects its output filename
issue: uibcdf/molsysmt#370
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: inspected
area: [form, convert]
guard: tests/form/file_trjpk/test_queries_and_roundtrip.py::test_identity_conversion_copies_to_requested_filename
normative:
blocked_by: []
supersedes: []
---

# TRJPK identity conversion rejects its public output filename

**Reported:** 2026-10-10, final TRJPK adapter/documentation review.
**Status:** Repaired; public copy and legacy-alias guards executed locally.

## What

The public dispatcher supplies `output_filename` when converting to a file path:

```python
msm.convert(source_trjpk, to_form="copy.trjpk")
```

The legacy TRJPK identity converter instead accepts only `output_name` and forwards
that unsupported keyword to `extract()`, whose argument is `output_filename`.
Converting without a destination also reaches that mismatch. The extraction
all-selection branch attempts to copy a file onto itself by default.

## How

The dispatcher in `molsysmt/basic/convert.py` and the signatures/call in
`molsysmt/form/file_trjpk/to_file_trjpk.py` establish the keyword mismatch.
The default branch of `file_trjpk/extract.py` establishes the same-file copy.

## Why

This existing advertised identity/copy conversion cannot complete through the
public API. It belongs to bounded pre-1.0 adapter stabilization, not a new format.

## What is measured and what is assumed

The original mechanisms are source-inspected; no original exception trace is
claimed. After repair, public destination copy, identity without a destination,
copy_if_all=False and the legacy output_name adapter alias are tested using the
independently written local fixture. Destination bytes must match the source.

## What was refuted

No new pickle codec or subset editing is needed for an identity file copy.
The existing dictionary subset writer repaired in #365 is a separate operation.

## Scope and exclusions

Accept the dispatcher's output_filename, retain the old output_name keyword and
positional signature, and avoid copying onto the same path. A distinct destination
makes an independent file; omitting it retains the source path. Subset extraction
from the legacy file adapter remains explicitly unsupported.

## Acceptance criteria

- Public identity conversion writes exactly the requested destination bytes.
- Identity without a destination leaves the source unchanged.
- The legacy alias continues to work with argument digestion enabled.
- Reject contradictory simultaneous output aliases.
- Document the distinction between identity copy and dictionary subset export.

## Resolution

The converter adds output_filename without shifting its existing positional
parameters, rejects conflicting aliases, and delegates the resolved filename to
the existing extraction boundary. That boundary copies only to a distinct path.
The legacy output_name uses the existing canonical filename digester through a
private alias, avoiding a second filename-validation implementation. Both output
keywords are registered as optional identity converter arguments. The final
TRJPK query/export/identity selection and identity doctest pass 30 cases with
no warnings; the alias guard rejects any missing-digester warning. The guard's exact byte comparison protects actual output delivery, not merely a
matching function signature.

## Provenance

Linux shared development environment, Python 3.14.7, 2026-10-10.
Original source: d47b528dabc0a68bf0ce90660b6c3a71701e674c.
