---
summary: Evaluate single-assessment delegation for public molecular-system predicates
issue: uibcdf/molsysmt#154
status: open
opened: 2026-08-13
closed:
verification: measured
area: [basic]
guard:
normative:
blocked_by: []
supersedes: []
---

# Evaluate single-assessment delegation for public molecular-system predicates

**Reported:** 2026-08-13, while re-auditing the withdrawn diagnosis in
uibcdf/molsysmt#147.
**Status:** open, post-1.0 unless a correctness symptom is found.

## What

Evaluate a single-assessment internal contract for public functions whose
`molecular_system` argument has already been classified by the boundary digester. The
first target is `molsysmt.basic.has_attribute`: keep full public validation, but avoid
reassessing the same native object inside `validate_molecular_system_argument` and again
inside the selected form adapter.

## How

Split classification from enforcement without weakening either:

1. let `digest_molecular_system` obtain one `MolecularSystemAssessment`;
2. let the validator enforce that existing assessment instead of calling
   `assess_molecular_system` again;
3. after the public `has_attribute` boundary has validated the input and selected a
   registered form, delegate to that form's predicate with `skip_digestion=True`;
4. retain ordinary digestion for direct adapter calls and for every public call whose
   input has not crossed that boundary.

The design should be generalized only after measuring another public function. It must
not become an implicit global cache or an identity-based certification protocol.

## Why

A direct public `msm.has_attribute(native_molsys, 'n_atoms')` currently performs four
molecular-system assessments: two at the public boundary and two at the form-adapter
boundary. The body is a cheap predicate, so the redundant work is visible even though
the absolute cost is small.

## What is measured and what is assumed

Measured on 2026-08-13 with the bundled MolSysViewer dialanine `MolSys`, Python 3.13:

| operation | assessments | median baseline | controlled single-assessment probe |
| --- | ---: | ---: | ---: |
| `msm.has_attribute(..., 'n_atoms')` | 4 | 142–161 µs | about 79–137 µs, depending on probe scope |
| `msm.get(..., n_atoms=True)` | 2 | 461 µs | 446 µs |
| `msm.select(..., selection='all')` | 2 | 198 µs | 181 µs |
| `msm.get_attributes(...)` | 2 | 21.94 ms | no measurable improvement |

One standalone native `assess_molecular_system` costs about 6.2–6.5 µs in this fixture.
The large relative improvement belongs only to the very cheap predicate; no library-wide
speedup is claimed.

Assumption: passing a previously computed immutable assessment through the validation
step will remain simpler than making several validators independently special-case
native forms. This must be reviewed against composite-list inputs before implementation.

## What was refuted

- The viewer slowdown is not caused by these public-boundary assessments: its 510
  form-level predicates already use the fast path and perform zero assessments.
- A permanent cache is unnecessary and risks staleness when a mutable composite system
  changes.
- Restoring a value passport is rejected; uibcdf/molsysmt#153 removed an unreachable
  protocol that no consumer used.
- Removing digestion from public functions is rejected because digestion also normalizes
  and enforces composite-system consistency.

## Scope and exclusions

This proposal covers redundant assessment and already-validated form delegation at
MolSysMT public boundaries. It excludes MolSysViewer's duplicate inventory computation,
ArgDigest internals, PyUnitWizard canonicity costs, form discovery changes, and general
memoization. It does not block the 1.0 release because no correctness failure or material
end-to-end cost has been demonstrated.

## Acceptance criteria

1. Public invalid, multiple-system, and structurally inconsistent inputs retain the same
   diagnostics and normalization behavior.
2. A native public `has_attribute` call performs one assessment, not four.
3. The form predicate receives `skip_digestion=True` only after successful public
   validation and registered-form selection.
4. Composite-list and path-like inputs have explicit regression coverage.
5. A benchmark records absolute and relative effects without extrapolating the cheap
   predicate result to heavier APIs.
6. The public API and scientific return values remain unchanged.

## Dependencies and risks

The main risk is accidentally accepting a malformed composite system because an
assessment is reused beyond the call in which it was produced. Keep it call-local and
immutable. Schedule after 1.0 so this micro-optimization does not invalidate the current
F5 candidate without a correctness reason.

## Provenance

Measured 2026-08-13 on the MolSysMT development host, Python 3.13, using the installed
editable MolSysMT and MolSysViewer checkouts and the bundled dialanine demo. Timings used
seven repeats for direct operations; the viewer audit used instrumented call counts and
separate alternating operation-level trials. Normal pytest was not needed because this
was a read-only measurement campaign.
