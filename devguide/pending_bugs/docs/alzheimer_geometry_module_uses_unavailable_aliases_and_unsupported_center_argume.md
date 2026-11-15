---
summary: Alzheimer geometry module uses unavailable aliases and unsupported center arguments
issue: uibcdf/molsysmt#758
status: open
opened: 2026-11-14
closed:
severity: medium
verification: inspected
area: [docs, structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Alzheimer geometry module uses unavailable public calls

**Reported:** 2026-11-14 in the #334 geometry-example review, after finding
#757's independent endpoint-position reporting error.
**Status:** open; inspect the actual lesson and receive a bounded correction next.

## What

`docs/content/course/Path_Alzheimer/30_Geometrical_Measurements.ipynb`
calls `msm.get_distances`, `msm.get_minimum_distances` and `msm.get_angles`.
The current root lazy registry exports none of those aliases; their public
owner is `msm.structure`. The center-distance call also supplies
`center_of_selection=True`, which is absent from `get_distances`' signature;
its two endpoints use independent `center_of_atoms` flags.

The lesson assigns the minimum-distance tuple to one variable and calls it a
distance. Its narrative also suggests that geometry proves fit/affinity, even
though the setup simply merges a downloaded fibril and newly built peptide,
without an explicitly placed or qualified complex. Those explanatory claims
need correction, not a new docking or affinity algorithm.

## How

Read the actual nine cells against `molsysmt/__init__.py` and the public
structure signatures. The first obsolete call raises before the intended
measurement can occur. The setup requests live `pdb:2BEG`, so a full execution
has not been claimed from the current offline geometry cohort. Hard-coded
angle atoms and molecule-type selections also need checking against the actual
chosen system rather than being assumed to define the stated interface.

## Why

Readers cannot run the advertised measurement workflow on current MolSysMT.
Its scientific interpretation overstates what coordinate measurements establish.
This is admitted pre-1.0 documentation correctness work under #334, not the
post-1.0 missing micro-contract debt in #512.

## Proposed bounded correction

- Retain the fibril/peptide teaching context and all distance, closest-contact,
  angular and challenge scenarios; preserve existing anchors and figures.
- Use supported form-agnostic `msm.structure` tools with explicit independent
  endpoints, quantity handling and local-to-source index correspondence.
- Choose and document a deterministic input/placement strategy. Prefer suitable
  bundled data; if no faithful input exists, record the required bounded fixture
  and its provenance before adding it. Do not silently describe arbitrary merged
  coordinates as a docked or experimentally established complex.
- Explain that these are coordinate observables, without an affinity estimate,
  chemical-interaction assignment, binding proof or pose-quality validation.
- Execute the actual complete corrected lesson, inspect its numerical results
  independently and receive the rendered article.

## What is measured and what is assumed

The unavailable aliases and unsupported keyword are source-inspected. No live
PDB download, preparation, docking or full lesson execution has occurred in this
review. #757's separate 21-case geometry receiving and nine executed tool
notebooks do not qualify this course module.

## Acceptance criteria

The actual lesson runs on supported public calls, reports physically correct
quantities/axes/source indices, preserves its scientific scenarios and clearly
states the input and interpretation limits. A regression must exercise those
actual cells against independent coordinate/membership expectations; a token
rename or successful Sphinx build alone is insufficient.

## Provenance

Inspected on 6deb0200c plus the separate #757 documentation/test delta, on
2026-11-14. Runtime, providers, algorithms and the native binary are unchanged.
