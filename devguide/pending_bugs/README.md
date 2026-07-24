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

- `form_attributes_declared_without_getters.md`

### Incorrect success or hidden failure

- `smonitor_warn_drops_structured_extra.md`
- `dihedral_angles_broadcast_mismatch_pbc.md` — a documented broadcast-shaped `angles`
  argument is honoured on the non-periodic path of `set_dihedral_angles` but read out of
  bounds (unchecked, `njit`) on the periodic one.

### Contract and maintainability

- `course_module_numbering_overlaps.md`
- `sasa_is_orthogonal_typo.md` — `_is_orthogonal` tests a box length instead of an
  off-diagonal, so the orthogonal fast path in the SASA MIC wrap is unreachable. Results
  stay correct; the cost is that cubic boxes pay for the triclinic branch.

Severity within a group still depends on the affected public workflow. Confirmed
bugs require a regression test; suspected bugs require a minimal reproduction
before implementation.
