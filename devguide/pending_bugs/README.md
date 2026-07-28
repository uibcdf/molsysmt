# Pending Bugs

This directory contains unresolved defect reports. Entries are evidence and work
queues, not normative specifications.

A report should contain a reproduction or concrete inspection evidence, affected
public behavior, severity, likely cause, and acceptance tests. When a defect is
fixed, add regression tests, update the relevant normative guide, and remove or
archive the report in the same change.

The presence of a report takes precedence over an unqualified historical claim
that the affected surface is fully verified.

## Current triage

### Scientific-integrity risk

- `form_attributes_declared_without_getters.md` — Tier 1 is resolved; Tier 2 and
  Tier 3 remediation is pending.

### Incorrect success or hidden failure

- `smonitor_warn_drops_structured_extra.md` — reported upstream and pending there;
  worked around inside MolSysMT.

### Contract and maintainability

- `course_module_numbering_overlaps.md` — **the structural defect is closed.** The
  Common Core is 1–20, every Path is 21–54, and the numbering contract is guarded
  executably by `devtools/scripts/validate_course.py`, which passes as part of the
  fast release gate. What remains is two editorial cross-references inside Common
  Core notebooks 12 and 17 that need a content decision rather than a number swap;
  they belong to lifecycle stage F4. The report is kept open only for those two
  items — do not read it as an open numbering defect.

Severity within a group still depends on the affected public workflow. Confirmed
bugs require a regression test; suspected bugs require a minimal reproduction
before implementation.

## Recently closed

Four reports filed on 2026-07-24 during the Rust port described defects in the
Numba implementation. Segment D removed that implementation, and the Rust kernels
that replaced it implement the correct behaviour, so the reports were archived on
2026-07-28 with a resolution note under `../archive/resolved_bugs/`:
`dihedral_angles_broadcast_mismatch_pbc.md`, `sasa_is_orthogonal_typo.md`,
`wrap_to_mic_triclinic_not_minimum_image.md`, and
`principal_axes_eigenvector_sign_unspecified.md`.

A report is not closed merely because the implementation it describes was deleted:
each archived note records where the correct behaviour now lives and which test
guards it. Where no test does, that gap is tracked in
[`rust_migration_documentation_and_test_residue.md`](../pending_proposals/rust_migration_documentation_and_test_residue.md)
rather than left implicit.
