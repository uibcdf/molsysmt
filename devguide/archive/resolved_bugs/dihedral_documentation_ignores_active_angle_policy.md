---
summary: Dihedral documentation ignores the active angle policy
issue: uibcdf/molsysmt#357
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: low
verification: reproduced
area: [docs, structure, units]
guard: tests/structure/get_dihedral_angles/test_angle_policy.py::test_dihedral_angles_follow_active_angle_policy
normative: docs/content/user/foundations/governance/quantities_and_units.md
blocked_by: []
supersedes: []
---

# Dihedral documentation ignores the active angle policy

**Reported:** 2026-10-09 by DockingMT in uibcdf/molsysmt#357.
**Status:** Resolved; documentation matches the existing configurable angle output.

## What

The public `get_dihedral_angles` docstring promises degrees in its description
and return section. Its output instead follows the active PyUnitWizard angle
policy. A four-atom analytical 45-degree torsion supplied in angstroms returns
`0.7853981633974484 radian` under a radians policy and
`45.00000000000001 degree` under a degrees policy, including pm/fs contexts.

## How

The function correctly wraps kernel output in radians and calls
`puw.standardize`. MolSysMT's initial policy includes radians and respects an
already active application/user policy. The two degrees-only prose claims do
not describe either the initial policy or the configurable public boundary.

## Why

A consumer interpreting unitless angular magnitudes according to the docstring
could apply the wrong target angle. DockingMT already extracts radians
explicitly; its independent controls remain owned by uibcdf/dockingmt#17.
No numerical defect or consumer workaround has been demonstrated here.

## What is measured and what is assumed

Executed the issue's four-atom public reproduction on source `c3c6303f4` in the
shared Linux development environment, Python 3.14.7 and PyUnitWizard
`0.28.1+3.g2ab37a5`. Both explicit radian extractions equal pi/4. The existing
Toolbox notebook already converts its displayed/plot values to degrees.
No installed replacement artifact or browser qualification is claimed.

## What was refuted

Changing the numerical implementation or globally forcing degrees would break
the user policy. The existing runtime behavior is correct; the prose is wrong.

## Scope and exclusions

Update the docstring, Foundations, Toolbox, an applicable analysis recipe and
the unit-safety course. Preserve code cells and saved notebook outputs when
editing narrative only. Do not change kernels, defaults, input normalization,
candidate refs, original package bytes or paused publication.

## Acceptance criteria

- Return documentation states the active angle policy and explicit extraction.
- An analytical torsion has the same physical value under radians and degrees.
- Unit contexts restore the enclosing/session policy.
- The public doctest and existing dihedral regressions pass.
- Maintained user guidance explains the same contract.

## Resolution — 2026-10-09

The docstring description and Returns section now identify the active angle
policy. Notes and an executable bundled-system example distinguish physical
quantities from explicitly converted numerical magnitudes. Foundations holds
the durable output contract; Toolbox, the trajectory-analysis recipe and Common
Core Module 9 explain the same distinction. Notebook edits change narrative
only; code cells and saved outputs are preserved.

The guard uses an independent analytical pi/4 torsion, angstrom inputs and
nested pm/fs contexts. It checks the actual quantity unit, magnitude, explicit
radian extraction and enclosing/session policy restoration. It protects the
existing numerical contract; the named normative document owns the prose
correction. No text-matching validator is added.

Commands in the shared development environment:

```bash
python -m pytest tests/structure/get_dihedral_angles --receptor=llm -n12
python -m pytest molsysmt/structure/get_dihedral_angles.py --doctest-modules --receptor=llm -n12
```

Results: **6 passed** (four existing regressions and two angle-policy controls),
and **1 doctest passed**. The bundled 0.4 example emits the expected legacy-H5MSM
warning; migration is separately covered and is outside this issue.

Ruff lint and formatting pass repository-wide. The fourteen fast release
gates pass, including developer-guide integrity and course structure. A direct
AST comparison confirms unchanged function computation, and JSON comparisons
confirm unchanged code/output cells in all three edited notebooks. These are
scoped source checks; heavy qualification matrices remain paused.
