---
summary: Conda ABI3 artifact validation rejects the supported Python 3.14 range
issue: uibcdf/molsysmt#347
status: resolved
opened: 2026-10-06
closed: 2026-10-06
severity: medium
verification: reproduced
area: [packaging, tests]
guard: devtools/tests/test_validate_conda_abi3_artifact.py::test_accepts_platform_package_with_cep20_metadata
normative:
blocked_by: []
supersedes: []
---

# Conda ABI3 artifact validation rejects the supported Python 3.14 range

**Reported:** 2026-10-06, while verifying the staging candidate requested by MolSysViewer.
**Status:** Resolved in validation tooling; original package bytes remain unchanged.

## What

The standalone artifact validator rejects a legitimate 0.23.0 ABI3 package:

```bash
python devtools/scripts/validate_conda_abi3_artifact.py \
  build/qualification/023-staging/packages/linux-64/molsysmt-0.23.0-pyabi3h03bb3b7_0.conda \
  --expected-subdir linux-64
```

The initial command exits 1 with
`package does not declare exactly one Python >=3.11,<3.14 requirement`.
The file declares `python >=3.11,<3.15`, matching the public Python 3.11–3.14
contract in `pyproject.toml` and the Conda recipe.

## How

`validate_extracted_artifact` retains a hard-coded upper bound from the earlier
Python range. Its synthetic acceptance fixtures preserve the same stale bound,
so the six existing tests fail to expose the mismatch.

The validator now reads the authoritative `project.requires-python` from
`pyproject.toml` and compares parsed specifier sets. Equivalent version spelling
such as 3.11 and 3.11.0 is accepted. Missing, duplicate, invalid, narrower and
wider Python requirements are rejected. Native platform, ABI3 filename,
relocation and runtime-support checks retain their previous behavior.

## Why

The obsolete bound prevents artifact sign-off and the coordinated handoff under
uibcdf/molsysmt#334 even though the actual package has correct metadata.
The defect affects the developer tool, rather than the molecular runtime or
already produced package files.

## What is measured and what is assumed

- The initial real Linux x86-64 package check exits 1 on the obsolete bound.
- The corrected validator passes the unchanged Linux x86-64 and ARM packages.
- Thirteen focused tests pass, including seven rejection cases covering the
  requirement's actual support boundary and multiplicity.
- Registry, producer and downloaded-file SHA-256 values agree for both packages.
  Candidate production remains run 37534744593, source
  `46ef28eb60a258aa77d82ff1bc39ee0d1591e3c9`, version 0.23.0, build 0.

## What was refuted

Corrupt package metadata and an incorrect package Python range are ruled out
by inspecting the actual artifacts and the authoritative project range.
Rebuilding or re-uploading would change tested bytes without correcting the
validation defect, so no package mutation is needed.

## Scope and exclusions

This correction updates one developer validator and its tests. It does not
change public dependency floors, runtime APIs, original producer identity,
staging coordinates or package bytes. Installed-pair qualification remains
required independently.

## Acceptance criteria and resolution

The positive guard accepts the real supported Python range and fails under the
previous validator. Rejection cases ensure that merely admitting Python 3.14
cannot admit an unbounded or otherwise incompatible package. Both real Linux
artifacts pass the corrected validator. Ruff checks and developer-guide
validation accompany the change.

## Provenance

Linux shared development environment, Python 3.14.7, twelve pytest workers,
pytest-receptor `llm`, 2026-10-06. Focused run: 13 passed in 3.77 s. Package
identities and qualification receipts remain owned by uibcdf/molsysmt#334.
