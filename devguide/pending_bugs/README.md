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

- `conversion_fidelity_wip_contract_gaps.md` — three untracked fidelity modules
  expose 38 failures across audit scopes, native dictionary exhaustiveness,
  strict loss detection, schema and adapter gaps, and a separate PDB workstream;
  the proposed release audit currently fails during import.
- `smonitor_warn_drops_structured_extra.md`
- `dihedral_angles_broadcast_mismatch_pbc.md` — a documented broadcast-shaped `angles`
  argument is honoured on the non-periodic path of `set_dihedral_angles` but read out of
  bounds (unchecked, `njit`) on the periodic one.
- `wrap_to_mic_triclinic_not_minimum_image.md` — `wrap_to_mic` applies the minimum image
  convention on orthogonal boxes but not on triclinic ones (55/300 sampled vectors), because
  its 27-image search iterates images of the original vector instead of the wrapped one.
  `unwrap.py` already implements the correct pattern.

### Contract and maintainability

- `course_module_numbering_overlaps.md`
- `principal_axes_eigenvector_sign_unspecified.md` — the principal axes are returned with
  whatever sign LAPACK produced, so the output is not a function of the input alone and can
  flip with a LAPACK version, thread count or compute backend.
- `sasa_is_orthogonal_typo.md` — `_is_orthogonal` tests a box length instead of an
  off-diagonal, so the orthogonal fast path in the SASA MIC wrap is unreachable. Results
  stay correct; the cost is that cubic boxes pay for the triclinic branch.

Severity within a group still depends on the affected public workflow. Confirmed
bugs require a regression test; suspected bugs require a minimal reproduction
before implementation.
