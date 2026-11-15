---
summary: Alzheimer peptide-synthesis module uses unsupported capping and conformation keywords
issue: uibcdf/molsysmt#759
status: open
opened: 2026-11-14
closed:
severity: medium
verification: inspected
area: [docs, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Alzheimer peptide synthesis uses unsupported builder keywords

**Reported:** 2026-11-14 while tracing the input context of #758.
**Status:** open; next finite pre-1.0 course correctness item under #334.

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

This report is source-inspected, not a completed notebook execution. The current
#758 geometry receiving builds only plain KLVFF; it does not qualify this other
module's capping, conformation or visual output.

## Acceptance criteria

The actual module executes on supported public calls, retains all scenarios,
reports correct group/index/unit semantics and measured torsions, and preserves
its static visualization. Add a regression on the real cells, with independent
inventory/geometry expectations. A renamed token or green Sphinx build is not
sufficient.

## Provenance

Inspected on cc58c0512 plus the separate #758 documentation/test delta. No runtime
API, provider, engine, dependency or native binary is changed by this report.
