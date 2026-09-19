---
summary: Scientific evidence registry accepts tests that were never executed
issue: uibcdf/molsysmt#196
status: resolved
opened: 2026-09-02
closed: 2026-09-19
severity: high
verification: measured
area: [tests, ci]
guard: devtools/tests/test_execute_scientific_evidence.py
normative: devguide/scientific_validation.md
blocked_by: []
supersedes: []
---

# Scientific evidence registry accepts tests that were never executed

**Reported:** 2026-09-02, split from the gate audit in uibcdf/molsysmt#187.
**Status:** resolved. Registry structure and executed scientific evidence now have
separate names, commands, guarantees, and release gates.

## What

`validate_scientific_evidence.py` reports that the scientific evidence registry is valid
after checking only that every cited pytest node is syntactically defined. It neither
collects nor executes those nodes. Consequently, the validator itself cannot distinguish
a passing scientific oracle from a test whose body fails, skips unconditionally, or has
no scientific assertion.

```bash
$ python devtools/scripts/validate_scientific_evidence.py
Scientific evidence registry valid: 43 validated, 0 partial, 0 gaps.
```

That output is a valid statement about registry structure. It is not, by itself, evidence
that the 47 cited nodes passed.

## How

`devtools/scripts/validate_scientific_evidence.py::_test_node_exists` parses the cited
file with `ast`, gathers top-level function names, and returns success when the requested
name is present. `validate_registry` then treats that successful lookup as sufficient
for the registry entry. No pytest result enters the data model or the validation result.

The CI configuration partly compensates for this separation: `ci-weekly.yaml` runs
`tests/scientific_truth` after validating the registry, and `ci-full.yaml` runs the full
suite. The fast release gate and `ci-devguide.yaml`, however, run only the structural
validator while its success message and generated matrix use the status `validated`.

## Why

The matrix is the normative scientific-evidence record for stable APIs. A local release
assessment can therefore report 43 validated capabilities without executing any of the
nodes on which those classifications depend. Separate CI execution reduces the chance
of publishing a regression, but it does not make the validator's claim self-contained
and does not protect against unconditional skips or assertion-free evidence tests.

## What is measured and what is assumed

Inspected: the AST-only node lookup, the registry validation path, the fast release-gate
membership, and the scientific-test invocations in `ci-weekly.yaml` and `ci-full.yaml`.

Measured on 2026-09-02: the current registry contains 43 capabilities, all classified
`validated`, backed by 47 cited test nodes. The command above validates the registry
without invoking pytest.

Assumed: none. This report does not claim that any current scientific result is wrong or
that the cited tests fail.

Measured after the repair on 2026-09-19: all 47 unique registered nodes collected as
54 parametrized cases and passed with zero failures, errors, or skips. The focused
validator, executor, workflow-contract, and complete Scientific Truth battery passed
119 tests. The complete MolSysMT suite passed 10,211 tests with 11 unrelated,
dependency-dependent skips, and the fast release gate passed 13/13.

## What was refuted

*The scientific suite is never executed in CI.* Refuted. The weekly workflow explicitly
runs `python -m pytest --receptor=ci tests/scientific_truth`, and the full workflow runs
the complete pytest suite. The defect is the meaning and self-containment of this
validator and its matrix, not the absence of all downstream execution.

*A defined node is sufficient evidence.* Refuted as a gate property. Definition proves
addressability, not a passing oracle or a meaningful assertion.

## Scope and exclusions

Covers the contract between the evidence registry, its generated matrix, and the
validator that certifies them. Covers handling of failing, skipped, uncollectable, and
assertion-free cited nodes.

Excludes changing scientific algorithms, tolerances, or the current evidence
classifications unless executing the nodes reveals a separate defect. Excludes the
docstring work in uibcdf/molsysmt#187.

## Acceptance criteria

1. The maintained contract distinguishes registry-structure validation from executed
   scientific evidence.
2. A cited node that fails collection or execution cannot support `validated` in the
   release evidence result, or the matrix and command output explicitly stop claiming
   that structural validation establishes executed evidence.
3. Unconditional skips and empty scientific tests have an explicit policy and an
   executable guard.
4. The fast and heavy release instructions identify which step establishes each claim.

All four criteria were met on 2026-09-19.

## Resolution

`validate_scientific_evidence.py` remains a cheap structural validator and now says
explicitly that it did not execute tests. The generated matrix carries the same warning
and the structural gate rejects cited functions without an assertion-bearing operation.
This anti-emptiness check is not presented as proof that an assertion is scientifically
adequate; independent-oracle metadata and review remain the authority for that claim.

`execute_scientific_evidence.py` is the separate execution authority. It validates the
registry, runs exactly its unique node IDs once and without xdist, parses pytest's JUnit
result, and fails on collection failure, test failure, error, or any skip. Its optional
JSON certificate records the commit, tracked-source state, Python, platform, aggregate
outcomes, and complete node inventory. Release workflows use `--require-clean`, so a
certificate cannot attribute modified tracked source to the named commit.

`ci-full.yaml` and `ci-weekly.yaml` execute this zero-skip gate and retain one certificate
per matrix cell. The fast gate and `ci-devguide.yaml` retain only structural validation.
The release guide and Scientific Validation Contract now state which result establishes
each claim.

## Dependencies and risks

The resolved boundary keeps the dependency-light structural validator fast and runs the
47 registered nodes only in the heavy gate. The measured local execution takes about
six seconds. A missing optional oracle now makes the release certificate fail rather
than silently reducing its evidence.

## Provenance

Inspected and counted on 2026-09-02 at repository commit `48ea5b91c`, Linux
7.0.0-28-generic x86_64, Python 3.13.14.

Reproduced and repaired on 2026-09-19 on Linux 7.0.0-28-generic x86_64, Python
3.13.14, from a working tree based on `41d42449e`.
