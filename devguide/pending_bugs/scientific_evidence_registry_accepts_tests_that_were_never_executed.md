---
summary: Scientific evidence registry accepts tests that were never executed
issue: uibcdf/molsysmt#196
status: open
opened: 2026-09-02
closed:
severity: high
verification: inspected
area: [tests, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Scientific evidence registry accepts tests that were never executed

**Reported:** 2026-09-02, split from the gate audit in uibcdf/molsysmt#187.
**Status:** open.

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

## Dependencies and risks

Executing 47 nodes inside every structural invocation may make a fast, dependency-light
validator slow or unavailable. A better boundary may keep structural validation fast
and add a separately named execution certificate to the release process. The chosen
design must not hide skips as successes.

## Provenance

Inspected and counted on 2026-09-02 at repository commit `48ea5b91c`, Linux
7.0.0-28-generic x86_64, Python 3.13.14.
