---
summary: Review ownership and location of form/_h5msm05_* implementation modules
issue: uibcdf/molsysmt#438
status: open
opened: 2026-10-23
closed:
verification: inspected
area: [form, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Reviewing H5MSM 0.5 implementation ownership and location

**Reported:** 2026-10-23, by the maintainer during the PDBQT/comparison work.
**Status:** Open review; no relocation or new public API is selected.

## What

Assess whether the seven private `_h5msm05_*.py` modules belong directly under
`molsysmt/form`, and document a coherent ownership map before moving files.
The naming and location question does not establish a runtime or scientific defect.

## How

Inspected modules and responsibilities:

| Module suffix | Present responsibilities |
| --- | --- |
| `modular` | Domain composition, file readers/writers, migrations and calculation-chemistry access |
| `structures` | Structural series encoding, selected reads, append and validation |
| `topology` | Independent topology serialization |
| `associations` | Domain-axis sizes, maps and association consistency |
| `iterator` | H5MSM 0.5 structure-block iteration |
| `alternate_location` | Alternate-location encoding, validation and append |
| `bioassembly` | Assembly record preparation, encoding and reading |

Inspect all callers, including `molsysmt.h5msm`, the file adapter,
`_private/h5msm.py`, topology chemistry access and ionic interactions. Distinguish
schema/codec/storage operations from adapter dispatch and reusable domain
operations. Review the adjacent `_h5msm_chemical_states.py` boundary as context,
without silently expanding the requested relocation scope.

Compare the current layout with a dedicated private H5MSM implementation package
or a private shared-format package. `molsysmt/h5msm.py` and
`molsysmt/_private/h5msm.py` already exist as modules: a package proposal must
account for those paths and imports rather than assuming an empty namespace.
Keep format-specific schema code together; domain ownership alone does not mean
placing persistence implementation in the public domain classes.

## Why

The implementation serves public persistence and several internal consumers,
not only one form adapter. A deliberate package boundary can clarify dependency
direction and maintenance. Moving files purely for visual tidiness may instead
introduce import cycles or spread a versioned codec across unrelated owners.

## Evidence and acceptance

**Inspected:** file inventory, imports and function/class definitions. No timing,
module-loading improvement or existing architectural defect is demonstrated.

The review must produce a responsibility/caller map, alternatives, decision and
bounded migration plan. Any accepted implementation must preserve public API
paths, schema 0.5, units, axis maps, resource ownership and lazy form discovery.
Update internal imports, diagnostics, tests and maintained documentation together;
exercise persistence, selection, iteration, migration and conversion guards.
Do not duplicate codecs or change the on-disk format as a side effect.

## Scope

This is a review request, not authorization for immediate relocation, package
publication or an additional 1.0 blocker. Existing stabilization work continues.
