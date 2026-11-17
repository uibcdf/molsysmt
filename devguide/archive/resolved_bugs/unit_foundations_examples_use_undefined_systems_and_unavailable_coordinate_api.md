---
summary: Unit foundations examples use undefined systems and unavailable coordinate API
issue: uibcdf/molsysmt#770
status: resolved
opened: 2026-11-16
closed: 2026-11-17
severity: medium
verification: reproduced
area: [docs]
guard: tests/documentation/test_unit_foundations_examples.py::test_unit_foundations_examples_keep_physics_and_restore_application_policy
normative:
blocked_by: []
supersedes: []
---

# Unit foundations examples do not demonstrate their claims

**Reported:** 2026-11-16, during #334's frozen native documentation review.
**Status:** corrected, executed and locally rendered with scoped policy/physical checks.

## What

Running the Python blocks in `quantities_and_units.md` raises `NameError` on
undefined `system`. The next block calls unavailable
`msm.structure.get_coordinates`. The four advertised equivalent calls do not
perform the same calculation, and merely changing the quantity backend does
not select an angstrom length standard. Direct assignments to configuration
attributes also fail to demonstrate supported scoped application policy.

## How

The old example describes input flexibility without providing a molecular input
or comparing physical results. It calls all bare-array quantity inputs universally
supported although their interpretation belongs to each operation's contract.

The replacement compares three actual length representations for one orthogonal
box: an angstrom string, a Pint quantity in pm and the box factory's explicitly
documented nm array. A second block uses OpenMM input/output with an explicit
angstrom standard inside `puw.context`, then demonstrates policy restoration.
No public runtime behavior or unit policy is changed.

## Why

This foundations page teaches a central cross-component numerical contract.
Examples that neither execute nor compare equivalent physics can mislead users
about backend selection, unit inference and application configuration authority.

## Evidence and limits

The original complete-page guard reproduces the `NameError`; the corrected
page executes with an outer Pint/pm/fs/degrees policy. Analytical diagonal boxes
protect physical values independently of their presentation backend, and the
outer form/length unit is verified after the OpenMM context. The first small
baseline contains other sparse-guard expectation failures, recorded under #769;
those are not additional unit defects. Both attempts are retained in the
[finite receiving record](../../../devtools/data/independent_native_work_334_20261116.json).

This is documentation receiving with installed optional OpenMM. It does not
establish every optional backend, numerical method or final package qualification.

## Acceptance

- All Python blocks execute together without substituted inputs.
- String, Pint and documented bare-array lengths yield the same analytical box.
- OpenMM quantities retain explicit dimensions and the chosen output standard.
- Exiting the context restores the real prior application form and units.
- Strict rendering retains the example code and reader-facing explanations.

## Local closeout — 2026-11-17

The complete strict site builds successfully, then the visually reviewed code
folding is rebuilt strictly. All 54 selected articles and their local links,
anchors and twelve figures are received. Seven static browser reading views
have no local HTTP or page errors; the changed examples are visually inspected.
The seven final example controls pass with no skips after the layout correction.
Original failed attempts and their exact interpretations remain retained.
This receiving neither renders a live molecular canvas nor qualifies an installed
release pair. No scientific runtime or native binary is changed.
