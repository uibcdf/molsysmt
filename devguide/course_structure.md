# Four Paths Course Maintenance Map

The maintained course is `docs/content/course/`, titled “The Four Paths of the
MolSysMT's Master”. This file records its actual repository structure and the
rules for keeping it synchronized with the library.

## Current inventory

Excluding notebook checkpoints, the course currently contains:

- `Common_Core`: 20 notebooks numbered 01–20;
- `Path_Alzheimer`: 34 notebooks numbered 21–54;
- `Path_Enzyme`: 34 notebooks numbered 21–54;
- `Path_Antiviral`: 34 notebooks numbered 21–54;
- `Path_Biophysics`: 34 notebooks numbered 21–54.

This is 156 notebooks. Every complete route through the course contains the
20-module Common Core followed by one 34-module Path, for 54 modules with no
gap or duplicate display number.

`docs/content/course/course_manifest.yml` is the identity authority. Each
notebook carries its manifest `id` as its top-level MyST label. These semantic
labels remain stable if display numbers or filenames change; internal links use
the labels rather than reconstructing identity from a module number.

`devtools/scripts/validate_course.py` enforces the 20 + 4x34 inventory,
numbering, toctrees, manifest coverage, unique semantic identifiers, and exact
manifest-to-notebook label agreement.

The earlier six-phase, single 50-module proposal is archived under
`archive/assessments/` and is not the current course map.

## Maintenance contract

When public behavior changes, identify affected notebooks by symbol and concept,
then verify:

- the import and public signature used;
- bundled system paths and network assumptions;
- expected shapes, units, values, and warnings;
- viewer/backend availability;
- links to User Guide and API material;
- notebook execution from a clean supported environment.

Do not mark a course topic verified because another path has a similarly named
notebook. Each path can contain different code and scientific assumptions.

## Native-performance synchronization

The path-specific performance modules must teach that native kernels are
precompiled and separate import, preparation, and execution costs in
benchmarks. They must not present a JIT warm-up workflow.

## Pending review material

Unresolved retrospective notes live under
`pending_proposals/course_review/`. They are planning inputs, not current course
requirements. Once accepted, split them into testable work items and close or
archive the original note.
