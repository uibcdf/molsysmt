---
summary: Placement recipe guard rejects the added rotation example by counting code fences
issue: uibcdf/molsysmt#651
status: active
opened: 2026-11-08
closed:
severity: medium
verification: reproduced
area: [tests, docs]
guard: tests/documentation/test_move_away_examples.py::test_placement_recipe_preserves_centers_modes_and_ownership
normative:
blocked_by: []
supersedes: []
---

# Execute placement outcomes rather than count code fences

## What

The placement recipe gained its declared captured-center rotation example, but
its executable guard still requires exactly four Python fences. There are now
five. The full-source partial stream on `fbafc69a5` records `assert 5 == 4`
before any example runs. No incorrect molecular geometry is established by
that guard failure. The public recipe and rotation were already separately
received; the stale blanket count is a test-lifecycle omission.

## Correction and acceptance

Execute every Python fence and require the literal resulting coordinates for
source-anchor centering, automatic increment, explicit offset, reflection and
inverse, captured-center positive rotation, and unchanged original ownership.
Retain the recipe's own midpoint and geometry assertions. Require nonempty
examples, but do not tie scientific acceptance to how prose splits code fences.
Run under nm/ps and pm/fs application policies. Preserve the recipe, anchors,
all examples, output values and underlying operators.

Receive the whole documentation test directory and adjacent public graph/H
policy examples, then fast checks. Inspect other existing fence/cell guards at
this checkpoint. Full-source #612 remains pending until the exact source gate
completes; a premature next eight-GiB attempt was deliberately stopped once
this final partial-stream failure was recovered. All interrupted attempts
remain in the resource record. Do not claim that earlier partial streams were
complete or failure-free.

## Nondefault-unit control — 2026-11-08

The first expanded documentation receiving yields 597 passes and one failure
under pm/fs: the recipe compared converted nm values to integer literals with
bitwise equality (a 4.44e-16 difference). Preserve the exact no-write guarantee
by comparing to an independent unit-bearing coordinate snapshot in its own
unit, and test expected physical geometry separately at rtol=0/atol=1e-12 nm.
This is a comparison-contract correction, not a tolerance-based waiver of a
source mutation. The default geometry and all examples remain unchanged.

## Directed acceptance — 2026-11-08

The corrected full documentation directory plus adjacent graph/H-policy
examples passes 598 cases, zero skips/failures/errors. Both unit policies
execute every placement fence and independent literal-coordinate checks.
The recipe now keeps an owned unit-bearing copy for exact no-write checks.
The source operators, scenario coordinates, anchors and course code remain
unchanged. Existing Sphinx/provider warnings are preserved. Peak memory is
1,022,181,376 bytes under the two-GiB/one-CPU cap, without high/max/OOM events.
Other inspected fixed fence/cell guards match their current inputs; this
scoped receiving does not certify every documentation page or complete #612.
