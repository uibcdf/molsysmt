---
summary: Geometric-transformation course examples fail during system preparation
issue: uibcdf/molsysmt#454
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: low
verification: reproduced
area: [docs]
guard: tests/documentation/test_center_examples.py
normative:
blocked_by: []
supersedes: []
---

# Geometric-transformation course examples fail during system preparation

**Reported:** 2026-10-24 while executing every course use of center during
uibcdf/molsysmt#451. **Status:** resolved; both real-source notebooks and offline contract guards execute.

## What

The Enzyme and Alzheimer Module 46 notebooks fail before centering. The Enzyme
setup passes the retired from_form argument to convert and assumes a direct
SMILES-to-MolSys conversion can create geometry. The Alzheimer setup merges
all ten 2BEG structures with one built peptide pose. After fixing setup,
both also request a live view without the required pre-exported static scene.
Amyloid peptide chains cannot be distinguished from the added peptide by a
generic protein-versus-peptide classification.

## How

Run the notebooks with the documented forced notebook executor. The first fails
with UnknownArgumentError for from_form; the second raises a structural count
mismatch (10 versus 1). These failures occur before center, so they are not
scientific regressions from its redesign.

Use an explicitly tagged SMILES conversion to RDKit, add hydrogens and embed one
seeded 3D conformer before conversion to MolSys. This is a reproducible
illustrative pose, not an inferred binding pose or relaxed minimum. Select the
first fibril structure before merging and retain explicit source atom indices
for fibril and newly added peptide. Use actual before/after rotation projections
and pair-distance checks instead of an unavailable static scene. Both modules
now explain the source/destination centering contract and assert its result.

## Why

Readers cannot reproduce the public transformation examples. The old biological
classification can also select no fibril atoms or transform both peptide
populations, even after structure counts are corrected.

## What is measured and what is assumed

Both original setup errors were executed with the actual remote input systems.
The corrected Alzheimer notebook executes its full scientific workflow in
15.1 seconds. The final Enzyme notebook, including explicit substrate populations
and seeded RDKit embedding, executes in 14.7 seconds. Local pytest
guards replace only remote PDB identifiers with bundled molecular inputs while
executing the notebook's real public preparation and transformation calls.
These substitutions qualify contracts, not equivalence of biological models.
Actual source execution is recorded separately from that offline guard.

## What was refuted

Relaxing merge count checks, allowing obsolete convert keywords, changing
center to move unintended populations, and pretending a missing static scene
exists would hide the failures rather than repair the examples.

## Scope and exclusions

Only the two Module 46 notebooks and their content-protection contracts are
changed. No SMILES geometry backend or general merge policy is added. Broader
course prose and Sphinx warning debt remain under uibcdf/molsysmt#144.

## Acceptance criteria

Execute both notebooks successfully, preserve unit-bearing transforms and rigid
pair distances, assert centered source populations and run the independent
local-input guard in tests/documentation/test_center_examples.py. Keep the
common tutorial, placement recipe and course examples synchronized.

## Provenance

2026-10-24, Linux/Python 3.14.7, existing development environment. Real source
inputs: PDB 6EQE, first structure of PDB 2BEG, seeded RDKit BHET conformer and
built KLVFF peptide. This is source documentation evidence, not installed-package
or scientific binding-pose qualification.

## Verification

The recipe plus both local-input course guards pass: **3 passed in 13.31 seconds**
with pytest-receptor and 12 workers. They execute actual source cells and real
public preparation, centroid and transformation tools; only the remote PDB
identifiers are replaced. The Alzheimer fixture deliberately supplies a
multi-structure peptide ensemble, protecting the explicit single-structure
preparation and original-atom population boundaries. The Enzyme fixture still
uses the actual tagged SMILES, RDKit conformer and native conversion route;
reintroducing from_form or omitting geometry fails. Numerical checks protect
centers and pair-distance preservation, not just notebook formatting.

Both full notebooks also execute on their intended real-source systems and save
their outputs. Actual before/after plots replace unconfigured live scenes.
No new 3D runtime asset or alternate viewer is introduced. Course structure,
Ruff, Sphinx and fast repository gates pass, retaining accepted unrelated
Sphinx warnings. Source evidence is separate from any installed release pair.
