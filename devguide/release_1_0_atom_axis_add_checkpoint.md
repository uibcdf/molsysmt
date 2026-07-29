# Atom-Axis Add Integration Checkpoint

**Date:** 2026-07-29
**Status:** `DONE`
**Exact implementation commit:** `2865c3122`
**Release stage:** F5 candidate-base preparation

## Purpose

This checkpoint integrates the pre-existing `add()` work before the exact-
commit release campaign. It does not add another release stage or change the
96% weighted completion. It ensures that the F5 candidate starts from one
coherent atom-axis addition contract instead of an incomplete working tree.

## Contract

`add()` grows a molecular system along the atom axis. It is distinct from
`append_structures()` and `concatenate_structures()`, which grow or join the
structure axis.

For native structural data:

- source atom and structure selections are applied before addition;
- source and target structure counts must match after selection;
- coordinates, velocities, B factors, and occupancies are concatenated when
  both sides provide the attribute;
- a one-sided atom-aligned attribute is dropped with
  `StructuralAttributeDropWarning`;
- target structure-aligned metadata such as time, box, and energies is
  preserved;
- the complete candidate payload is validated before assignment;
- native `MolSys.add()` commits topology and structures together or leaves the
  target unchanged.

## Repairs included

- `molsysmt.Structures` form dispatch now calls atom-axis `add()` instead of
  structure-axis `append()`.
- `molsysmt.basic.add()` processes every source in a source sequence, passes
  only adapter-supported arguments, and preserves scalar return shape for a
  scalar non-in-place target.
- Native `MolSys` addition no longer leaves a topology-only mutation when
  structural validation fails.
- Direct native and public regressions cover shared attributes, one-sided
  attributes, warning-as-error atomicity, selected axes, multiple sources, and
  structure-count rejection.
- The native contract, User Guide tutorial, public docstring, and Common Core
  module 18 describe the same behavior.

## Verification

- focused native and public regression gate: 30 passed;
- expanded add/native/form/MolSys/structural-growth gate: 554 passed;
- `molsysmt.basic.add` doctest: 1 passed;
- affected User Guide and Common Core notebooks: 2 passed from fresh kernels;
- Ruff over the complete `molsysmt` package and affected tests: passed;
- developer-guide and course validators: passed;
- fast release gate: 12/12 passed;
- `git diff --check`: passed.

The 554-test result was produced on the implementation worktree immediately
before commit `2865c3122`. The implementation did not change between that run
and the commit. F5 still requires its clean exact-commit full suite, wheel, and
documentation gates; this checkpoint does not claim those results.

## Resume point

Use `2865c3122` plus this documentation-only checkpoint as the clean base for
F5. The next action remains the exact-commit release campaign. No atom-axis
addition work is pending unless that campaign exposes a new defect.
