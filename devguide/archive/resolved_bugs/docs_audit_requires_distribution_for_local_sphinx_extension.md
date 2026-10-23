---
summary: Documentation dependency guard requires an external distribution for a local Sphinx extension.
issue: uibcdf/molsysmt#427
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: low
verification: reproduced
area: [docs, testing]
guard: devtools/tests/test_audit_dependency_contract.py::test_docs_extra_supplies_the_configured_theme_and_extensions
normative:
blocked_by: []
supersedes: []
---

# Documentation dependency guard misclassifies a local extension

**Reported:** 2026-10-22 while validating the new Viewer source route under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.
**Status:** resolved tooling defect; no runtime dependency is added.

## What

The real configured documentation passes Sphinx but the dependency guard fails:

```text
python -m pytest --receptor=llm devtools/tests/test_audit_dependency_contract.py::test_docs_extra_supplies_the_configured_theme_and_extensions -x
AssertionError: Missing documentation provider for key_takeaway
```

## How

`docs/conf.py` adds `docs/_ext` to the import path and declares `key_takeaway`.
Its delivered source is `docs/_ext/key_takeaway.py`. The guard previously mapped
every non-Sphinx module to an external distribution by replacing underscores
with hyphens, without checking that local route. Both the test and extension
predate the tools integration; the defect is not caused by its new entry point.

## Why

A valid local extension was rejected, encouraging an unnecessary external
package. The source/built documentation do not require a `key-takeaway` package.

## What was refuted

Adding a guessed dependency is not a repair for an extension delivered in the
repository. Removing the extension or disabling its guard would weaken course
rendering and external dependency checks.

## Resolution

The guard checks for a real module/package source under the configured local
extension directory before requiring an external provider. Missing local files
still take the external dependency check; the checks for actual external themes
and extensions remain intact. The guard above exercises the real configuration,
local source and declared documentation extras. No scientific code, method,
public dependency floor or package publication changes.

## Provenance

Python 3.14 development environment `molsyssuite@uibcdf_3.14`; inspected base
`f0902ef6f6538c2b633d9e006852ac5203050f63`. Initial dependency-tool group: ten
pass and this one failure before maxfail. Focused corrected evidence is retained
with the closing commit. This is separate from addon runtime qualification.
