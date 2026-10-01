---
summary: Docstring validator omits interaction families
issue: uibcdf/molsysmt#279
status: resolved
opened: 2026-10-01
closed: 2026-10-01
severity: medium
verification: measured
area: [docs, api, tests]
guard: devtools/tests/test_validate_docstrings.py::test_missing_exported_detector_docstring_fails_gate
normative:
blocked_by: []
supersedes: []
---

# Docstring validator omits interaction families

**Reported:** 2026-10-01, lifecycle validation of uibcdf/molsysmt#278.
**Status:** Resolved; exported interaction families are discovered dynamically and mutation-tested.

## What

The docstring validator's fixed public-module inventory includes legacy hbonds
but none of the modern interactions families. An exported modern detector with
no docstring still lets the validation gate pass. The prior detector reports'
validator counts did not establish docstring fidelity for those omitted functions.
Their explicit doctests and rendered tutorials remain separate valid evidence.

## How

Observed from the repository root, in a temporary process without changing source:

```python
import molsysmt as msm
from devtools.scripts.validate_docstrings import validate
msm.interactions.hydrophobic.get_hydrophobic_interactions.__doc__ = None
assert validate() == 0
```

The pre-fix gate reported 209 checked functions and success. Discover modules
from interactions.__all__ so current and future exported families enter the
existing signature/docstring/default checks. Missing or broken family imports
must not silently reduce coverage. Keep identity deduplication for legacy aliases.

## Why

A passing release gate omitted the very detectors being introduced. This is a
coverage gap, distinct from the vacuous-content defect of uibcdf/molsysmt#187.
That archived record was inspected because the root contribution rule links it
as the concrete example for this validator's intent. No historical rule is changed.

## What is measured and what is assumed

**Measured:** the missing-docstring mutation returns zero before the fix.
No claim is made that the present validator covers all public class methods or
all nested namespaces. This correction covers the omitted interactions families.

## What was refuted

- The legacy hbonds namespace does not cover the modern attributed entry point
  or ionic, aromatic, halogen and hydrophobic detector functions.
- A successful API stability registry does not establish docstring quality.
- Manually listing each new family would leave the same omission mechanism for
  the next family. Public exported-family discovery is the durable boundary.

## Scope and exclusions

Preserve the existing docstring parser, stable-API content checks, lazy runtime
semantics and duplicate-function suppression. Do not expand this into a full
class-method documentation campaign. Mutation tests must demonstrate that the
real exported functions fail the gate when documentation is absent or wrong.

## Acceptance criteria

- Every public interaction family contributes exported functions to validation.
- Missing detector docstrings fail; a wrong documented default also fails.
- A temporary newly exported family is checked without editing a validator list.
- Existing codebase and validator regression tests pass.

## Resolution

The validator now visits modules declared by interactions.__all__. This includes
all seven current public families and admits the next exported family without
a manual validator edit. Import failures are not swallowed, and existing function
identity deduplication preserves legacy aliases. No scientific detector behavior
or docstring-parser rule changes.

The guard mutates the real exported detector in each of seven families and proves
missing documentation fails with its public qualified name. Additional controls
mutate an actual method default and temporarily export an undocumented new family;
both must fail. Nineteen regression tests pass in 1.64 seconds with:

```bash
python -m pytest devtools/tests/test_validate_docstrings.py --receptor=llm
```

The corrected codebase validation passes 216 functions. Ruff passes. This proves
coverage of exported interaction functions, not all public class methods.

## Validation provenance

2026-10-01, Linux x86_64, Python 3.13.14, source patch based on review commit
6bb5357a3. The source reproduction ran before the fix and returned zero with an
undocumented hydrophobic detector. Tests afterward require a nonzero result.
This isolates the omission mechanism instead of merely checking module counts.
The closing issue names the immutable implementation commit.
