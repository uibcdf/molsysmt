---
summary: Devguide closure accepts guards unrelated to the reported defect
issue: uibcdf/molsysmt#197
status: blocked
opened: 2026-09-02
closed:
severity: medium
verification: inspected
area: [docs, ci]
guard:
normative:
blocked_by: [uibcdf/molsyssuite#26]
supersedes: []
---

# Devguide closure accepts guards unrelated to the reported defect

**Reported:** 2026-09-02, split from the gate audit in uibcdf/molsysmt#187.
**Status:** blocked by the shared guard-semantics decision in
`uibcdf/molsyssuite#26`. This report now owns only the MolSysMT implementation.

## What

The reporting protocol says a resolved defect names "the test that fails if the defect
returns." The enforced rule accepts any existing path under a test tree, optionally
followed by any text after `::`. A report can therefore close with an unrelated test
file or a nonexistent node while `validate_devguide.py` passes.

```bash
$ python -c "..."
```

## How

`devtools/scripts/devguide_reports.py::_validate_guard` splits the guard at the first
`::`, checks that the path begins with `tests/`, `devtools/tests/`, or `rust/`, and checks
only that the resulting path exists. It does not require a pytest node, verify that a
named node exists, or express a reviewable relationship between the test and the report.

The last property cannot be proved from a path alone. The defect is therefore both a
weak mechanical check and protocol wording that presents a human relevance judgement as
though the validator established it.

## Why

The archive is the project's durable defect record. A syntactically valid but irrelevant
guard makes the closure condition appear stronger than it is and gives future
maintainers no precise regression entry point. It does not directly change library
behavior, which is why the severity is medium.

## What is measured and what is assumed

Inspected: the normative closing language in `reporting_protocol.md` and the complete
implementation of `_validate_guard`.

Assumed: no current archived entry is accused of naming an irrelevant guard. That would
require a separate audit of each defect against its test.

## What was refuted

*The validator can prove that a test would fail for the reported defect.* Refuted. That
semantic relationship requires review or a deliberately constructed mutation; neither
can be inferred from path existence.

*Path existence is the whole intended contract.* Refuted by the repeated normative
wording that the guard is the test that fails when the defect returns.

## Scope and exclusions

Covers MolSysMT's schema, `_validate_guard` implementation, validator tests, and closure
workflow after the common contract is accepted. The suite-wide meaning of `guard`, the
pytest profile, non-pytest extension rules, migration policy, and coordinated rollout are
owned by `uibcdf/molsyssuite#26` and must not be decided independently here.

Excludes re-evaluating every historical guard and excludes the docstring validator work
in uibcdf/molsysmt#187.

## Acceptance criteria

1. MolSysMT implements the pytest and non-pytest selector semantics accepted in
   `uibcdf/molsyssuite#26` without adding a competing local definition.
2. A guard that names a nonexistent pytest node is rejected.
3. MolSysMT's protocol distinguishes mechanically checked addressability from the
   reviewer-owned claim that the test protects against the reported defect.
4. Validator mutation tests reject a missing path and a missing node without accepting
   a shape-only substitute.
5. The closing workflow records enough specificity for a maintainer to run the guard.

## Dependencies and risks

The central policy decision is tracked by `uibcdf/molsyssuite#26`. Rust tests and
parametrized pytest nodes do not share one discovery format. Tightening the schema must
preserve legitimate non-pytest guards or define an explicit form for them rather than
pretending one parser covers every test tree.

## Provenance

Source inspected on 2026-09-02 at repository commit `48ea5b91c`.
