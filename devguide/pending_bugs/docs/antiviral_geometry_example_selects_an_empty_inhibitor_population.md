---
summary: Antiviral geometry example selects an empty inhibitor population in 6LU7.
issue: uibcdf/molsysmt#634
status: partial
opened: 2026-11-07
closed:
severity: medium
verification: reproduced
area: [docs, course, structure]
guard: tests/documentation/test_center_examples.py::test_antiviral_geometric_course_moves_only_inhibitor_chain
normative:
blocked_by: []
supersedes: []
---

# Antiviral inhibitor identity

## What

The Antiviral Module 46 example selects `molecule_type=="small molecule"`
before centering/rotating the deposited 6LU7 inhibitor. The PDB-ID route reads
mmCIF/BinaryCIF entity information and classifies that inhibitor as a peptide.
The selected population is empty; the native center correctly rejects it.
This precedes the new #602 constructor example and is an existing course defect.

## How

The actual five-notebook campaign completes four notebooks and fails Antiviral.
Retained BinaryCIF gzip SHA-256 is
`033135f2a67384eb05dc8dff54115e41fc6bb093fa9143e544a18953f4cea16a`.
It produces 2,500 atoms, with 49 inhibitor atoms on label chain B / author chain
C. The inhibitor spans six groups, including 02J, PJE and 010; there is no
single N3 group. Both `chain_id=="B"` and `chain_name=="C"` select the 49
atoms, while the small-molecule query selects zero.

The retained legacy PDB control has SHA-256
`385497151c2c093d764ffbc694589c2c1db35be638e49d715d4d8af38903966e`.
Its generic small-molecule query selects only eight atoms, so replacing the
reader is not a valid whole-inhibitor selection fix. Its LINK records describe
the inhibitor/protein connection. Different available entity information is
not, by itself, evidence of a parser classification defect.

## Why

A geometric exercise must name its actual moving population. N3 is the
peptidic inhibitor represented by the deposited chain, not a guarantee that a
generic small-molecule category will identify it. The covalent connection also
means that a rigid coordinate rotation must not be presented as establishing a
physically valid new pose or changing chemical assignments.

## Correction and acceptance

Use the explicit author-chain identity with a nonempty check, retain the
6LU7 example and explicit units, and distinguish label IDs from author names.
Capture the center/initial coordinates before the edit, preserve other atoms
and keep the new independent matrix-equivalence assertion. Add an executable
offline guard with two peptide populations: only the intended chain may move,
with its coordinates checked against an independent signed rotation formula.
The original small-molecule query must fail that guard before correction.
Reexecute the real notebook and retain the failed campaign/input hashes.

The native selection/center implementation, parser classification policies,
chemical state and #421 graphical acceptance are not modified by this fix.

## Local receiving — 2026-11-07

The corrected real notebook completes both code cells, prints 49 selected atoms
and generates the actual before/after figure. Its unselected-coordinate and
selected-geometry assertions pass. Together with the four unchanged notebooks
that completed in the first campaign, all five #602 notebooks are now executed;
the original first campaign still has native exit one and is not relabelled.

The offline guard uses two complete native peptide inventories and independently
checks the intended chain, signed rotation and unchanged other population. It
passes with one retained headless-plot warning. Initial guard-authoring attempts
used a topology-free trajectory seed and then an extra center axis; those failures
are retained but are not evidence of native classification or geometry defects.
Source/public delivery and issue closeout remain pending.

The portable [combined receiving receipt](../../../devtools/data/axis_angle_and_transform_receiving_602_633_634_637_20261107.json) retains native exits, original failed attempts, source fingerprints and the separately incomplete candidate/host gates. All fourteen final fast source gates pass.
