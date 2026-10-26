---
summary: Conformational engineering course examples use obsolete torsion arguments.
issue: uibcdf/molsysmt#468
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [docs, structure]
guard: tests/documentation/test_conformational_engineering_course.py
normative:
blocked_by: []
supersedes: []
---

# Conformational engineering course examples use obsolete torsion arguments

## What

Four specialized Module 27 notebooks use obsolete named torsion edit keywords,
unsupported torsion attributes in get(), malformed remote source spellings or
an ignored independent return. The original examples also infer stability,
functional gate opening and substrate accessibility from unqualified rotations.

## How

Use the existing public topology quartet/path discovery, covalent block tools
and structure measurements/editors. Supply explicit angular quantities, isolated
nonperiodic geometry and independent returned systems. Preserve KLVFF, PET
hydrolase 6EQE, N3/6LU7 and channel complex 1K4C as the original biological cases.
Inputs are now byte-pinned offline catalog resources from uibcdf/molsysmt#469;
the split-DBREF parser prerequisite was repaired in uibcdf/molsysmt#474.

For N3 retain the original measurement-only exercise: chain C spans six groups,
not a generic small-molecule selection. Its deposited connectivity supports
measurable paths but does not establish all ligand bonds, ring constraints or
rotatable-bond chemistry. Do not introduce unjustified fragment rotation to
make this example look like the other three. A future edit requires complete
chemical preparation and an explicit physically justified bond/block choice.

## Why

Working signatures and notebook schemas alone do not establish a scientific
example. Selection must identify the intended biological atoms; angular targets
must be reached and moving/fixed populations must match the public contract.
No new engine, method, torsion algorithm or chemical repair is introduced here.
Existing public tools own these operations; the course only composes them.
No new Ackredit method registration is applicable. Dataset authorship and
publications remain linked by the source manifest and structure pages.

## Acceptance criteria

Force-execute all four offline notebooks. Independently verify signed circular
angles, complete Rodrigues rotations, unchanged nonmoving atoms, original
coordinates, topology and box. Run the same code under nm/radians and pm/degrees
policies; reject remote lookup. Preserve deposited TRP A159 and CYS C90 labels,
N3 chain C, KLVFF sequence and terminal torsion counts. Distinguish imposed
geometry from energy minimization, binding, functional gating and validation.
Add per-page content contracts and retain course anchors/navigation.

## Resolution — 2026-10-26

All four original biological scenarios now use existing public tools with
explicit index quartets and physical units. KLVFF reaches phi -135 degrees and
psi +135 degrees before the third amino acid's psi shifts +45 degrees. TRP A159
chi1 shifts +180 degrees; CYS C90 phi shifts +10 degrees. N3 retains 49 atoms,
six source groups and 47 reversal-deduplicated, four-distinct-atom measurable
paths from declared connectivity, with no unsupported bond-rotation inference.
The editor's default independent return is assigned rather than discarded.

**Contract-tested:** `python -m pytest
 tests/documentation/test_conformational_engineering_course.py
 tests/structure/test_dihedral_edit_contract.py --receptor=llm -n 12` passes
**326 tests**, exit 0, in 11.23 seconds. Eight course cases execute all code
under nm/radians and pm/degrees policies with remote DNS forbidden. The guard
compares circular signed projection angles and complete independent Rodrigues
rotations, fixed atoms, unchanged source buffers, topology and box. Its source
labels identify the intended biological site, not merely a quartet count.
No named-torsion edit kwargs or nonexistent get() torsion attributes remain.

Initial guard runs rejected overstrict numerical comparisons: converting the
same coordinates through different explicit unit routes differed below
1e-15 nm, and the existing torsion kernel near planar initial coordinates
left about 1.5e-8 radians target error. Native source buffers remain checked
bit-for-bit; converted fixed coordinates allow 2e-13 nm and circular angles
1e-7 radians. These tolerances describe the actual scientific assertions;
no geometry kernel or notebook output was changed to satisfy the guard.

All four notebooks were force-executed with
`MSM_VIEWS_FROM_HTML_FILES=True MPLBACKEND=Agg python docs/execute_notebooks.py
 -q -n 12 -f <the four Module 27 paths>` (6.2–6.9 seconds each). Their stored
outputs and code fingerprints accompany the source. Visualization is an
optional linked inspection step, without generating live widget assets during
execution. Each page has a content-protection contract; the function inventory
records actual earlier introductions in Common Core rather than claiming
these examples introduce a new API.

The raw 491-notebook schema guard passes (8.07 seconds). The incremental HTML
build exits 0 with **zero errors and 29 warnings**; header-level and existing
not-in-toctree warnings remain under uibcdf/molsysmt#144, which is not closed.
All 14 fast release gates pass; Ruff check and formatting pass for the new
guard. These source checks do not
qualify functional gating, binding, energy minima, an installed pair, another
platform or the 1.0 release.
