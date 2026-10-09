---
summary: Development CI skipping is implemented and governed
issue: uibcdf/molsysmt#123
status: resolved
opened: 2026-10-09
closed: 2026-10-09
verification: inspected
area: [docs, api]
guard: devtools/tests/test_nightly_full_gate.py
normative: devguide/devtools_and_ci.md
blocked_by: []
supersedes: []
---

# Development CI skipping is implemented and governed

**Reported:** Historical issue reconciled during the 2026-10-09 pre-1.0 audit.
**Status:** Resolved; the existing mechanism answers the original request.

## What

The requested mechanism exists: internal maintainers can use a deliberate
`[skip ci]` marker on a direct development push. Ordinary pushes run smoke;
PRs must not use skip markers. The nightly full-suite decision retains skipped
commits as debt until a complete Linux matrix succeeds; the weekly route is
independent of markers. A backlog probe does not execute or clear that debt.

## How

The implemented smoke condition, `nightly_full_gate.py`, scheduled workflow and
existing gate tests cover this behavior. The maintained developer-tools/CI guide
owns the workflow contract. During reconciliation, its Python range was stale
(3.11–3.13 instead of the actual 3.11–3.14), and three guides treated a skip
marker as an unconditional release disqualification. They now match the accepted
root/suite rule: omit markers for new candidates; an original recorded producer
may use an explicitly authorized manual recovery route only with every required
exact-commit and installed-artifact gate executed and verified. Preserve producer
identity and original bytes/digests. No workflow or validation gate is weakened.

## Why and exclusions

The request is delivered, rather than a remaining post-1.0 capability. Reconcile
the obsolete issue and contradictory instructions; no new skip route, dispatch,
full matrix, artifact rebuild, publication authorization or candidate selection
is introduced. The existing release pause and all mandatory qualification gates
remain in force. No calendar schedule or unsupported interpreter is changed.

## Acceptance and provenance

Inspected source `e2de5f88c` and maintained contracts in the shared Linux/Python
3.14.7 development environment. The named guards are executed as part of this
bounded reconciliation; final results are recorded below before closure.

Executed the named existing selection with pytest-receptor and twelve workers:
**21 passed**, as part of the 57-case reconciliation selection. Results
are scoped source evidence; no hosted full matrix was dispatched.

All fourteen fast gates and repository-wide Ruff checks pass. This checkpoint
does not replace an exact-candidate full or installed-package matrix.
