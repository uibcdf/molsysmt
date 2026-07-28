# Four Paths Course Maintenance Map

The maintained course is `docs/content/course/`, titled “The Four Paths of the
MolSysMT's Master”. This file records its actual repository structure and the
rules for keeping it synchronized with the library.

## Current inventory

Excluding notebook checkpoints, the course currently contains:

- `00_Common_Core`: 20 notebooks numbered 01–20;
- `01_Path_Alzheimer`: 34 notebooks numbered 17–50;
- `02_Path_Enzyme`: 34 notebooks numbered 17–50;
- `03_Path_Antiviral`: 34 notebooks numbered 17–50;
- `04_Path_Biophysics`: 34 notebooks numbered 17–50.

This is 156 notebooks. The landing page currently describes a common core of
modules 1–16, so modules 17–20 overlap between the common core and every path.
That mismatch is a confirmed documentation defect; see
`pending_bugs/course_module_numbering_overlaps.md`.

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
