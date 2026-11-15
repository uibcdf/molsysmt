---
summary: Structure scene generator still calls the retired topology quartet API
issue: uibcdf/molsysmt#760
status: resolved
opened: 2026-11-15
closed: 2026-11-15
severity: medium
verification: reproduced
area: [docs, structure]
guard: tests/documentation/test_structure_scene_quartets.py
normative:
blocked_by: []
supersedes: []
---

# Structure scene generation calls a retired quartet API

**Reported:** 2026-11-15 while preparing the separate #759 lesson scene.
**Status:** active; bounded namespace repair and actual-statement receiving.

## What

`docs/generate_static_views/tools_structure.py` obtains phi quartets through
`msm.topology.get_dihedral_quartets`, removed when graph-dependent operations
moved to `chemical_states`. Reaching its torsion scenes raises `AttributeError`.

## How

The regression executes the generator's actual `phi_quartets`, `molsys_set` and
`molsys_shifted` assignments on its bundled villin input. AST extraction avoids
executing unrelated lipid, alignment and scene-export operations. Before the
repair, both ordinary and pm/fs policy cases fail at the retired namespace.

## Why

Maintainers cannot regenerate these torsion illustrations. This finding does
not show that the already committed scene coordinates are incorrect. Update
only the supported owning namespace; do not regenerate unrelated scenes.

## Acceptance criteria

The real statements obtain C-N-CA-C quartets, set the chosen phi to 60 degrees,
shift it by 90 degrees and preserve the source. Signed-angle assertions use
independent NumPy geometry and circular differences under two unit policies.
Existing exported scene bytes remain unchanged.

## Provenance

Linux, existing Python 3.14.7, source parent 1b3b16191 and unchanged native
binary 4ffb82e4. The finite baseline has two failures and no passed cases;
expected legacy-H5MSM warnings describe the unchanged bundled 0.4 fixture.
No package construction, installation, hosted qualification or scientific
profile certification is part of this correction.

## Resolution — 2026-11-15

The actual notebook uses the explicit capped sequence and the existing public
quartet, copy and geometric-edit tools. The returned five phi, five psi and
five omega quartets reach the declared targets, modulo the angular branch cut.
Independent NumPy angles, unchanged source coordinates, cap connectivity and
bond-length preservation are checked under nm/ps and pm/fs policies. Targets
apply to returned quartets; the lesson does not classify or predict a stable
helix. The extended-region challenge remains a declared modeling exercise.

All seven code cells execute in a fresh kernel. A dedicated generator executes
the same scientific cells and exports only this model. The saved scene is
received against calculated coordinates and atom/group axes under both unit
policies. The browser loads all 109 atoms, actual Mol* coordinates and a framed
ball-and-stick image using local assets under a /molsysmt/ deployment prefix.
The screenshot is inspected. This static scene does not close #615's distinct
cold Jupyter canvas investigation or qualify the final installed pair.

The final overlapping selected cohort, including adjacent construction/torsion
controls and #760/#761, passes 23 cases without omissions. The original four
unsupported-argument failures and authored test/preflight mistakes remain
unsuccessful evidence in the
[receipt](../../../devtools/data/peptide_course_receiving_759_761_20261115.json).
No runtime API, scientific method, dependency or native binary changes.
