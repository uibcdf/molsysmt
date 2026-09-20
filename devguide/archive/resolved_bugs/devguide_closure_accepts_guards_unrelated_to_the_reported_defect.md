---
summary: Devguide closure accepts guards unrelated to the reported defect
issue: uibcdf/molsysmt#197
status: resolved
opened: 2026-09-02
closed: 2026-09-20
severity: medium
verification: reproduced
area: [docs, ci]
guard: devtools/tests/test_validate_devguide.py::test_a_guard_with_a_missing_node_is_refused
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Devguide closure accepts guards unrelated to the reported defect

**Reported:** 2026-09-02, split from the gate audit in uibcdf/molsysmt#187.
**Status:** resolved on 2026-09-20 after adoption of the shared guard semantics in
`uibcdf/molsyssuite#26`.

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

## Resolution

MolSysMT now applies the common static Python profile prospectively to reports resolved
on or after 2026-09-20. The validator parses the named test module and requires the
module, function, or class-method selector to resolve to a statically collected pytest
test. It rejects nonexistent nodes, parameter IDs, unsafe paths, globs, comma-separated
targets, and command text while preserving historical archive syntax.

The guard above protects the actual failure mechanism: it constructs the former false
positive, `tests/basic/test_get_form_battery.py::test_routes`, whose file exists but whose
node does not, and asserts that closure validation refuses it. The protocol now states
the separate reviewer responsibility for deciding whether an addressable test is
relevant to the reported defect. A future non-pytest guard must first define the bounded
local selector profile required by the central contract.
