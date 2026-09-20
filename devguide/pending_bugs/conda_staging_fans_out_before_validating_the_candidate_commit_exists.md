---
summary: Conda staging fans out before validating the candidate commit exists
issue: uibcdf/molsysmt#213
status: active
opened: 2026-09-20
closed:
severity: medium
verification: reproduced
area: [build, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Conda staging fans out before validating the candidate commit exists

**Reported:** 2026-09-20, during the corrective MolSysMT 0.22.0 build-3 staging
dispatch.
**Status:** active; the defect is reproduced and the pre-fan-out check is implemented
locally.

## What

The manual staging input gate accepts any 40-character lowercase hexadecimal string.
It does not establish that the named commit exists in the repository before expanding
the five-platform matrix:

```bash
gh workflow run build_and_upload_conda_packages.yaml \
  --repo uibcdf/molsysmt \
  -f candidate_sha=dc5b0ac2823e1e40a2c624650f67de8c63cf225c \
  -f version=0.22.0 -f target=all -f build_number=3
```

Run `35498719699` passed `Validate the immutable candidate identity`, allocated all
five native runners, and then failed each one in `Check out the exact candidate`.

## How

`.github/workflows/build_and_upload_conda_packages.yaml` validates only the input syntax
in the `prepare` job. Repository resolution occurs for the first time in the matrix
job. The correction checks out the exact manual SHA or release tag in `prepare`, after
the syntax check and before GitHub expands `build-and-publish`.

## Why

Invalid operator input consumes five hosted runners, produces five redundant failures,
and obscures one input error as a cross-platform build failure. It publishes no package,
so severity is medium rather than high.

## What is measured and what is assumed

**Measured:** run `35498719699` completed one successful prepare job and five failed
matrix jobs. `gh-run-receptor` identified exit code 128 from Git on every platform and
reported zero artifacts.

**Measured:** local `git rev-parse HEAD` returned the real candidate
`dc5b0ac28fb45d91eac7a95ea9d96988329509a5`; the dispatched suffix was not that commit.

## What was refuted

The Conda recipe and platform toolchains were not reached. This was not a five-platform
source failure and no channel coordinate was uploaded.

## Scope and exclusions

This covers resolving manual candidate SHAs and release tags before matrix fan-out. It
does not change the candidate version rules, build matrix, recipe, publication action,
or channel policy.

## Acceptance criteria

- The prepare job resolves the exact candidate before any platform job starts.
- A repository test requires the pre-fan-out checkout and its immutable ref expression.
- A valid exact candidate still reaches the normal five-platform matrix.

## Dependencies and risks

The corrective build-3 staging run for uibcdf/molsysmt#195 must be relaunched after this
guard lands. A checkout in `prepare` adds one small repository fetch but prevents five
larger wasted allocations on invalid input.

## Provenance

GitHub Actions run `35498719699`, five GitHub-hosted native runners, workflow commit
`dc5b0ac28fb45d91eac7a95ea9d96988329509a5`, 2026-09-20. Compact diagnosis produced by
`gh-run-receptor` with the Conda profile.
