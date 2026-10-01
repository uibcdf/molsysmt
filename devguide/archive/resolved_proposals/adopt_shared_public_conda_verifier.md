---
summary: Call the pinned common public Conda verifier and retain independent evidence.
issue: uibcdf/molsysmt#275
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: measured
area: [governance, release]
guard: devtools/tests/test_verify_public_package.py
normative:
blocked_by: []
supersedes: []
---

# Shared public Conda verification

**Reported:** 2026-10-01, following uibcdf/molsyssuite#48 and #27.
**Status:** Resolved: common provider adopted and its public-file verification passed.

## What

Replace copied verification or inline shell code with the common exact-file
provider. Keep release identity, platform selection, installed-package checks
and mutation credentials local.

## How

Promotion and independent workflows call the immutable MolSysSuite action
`399d33a4ee0da148571cba7cfc004e3f3a2e71e7`. Its non-login shell avoids the reproduced logout failure.
Anonymous release-metadata and solver-index checks establish each exact file's
main label, identity, build and SHA-256. Evidence is retained with `always()`.
The independent workflow contains no promotion or upload credentials.

## Why

One tested provider prevents duplicated logic from drifting. A read-only recheck
recovers evidence without repeating a public registry mutation.

## What is measured and what is assumed

Source routing is inspected. Provider tests and six original public-file checks
are recorded in uibcdf/molsyssuite#48. Local guard: `devtools/tests/test_verify_public_package.py`.
No new installed-pair scientific evidence is claimed.

## Alternatives and refuted paths

Keeping a corrected local copy would retain duplication. Repeating promotion
would conflate verification recovery with registry mutation.

## Scope and exclusions

Conda workflow governance. No package release, promotion or full scientific suite.
Existing component-specific installation checks keep their separate meaning.

## Acceptance criteria

Both workflows call the same pinned provider, retain independent evidence and
pass their local governance guards. Hosted read-only evidence checks the actual
provider call without a registry mutation.

## Local implementation issues

This report owns uibcdf/molsysmt#275. Provider: uibcdf/molsyssuite#48.

## Dependencies and risks

An unavailable index fails verification; it never triggers another upload.
Policy and broader release routing remain coordinated under uibcdf/molsyssuite#27.

## Provenance

2026-10-01; isolated clean checkout; administrative tests only. Provider revision
`399d33a4ee0da148571cba7cfc004e3f3a2e71e7`. Hosted execution evidence will be appended before closure.

## Resolution and measured evidence

Administrative verification passed 6 selected local tests. Native hosted
run 36860167904 executed the pinned shared action, verified the exact public file
and retained independent evidence. The common provider and six-file inventory
were verified centrally in run 36850953842. The local guard protects the actual
provider pin, package/filename/digest inputs and `always()` evidence retention.
No promotion or package release was repeated.
