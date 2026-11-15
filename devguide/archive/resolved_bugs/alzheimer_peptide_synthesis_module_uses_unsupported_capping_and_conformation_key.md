---
summary: Alzheimer peptide-synthesis module uses unsupported capping and conformation keywords
issue: uibcdf/molsysmt#759
status: resolved
opened: 2026-11-14
closed: 2026-11-15
severity: medium
verification: reproduced
area: [docs, build]
guard: tests/documentation/test_peptide_synthesis_course.py
normative:
blocked_by: []
supersedes: []
---

# Alzheimer peptide synthesis uses unsupported builder keywords

**Reported:** 2026-11-14 while tracing the input context of #758.
**Status:** resolved; actual-cell, saved-scene and article receiving under #334.

## What

`docs/content/course/Path_Alzheimer/24_Peptide_Synthesis.ipynb` calls
`msm.build.build_peptide('KLVFF', n_terminal='ACE', c_terminal='NME')` and
`msm.build.build_peptide('KLVFF', configuration='alpha-helix')`.
Neither capping keyword nor `configuration` exists in the current public builder
signature. Its first plain KLVFF construction remains supported.

## How

The actual lesson contains these calls in its second and third code cells.
The current native builder constructs from ordered group labels: explicit cap
labels belong in that input sequence. A conformation requires the appropriate
existing state-dependent quartet and geometric torsion operations, with measured
results, rather than a keyword that the builder does not accept.

## Why

The advertised capped-versus-uncapped and helical examples do not run on the
current API. Preserve these teaching scenarios and scientific limits while
using supported tools. This is documentation correctness, not a reason to add
new convenience keywords or redesign the peptide builder before 1.0.

## Proposed bounded correction

- Keep KLVFF, the initial construction, the explicit ACE/NME comparison and the
  helical-coordinate scenario.
- Use supported cap labels and public quartet/torsion operations; verify the
  actual groups, bonds and measured phi/psi instead of only the requested name.
- State that initial/assigned geometry does not establish a complete chemical
  state, an energy minimum or a stable helical population.
- Preserve the visualization intent through the maintained static-export path,
  with a dedicated generator and actual saved output receiving.
- Execute the complete corrected lesson under ordinary and non-default units,
  receive independent measurements and inspect the rendered article.

## What is measured and what is assumed

The original diagnosis was source-inspected. The separate #758 geometry work
built only plain KLVFF and did not qualify this module. The baseline and the
completed actual-cell, kernel and scene receiving below now qualify this
bounded documentation correction.

## Acceptance criteria

The actual module executes on supported public calls, retains all scenarios,
reports correct group/index/unit semantics and measured torsions, and preserves
its static visualization. Add a regression on the real cells, with independent
inventory/geometry expectations. A renamed token or green Sphinx build is not
sufficient.

## Provenance

Inspected on cc58c0512 plus the separate #758 documentation/test delta. No runtime
API, provider, engine, dependency or native binary is changed by this report.

## Implementation choice — 2026-11-15

Retain uncapped KLVFF and construct the explicit capped sequence
`AceLysLeuValPhePheNme`. Derive phi/psi/omega quartets from the actual stored graph,
copy the capped system, and request declared initial helical-region torsions
through the public geometric editor. Validate achieved angles modulo the branch
cut, unchanged source/chemical inventory and bond lengths. Do not add builder
keywords, a secondary-structure classifier or an energy protocol.

Pre-generate only this lesson's transparent static MolSysViewer export with the
existing frozen documentation runtime and shared asset route. Notebook execution
embeds that received scene; it must not construct live views or export scenes in
ordinary pre-execution. Compare the exported molecular coordinates with the
actual lesson calculation and receive the iframe on the built page. Keep source,
headless visual and final installed-pair qualifications distinct.

## Resolution — 2026-11-15

The actual notebook uses the explicit capped sequence and the existing public
quartet, copy and geometric-edit tools. The returned five phi, five psi and
five omega quartets reach the declared targets, modulo the angular branch cut.
Independent NumPy angles, unchanged source coordinates, cap connectivity and
bond-length preservation are checked under nm/ps and pm/fs policies. Targets
apply to returned quartets; the lesson does not classify or predict a stable
helix. The extended-region challenge remains a declared modeling exercise.

All seven code cells execute in fresh kernels under ordinary and explicitly
configured pm/fs/degrees application policies. A dedicated generator executes
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
