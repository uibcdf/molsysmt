---
summary: Citation test pins 1.0.0 and fails on the published 0.22.4 release
issue: uibcdf/molsysmt#248
status: resolved
opened: 2026-09-25
closed: 2026-09-25
severity: medium
verification: reproduced
area: [release]
guard: devtools/tests/test_citation_release_tools.py::test_repository_citation_metadata_is_coherent
normative:
blocked_by: []
supersedes: []
---

# Citation test pins 1.0.0 and fails on the published 0.22.4 release

**Reported:** 2026-09-25, while testing the Zenodo verifier correction.
**Status:** Resolved; evergreen checks use current citation metadata, and
the focused module passed 5/5 locally on 2026-09-25.

## What

The citation test suite fails on current, internally coherent repository
metadata because two tests hard-code the future version `1.0.0`.

```bash
pytest --receptor=llm devtools/tests/test_citation_release_tools.py -x
# AssertionError: CITATION.cff version '0.22.4' does not match expected '1.0.0'
```

## How

`devtools/tests/test_citation_release_tools.py` passes `"1.0.0"` to
`validate_repository` in the repository-coherence and wrong-DOI tests. The
validator already has a mode without `expected_version` that checks the
version syntax and agreement of all derived citation surfaces against the
current `CITATION.cff`. Use that mode for evergreen tests; keep an explicit
version only when testing preparation of a specific synthetic release.

## Why

Release metadata tests turn red after preparing an ordinary pre-1.0 version,
adding noise to the release gate and concealing real citation failures. Viewer
previously corrected the same pattern in its own citation tests.

**Proposal:** the problem it solves, with the evidence behind it. One driven by a
measurement carries the measurement; one driven by a judgement says so plainly.

## What is measured and what is assumed

The failing assertion and current `CITATION.cff` version were observed
locally on 2026-09-25. The production citation validator passes when run
against the same repository without an artificial expected version.

## What was refuted

The citation metadata itself is not inconsistent: the failure names only the
test's expected-version argument. Deleting version validation entirely is
unnecessary; the validator still checks version format and derived surfaces.

## Scope and exclusions

Only evergreen citation tests are changed. The release gate's explicit
`--expected-version` check remains appropriate for an exact candidate, and
no public metadata or tagged release is changed.

## Acceptance criteria

The entire focused citation test module passes with `CITATION.cff` at
0.22.4; a deliberately wrong DOI still fails. A mechanically addressable
pytest selector protects the repository-coherence assertion.

## Dependencies and risks

No external dependency. The test must continue checking current metadata;
using the optional validator mode does not skip the internal consistency
checks.

## Provenance

Observed 2026-09-25 in the local MolSysMT development environment with
pytest-receptor's compact report. This is an exact test assertion failure,
not a performance measurement.
