---
summary: Keep controlled Viewer artifacts outside the scientific source checkout.
issue: uibcdf/molsysmt#669
status: partial
opened: 2026-11-09
closed:
severity: medium
verification: reproduced
area: [ci, provenance, viewer]
guard: devtools/tests/test_execute_scientific_evidence.py::test_controlled_viewer_wheel_preserves_clean_source_certificate
normative:
blocked_by: []
supersedes: []
---

# Controlled wheel dirties the scientific checkout

**Status:** correction prepared in PR #668; owner review and corrected hosted
receiving remain required. No source-cleanliness rule is relaxed.

## What

Full CI downloads the controlled Viewer wheel under `controlled-wheelhouse/`
inside the checked-out source. Seven emitted certificates in run 42659643113
report 107/107 scientific cases passing but refuse release eligibility because
that file is untracked. This is an artifact-placement failure, not evidence of
incorrect scientific results or a defect in the certificate's clean-source rule.

## How

The independently verified original Linux/Python 3.14 artifact is 13694390542,
ZIP SHA-256 `98829f7874b074c426fcfd9f56e62f5c109daf5ef086bdef8b312a0ecb866c53`.
Its before/after states retain commit `da08fb1e4518d7334f07dbac9f1263d3b717d814`,
clean tracked source and the same unknown wheel path. The public failure and
remaining matrix dispositions are attached to the owning issue.

The regression uses the actual workflow's build/download/install/upload paths,
an independent real Git commit and the actual certificate. Before correction
it gives one failure/one pass: the declared workflow placement fails, while a
deliberately untracked wheel is correctly refused. The correction places all
wheel paths under runner temporary storage and preserves shell quoting. The
test also expands the actual install pattern in Bash with spaces in the runner
directory, proving it still supplies one artifact argument. The refusal control
continues to put a wheel inside source; no allowlist or ignore is broadened.

The cancelled macOS/Python 3.14 job 129307576249 has runner_id=0, no runner name
and no steps. Its 45-minute elapsed interval is queued time, not an observed
test timeout. No scientific certificate exists for that unexecuted cell.

The corrected affected collection passes 160 cases with fixed inputs, including
the complete certificate tests and required addon/dependency preflights. An
intermediate attempt retains nine failures/151 passes: the first quoting layout
was not recognized by the existing static route audit and did not match the
new test's raw-pattern selector. Canonical quoting of the dynamic temporary
root fixes both while real Bash expansion still preserves spaces. These are
prepared-route failures, not additional scientific defects or waived checks.

## Why

A dependency artifact is not scientific source. Keep acquisition products
outside checkout while retaining strict source identity, exact Viewer pins,
one portable wheel, zero-skip evidence and the complete native matrix. The
existing smoke command also receives the certificate regression module.

Scoped local receiving and failed originals belong to the consumer's private
packet under uibcdf/molsysviewer#315. The source fix does not authorize packages,
tags, promotions, release claims or treating the incomplete matrix as passing.
