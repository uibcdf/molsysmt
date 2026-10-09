---
summary: Hydrogen-bond output design is implemented
issue: uibcdf/molsysmt#22
status: resolved
opened: 2026-10-09
closed: 2026-10-09
verification: inspected
area: [docs, api]
guard: tests/interactions/hbonds/test_buch_results.py::test_buch_analysis_keeps_coverage_roles_and_actual_participant_universe
normative: devguide/interactions_api.md
blocked_by: []
supersedes: []
---

# Hydrogen-bond output design is implemented

**Reported:** Historical issue reconciled during the 2026-10-09 pre-1.0 audit.
**Status:** Resolved; the existing mechanism answers the original request.

## What

The original question compared ragged lists, dictionaries, tensors and a dedicated
hydrogen-bond object. The implemented public result separates compact typed
relations from sparse occurrences in the general `molsysmt.Interactions` class.
Buch and Luzard-Chandler optionally return that result; legacy outputs retain
rectangular arrays for equal counts and aligned lists for variable counts,
including empty structures.

## How

The owning contract is the Interaction Analysis API. The Buch guard calculates
actual varying/empty structures, compound donor/hydrogen/acceptor roles, atom
queries, evaluated scope and a named H5MSM round trip. It is existing behavioral
evidence, not a new test reproducing an implementation detail. No implementation
change or new detector is needed to answer the original design question.

## Why and remaining ownership

Keeping this historical question open incorrectly suggests that the result
representation remains undecided. Close its design scope; #250, #254 and #334
retain final coordinated-candidate acceptance, including the release pause.
Individual editing and streaming remain separately owned by #335 and #336.
The result/profile contract remains experimental; this closure does not stabilize
scientific profiles or qualify a replacement package.

## Acceptance and provenance

Inspected source `e2de5f88c` and maintained contracts in the shared Linux/Python
3.14.7 development environment. The named guards are executed as part of this
bounded reconciliation; final results are recorded below before closure.

Executed the named existing selection with pytest-receptor and twelve workers:
**30 passed**, as part of the 57-case reconciliation selection. Results
are scoped source evidence; no hosted full matrix was dispatched.

All fourteen fast gates and repository-wide Ruff checks pass. This checkpoint
does not replace an exact-candidate full or installed-package matrix.
