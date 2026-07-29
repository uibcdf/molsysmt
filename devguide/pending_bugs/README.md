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

- `sphinx_warning_baseline_and_api_reference_debt.md` — the documentation builds
  and the course has no nonexistent toctree target, but historical API,
  navigation, heading, title, and notebook-metadata warning families remain.
  The baseline is measured and explicitly accepted as non-blocking for the 1.0
  source release; new warnings must not be hidden or globally suppressed.
- `iterator_without_explicit_attributes_fails_for_partial_forms.md` — the
  documented molecular-system-yielding mode fails during construction for
  coordinate-only and topology-plus-trajectory inputs; explicit attribute
  iteration remains usable.

Severity within a group still depends on the affected public workflow. Confirmed
bugs require a regression test; suspected bugs require a minimal reproduction
before implementation.

## Recently closed

`course_module_numbering_overlaps.md` was archived on 2026-07-29 after the two
remaining Common Core narrative references were replaced with stable semantic
links and a full Sphinx build completed. The 156-notebook structural contract
remains guarded by `devtools/scripts/validate_course.py`.

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
[`rust_migration_documentation_and_test_residue.md`](../archive/resolved_proposals/rust_migration_documentation_and_test_residue.md)
rather than left implicit.
