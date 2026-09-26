---
summary: Zenodo verifier rejects valid archived releases without a tree-tag related identifier
issue: uibcdf/molsysmt#247
status: resolved
opened: 2026-09-25
closed: 2026-09-25
severity: medium
verification: reproduced
area: [release]
guard: devtools/tests/test_citation_release_tools.py::test_zenodo_record_accepts_repository_and_exact_archive_without_tree_url
normative:
blocked_by: []
supersedes: []
---

# Zenodo verifier rejects valid archived releases without a tree-tag identifier

**Reported:** 2026-09-25, while closing the paired 0.22.4/0.23.4 release.
**Status:** Resolved; the corrected verifier passed against public record
`22959294` on 2026-09-25.

## What

MolSysMT's Zenodo record `22959294` is published with version `0.22.4`,
concept DOI `10.5281/zenodo.1298752`, distinct version DOI
`10.5281/zenodo.22959294`, GitHub repository identity and a single archived
`uibcdf/molsysmt-0.22.4.zip` file. The local verifier nevertheless rejects
it:

```bash
python devtools/scripts/verify_zenodo_release.py 0.22.4 --timeout 0
# Zenodo release: FAIL — record does not identify GitHub tag
# https://github.com/uibcdf/molsysmt/tree/0.22.4
```

## How

`devtools/scripts/verify_zenodo_release.py::validate_record` requires a
`metadata.related_identifiers` entry ending in `/tree/<version>`. Zenodo's
actual record instead exposes the repository URL both as a related
identifier and as `metadata.custom["code:codeRepository"]`, and names the
version in `metadata.version` and the archived ZIP filename. MolSysViewer's
verifier already accepts this repository-and-archive shape. Accept either
explicit tag URL or exact repository identity plus exact versioned archive,
while keeping concept DOI, distinct version DOI, published status and
nonempty file checks. Guard against unrelated repositories and wrong
archive versions, not just missing strings.

## Why

The post-release verification workflow remains red after a successful
Zenodo ingestion. This prevents machine-confirmed citation sign-off and may
prompt unnecessary account-side recovery or duplicate deposits. The archive
itself is public; the defect is in the checker, not in release packaging.

**Proposal:** the problem it solves, with the evidence behind it. One driven by a
measurement carries the measurement; one driven by a judgement says so plainly.

## What is measured and what is assumed

The public Zenodo records API returned record `22959294` with the DOI and
metadata above on 2026-09-25. The Viewer-specific verifier passed on its
corresponding record `22959304`; running the MolSysMT verifier against the
Viewer repository was not a valid Viewer test because their identity
contracts differ. The records arrived after the first 900-second polling
window, so that earlier timeout was a delay, not absence.

## What was refuted

Zenodo ingestion failure is refuted by the public, published record and its
file inventory. A repository mismatch is refuted by both repository identity
fields. Loosening validation to version alone is rejected because a record
could point to the wrong source.

## Scope and exclusions

This report covers MolSysMT's read-only public record validator and its unit
tests. It does not republish the release, alter Zenodo metadata, or decide
the shared multi-hour retry window (`uibcdf/molsyssuite#49`).

## Acceptance criteria

The real metadata shape passes; a wrong version, concept DOI, repository,
archive key or unpublished state still fails. The command above reports
the correct version DOI against the public record. A focused pytest guard
must fail if the mandatory tree-URL assumption returns.

The focused guard passed locally, and the live verifier returned
`Zenodo release: PASS — 0.22.4 -> 10.5281/zenodo.22959294`.

## Dependencies and risks

No external dependency. The risk is accepting a same-version record from the
wrong repository or a nonmatching archive; the new negative cases guard it.

## Provenance

Observed 2026-09-25 on the repository workstation with the local Python
development environment. The reproducer uses the public
`https://zenodo.org/api/records` endpoint and no token. Record identifiers,
DOIs, filename, size and checksum are from the public API; the exact file
inventory is retained in the release checkpoint.
