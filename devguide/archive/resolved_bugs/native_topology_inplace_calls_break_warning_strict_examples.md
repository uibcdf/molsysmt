---
summary: Native topology inplace calls break warning-strict examples
issue: uibcdf/molsysmt#431
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [form, tests]
guard: tests/native/test_pandas_warning_compatibility.py
normative:
blocked_by: []
supersedes: []
---

# Native topology inplace calls break warning-strict examples

**Reported:** 2026-10-22 by MolSysViewer; consumer uibcdf/molsysviewer#264.
**Status:** Resolved; compatibility repair qualified with pandas 2.3.3 and 3.1.0.

## What

Native bond normalization calls deprecated `sort_values(inplace=True)` and
`reset_index(inplace=True)`. Hierarchy extraction and chemical-state extraction
also use deprecated DataFrame/Series reset operations. Public selection and
extraction routes can therefore fail when DeprecationWarning/UserWarning become
errors, as in the consumer's executable documentation.

## How

The development environment has pandas 2.3.3 and does not emit Pandas4Warning.
The published pandas 3.1.0 CPython 3.14 Linux wheel was downloaded and unpacked
under a task-specific temporary directory. A subprocess imports that package
ahead of the existing development packages; no environment or installed package
was changed. This is a source-checkout compatibility check, not qualification of
a new Conda artifact.

All seven new guards failed before the fix with the exact native Pandas4Warning
in `Bonds_DataFrame.sort_values`. The minimal reproduction is
`build_minimal_topology()` from `tests/native/test_topology_operations.py` under
`warnings.simplefilter('error', DeprecationWarning)` and the same UserWarning
filter. The source/fixture data are local and require no viewer runtime.

## Why

The warning is a supported-provider compatibility defect even when the current
pandas version still executes it. The consumer reports three documentation
examples failing on multiple platforms. No scientific output corruption has
been demonstrated; the fix must preserve existing topology values, ordering,
nullable dtypes, table/domain identity and independent source/output ownership.

## Repair and rejected alternatives

Bond sorting uses public `sort_values(ignore_index=True)` and positional owned
column arrays to update the existing authoritative Bonds_DataFrame. Keeping that
object matters to native aliases; replacing it with pandas' base DataFrame or
using private pandas managers is unnecessary. Explicit index assignment resets
already-owned extraction tables/Series without another copy or an inplace API.
Deleting an optional state column uses `del`, retaining the atom table object.

Warning filters, skipped consumer pages and a speculative upper bound on pandas
are rejected. No public scientific criterion, argument, quantity convention,
dependency floor or Ackredit calculation boundary changes here.

## Acceptance criteria

- The strict guards run on both installed pandas 2.3.3 and the isolated published
  pandas 3.1.0 package.
- Public native extraction/copy/pickle preserve values, string IDs, compact
  indices, known domains and source independence.
- Private bond sorting retains the original table and all nullable metadata;
  chemical-state extraction preserves remapped component membership/assignments.
- No consumer warning suppression is needed. Actual consumer-page and installed
  pair receiving remain separately owned by MolSysViewer.

## Verification

Primary guard: `tests/native/test_pandas_warning_compatibility.py`.
The same focused selection passes **1,366 tests** with zero failures/skips on
both pandas 2.3.3 (31.18 s) and pandas 3.1.0 (33.01 s), using 12 workers and
Pytest Receptor per run. Each run retains 15 legacy H5MSM warnings; no warning
was suppressed. The seven primary strict-warning guards pass in each version.
Ruff, the public-signature guard and all 14 fast gates pass.

The [source receipt](../../../devtools/data/native_pandas_compatibility_20261022.json)
records commands, versions, the downloaded wheel digest and tested executable
hashes. This is Linux/Python 3.14 source evidence, not a new installed artifact
or a rerun of MolSysViewer's documentation pages.

## Resolution

The native sorting/index-reset operations no longer depend on deprecated pandas
inplace keywords. The guard asserts actual warning-strict behavior and topology
semantics, including original authoritative bond-table identity, nullable
metadata, remapped component/atom assignments, pickle values and independent
source/output ownership. It fails on the pre-fix published-pandas 3.1.0 path.
The consumer can now receive the exact fix and rerun uibcdf/molsysviewer#264;
its package/publication qualification remains separately owned.
